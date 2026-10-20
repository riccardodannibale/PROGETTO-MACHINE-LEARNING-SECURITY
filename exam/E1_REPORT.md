# E1 — Rilevamento in-distribution di embedding LSB su pesi reali di CNN

**Progetto:** Beyond the X-Ray — Machine Learning Security, lavoro condiviso Riccardo–Fabrizio.
**Chiarimento:** «due architetture» qui indica le **piattaforme di calcolo** (Ubuntu/CPU x86_64 virtualizzata e macOS/ARM64 M4), **non due architetture differenti di reti CNN**. Il dataset e il protocollo E1 rimangono gli stessi.
**Chiusura su Ubuntu:** 19 ottobre 2026. **Replica cross-platform ricevuta:** 20 ottobre 2026. **Stato:** E1 completato e replicato su due piattaforme; E2 ed E3 ancora da eseguire.
**Risultati Ubuntu versionati:** commit [`d35f8f2`](https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY/commit/d35f8f2), branch `ricky`. **Replica Fabrizio:** file `results/replicas/e1_mac_m4/`; commit Mac `59f556c` (diff dei file esecutivi dichiarato vuoto da Fabrizio; hash SHA-256 del runner verificato).
**Metodologia:** protocollo *few-shot* adattato da Model X-Ray; non replica numerica esatta delle tabelle pubblicate dagli autori.

> **Risultato sintetico.** Sul test interno con checkpoint sorgente distinti, il detector *centroid* raggiunge, a **X=23**, AUROC media **0,901863 su Ubuntu x86_64** e **0,904378 su Mac M4 ARM64**, entrambe su 10 ripetizioni. Accuracy con soglia scelta esclusivamente sulla validation: **82,125% su Ubuntu** e **82,300% su Mac**. Per X=1,8,16 l'AUROC è prossima a 0,5. Questo risultato non costituisce una dimostrazione di generalizzazione OOD né di attacco steganografico funzionalmente indisturbato.

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

## 7. Replica di Fabrizio su Mac M4 — confronto delle piattaforme

### 7.1 Che cosa rappresenta il confronto e cosa NON rappresenta

**Confronto originale → Ubuntu → Mac.** Il lavoro originale **Model X-Ray** è il riferimento metodologico e di codice; i suoi risultati pubblicati derivano da condizioni che non sono state qui accertate come identiche al nostro protocollo e **non sono collocati in una tabella quantitativa comune**. Il **pilot upstream originale** e la **validation esplorativa E1 v1** rappresentano invece fasi interne di sviluppo, non un terzo test finale indipendente. I soli risultati direttamente accostati nella tabella seguente sono le due esecuzioni E1 v2 con dati e split corrispondenti.

**Riccardo:** Ubuntu 24.04 su VirtualBox, CPU x86_64, 6 vCPU, ~11 GiB RAM, 4 GiB swap. **Fabrizio:** macOS su Apple Silicon **M4 ARM64**, TensorFlow su CPU (Metal non attivato), Python 3.11.17, NumPy 1.26.4, TensorFlow 2.15.1, PyTorch 2.4.0; nessuna GPU TensorFlow visibile. Non sono due architetture **neuronali**: le 1.000 CNN sorgente hanno la stessa rappresentazione in entrambi i run.

Integrità dichiarata e confrontabile:

- `weights.npy` SHA-256: `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad`.
- `splits.csv` SHA-256: `3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f`.
- Upstream Model X-Ray fissato a `a880e332f556fc71faf8d3753931005d5d019339`.
- Payload v2 sintetici deterministici; 203 payload/identità nello smoke test Mac; 40/40 validation e 40/40 test dichiarati e coerenti con i CSV.

**Versioning e integrità aggiornati (audit 20 ottobre).** Il `project_commit` del test Ubuntu è `f5bf86b237ca61f1d845732be41aa24203855921`; quello Mac è `59f556c78c8f7b0f1dac60bbe41748415ac0a71b`. Fabrizio ha eseguito `git diff` sui file sperimentali e **riferisce che il diff è vuoto**; l’output testuale del diff non è incluso nell’archivio ricevuto. Separatamente, è stato verificato l’hash SHA-256 del runner conservato tra gli artefatti di lavoro: `a75aa3d844bb695a6d6155fe808394025b04c480d74d1e1b856eec5ca6f9c037`, coincidente con quello comunicato da Fabrizio. L’upstream e gli SHA di pesi e split coincidono nei `run_config.json` Mac. La conformità del runner non implica training bitwise-identico né consente di attribuire causalmente i residui al processore.

### 7.2 Risultati test E1 v2 — centroid (10 ripetizioni per X)

| X-LSB | AUROC Ubuntu x86_64 | AUROC Mac ARM64 | Δ Mac − Ubuntu | Accuracy Youden Ubuntu | Accuracy Youden Mac | FPR Youden Ubuntu | FPR Youden Mac |
|---:|---:|---:|---:|---:|---:|---:|---:|
| **1** | 0.500150 | 0.500209 | +0.000059 | 0.50025 | 0.50075 | 0.5180 | 0.4595 |
| **8** | 0.508232 | 0.509388 | +0.001156 | 0.50375 | 0.50350 | 0.4315 | 0.4605 |
| **16** | 0.501293 | 0.501425 | +0.000132 | 0.49850 | 0.50125 | 0.3735 | 0.3470 |
| **23** | 0.901863 | 0.904378 | +0.002515 | 0.82125 | 0.82300 | 0.1550 | 0.1605 |

Sono medie sui **200 checkpoint di test distinti** per ciascuna replica, con 200 versioni benign e 200 stego. La soglia Youden è scelta nella validation dello stesso fit, **non ottimizzata sul test**. In particolare, a X=23 la differenza di AUROC **Mac − Ubuntu è +0,002515**, e quella di accuracy Youden è **+0,00175** (0,175 punti percentuali). Queste differenze **non dimostrano superiorità del Mac** e non sono un test di significatività statistica.

### 7.3 Dettagli Mac: validation della campagna test, 1-NN e tempi

| X | AUROC centroid validation nei fit test Mac | AUROC centroid test Mac |
|---:|---:|---:|
| 1 | 0.500254 | 0.500209 |
| 8 | 0.495828 | 0.509388 |
| 16 | 0.502669 | 0.501425 |
| 23 | 0.883028 | 0.904378 |

A X=23, anche il classificatore secondario **1-NN** mantiene segnale di detection: AUROC test **0,815734 Ubuntu** e **0,819226 Mac**. La classifica centroid > 1-NN a X23 è coerente sulle due piattaforme, ma senza un test appaiato dei punteggi non formuliamo una conclusione di significatività statistica.

Fabrizio riporta **circa 100–110 secondi per fit test** su M4, senza OOM, esecuzione in processi isolati e utilizzo di `caffeinate` per evitare la sospensione del Mac. Questo è un dato operativo riferito alla sua macchina, non un benchmark hardware scientificamente controllato. Su Ubuntu era stato necessario introdurre l'isolamento per processo dopo un OOM nel precedente runner v1.

### 7.4 Verifiche eseguite sugli allegati e lacune residue

Il pacchetto ricevuto contiene `summary.csv` (32 righe: 16 validation + 16 test), `metrics_per_run.csv` (320 righe: 160 + 160) e `e1_v2_test.log`. Abbiamo ricalcolato direttamente dai 320 record tutte le medie di accuracy, AUROC, AUPRC, F1 e FPR riportate in `summary.csv` e verificato **40 coppie (replica, X) per ognuno dei due stage**.

**Materiali integrativi ora ricevuti e verificati.** Sono disponibili i `run_config.json` Mac di test e validation stand-alone, il relativo `validation_standalone_summary.csv`, il `payload_manifest_r00_x23.csv` (3 train + 200 validation + 200 test, 403 righe) e `mac_environment.txt`. Tutti e 403 gli SHA-256 dei payload sono stati **rigenerati indipendentemente** tramite lo schema `sha256-keyed-uint8-pcg64-per-model-v1` e coincidono. Le medie nel `summary.csv` della campagna test corrispondono ai 320 record Mac già presenti. Mancano tuttora il log per-run della validation stand-alone e il manifest payload Ubuntu corrispondente per un confronto riga-per-riga fra macchine. Il file ambiente Mac registra chip M4 10-core, 16 GB e macOS 27.0.1, ma mostra errori di shell durante il recupero delle versioni delle librerie: per Python/NumPy/TF restano validi i valori **dichiarati** nel resoconto precedente, non un rilevamento completo dal nuovo file.

### 7.5 Grafici del confronto fra piattaforme

- [AUROC Ubuntu vs Mac, centroid](../results/figures/e1/e1_platform_auroc.png).
- [Accuracy test con Youden, Ubuntu vs Mac](../results/figures/e1/e1_platform_accuracy_youden.png).
- [FPR test con Youden, Ubuntu vs Mac](../results/figures/e1/e1_platform_fpr_youden.png).
- [AUROC centroid vs 1-NN sulle due piattaforme](../results/figures/e1/e1_platform_methods.png).
- [Validation nei fit test e test, due piattaforme](../results/figures/e1/e1_platform_validation_test.png).
- [Excel unico E1, foglio **Confronto_piattaforme** con grafici modificabili](../results/figures/e1/E1_grafici.xlsx).

**Conclusione della replica:** il comportamento qualitativo E1 è riprodotto su due piattaforme CPU differenti, a parità degli hash di pesi e split e con risultati quantitativi prossimi. Ciò rafforza la credibilità operativa del benchmark **ID** ma non è una prova di generalizzazione a CNN di altra architettura, né garantisce uguaglianza bitwise.

---


### 7.6 Audit finale dei file ricevuti (20 ottobre 2026)

L’ultimo archivio consegnato da Fabrizio è acquisito **senza sovrascrivere i CSV finali già versionati**. La cartella `results/replicas/e1_mac_m4/audit/` comprende cinque sorgenti originali: `run_config_test.json`, `run_config_validation.json`, `validation_standalone_summary.csv`, `payload_manifest_r00_x23.csv` e `mac_environment.txt`, oltre ai riepiloghi derivati `platform_summary_aggregates.csv` e `audit_integrity.json`.

**Riscontri indipendenti:**

- I due `run_config.json` riportano gli stessi `weights_sha256`, `splits_sha256`, `upstream_commit`, seed 42, schema payload, lista X e parametri sperimentali; gli stage correttamente distinti sono `test` e `validation`. Il commit locale Mac differisce fra le due campagne, come registrato nei singoli file.
- Il runner `run_e1_final_v2.py` della copia di lavoro fornita produce SHA-256 `a75aa3d844bb695a6d6155fe808394025b04c480d74d1e1b856eec5ca6f9c037`, lo stesso comunicato da Fabrizio per i due commit test. Fabrizio dichiara **diff vuoto sui file di esecuzione**; conservare output e comandi del diff in caso di review tecnica.
- Il manifest `repeat=0`, `X=23` contiene **403 righe**: 3 train, 200 validation, 200 test. Tutti i **403 digest SHA-256 del payload** sono stati ricalcolati con seed per `row_index` e NumPy PCG64: **403/403 corrispondenze**. Ciò prova l’integrità del manifest rispetto allo schema, non una corrispondenza riga-per-riga con il manifest Ubuntu (non allegato).
- Il `validation_standalone_summary.csv` contiene **16 righe** (4 X × 2 metodi × 2 politiche) e dichiara 10 ripetizioni per configurazione. A X=23, metodo centroid, **AUROC Mac validation stand-alone = 0,882700**. La validation dentro i *fit test* Mac misura invece **0,883028**: non sono la stessa campagna. Il riepilogo della validation separata è disponibile, ma i relativi per-run non sono stati inclusi nell'ultimo ZIP.
- Il Mac ha **16 GB di RAM e 10 core CPU** (4 performance + 6 efficiency); il file ambiente registra macOS `27.0.1`, chip Apple M4 e `arm64`. Alcuni comandi della raccolta software sono falliti (`zsh: permission denied`), quindi il file non documenta da solo in modo esaustivo Python, NumPy e TF storici.

### 7.7 Analisi descrittiva dei tempi e limiti hardware

| Indicatore | Ubuntu 24.04 VirtualBox | Mac M4 CPU |
|---|---:|---:|
| Fit della campagna test distinti | 40 | 40 |
| `elapsed_sec` medio per fit | **217,124 s** | **104,412 s** |
| Totale dei 40 intervalli cronometrati | ~144,75 minuti | ~69,61 minuti |
| Rapporto delle medie Ubuntu/Mac | **2,079** | riferimento |
| Tempo end-to-end dell’intero processo | Non misurato | Non misurato |
| Picco memoria confrontabile | Non misurato | Non misurato |

La fonte dei tempi Ubuntu è l’**audit già eseguito sulla macchina di Riccardo** il 20 ottobre, con 40 fit deduplicati. La media Mac è stata anche ricalcolata dai 40 `elapsed_sec` univoci del CSV originale. `elapsed_sec` misura il tratto del runner cronometrato dopo una parte della preparazione dei dati e non include l'avvio Python: **non** può essere chiamato tempo end-to-end. Il rapporto **2,079** descrive il confronto tra *due ambienti storici*, non misura il vantaggio causale del chip M4; differiscono virtualizzazione, CPU, RAM, OS, build e possibili impostazioni di threading.

Le differenze tra le **medie** delle AUROC si possono calcolare dai `summary.csv` (X23, Mac−Ubuntu = **+0,0025145**), ma la **dispersione delle differenze paired** richiede tutte e dieci le coppie di record Ubuntu e Mac. Sulla VM di Riccardo `scripts/audit_e1_platforms.py` ha già prodotto `paired_per_run.csv`, `metrics_by_x.csv`, `timing_by_x.csv` in `~/mlsec-local/audits/e1_hardware_comparison/`. Per completare un eventuale supplemento statistico nel repository, importare questi tre CSV senza alterare i test originali. Le coppie condividono le stesse identità di test e non sono campioni esterni indipendenti: un IC bootstrap sui soli 10 fit, se calcolato, descriverebbe la variabilità *dei fit condizionata a questo zoo*, non la generalizzazione a nuovi zoo.

**Decisione operativa:** l’esperimento E1 è sufficientemente documentato e replicato per passare alla progettazione di E2. Un nuovo benchmark controllato di memoria/wall-clock può essere svolto in un’appendice separata, ma non è necessario ripetere 40 fit né riaprire il test E1.

Figure aggiuntive: `e1_hw_auroc_comparison.png`, `e1_hw_mac_elapsed_by_x.png`, `e1_hw_mac_runs_auroc.png`. Workbook `E1_grafici.xlsx`: fogli aggiunti `Audit_hardware` e `Mac_val_standalone` (i 9 grafici precedenti sono conservati; sono stati aggiunti 2 grafici Excel nativi).

## 8. Discussione

**Messaggio principale.** La replica Mac M4 conferma qualitativamente la baseline Ubuntu, con AUROC X23 rispettivamente 0,904378 e 0,901863. Nel setting E1 il metodo centroid discrimina bene campioni benign/stego quando si sovrascrivono **23 bit di mantissa** (AUROC media ~0,902), ma ha un comportamento vicino al caso per **X=1,8,16** (AUROC 0,500–0,508). Questo è un risultato sul **particolare zoo e protocollo few-shot** studiati, non una misura universale di efficacia contro stegomalware.

La forte transizione a X23 è compatibile con un cambiamento molto più pronunciato della distribuzione dei pesi. Dal solo risultato di detection **non** possiamo inferire che un payload X23 mantenga inalterata l'utilità dei CNN, sia furtivo, venga recuperato esattamente o rappresenti malware eseguibile. Analogamente, il risultato quasi-casuale a X≤16 non prova che ogni possibile detector fallirebbe.

**Generalizzazione.** La robustezza ID misurata non dice come il detector reagisce ad attacchi di famiglia diversa (E2) né a cambi di architettura, serializzazione o lifecycle (E3 e possibili approfondimenti di tesi).

**Statistica.** La media sulle 10 ripetizioni descrive la variabilità del training e dei payload, ma un'inferenza rigorosa sul mondo esterno dovrebbe rispettare l'accoppiamento benign/stego e l'unità indipendente **checkpoint di origine**. Non attribuiamo p-value, intervalli di confidenza o differenze significative non calcolate.

## 9. Limiti e validità delle conclusioni

1. **Un solo zoo, un'architettura/popolazione di checkpoint.** Anche il Mac M4 misura lo stesso zoo e non aumenta la diversità di architettura neurale; validità esterna non dimostrata.
2. **Checkpoint test identity-disjoint ma non zoo-disjoint** e precedente esplorazione del medesimo zoo. Non chiamare il test incontaminato in senso assoluto.
3. **Few-shot estremo:** 3 identità train (6 osservazioni), 10 repliche; risultati sensibili alla casualità di training, specialmente vicino a score zero.
4. **Precisione numerica:** un run della validation v2 si è fermato per 1/400 discordanza fra margine e inferenza upstream; diagnostica successiva 0/400. Non è stata dimostrata determinismo TensorFlow bit-a-bit.
5. **Payload deterministici ≠ payload malware reale.** Byte inerti pseudo-casuali, non eseguibili; assenza di test di utility/recupero.
6. **Soglia Youden della validation.** Le accuracy Youden misurate sulla medesima validation sono ottimistiche; solo il test successivo supporta una valutazione indipendente della soglia.
7. **Classi bilanciate al 50%.** AUPRC dipende dalla prevalenza; deployment con prevalenze differenti richiede una valutazione specifica.
8. **Incertezza limitata.** Nella tabella di sintesi è disponibile SD dell'accuracy; non sono stati stimati IC cluster-aware e TPR@FPR molto basse non sarebbero giustificati da 200 benign test.
9. **Solo detection.** Attacco fattibile, recovery, execution, degrado di accuracy CNN e compromissione reale dei modelli non misurati.
10. **Confronto fra piattaforme.** Commit Mac e Ubuntu differenti; assenza di full run_config/manifest Mac e validation stand-alone allegata; nessuna prova che le piccole differenze siano causate unicamente da CPU o sistema operativo.

## 10. Conclusione E1 e collegamento a E2/E3

E1 conclude una **baseline sperimentale replicata su Ubuntu CPU x86_64 e Mac M4 CPU ARM64** su 1.000 checkpoint autentici con split identità-disgiunti, esempi paired, payload sintetici tracciati, 40 fit di validation e 40 fit sul test riservato. In questo regime, **X23 è rilevabile con AUROC media 0,901863 (Ubuntu) e 0,904378 (Mac)** dal centroid few-shot, mentre **X≤16 resta vicino a 0,5**. La calibrazione su validation produce **accuracy media test 0,82125** e **FPR 0,1550** a X23.

La replica cross-platform riproduce il comportamento **a livello aggregato** e non è una prova di equivalenza bitwise o attribuzione causale delle differenze al solo hardware. Il risultato non è una nuova difesa, né dimostra OOD generalization. **E2** confronterà il detector con un embedding di famiglia diversa non visto nell'addestramento; **E3** verificherà se i risultati resistono a controlli più forti su origine e trasformazioni. Il quadro di ricerca seguirà criteri di comparabilità e pre-registrazione delle scelte, senza sfruttare il test E1 per decidere retroattivamente i parametri.

## 11. Materiali, riferimenti e provenienza delle affermazioni

**Dati primari** (da usare per qualunque citazione numerica):

- **Replica Fabrizio Mac M4:** `results/replicas/e1_mac_m4/{summary.csv,metrics_per_run.csv,e1_v2_test.log,replication_manifest.md}`. I CSV sono estratti senza modificarli dallo ZIP fornito da Fabrizio e le medie sono state ricontrollate.

- `results/validation/e1_uniform_v2/{summary.csv,metrics_per_run.csv,run_config.json}`.
- `results/test/e1_uniform_v2/{summary.csv,metrics_per_run.csv,run_config.json}`.
- `manifests/e1_uniform_v1/{protocol.json,splits.csv}`.
- I file per-run `metrics.json` e `predictions_{validation,test}.csv` sono conservati nell'area locale `~/mlsec-local/runs/`.

**Codice:** `scripts/run_e1_final_v2.py`, `scripts/run_e1_v2_matrix.sh`, `scripts/run_e1_v2_test_matrix.sh`, `scripts/diagnose_e1_v2_centroid.py` e `external/ModelXRay` (submodule); dipendenze in `configs/modelxray-ubuntu24-py311.lock.txt`.

**Letture:** [Model X-Ray, codice](https://github.com/danigil/ModelXRay); [MaleficNet](https://doi.org/10.1007/978-3-031-17143-7_21); [Do You Trust Your Model?](https://doi.org/10.1109/TDSC.2025.3586703); [GHRP STL10, Zenodo](https://zenodo.org/records/6631784). Le fonti citate in questa bozza richiedono completamento delle voci bibliografiche formali quando si redigerà la relazione d'esame definitiva.

**Attenzione:** i risultati quantitativi di questo documento derivano dalle tabelle `summary.csv` fornite durante l'esecuzione; per aggiungere barre di errore AUROC, IC e curve ROC per checkpoint occorre rileggerne le metriche per-run e predizioni, senza inventare dati.

### Appendice hardware e riproducibilità

- Audit di dettaglio: [`E1_HARDWARE_FINAL_AUDIT.md`](../docs/E1_HARDWARE_FINAL_AUDIT.md).
- Sorgenti ricevute: [`results/replicas/e1_mac_m4/audit/`](../results/replicas/e1_mac_m4/audit/).
- I risultati Ubuntu e Mac originali restano immutati nelle cartelle `results/test/e1_uniform_v2/` e `results/replicas/e1_mac_m4/`.
