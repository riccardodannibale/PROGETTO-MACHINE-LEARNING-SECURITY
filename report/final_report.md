# Beyond the X-Ray
## Rilevare modifiche steganografiche nei pesi delle reti neurali

**Progetto di Machine Learning Security**  
**Autori:** Riccardo D'Annibale e Fabrizio Mazzilli  
**Esperimenti:** E1, E2, E3  
**Versione di riferimento:** branch `main`, stato precedente alla pulizia finale: `33edfb9aaca05fd3668896aaf1db139d81240ae2`.

---

## Come leggere questa relazione

Questa relazione riunisce in un unico documento l'introduzione teorica, il disegno sperimentale, i risultati, le analisi di controllo, i limiti, le indicazioni di riproducibilità e la mappa dei file essenziali. È organizzata dal generale al particolare: prima spiega il problema con parole semplici, poi descrive metodi, esperimenti e dettagli tecnici.

La repository conserva separatamente alcuni registri E2 congelati e di autorizzazione: non sono manuali duplicati, ma documenti di provenienza sottoposti a controlli di hash dal codice. Non vanno modificati o rimossi senza una revisione formale del protocollo.

# 1. Panoramica e teoria

## 1.1 Reti neurali e pesi

Una rete neurale è un modello matematico che apprende a svolgere un compito, ad esempio classificare immagini. Durante l'addestramento vengono aggiornati numerosi parametri numerici, chiamati **pesi** (*weights*), che determinano il comportamento del modello. Un file di checkpoint conserva i valori di questi parametri in un determinato momento.

Il progetto non studia direttamente le immagini di STL10 come oggetto principale del rilevamento: analizza i vettori dei pesi estratti dai checkpoint di piccole reti convoluzionali (**CNN**, *Convolutional Neural Networks*). Ogni modello della collezione utilizzata è rappresentato da un vettore di 2.864 valori `float32`. Il formato `float32` rappresenta ogni valore usando 32 bit.

## 1.2 Steganografia nei modelli

La **steganografia** consiste nel nascondere un messaggio all'interno di un contenitore in modo che la presenza del messaggio sia difficile da notare. Il contenitore può essere un'immagine, un file audio o, come in questo studio, il vettore dei pesi di una rete neurale.

La modifica steganografica altera i parametri del modello per codificare un'informazione. Dal punto di vista della sicurezza, un modello scaricato da una fonte esterna non dovrebbe essere considerato affidabile soltanto perché il file si apre o produce previsioni plausibili: i suoi pesi potrebbero essere stati modificati.

Questo progetto valuta un rilevatore ispirato a **Model X-Ray**. La domanda centrale è se un rilevatore addestrato su una famiglia di modifiche ai pesi riesca a riconoscere anche una famiglia diversa, che non ha incontrato durante addestramento e calibrazione.

## 1.3 X-LSB: modificare i bit meno significativi

LSB significa *Least Significant Bit*, cioè bit meno significativo. Nella rappresentazione `float32`, i 32 bit sono organizzati in un bit di segno, otto bit di esponente e 23 bit di mantissa. La mantissa contribuisce alla precisione del numero.

La tecnica X-LSB modifica i primi X bit meno significativi della mantissa. In E1 vengono studiati quattro livelli:

| X | Descrizione |
|---:|---|
| 1 | Modifica il bit meno significativo della mantissa |
| 8 | Modifica gli otto bit meno significativi |
| 16 | Modifica sedici bit meno significativi |
| 23 | Modifica tutti i 23 bit della mantissa |

Aumentare X rende generalmente la modifica più incisiva. X=23 è la condizione di riferimento scelta per addestrare e calibrare il rilevatore in E2. Il numero massimo di posizioni di bit coinvolgibili non va confuso con la capacità effettiva del messaggio: non significa che siano garantiti altrettanti bit di payload recuperabili.

## 1.4 Spread-spectrum: distribuire un segnale

Lo **spread-spectrum** è una famiglia di tecniche che distribuisce un segnale su molte componenti del contenitore. Nel prototipo di questo progetto si nasconde un messaggio sintetico e inerte di 16 bit all'interno di un vettore di 2.864 pesi, usando 16 codici pseudocasuali ortogonali.

I codici vengono generati in modo deterministico da una chiave/seme, dalla ripetizione e dall'identificativo del checkpoint. In termini semplificati, la perturbazione aggiunta ai pesi è proporzionale a `alpha`, alla norma del vettore originale e a una combinazione dei codici di spreading. Il parametro `alpha` controlla l'intensità relativa della perturbazione; i valori principali studiati sono 0.16 e 0.24.

Il decoder ricostruisce i 16 bit dai pesi modificati usando la chiave e l'identificativo del checkpoint, senza necessitare dei pesi benigni originali. È una **implementazione didattica del progetto**, denominata `e2-keyed-orthogonal-spread-v0-educational`: è ispirata ai principi generali dello spread-spectrum, ma **non è il software originale MaleficNet**. Non implementa la pipeline originale di correzione degli errori (ECC/LDPC), fine-tuning e configurazione del lavoro pubblicato. Non viene usato né distribuito malware; i payload sono sintetici e inerti.

## 1.5 Model X-Ray, rete Siamese e few-shot learning

Il progetto utilizza il codice upstream di **Model X-Ray**, fissato al commit Git `a880e332f556fc71faf8d3753931005d5d019339` nel submodule `external/ModelXRay`.

Il metodo trasforma il vettore dei pesi in una rappresentazione bidimensionale di dimensione 100 × 100 e la passa a una rete convoluzionale Siamese. Una rete **Siamese** ha due rami con la stessa architettura e gli stessi parametri condivisi: impara una rappresentazione in cui esempi simili risultano vicini e quelli diversi più lontani.

L'approccio è **few-shot learning** perché utilizza pochissimi esempi per imparare una distinzione. Ogni fit del progetto utilizza tre identità di checkpoint nel training pool, ciascuna con un esempio benigno e uno modificato: sei esempi di training in tutto.

Il punteggio principale usa la distanza dai centroidi (*centroid distance*): si calcola un centro delle rappresentazioni benigne e uno delle rappresentazioni modificate, poi si confrontano le distanze del campione da entrambi. Il margine è definito come distanza dal centro benigno meno distanza dal centro stego; valori più alti favoriscono la classe modificata. Come metodo secondario viene usato 1-NN (*one-nearest-neighbor*), che confronta il campione con l'esempio di training più vicino.

## 1.6 Metriche: come interpretare i numeri

| Metrica | Significato |
|---|---|
| **AUROC** | Capacità di ordinare correttamente esempi modificati sopra quelli benigni considerando tutte le soglie. 1 indica ranking perfetto; 0,5 è circa casuale. |
| **Accuracy** | Percentuale di classificazioni corrette a una soglia specifica. |
| **TPR / Recall** | Quota dei campioni modificati che vengono riconosciuti correttamente. |
| **FNR** | Quota dei campioni modificati che non vengono rilevati; è pari a 1 − TPR. |
| **FPR** | Quota dei campioni benigni classificati erroneamente come modificati. |
| **Precision** | Quota dei campioni segnalati come modificati che sono davvero modificati. |
| **F1-score** | Media armonica tra precision e recall. |
| **AUPRC** | Area sotto la curva precision-recall, utile per valutare il compromesso tra precisione e richiamo. |
| **Deviazione standard (SD)** | Misura la variabilità dei risultati tra i fit. |

L'AUROC valuta il ranking e non richiede di scegliere una singola soglia. Per le metriche che richiedono una decisione binaria viene usata, tra le altre, la soglia `val_youden`, selezionata sulla validation massimizzando l'indice di Youden (`TPR − FPR`). La soglia viene poi mantenuta sul test: non viene scelta osservando le etichette OOD del test.

# 2. Obiettivo e disegno sperimentale

Lo studio è diviso in tre esperimenti con ruoli distinti.

- **E1 — Baseline in-distribution:** misura quanto il rilevatore distingue le modifiche X-LSB ai diversi livelli X.
- **E2 — Trasferimento a una famiglia diversa:** addestra/calibra il rilevatore solo su X-LSB X=23 e verifica se riconosce anche il metodo spread-spectrum sintetico.
- **E3 — Controlli appaiati:** analizza retrospettivamente i punteggi E2 per controllare alcune spiegazioni alternative del calo di prestazioni.

## 2.1 Dataset e separazione

La ricerca usa 1.000 checkpoint CNN della collezione GHRP/STL10, ciascuno con 2.864 parametri `float32`. Il riferimento alla collezione è il record Zenodo 6631784: https://zenodo.org/records/6631784.

La separazione congelata è effettuata per identità del checkpoint sorgente:

| Partizione | Numero di checkpoint | Uso |
|---|---:|---|
| Training pool | 600 | Selezione dei pochi esempi usati per addestrare ogni fit |
| Validation | 200 | Calibrazione e controlli prima del test |
| Test | 200 | Valutazione finale |
| **Totale** | **1.000** | |

La versione benigna e quella modificata dello stesso checkpoint rimangono sempre nella stessa partizione. Questo evita che una versione della stessa identità compaia nel training e l'altra nel test. Il file `manifests/e1_uniform_v1/splits.csv` registra gli assegnamenti; `protocol.json` registra le dimensioni, il seme e gli hash attesi.

Hash SHA-256 dello split: `3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f`.  
Hash SHA-256 della matrice dei pesi originale: `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad`.

Dieci fit sono eseguiti per configurazione e piattaforma. Le ripetizioni cambiano la selezione few-shot e i semi, ma **riutilizzano gli stessi 200 checkpoint di test**: misurano la variabilità tra fit, non dieci dataset di test indipendenti. Non è corretto sommare le ripetizioni e descriverle come 2.000 checkpoint indipendenti.

# 3. Esperimento E1 — Baseline X-LSB

## 3.1 Domanda e procedura

E1 risponde alla domanda: il rilevatore ispirato a Model X-Ray riesce a distinguere modelli benigni da modelli modificati tramite X-LSB?

Vengono valutati X=1, 8, 16 e 23. Per ogni configurazione si effettuano dieci fit. La selezione degli esempi few-shot avviene nel training pool; la validation serve per controllare il comportamento e calibrare la soglia. I risultati finali sono confrontati tra Ubuntu e Mac M4.

E1 v2 è il protocollo finale in-distribution del progetto. Gli output esplorativi v1, quando presenti nella storia locale dello sviluppo, non vanno mescolati con le metriche v2.

## 3.2 Risultati principali

AUROC medio del metodo centroid sul test:

| X-LSB | Ubuntu | Mac M4 |
|---:|---:|---:|
| 1 | 0.500150 | 0.500209 |
| 8 | 0.508233 | 0.509388 |
| 16 | 0.501293 | 0.501425 |
| **23** | **0.901863** | **0.904378** |

A X=1, 8 e 16 l'AUROC rimane vicino a 0,5: il ranking non è utile nelle condizioni provate. A X=23 il rilevatore raggiunge circa 0,90 su entrambe le piattaforme, indicando una buona capacità di distinguere i campioni X-LSB modificati nella collezione studiata.

Con la soglia Youden scelta sulla validation, l'accuracy media a X=23 è 0.82125 su Ubuntu e 0.82300 su Mac M4. I corrispondenti FPR sono 0.1550 e 0.1605. Il metodo 1-NN è secondario e ottiene AUROC 0.815734 su Ubuntu e 0.819226 su Mac M4 a X=23.

## 3.3 Replica hardware

La replica Mac M4 utilizza la stessa collezione di checkpoint e lo stesso protocollo, non un nuovo zoo di architetture. A X=23 i valori centroid sono vicini: 0.901863 su Ubuntu e 0.904378 su Mac M4, con differenza Mac−Ubuntu di circa +0.002515.

L'audit dei tempi registra una media di 217.124 secondi su Ubuntu e 104.412 secondi su Mac M4 per la sezione misurata. Il rapporto descrittivo è circa 2.079. Non è un benchmark causale isolato: ambiente virtualizzato, sistema operativo, CPU, build TensorFlow e memoria sono fattori confondenti. I tempi non includono tutte le fasi del processo.

**Conclusione E1:** il rilevatore distingue bene la condizione X-LSB X=23, ma non dimostra una sensibilità analoga ai livelli X=1, 8 e 16.

# 4. Esperimento E2 — Trasferimento a spread-spectrum

## 4.1 Domanda e procedura

E2 studia il trasferimento tra famiglie di modifica dei pesi. Il rilevatore viene addestrato usando solo X-LSB X=23 e calibrato usando soltanto la validation X-LSB. Lo stesso fit viene poi utilizzato per valutare:
- la condizione ID X-LSB X=23;
- la condizione OOD spread-spectrum alpha=0.24 (primaria);
- la condizione OOD spread-spectrum alpha=0.16 (secondaria).

Le condizioni condividono le identità sorgente del test e il detector del fit; il detector non viene riaddestrato separatamente per l'OOD. Sono eseguiti dieci fit per piattaforma. La metrica primaria è la differenza appaiata `AUROC(OOD alpha=0.24) − AUROC(ID X-LSB)`.

Il protocollo E2 prevede controlli fail-closed: hash del runner, hash dello split e dei pesi, configurazioni, completamento della validation, approvazione separata del test e output separati. Il test non deve essere aperto per ottimizzare alpha, soglie o fit sulla base delle sue etichette.

## 4.2 Risultati centroid

| Condizione | Ubuntu: media ± SD | Mac M4: media ± SD |
|---|---:|---:|
| ID: X-LSB X=23 | 0.904273 ± 0.063014 | 0.904300 ± 0.059861 |
| OOD: spread alpha=0.24 | 0.477620 ± 0.039926 | 0.474500 ± 0.037686 |
| OOD: spread alpha=0.16 | 0.494701 ± 0.024164 | 0.491042 ± 0.022405 |
| **Delta alpha=0.24 − ID** | **−0.426653 ± 0.085535** | **−0.429800 ± 0.084764** |

La differenza primaria è negativa in tutti e dieci i fit su entrambe le piattaforme. Il metodo 1-NN mostra lo stesso andamento generale: AUROC ID pari a 0.820174 su Ubuntu e 0.816670 su Mac M4; a alpha=0.24 scende rispettivamente a 0.480515 e 0.480939.

Il calo da circa 0,90 a valori vicini a 0,5 indica che il detector addestrato su X-LSB non trasferisce il proprio ranking alla specifica implementazione spread-spectrum sintetica valutata. Non significa che il detector sia generalmente inutile: E1 mostra che sa riconoscere la condizione su cui è stato addestrato.

## 4.3 Confronto tra piattaforme

I risultati aggregati Ubuntu e Mac M4 sono molto vicini. Per alpha=0.24 la differenza Mac−Ubuntu dell'AUROC è −0.003120; per ID è circa +0.000028. Questo supporta la coerenza descrittiva della replica tra piattaforme, ma non equivale a una dimostrazione di equivalenza statistica né implica che l'addestramento TensorFlow sia bitwise-identical.

## 4.4 Precisione CSV e controllo della soglia

Durante l'audit della validation Mac M4 è stato osservato che il parser CSV predefinito poteva arrotondare alcuni valori di score molto vicini alla soglia, eliminando una differenza di un ULP (*unit in the last place*). La lettura è stata corretta usando `pandas.read_csv(..., float_precision="round_trip")` e il controllo di regressione dedicato. Con la lettura round-trip l'audit riportava zero mismatch; anche l'audit Ubuntu riportava zero mismatch.

La correzione riguarda il modo in cui i valori floating-point vengono letti dal CSV per verificare una disuguaglianza stretta. Non ha modificato detector, training, semi, split, punteggi, soglie o metriche preregistrate.

## 4.5 Pilot di utility

Prima del test E2 è stato svolto un pilot esplorativo sul comportamento delle CNN originali dopo la modifica dei pesi. Sono stati usati tre checkpoint del training pool (row_index 3, 4 e 7) e le stesse 256 immagini per condizione, senza fine-tuning.

| Condizione | Accuracy media immagini | Differenza dal benigno | Relative L2 media |
|---|---:|---:|---:|
| Benigno originale | 37.2396% | 0 pp | 0% |
| X-LSB X=23 | 26.0417% | −11.1979 pp | 31.2191% |
| Spread alpha=0.16 | 35.6771% | −1.5625 pp | 16.0000% |
| Spread alpha=0.24 | 31.3802% | −5.8594 pp | 24.0000% |

Nel piccolo pilot i messaggi da 16 bit sono stati recuperati tutti sui tre checkpoint alle due intensità spread. Il campione è però troppo piccolo per sostenere una conclusione generale sulla conservazione dell'utilità delle CNN. Questo pilot è un controllo di fattibilità, non il risultato principale di E2.

## 4.6 Interpretazione e confondenti

E2 fornisce evidenza che il detector few-shot addestrato su X-LSB X=23 non trasferisce la propria capacità di ranking alla specifica tecnica spread-spectrum sintetica usata qui. Tuttavia, X-LSB X=23 e spread alpha=0.24/0.16 non sono stati pareggiati perfettamente per intensità relativa della perturbazione o capacità del payload. Nel pilot G2 la relative L2 media per X-LSB X=23 era circa 0.3126, mentre spread usa per costruzione 0.16 e 0.24. Non si può quindi isolare causalmente la sola famiglia di embedding come spiegazione del calo.

# 5. Esperimento E3 — Controlli appaiati

## 5.1 Scopo

E3 è un'analisi retrospettiva dei punteggi del test E2. Non addestra un nuovo detector e non introduce un nuovo holdout indipendente. Controlla che ogni identità sorgente abbia una versione benigna e una modificata, che i metadati siano bilanciati nelle coppie, che i punteggi benigni rimangano uguali tra condizioni e che il tasso di falsi positivi resti coerente alla soglia di validation già fissata.

## 5.2 Risultati centroid a alpha=0.24

| Metrica | Ubuntu ID | Ubuntu OOD | Mac ID | Mac OOD |
|---|---:|---:|---:|---:|
| AUROC | 0.9043 | 0.4776 | 0.9043 | 0.4745 |
| TPR | 0.8135 | 0.1815 | 0.8190 | 0.1785 |
| FNR | 0.1865 | 0.8185 | 0.1810 | 0.8215 |
| FPR | 0.1820 | 0.1820 | 0.1750 | 0.1750 |
| Concordanza appaiata | 0.9265 | 0.4765 | 0.9280 | 0.4800 |

La TPR cala nettamente: su Ubuntu passa da circa 81% a 18%, e su Mac da circa 82% a 18%. La FPR rimane costante all'interno della piattaforma perché i punteggi benigni sono invariati e viene mantenuta la stessa soglia di validation. La FNR cresce in modo corrispondente.

Il baseline di accuratezza maggioritaria basato soltanto sui metadati è 50% per costruzione, perché ogni checkpoint sorgente contribuisce con un campione benigno e uno modificato. Questo riduce una possibile scorciatoia basata sui metadati controllati, ma non esclude ogni possibile shortcut in preprocessing, serializzazione o rappresentazione.

**Conclusione E3:** i controlli indicano che il peggioramento E2 è associato soprattutto alla perdita di TPR sui campioni modificati, non a un cambiamento del comportamento sui campioni benigni o della FPR alla soglia fissata. E3 resta un'analisi post-hoc, non un test indipendente.

# 6. Conclusioni generali

I tre esperimenti raccontano una storia coerente:
1. E1 mostra che il detector few-shot distingue bene la condizione X-LSB X=23 nella collezione studiata.
2. E2 mostra che lo stesso detector non conserva tale capacità di ranking sulla specifica tecnica spread-spectrum sintetica non vista in training e validation.
3. E3 mostra che il calo di TPR si verifica mantenendo stabili i punteggi benigni e la FPR alla soglia fissata.

Il contributo principale è documentare sperimentalmente un limite di trasferimento tra famiglie di modifica dei pesi per un detector addestrato su una sola famiglia. Non viene dimostrato che tutte le tecniche spread-spectrum siano invisibili, che il vero MaleficNet sia stato replicato, che tutte le CNN mantengano la propria utilità dopo l'embedding o che Model X-Ray non funzioni in generale.

# 7. Limiti dello studio

- **Una sola collezione di checkpoint:** non è stata dimostrata la generalizzazione a molte architetture o a zoo indipendenti.
- **Identità di test riutilizzate:** le dieci ripetizioni condividono gli stessi 200 checkpoint test e non sono dieci holdout indipendenti.
- **Intensità e payload non pareggiati:** X-LSB X=23 e spread alpha=0.24/0.16 differiscono per perturbazione relativa e capacità.
- **E3 retrospettivo:** analizza punteggi E2 già osservati, non crea un nuovo test blind.
- **Payload sintetici e inerti:** non viene testato malware eseguibile o un attacco operativo.
- **Pilot di utility limitato:** solo tre CNN e 256 immagini per condizione.
- **Artefatti non completi:** i checkpoint originali e alcuni file grezzi di prediction/intermedi non sono redistribuiti nella repository.
- **Riproducibilità numerica:** gli aggregati Ubuntu/Mac sono vicini, ma non si sostiene l'identità bitwise dell'addestramento TensorFlow.
- **Storia del dataset:** lo stesso zoo è stato esplorato nella fase di sviluppo; non deve essere descritto come un holdout esterno totalmente intatto.

Per un futuro lavoro esteso, sarebbe opportuno utilizzare checkpoint provenienti da collezioni indipendenti, un holdout esterno, più architetture e confronti con perturbazioni e capacità di payload pareggiate.

# 8. Riproducibilità e utilizzo della repository

## 8.1 Tre livelli diversi di verifica

È importante distinguere:
1. **Controllo delle tabelle pubblicate:** verifica che i CSV aggregati E2/E3 siano coerenti tra loro.
2. **Audit degli output originali:** richiede i file di prediction, log e configurazioni locali conservati sulle macchine sperimentali.
3. **Riesecuzione completa:** richiede dataset, checkpoint originali, ambiente compatibile, codice upstream e protocolli congelati.

Il passaggio 1 non implica che siano stati ripetuti training e test. Il progetto mantiene pubblicati i risultati e alcuni audit, ma non include tutti i checkpoint e gli output grezzi.

## 8.2 Verifiche leggere su una nuova copia

Clonare il progetto con il submodule:

```bash
git clone --recurse-submodules https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY.git
cd PROGETTO-MACHINE-LEARNING-SECURITY
```

Controllare i risultati aggregati E2/E3:

```bash
python3 scripts/verify_published_results.py
```

Eseguire i controlli essenziali della consegna e dei contratti E2:

```bash
python3 tests/test_repository_layout.py
python3 tests/test_verify_published_results.py
python3 tests/test_e2_g5_preflight.py
python3 tests/test_e2_g7_release_contract.py
```

Questi controlli non addestrano il detector, non caricano i checkpoint originali e non ricostruiscono l'AUROC da tutte le prediction grezze. Dopo la rimozione della workflow CI, vanno eseguiti manualmente.

## 8.3 Ambiente e riesecuzione completa

L'ambiente registrato è Ubuntu 24.04 LTS e Python 3.11. Il file `configs/modelxray-ubuntu24-py311.lock.txt` contiene le versioni fissate delle dipendenze. Gli script di setup sono `scripts/setup_linux.sh` e `scripts/check_setup.sh`; prima di eseguirli occorre verificare che il percorso locale predefinito `$HOME/mlsec-local` sia adatto al computer.

Per una riesecuzione completa servono:
- la collezione originale di checkpoint GHRP/STL10;
- il vettore estratto `weights.npy` e il relativo manifest;
- il file di split congelato;
- il submodule Model X-Ray al commit fissato;
- le dipendenze compatibili;
- gli input validation/test e gli output locali richiesti dai runner.

Il file `dataset.pt` contiene immagini/etichette STL10 pre-elaborate; `weights.npy` contiene invece i parametri estratti dalle CNN. Sono artefatti differenti. La repository non include la collezione originale completa né tutti i file intermedi. I dati devono essere ottenuti dalla fonte originale e utilizzati nel rispetto delle relative condizioni di licenza.

Le entry point principali sono:
- E1: `scripts/run_e1_final_v2.py`, `scripts/run_e1_v2_matrix.sh`, `scripts/run_e1_v2_test_matrix.sh`;
- E2: `scripts/run_e2_paired_v0.py`, con audit G6/G7 e il metodo `scripts/e2_synthetic_spread.py`;
- E3: `scripts/e3_matched_controls.py` e `scripts/e3_compare_controls.py`.

I runner storici E2 includono verifiche di hash e percorsi congelati. Non spostare o modificare `docs/E2_PROTOCOL_FROZEN.md`, `docs/E2_G7_TEST_RELEASE_NOTICE.md` o i file sorgente richiamati senza una revisione formale e una nuova registrazione del protocollo. Non sovrascrivere gli output ufficiali e non rilanciare selettivamente i fit completati per migliorare il risultato.

# 9. Mappa dei file essenziali

| Percorso | Contenuto e ruolo |
|---|---|
| `README.md` | Presentazione sintetica e accesso a questa relazione. |
| `report/final_report.md` | Relazione completa: teoria, metodo, risultati, limiti e riproducibilità. |
| `scripts/` | Preparazione dati, runner E1/E2/E3, audit e verifica dei risultati aggregati. |
| `tests/` | Test essenziali per struttura della consegna, coerenza dei risultati e blocchi del protocollo E2. |
| `results/test/e1_uniform_v2/` | Metriche, configurazione e riepilogo del test E1 Ubuntu. |
| `results/replicas/e1_mac_m4/` | Riepilogo, metriche e manifest della replica E1 Mac. |
| `results/figures/e1/` | Figure principali E1 selezionate per la consegna. |
| `results/e2_final/` | Risultati aggregati e per fit E2, confronto Ubuntu/Mac, manifest e figure. |
| `results/e3_final/` | Risultati dei controlli E3 e confronto tra piattaforme. |
| `manifests/e1_uniform_v1/` | Split congelato e metadati del protocollo E1/E2. |
| `configs/` | Dipendenze fissate per l'ambiente registrato. |
| `external/ModelXRay/` | Submodule upstream Model X-Ray al commit fissato. |
| `docs/` | Solo i registri E2 congelati, l'autorizzazione al test e le due note storiche citate dal protocollo. |
| `.gitmodules` | Definizione del submodule esterno. |
| `.gitignore` | Esclude dati locali, checkpoint, cache, ambienti e output temporanei. |
| `LICENSE` | Licenza del codice originale del progetto. |

### File di codice principali

- **Preparazione:** `download_d1_stl10.sh`, `extract_d1_real_weights.py`, `make_e1_frozen_splits.py`, `setup_linux.sh`, `check_setup.sh`.
- **E1:** `run_e1_final_v2.py`, `run_e1_v2_matrix.sh`, `run_e1_v2_test_matrix.sh`, `plot_e1_comparison.py`.
- **E2:** `e2_synthetic_spread.py`, `run_e2_paired_v0.py`, `e2_intensity_train_audit.py`, `e2_g3_cnn_forward_train.py`, `e2_g3_train_utility.py`, `e2_g6_audit_validation_v2.py`, `e2_g6_run_validation.sh`, `e2_g7_prepare_test_release.py`, `e2_g7_run_test.sh`, `e2_g7_audit_test.py`, `e2_g7_compare_platforms.py`.
- **E3 e riepiloghi:** `e3_matched_controls.py`, `e3_compare_controls.py`, `verify_published_results.py`.

### Tabelle e figure essenziali mantenute

- E1: riepiloghi e metriche per fit su Ubuntu/Mac; manifest e audit della replica Mac; figure AUROC principali.
- E2: `summary.csv`, AUROC appaiati per ripetizione, statistiche cross-platform, source manifest e tre plot ID/OOD.
- E3: riepiloghi e risultati per fit Ubuntu/Mac, tabelle cross-platform e grafico TPR/FPR.

I log diagnostici ad hoc, i risultati intermedi di validation non necessari alla sintesi finale, i pilot di sviluppo e le figure duplicate non sono inclusi nella versione di consegna ripulita. I numeri essenziali del pilot sono riportati nella sezione E2.

# 10. Pulizia della consegna

La pulizia è stata effettuata per rendere la repository leggibile senza cancellare le prove principali:
- la workflow `.github/` è stata rimossa su richiesta; non sono quindi più eseguiti controlli GitHub Actions automatici a ogni push/pull request;
- le guide e le note descrittive separate sono state integrate in questa relazione;
- `REPRODUCING.md` e le copie PDF/DOCX parallele sono state rimosse dal repository per mantenere un solo report canonico in Markdown;
- sono stati rimossi output esplorativi, audit di sviluppo ridondanti, diagnostiche puntuali, grafici duplicati e test helper non necessari alla consegna;
- sono stati conservati i risultati finali per fit e aggregati, i manifest, gli script essenziali e i test di verifica della consegna;
- la cartella `docs/` è stata ridotta ai registri E2 che il runner verifica e alle note storiche citate dal protocollo congelato.

La rimozione della workflow non elimina la possibilità di verificare il progetto: significa soltanto che i controlli elencati nella sezione precedente devono essere avviati manualmente.

# 11. Licenze e componenti di terze parti

Il codice originale del progetto è distribuito secondo la licenza MIT riportata nel file `LICENSE`. Questa licenza non sostituisce né modifica i termini dei componenti esterni.

Model X-Ray è un progetto di terze parti collegato tramite submodule e mantiene la propria licenza e i propri obblighi di attribuzione. La collezione GHRP/STL10 è distribuita dalla fonte originale indicata nel record Zenodo 6631784: prima di redistribuire checkpoint, immagini, pesi o derivati, occorre verificare i termini applicabili. La repository pubblica non include i checkpoint originali completi.

# 12. Glossario

| Termine | Significato |
|---|---|
| **AUROC** | Misura la qualità del ranking tra classe benigna e modificata. |
| **Checkpoint** | File che conserva i parametri di una rete neurale in un dato momento. |
| **CNN** | Rete neurale convoluzionale, comunemente usata per immagini. |
| **Centroid** | Centro delle rappresentazioni di una classe, usato per confrontare distanze. |
| **Few-shot** | Apprendimento basato su pochissimi esempi. |
| **FPR / FNR** | Tasso di falsi positivi / tasso di falsi negativi. |
| **ID / OOD** | In-distribution, condizione simile a quella di training / out-of-distribution, condizione diversa. |
| **LSB** | Bit meno significativo di un numero. |
| **Manifest** | File che registra identità, configurazioni, provenienza o hash degli input. |
| **Submodule Git** | Collegamento a un altro repository Git fissato a una versione specifica. |
| **TPR** | Quota dei campioni modificati rilevati correttamente. |
| **Youden threshold** | Soglia selezionata sulla validation massimizzando TPR−FPR. |

# 13. Riferimenti

1. D. Gilkarov e R. Dubin, *Model X-Ray: Detection of Hidden Malware in AI Model Weights Using Few Shot Learning*, arXiv:2409.19310 (2024); versione journal in *Journal of Information Security and Applications* (2026), DOI: 10.1016/j.jisa.2026.104517. Codice: https://github.com/danigil/ModelXRay.
2. D. Hitaj et al., *MaleficNet: Hiding Malware into Deep Neural Networks Using Spread-Spectrum Channel Coding*, ESORICS 2022, DOI: 10.1007/978-3-031-17143-7_21.
3. D. Hitaj et al., *Do You Trust Your Model? Emerging Malware Threats in the Deep Learning Ecosystem*, arXiv:2403.03593 (2024).
4. Collezione GHRP/STL10, record Zenodo 6631784: https://zenodo.org/records/6631784.

**Ambito:** progetto universitario di ricerca. I risultati vanno interpretati esclusivamente entro le condizioni sperimentali e i limiti esplicitati in questa relazione.
