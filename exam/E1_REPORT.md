# E1 — Rilevamento in-distribution di embedding LSB su pesi reali di CNN

**Progetto:** Beyond the X-Ray — Machine Learning Security, lavoro condiviso Riccardo–Fabrizio.  
**Data di chiusura sperimentale:** 19 ottobre 2026. **Stato:** E1 concluso; E2 ed E3 ancora da completare.  
**Risultati finali versionati:** commit [`d35f8f2`](https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY/commit/d35f8f2), branch `ricky`.  
**Metodologia:** protocollo *few-shot* adattato da Model X-Ray; non replica numerica esatta delle tabelle pubblicate dagli autori.

> **Risultato sintetico.** Sul test interno con checkpoint sorgente distinti, il detector *centroid* raggiunge, a **X=23**, AUROC media **0,9019** su 10 ripetizioni e accuracy **82,13%** con soglia scelta esclusivamente sulla validation. Per X=1,8,16 l'AUROC è prossima a 0,5. Questo risultato non costituisce una dimostrazione di generalizzazione OOD né di attacco steganografico funzionalmente indisturbato.

---

## 1. Background, contesto e research question

### 1.1 Problema di sicurezza

I checkpoint di machine learning sono file utilizzati per distribuire modelli pre-addestrati e aggiornamenti. Oltre alla sicurezza del codice di caricamento, interessa l'**integrità numerica dei parametri**: contenuto estraneo può essere incorporato nei bit di rappresentazione dei pesi. Gli embedding *X-LSB* sostituiscono X bit meno significativi della mantissa di valori float32. L'intensità controlla la quantità di informazione alterata, ma un embedding più intenso può aumentare anche la perturbazione dei parametri e rendere l'attacco più facilmente rilevabile.

Model X-Ray è il punto di partenza metodologico. Il suo codice implementa trasformazioni/representations dei pesi, uno schema few-shot Siamese e baseline. La letteratura contempla già setting in-distribution e OOD; il presente lavoro di corso mira prima di tutto a una **misurazione controllata e riproducibile**, non a rivendicare la scoperta del problema o un nuovo detector.

### 1.2 Obiettivo del progetto complessivo

La domanda è: **un detector basato su Model X-Ray riproduce un comportamento misurabile in-distribution e come si comporta con embedding di famiglie non viste, mantenendo controlli rigorosi sui confondenti?** Per isolare la risposta abbiamo separato il programma in:

| ID | Scopo | Train | Valutazione | Stato |
|---|---|---|---|---|
| **E1 — ID** | Stabilire baseline robusta su attacco noto. | LSB su CNN del dataset selezionato. | LSB su checkpoint mai usati nell'addestramento, stesso zoo. | **Concluso**, 40 validation + 40 test, v2. |
| **E2 — OOD attack shift** | Misurare generalizzazione a una famiglia di embedding non vista. | LSB, come E1. | Nuova famiglia di embedding; evitare cambi di architettura e attack family simultanei. | **Pianificato**, dati non ancora disponibili. |
| **E3 — controlli** | Cercare scorciatoie e leakage. | Protocollo matched. | Bilanciamento, provenance, serializzazione/metadati, altri fattori confondenti. | **Pianificato**, con alcune garanzie di base già in E1. |

E2 ed E3 non sono risultati acquisiti: non riportiamo AUROC inventate né anticipiamo una conclusione OOD. L'eventuale percorso di tesi individuale e un possibile paper sono distinti dalla consegna dell'esame.

### 1.3 Obiettivo specifico E1 e ipotesi

Dato un classificatore few-shot addestrato con **tre coppie** benign/stego ricavate da CNN originali, misurare la capacità di distinguere nuove CNN benign da CNN stego su **identità non viste**, in quattro intensità X-LSB: **1, 8, 16, 23**. L'ipotesi esplorata è che la detection aumenti per alterazioni molto invasive, mentre per X bassi il segnale potrebbe non essere distinguibile dal rumore della rappresentazione. Prima del test è stato congelato **centroid/AUROC come confronto primario**, con 1-NN e metriche a soglia come secondarie.

## 2. Dataset, provenienza e preparazione

### 2.1 Origine delle CNN

Sono stati utilizzati **1.000 checkpoint autentici di CNN** provenienti dallo zoo GHRP/STL10, scaricato dalla raccolta [Zenodo 6631784](https://zenodo.org/records/6631784). Una prima verifica ha evidenziato che `dataset.pt` rappresentava immagini STL10, e non poteva essere trattato come vettore di pesi per la detection: l'estrazione iniziale da immagini è stata scartata. La pipeline corretta `scripts/extract_d1_real_weights.py` ha estratto veri pesi dei checkpoint, ottenendo `weights.npy` di forma **(1000,2864)** e dtype **float32**. La provenienza è registrata in `checkpoint_manifest.csv` e `extraction_summary.json` locali.

L'uniformità delle 1.000 CNN consente un test ID a rappresentazione coerente ma **limita le conclusioni alla distribuzione analizzata**.

### 2.2 Split e unità statistica

Il protocollo congelato `manifests/e1_uniform_v1/{splits.csv,protocol.json}` assegna **600 checkpoint al pool train, 200 alla validation e 200 al test**. Ogni replica estrae tre identità dal pool train, con campioni benign e stego appaiati per identità. I derivati di un checkpoint non attraversano gli split.

| Elemento | Quantità |
|---|---:|
| CNN originali distinte nel dataset | 1.000 |
| Pool train disponibile | 600 |
| Checkpoint sorgente per singolo training few-shot | **3** |
| Campioni effettivi per training | **6** (3 benign + 3 stego) |
| Checkpoint distinti di validation | 200 |
| Osservazioni per validation e replica | **400** (200 + 200) |
| Checkpoint distinti di test | 200 |
| Osservazioni per test e replica | **400** (200 + 200) |
| Ripetizioni per X | 10 |
| Livelli X-LSB | 1, 8, 16, 23 |
| Fit per campagna | **40** |

I campioni benign/stego di una stessa CNN sono correlati: **400 osservazioni non equivalgono a 400 checkpoint indipendenti**. La prevalenza delle due classi è 50% per costruzione, quindi AUPRC va interpretata rispetto a un riferimento casuale vicino a 0,5.

### 2.3 Assenza di leakage diretto e limite dello stesso zoo

Il runner verifica hash e identità dei checkpoint, lo split per sorgente e che la soglia sia scelta sulla validation. La partizione test non è stata letta durante il *preflight*. Ciononostante, alcune prove esplorative precedenti al congelamento del protocollo hanno coinvolto lo stesso zoo: il test è una **valutazione interna con checkpoint disgiunti**, non una validazione esterna completamente incontaminata. Il solo uso della parola “blind” non elimina questo limite.

## 3. Threat model e costruzione degli esempi

### 3.1 Attacco sintetico

Per ciascun checkpoint si prende un vettore float32 benign. Si applica l'algoritmo `img_pp_xlsb_attack` di Model X-Ray per sovrascrivere **X bit meno significativi della mantissa** di ciascun peso con bit ricavati da un payload. I payload sono **byte pseudo-casuali sintetici, inerti e non eseguibili**. Non è stata effettuata esecuzione di malware né verificata l'operatività di un trojan.

In v2 ogni checkpoint ha un payload diverso ma riproducibile. Il runner genera **16.384 byte** tramite **SHA-256 per derivare il seed** e **PCG64 NumPy** per produrre byte uniformi. La chiave combina schema, seed 42, ripetizione, X e `row_index`. Il file binario temporaneo viene passato all'attacco upstream e poi eliminato; `payload_manifest.csv` registra gli SHA-256 dei payload generati.

### 3.2 Paired design e rappresentazione

Per ogni checkpoint si costruiscono una cover (`X=0`) e una versione stego (`X∈{1,8,16,23}`), quindi si usa la rappresentazione immagine **gf**, dimensione **100×100**, della pipeline upstream. L'uso della medesima sorgente per benign/stego riduce il rischio che il detector riconosca l'origine invece dell'attacco. Non dimostra da solo l'assenza di scorciatoie legate alla trasformazione: queste verranno approfondite in E3.

## 4. Modello, protocollo di valutazione e metriche

### 4.1 Detector few-shot

Il modello è il Siamese CNN originale di Model X-Ray (`train_fsl`, architettura `osl_siamese_cnn`, modalità `ub`) richiamato dal nostro runner. L'upstream è fissato al commit **`a880e332f556fc71faf8d3753931005d5d019339`**; non sono state editate le sue sorgenti. Lo stesso embedding appreso alimenta due classificatori:

- **Centroid (primario):** distanza euclidea fra l'embedding di un checkpoint e la media degli embedding di train di ciascuna classe.
- **1-NN (secondario):** distanze euclidee dai campioni few-shot di train, considerando il vicino più prossimo di ciascuna classe.

Lo score è il margine `d(benign) - d(stego)`: **score > 0** favorisce stego. Le predizioni ricavate dal margine sono controllate rispetto alle funzioni d'inferenza upstream; eventuali discordie interrompono l'esperimento.

### 4.2 Threshold e separation of duties

Riportiamo due politiche di decisione binaria:

1. **`original_zero`**: soglia fissa `0` sul margine.
2. **`val_youden`**: soglia selezionata massimizzando l'indice di Youden `TPR−FPR` **esclusivamente sui 200 checkpoint validation** di ciascuna replica.

AUROC e AUPRC sono metriche di ranking, quindi **non cambiano** tra le due soglie. Per il test, il Siamese viene **riaddestrato** con lo stesso protocollo e seed; per quel nuovo modello la soglia è calcolata sui campioni di validation e applicata al test **senza scegliere la soglia sulle etichette test**. Poiché i pesi del detector della validation precedente non sono stati salvati, la ricalibrazione sul nuovo modello era necessaria: le due campagne di validation non vanno confuse.

Metriche: accuracy; AUROC (primaria, centroid); AUPRC; precision, recall, F1; tasso falsi positivi (`FPR=FP/(FP+TN)`). Il file `metrics_per_run.csv` comprende altre metriche come balanced accuracy, specificità e conteggi per classe. I riepiloghi riportano media su **10 repliche** e deviazione standard dell'accuracy. **Non abbiamo calcolato intervalli di confidenza cluster-aware né riportato deviazioni standard AUROC nel riepilogo.**

### 4.3 Setup computazionale

Esperimenti eseguiti su **Ubuntu 24.04 in VirtualBox**, CPU (senza GPU), **6 vCPU**, circa **11 GiB RAM** e **4 GiB swap**. Ambiente Python 3.11 locale con pacchetti congelati (`configs/modelxray-ubuntu24-py311.lock.txt`). Per contenere l'uso di memoria, ogni training del runner v2 viene eseguito in un **processo separato** e può essere ripreso senza sovrascrivere i run conclusi.

## 5. Sviluppo dell'esperimento: piloti, diagnosi e freeze

Il percorso sperimentale è documentato per evitare la falsa impressione che il protocollo finale sia stato scelto retroattivamente in base al test.

| Campagna | Obiettivo, osservazione | Decisione |
|---|---|---|
| **Pilot upstream** | 8 combinazioni rapide (4 X × 2 repliche). Centroid ~50% per X≤16, ~84,75% per X=23. | Segnale promettente, ma protocollo non sufficiente come valutazione finale. |
| **Pilot paired** | 4 combinazioni (X16 e X23 × 2 repliche), 3 sorgenti train e 300 sorgenti test pilota. Centroid ~49,58% X16 e ~85,00% X23. | Usare esempi benign/stego matched e split congelati. |
| **Freeze split** | Manifest train/validation/test 600/200/200, checkpoint IDs/hashes e dimensioni verificati. | Non cambiare la partizione per migliorare i risultati. |
| **Validation v1 (esplorativa)** | 40 run con attacco casuale interno; centroid AUROC media ~0,870 per X23. | Mancava ricostruibilità esatta dei payload: conservare separata, non usare come risultato definitivo. |
| **Diagnosi riproducibilità** | Senza attacco l'immagine è stabile. `PayloadType.RANDOM` produce output diversi a seed NumPy globale uguale; file binario temporaneo riproduce output identici. | Generazione deterministica per checkpoint e controllo hash dei payload. |
| **Smoke v2** | X23, replica 0, modalità `es`; 800 righe predizioni (2 metodi × 400 esempi), 203 payload diversi (3 train+200 val), AUROC centroid ~0,861. | V2 funzionante; smoke non comparabile come fit definitivo `ub`. |
| **Validation v2 finale** | 40/40 training `ub`; primo arresto a 32/40 per 1 discordanza numerica centroid su 400 campioni al livello X1. | Diagnostica separata senza discordie, una riesecuzione mirata documentata; completate 40/40 prove. |
| **Freeze protocollo test** | Script di test versionato, `--preflight` 40/40, Git pulito, scelta primario fissata. | Eseguire test su 200 identità riservate, senza tuning successivo. |
| **Test v2 finale** | 40/40 run isolati; metriche validation e test correttamente salvate e controllate; commit `d35f8f2`. | E1 chiuso; risultati non modificati in risposta alle prestazioni del test. |

**Nota su riproducibilità:** i *payload* v2 sono riproducibili per construction. Il *training TensorFlow* con uguali seed potrebbe non essere bitwise deterministico. Il caso di discordanza vicino a score zero e la ripetizione controllata riguardavano la **validation**, prima del test; non è stata provata una perfetta stabilità numerica del classificatore.

## 6. Risultati quantitativi

### 6.1 Validation v2 di sviluppo (40 fit)

| X | AUROC centroid | Accuracy centroid, soglia 0 | Accuracy centroid, Youden (sulla stessa validation) |
|---:|---:|---:|---:|
| 1 | 0,500213 | 0,49925 | 0,50825 |
| 8 | 0,493719 | 0,49125 | 0,52800 |
| 16 | 0,504950 | 0,49950 | 0,53400 |
| **23** | **0,882645** | **0,79000** | **0,81800** |

Le accuracy `val_youden` di questa tabella sono **valori di sviluppo stimati sullo stesso split di calibrazione**; non vanno presentati come prestazione finale indipendente. La metrica di ranking AUROC è uguale per entrambe le politiche.

### 6.2 Test interno riservato: risultati principali (40 fit)

**Centroid — 10 ripetizioni per intensità.**

| X-LSB | AUROC test media | AUPRC test media | Accuracy test soglia 0 (media ± SD) | Accuracy test soglia Youden (media ± SD) | FPR test Youden |
|---:|---:|---:|---:|---:|---:|
| 1 | 0,500150 | 0,504064 | 0,50075 ± 0,00265 | 0,50025 ± 0,00142 | 0,5180 |
| 8 | 0,508232 | 0,509345 | 0,50150 ± 0,02015 | 0,50375 ± 0,01831 | 0,4315 |
| 16 | 0,501293 | 0,512234 | 0,49800 ± 0,01490 | 0,49850 ± 0,00835 | 0,3735 |
| **23** | **0,901863** | **0,902063** | **0,80375 ± 0,06920** | **0,82125 ± 0,07030** | **0,1550** |

La SD è la **deviazione standard campionaria delle accuracy tra 10 fit** (non un IC al 95%). I checkpoint test sono gli stessi tra repliche, quindi non trattiamo queste osservazioni come 10 test esterni indipendenti.

### 6.3 Confronto con la validation eseguita all'interno della campagna test

| X | AUROC centroid validation della campagna test | AUROC centroid test | Differenza test − validation |
|---:|---:|---:|---:|
| 1 | 0,500195 | 0,500150 | −0,000045 |
| 8 | 0,496286 | 0,508232 | +0,011946 |
| 16 | 0,504028 | 0,501293 | −0,002735 |
| **23** | **0,881812** | **0,901863** | **+0,020051** |

Questi dati derivano dagli **stessi fit della campagna test**: il sottoinsieme validation serve a determinare la soglia del relativo modello. Non confonderli con la validation di sviluppo, pubblicata separatamente.

### 6.4 Confronto con il metodo secondario 1-NN

| X | AUROC centroid test | AUROC 1-NN test | Δ centroid − NN |
|---:|---:|---:|---:|
| 1 | 0,500150 | 0,500190 | −0,000040 |
| 8 | 0,508232 | 0,498930 | +0,009302 |
| 16 | 0,501293 | 0,500670 | +0,000623 |
| **23** | **0,901863** | **0,815734** | **+0,086129** |

Al livello X23 centroid mostra una maggiore AUROC media rispetto al metodo 1-NN in questo setup. Essendo un confronto secondario, occorrerebbe analizzare le differenze **appaiate tra repliche** e relative incertezze prima di attribuire significatività statistica al divario.

### 6.5 Analisi accuracy/FPR a X23

Per il classificatore centroid sul test, passando da soglia 0 a soglia Youden calibrata sulla validation:

| Metrica | Soglia 0 | Soglia validation Youden |
|---|---:|---:|
| Accuracy media | 0,80375 | **0,82125** |
| F1 media | 0,793623 | **0,812583** |
| FPR medio | 0,1705 | **0,1550** |
| AUROC media | 0,901863 | 0,901863 |
| AUPRC media | 0,902063 | 0,902063 |

La calibrazione migliora leggermente accuracy e FPR medi a X23 sul test, **non** la capacità di ranking del detector. Per X≤16, la scelta di soglia non rende AUROC migliore di ~0,5 e può modificare sensibilmente FPR senza vera separazione.

### 6.6 Figure pronte per GitHub e file Excel

- **Figura 1:** [AUROC vs intensità X — validation di sviluppo, validation dei fit test, test](../results/figures/e1/e1_auroc_val_test.png).
- **Figura 2:** [Accuracy test — soglia originale vs Youden](../results/figures/e1/e1_accuracy_thresholds.png).
- **Figura 3:** [FPR test — soglia originale vs Youden](../results/figures/e1/e1_fpr_thresholds.png).
- **Figura 4:** [Confronto AUROC centroid vs NN sul test](../results/figures/e1/e1_auroc_centroid_nn.png).
- **Workbook editabile con grafici Excel nativi:** [E1_grafici.xlsx](../results/figures/e1/E1_grafici.xlsx).

Le figure allegate sono state predisposte usando i **valori dei riepiloghi CSV condivisi nei log**; per la verifica finale vanno **rigenerate sui CSV realmente versionati** con `scripts/plot_e1_results.py` prima del commit. Non ricostruirle a mano cambiando cifre o aggregazioni. Lo script non esegue training.

## 7. Discussione

**Messaggio principale.** Nel setting E1 il metodo centroid discrimina bene campioni benign/stego quando si sovrascrivono **23 bit di mantissa** (AUROC media ~0,902), ma ha un comportamento vicino al caso per **X=1,8,16** (AUROC 0,500–0,508). Questo è un risultato sul **particolare zoo e protocollo few-shot** studiati, non una misura universale di efficacia contro stegomalware.

La forte transizione a X23 è compatibile con un cambiamento molto più pronunciato della distribuzione dei pesi. Dal solo risultato di detection **non** possiamo inferire che un payload X23 mantenga inalterata l'utilità dei CNN, sia furtivo, venga recuperato esattamente o rappresenti malware eseguibile. Analogamente, il risultato quasi-casuale a X≤16 non prova che ogni possibile detector fallirebbe.

**Generalizzazione.** La robustezza ID misurata non dice come il detector reagisce ad attacchi di famiglia diversa (E2) né a cambi di architettura, serializzazione o lifecycle (E3 e possibili approfondimenti di tesi).

**Statistica.** La media sulle 10 ripetizioni descrive la variabilità del training e dei payload, ma un'inferenza rigorosa sul mondo esterno dovrebbe rispettare l'accoppiamento benign/stego e l'unità indipendente **checkpoint di origine**. Non attribuiamo p-value, intervalli di confidenza o differenze significative non calcolate.

## 8. Limiti e validità delle conclusioni

1. **Un solo zoo, un'architettura/popolazione di checkpoint.** Validità esterna non dimostrata.
2. **Checkpoint test identity-disjoint ma non zoo-disjoint** e precedente esplorazione del medesimo zoo. Non chiamare il test incontaminato in senso assoluto.
3. **Few-shot estremo:** 3 identità train (6 osservazioni), 10 repliche; risultati sensibili alla casualità di training, specialmente vicino a score zero.
4. **Precisione numerica:** un run della validation v2 si è fermato per 1/400 discordanza fra margine e inferenza upstream; diagnostica successiva 0/400. Non è stata dimostrata determinismo TensorFlow bit-a-bit.
5. **Payload deterministici ≠ payload malware reale.** Byte inerti pseudo-casuali, non eseguibili; assenza di test di utility/recupero.
6. **Soglia Youden della validation.** Le accuracy Youden misurate sulla medesima validation sono ottimistiche; solo il test successivo supporta una valutazione indipendente della soglia.
7. **Classi bilanciate al 50%.** AUPRC dipende dalla prevalenza; deployment con prevalenze differenti richiede una valutazione specifica.
8. **Incertezza limitata.** Nella tabella di sintesi è disponibile SD dell'accuracy; non sono stati stimati IC cluster-aware e TPR@FPR molto basse non sarebbero giustificati da 200 benign test.
9. **Solo detection.** Attacco fattibile, recovery, execution, degrado di accuracy CNN e compromissione reale dei modelli non misurati.

## 9. Conclusione E1 e collegamento a E2/E3

E1 conclude un **baseline sperimentale** su 1.000 checkpoint autentici con split identità-disgiunti, esempi paired, payload sintetici tracciati, 40 fit di validation e 40 fit sul test riservato. In questo regime, **X23 è rilevabile con AUROC media 0,901863** dal centroid few-shot, mentre **X≤16 resta vicino a 0,5**. La calibrazione su validation produce **accuracy media test 0,82125** e **FPR 0,1550** a X23.

Il risultato non è una nuova difesa, né dimostra OOD generalization. **E2** confronterà il detector con un embedding di famiglia diversa non visto nell'addestramento; **E3** verificherà se i risultati resistono a controlli più forti su origine e trasformazioni. Il quadro di ricerca seguirà criteri di comparabilità e pre-registrazione delle scelte, senza sfruttare il test E1 per decidere retroattivamente i parametri.

## 10. Materiali, riferimenti e provenienza delle affermazioni

**Dati primari** (da usare per qualunque citazione numerica):

- `results/validation/e1_uniform_v2/{summary.csv,metrics_per_run.csv,run_config.json}`.
- `results/test/e1_uniform_v2/{summary.csv,metrics_per_run.csv,run_config.json}`.
- `manifests/e1_uniform_v1/{protocol.json,splits.csv}`.
- I file per-run `metrics.json` e `predictions_{validation,test}.csv` sono conservati nell'area locale `~/mlsec-local/runs/`.

**Codice:** `scripts/run_e1_final_v2.py`, `scripts/run_e1_v2_matrix.sh`, `scripts/run_e1_v2_test_matrix.sh`, `scripts/diagnose_e1_v2_centroid.py` e `external/ModelXRay` (submodule); dipendenze in `configs/modelxray-ubuntu24-py311.lock.txt`.

**Letture:** [Model X-Ray, codice](https://github.com/danigil/ModelXRay); [MaleficNet](https://doi.org/10.1007/978-3-031-17143-7_21); [Do You Trust Your Model?](https://doi.org/10.1109/TDSC.2025.3586703); [GHRP STL10, Zenodo](https://zenodo.org/records/6631784). Le fonti citate in questa bozza richiedono completamento delle voci bibliografiche formali quando si redigerà la relazione d'esame definitiva.

**Attenzione:** i risultati quantitativi di questo documento derivano dalle tabelle `summary.csv` fornite durante l'esecuzione; per aggiungere barre di errore AUROC, IC e curve ROC per checkpoint occorre rileggerne le metriche per-run e predizioni, senza inventare dati.
