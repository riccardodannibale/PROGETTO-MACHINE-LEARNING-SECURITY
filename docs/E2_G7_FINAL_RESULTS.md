# E2 — Chiusura dei risultati ID/OOD e confronto hardware

**Progetto Machine Learning Security — “Beyond the X-Ray”**  
**Data:** 22 ottobre 2026 · **Fase:** progetto universitario (dicembre 2026), base per eventuale tesi magistrale 2027.  
**Stato:** le due campagne test sono completate; audit G7 Ubuntu dichiarato OK nel log e audit G7 Mac dichiarato OK da Fabrizio. Confronto statistico dei CSV verificato. Questo report non è una nuova replica di MaleficNet né un test esterno indipendente.

## 1. Domanda sperimentale e protocollo

Quanto generalizza un detector Siamese Model X-Ray addestrato **esclusivamente su embedding X-LSB X=23** quando valuta, senza riaddestramento né modifica della soglia, una famiglia di embedding **spread-spectrum sintetica** non incontrata in training? Il test appaia tre condizioni sugli stessi checkpoint sorgente: **ID X-LSB X=23**, **OOD spread α=0,24** (primaria), **OOD spread α=0,16** (secondaria). Si usano 10 fit ripetuti per piattaforma; l'osservazione primaria è la differenza intra-fit di AUROC del metodo **centroid**, OOD24 − ID. Le soglie `val_youden` sono selezionate solo sulla validation LSB.

Dettagli del blocco sperimentale: 1.000 checkpoint nello zoo (600 train / 200 validation / 200 test), 2.864 pesi float32 per checkpoint; training per fit basato su 3 checkpoint benigni e corrispondenti 3 esempi LSB, test checkpoint-disjoint rispetto al training/validation; due ambienti, Ubuntu VirtualBox x86_64 e Mac M4 ARM64. Nel test, **ogni singolo fit** vede le tre condizioni attraverso lo **stesso Siamese**. Il test è lo stesso zoo già usato in E1 e non è un nuovo holdout esterno mai consultato.

## 2. Risultato principale: AUROC del metodo centroid

| Misura sul test | Ubuntu (media ± SD, 10 fit) | Mac M4 (media ± SD, 10 fit) |
|---|---:|---:|
| ID X-LSB X=23 | 0.904273 ± 0.063014 | 0.904300 ± 0.059861 |
| OOD spread α=0,24 | 0.477620 ± 0.039926 | 0.474500 ± 0.037686 |
| OOD spread α=0,16 | 0.494701 ± 0.024164 | 0.491042 ± 0.022405 |
| **ΔAUROC principale = OOD24 − ID** | **-0.426652 ± 0.085535** | **-0.429800 ± 0.084764** |
| ΔAUROC secondario = OOD16 − ID | -0.409571 ± 0.067280 | -0.413257 ± 0.064283 |

**Interpretazione:** l'AUROC ID ≈0,904 indica buona discriminazione del tipo di embedding visto in training; AUROC OOD α=0,24 ≈0,475–0,478 è vicino al livello casuale 0,5. **Tutte le 10 differenze intra-fit sono negative su entrambe le piattaforme (20/20 confronti piattaforma×fit)**. Il sistema *in questa configurazione* non distingue efficacemente i pesi benigni da quelli con l'embedding spread sintetico. Il valore inferiore a 0,5 non autorizza da solo conclusioni sulla possibilità di invertire stabilmente le decisioni o sull'invisibilità di ogni tecnica spread-spectrum.

Per completezza, con metodo 1-NN AUROC ID è **0.820174** su Ubuntu e **0.816670** su Mac; AUROC OOD24 è **0.480515** e **0.480939**, rispettivamente. Anche questo controllo secondario mostra un netto calo.

## 3. Riproducibilità Ubuntu ↔ Mac M4

La differenza media **Mac − Ubuntu** sul ΔAUROC principale è **-0.003148** (−0.315 punti percentuali di AUROC); lo scarto massimo assoluto tra piattaforme per una stessa ripetizione è **0.009850**. Correlazione Pearson dei dieci ΔAUROC appaiati: **r=0.9971**.

Le macchine non producono risultati bit-identici, ma il segno, la dimensione e l'andamento del calo OOD sono estremamente simili. **Non sono 20 test indipendenti**: le repliche hardware condividono split, checkpoint, semi e struttura sperimentale.

Gli intervalli riportati nel file `e2_cross_platform_statistics.csv` sono **intervalli descrittivi t al 95% calcolati sulle 10 ripetizioni**, *condizionati al dataset fisso*: Ubuntu Δ24 -0.4878…-0.3655, Mac -0.4904…-0.3692. Non rappresentano un'incertezza di generalizzazione a nuovi zoo o checkpoint esterni.

## 4. Recupero dei bit e utilità delle CNN

Secondo l'audit G7 Ubuntu, fra le **2.000 incorporazioni sui checkpoint test**, il recupero completo del payload sintetico di **16 bit** è riuscito in **1.974 casi (98,70%)** per α=0,24 e **1.552 casi (77,60%)** per α=0,16. Questo conferma che le perturbazioni sono spesso decodificabili indipendentemente dal detector; **non è una misura di esecuzione di malware**.

Il pilot separato G3-C, basato su **3 CNN del training pool e 256 immagini del valset originale per modello**, aveva misurato un'accuracy media **37,24% benign**, **26,04% X-LSB X=23**, **35,68% spread α=0,16** e **31,38% spread α=0,24**. Sono stime esplorative: il pilot non dimostra preservazione generalizzata dell'utilità funzionale di tutti i checkpoint.

## 5. Audit e provenienza

- **Ubuntu:** nel log fornito da Riccardo compare `E2 G7 OFFICIAL PAIRED TEST QA OK`, seguito da 10 fit, 160 record di metriche, 8.000 predizioni validation, 24.000 predizioni test e 8.030 record di payload. `summary.csv` e `paired_auroc_per_repeat.csv` sono ricostruiti fedelmente dal testo terminale allegato; per un audit indipendente completo delle predizioni serve la directory ufficiale conservata su Ubuntu.
- **Mac M4:** Fabrizio comunica lo stesso `G7 QA OK`; lo ZIP consegnato contiene `summary.csv`, `paired_auroc_per_repeat.csv`, `metrics_per_run.csv`. Da quest'ultimo abbiamo ricostruito **tutte le 16 righe** delle medie/SD di Mac e tutte le 10 righe degli AUROC appaiati, senza incongruenze. Lo ZIP **non contiene** i CSV delle 24.000 predizioni né i manifest dei payload: l'audit a livello di predizione su Mac rimane attestato dal log di Fabrizio, non rieseguibile sul solo ZIP.
- Runner E2 congelato SHA-256: `4719e6d947c5c5f7acba09f464ec0d2e5abf5182c642af8a063789ca217849ac`. Nessun riaddestramento fra condizioni ID/OOD di uno stesso fit; nessun tuning post-test.

## 6. Limiti da riportare senza eccezioni

1. **Non è MaleficNet originale.** L'attacco OOD è uno *spread-spectrum sintetico ispirato al principio di diffusione*, con messaggi innocui da 16 bit, non codice eseguibile.
2. **Non è un confronto a intensità o capacità matched.** X-LSB X=23 e spread α=0,24/0,16 differiscono per meccanismo, perturbazione relativa L2 e quantità di informazione incorporata. Il calo AUROC non può essere attribuito causalmente alla sola famiglia di attacco.
3. **Non è un holdout esterno veramente cieco.** I checkpoint test sono disgiunti per identità rispetto a train e validation, ma appartengono allo stesso zoo E1 già studiato in precedenza.
4. **Le dieci ripetizioni non sono dieci dataset indipendenti.** Le SD e gli intervalli descrivono variabilità dei fit su checkpoint test condivisi; non stimano da soli l'incertezza su nuovi dataset o nuove architetture CNN.
5. **La classe di modello è ristretta.** CNN omogenee da 2.864 parametri, setting specifico; niente estensione automatica a reti più grandi, transformer, attacchi arbitrari o malware reale.
6. **La preservazione funzionale è verificata solo su un pilot minuscolo.** Il decoder spread recupera spesso il payload, ma l'accuracy rimane condizione da valutare su scala maggiore nella futura tesi.

## 7. Conclusione adatta alla relazione del progetto

> Su 10 fit ripetuti e checkpoint test disgiunti dalle partizioni di addestramento e validation, il detector Siamese Model X-Ray addestrato solo su X-LSB X=23 mostra buona discriminazione ID (AUROC centroid ≈0,904), ma una marcata degradazione sullo spread-spectrum sintetico non osservato in training (AUROC ≈0,475–0,478 per α=0,24). Il ΔAUROC medio appaiato è −0,4267 su Ubuntu e −0,4298 su Mac M4, con risultati molto concordi tra le piattaforme. Questi dati dimostrano un limite di generalizzazione **interna a questo specifico confronto di embedding**, non una prova universale di invisibilità dell'attacco o una replicazione di MaleficNet.

**Stato:** campagne E2 e confronto hardware concluse. Per l'archiviazione definitiva del progetto restano il commit di questo report, l'inclusione dei grafici nella relazione e l'eventuale verifica dei manifest Mac originali su richiesta, senza riaprire o modificare i test.
