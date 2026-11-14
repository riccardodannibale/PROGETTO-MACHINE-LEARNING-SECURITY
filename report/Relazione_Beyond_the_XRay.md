---
title: "Beyond the X-Ray"
subtitle: "Rilevare modifiche steganografiche nei pesi delle reti neurali"
author: "Riccardo D'Annibale e Fabrizio Giuseppe Mazzilli"
date: "14 novembre 2026 - Relazione tecnica completa - Machine Learning Security"
---

# Valutazione sintetica

Il progetto risponde alla domanda concordata nella proposta iniziale: valutare un detector few-shot ispirato a Model X-Ray con split disgiunto per identità dei checkpoint e misurare il trasferimento da una modifica X-LSB a una seconda famiglia di embedding. Per andare oltre la sola replica, il lavoro introduce un encoder spread-spectrum keyed e didattico, un protocollo ID/OOD appaiato e controlli retrospettivi sui campioni benigni e sui metadati. Questo costituisce un contributo progettuale concreto, ma non va presentato come una nuova implementazione di MaleficNet né come una replica integrale del paper Model X-Ray.

E1 rileva la condizione X-LSB X=23 con AUROC circa 0,90, mentre X=1, 8 e 16 restano vicini al caso. E2 mostra che lo stesso detector non trasferisce il ranking alla specifica implementazione spread-spectrum provata: le AUROC OOD sono circa 0,47-0,49, cioè **al livello del caso entro la variabilità osservata**. E3 supporta l'interpretazione di una perdita di TPR sui campioni modificati, ma la stabilità della FPR è un controllo strutturale atteso, non una scoperta indipendente.

Il risultato è una base valida per un progetto magistrale e per avviare una tesi, non una tesi già completa: servono almeno intensità e capacità di payload appaiate, più architetture, un holdout realmente esterno e un confronto con un'implementazione MaleficNet autentica o con ulteriori famiglie di attacco.

# Come leggere questa relazione

**Versione di consegna:** branch `main`. I runner sperimentali E1/E2 richiedono il branch `ricky`, il cui head verificato al 14 novembre 2026 è `3ef84f73d994fc447b12bb99f265c203548480e4`. I file E1/E2 congelati risultano identici nei due branch; il vincolo sul branch è applicato dai runner per proteggere la provenienza degli esperimenti.

Questa relazione raccoglie in un unico documento la spiegazione del progetto, la teoria necessaria per comprenderlo, il disegno sperimentale, i risultati, i limiti, le istruzioni per controllare gli output e una mappa dei file essenziali. È scritta in modo progressivo: la prima parte fornisce una panoramica accessibile; le sezioni successive entrano nei dettagli tecnici.

La repository contiene anche alcuni **documenti di protocollo storici e immutabili** relativi all'esperimento E2. Non sono manuali aggiuntivi: sono registri di integrità e autorizzazione che il codice sperimentale controlla tramite hash e percorso. Per questo motivo vengono conservati separatamente e non riscritti dentro questa relazione.

# 1. Panoramica in parole semplici

Una rete neurale è un programma che impara a svolgere un compito regolando migliaia o milioni di numeri chiamati **pesi** (*weights*). Questi numeri determinano il comportamento del modello. Come altri file digitali, anche i pesi possono essere modificati per nascondere informazioni.

La **steganografia** consiste proprio nel nascondere un messaggio dentro un contenitore in modo che la presenza del messaggio sia difficile da notare. In questo progetto il contenitore non è un'immagine o un documento, ma il vettore numerico dei pesi di una rete neurale.

Il progetto studia un sistema di rilevamento ispirato a **Model X-Ray**. Il sistema viene addestrato con pochi esempi di pesi benigni e modificati e impara a distinguerli. La domanda centrale è: se il rilevatore impara a riconoscere una tecnica di modifica, riesce a riconoscere anche una tecnica diversa che non ha mai visto durante l'addestramento?

Per rispondere sono stati svolti tre esperimenti:

- **E1 - Baseline X-LSB:** misura se il rilevatore riconosce modifiche ai bit meno significativi dei pesi, a diversi livelli di intensità.
- **E2 - Trasferimento a spread-spectrum:** addestra il rilevatore solo su X-LSB e verifica se riconosce anche una tecnica sintetica spread-spectrum.
- **E3 - Controlli appaiati:** controlla se il calo di E2 è associato soprattutto alla difficoltà di riconoscere i campioni modificati, anziché a un cambiamento dei campioni benigni o a uno sbilanciamento dei metadati.

Il risultato principale è netto nelle condizioni testate: il rilevatore ottiene un'AUROC di circa **0,90** su X-LSB X=23, ma scende a circa **0,47-0,49** sullo spread-spectrum sintetico. Questo indica che la capacità appresa su X-LSB non si trasferisce automaticamente alla tecnica spread-spectrum specifica del progetto.

La conclusione è circoscritta. Non dimostra che tutti i metodi spread-spectrum siano invisibili, né che il software originale MaleficNet sia stato replicato. Il metodo spread-spectrum utilizzato qui è un prototipo didattico con payload sintetico e inerte.

# 2. Concetti teorici fondamentali

## 2.1 Reti neurali e pesi

Una rete neurale è composta da strati di calcolo. Durante l'addestramento, un algoritmo aggiorna i parametri numerici della rete per ridurre l'errore sui dati. Questi parametri sono chiamati **pesi** (*weights*) e, insieme a eventuali bias e altri parametri, definiscono il modello appreso.

In questo progetto vengono utilizzati piccoli modelli **CNN** (*Convolutional Neural Networks*), cioè reti neurali convoluzionali comunemente impiegate per elaborare immagini. Ogni checkpoint è rappresentato da un vettore di **2.864 valori `float32`**. Il formato `float32` rappresenta ogni numero usando 32 bit.

L'analisi non riguarda direttamente le immagini STL10, ma i vettori dei pesi estratti dai checkpoint. Le immagini servono soltanto nel piccolo pilot di utilità descritto nella sezione 8.

## 2.2 Steganografia nei modelli

In una modifica steganografica, un messaggio viene codificato nei parametri di un modello. L'obiettivo generale è far sì che il modello modificato possa ancora essere utilizzato, mentre i cambiamenti numerici risultino difficili da individuare.

Nel contesto della sicurezza, questo motiva un problema di controllo della supply chain dei modelli: un modello scaricato da una fonte esterna non dovrebbe essere considerato affidabile solo perché il file si carica correttamente o produce previsioni plausibili.

Il progetto valuta la capacità di un rilevatore di riconoscere alcune modifiche dei pesi. Non esegue malware, non incorpora codice eseguibile e non valuta un attacco operativo contro un sistema in produzione. I payload usati sono messaggi sintetici e inerti.

## 2.3 X-LSB: modifica dei bit meno significativi

LSB significa *Least Significant Bit*, cioè bit meno significativo. Un numero `float32` usa 1 bit per il segno, 8 per l'esponente e 23 per la mantissa. La mantissa contribuisce alla precisione del numero.

Una modifica X-LSB altera i primi X bit meno significativi della mantissa. Nel progetto vengono provati quattro livelli:

| Valore X | Modifica effettuata |
|---:|---|
| 1 | Il bit meno significativo della mantissa |
| 8 | Gli 8 bit meno significativi |
| 16 | I 16 bit meno significativi |
| 23 | Tutti i 23 bit della mantissa |

Aumentando X, la modifica può diventare più intensa. X=23 è la condizione usata come riferimento principale per l'addestramento e la calibrazione di E2.

È importante non interpretare `23 × 2.864 = 65.872` come numero di bit di messaggio recuperabili: è soltanto il numero massimo di posizioni di bit interessate sui 2.864 valori, non una misura della capacità effettiva del payload.

## 2.4 Spread-spectrum: distribuire il messaggio

Lo spread-spectrum è una famiglia di tecniche che distribuisce un segnale su molte componenti del contenitore. Nel prototipo del progetto, un messaggio sintetico di **16 bit** viene codificato usando 16 vettori pseudocasuali ortogonali nello spazio dei 2.864 pesi.

La matrice dei codici è generata in modo deterministico, usando una chiave/seme, l'indice del checkpoint e la ripetizione. I codici vengono ortonormalizzati. In forma semplificata, la modifica segue l'idea:

`w_modificato = w + (alpha * ||w||_2 / sqrt(B)) * C * b`

Dove:

- `w` è il vettore originale dei pesi;
- `B` è il numero di bit del messaggio, qui 16;
- `C` è la matrice dei codici ortogonali;
- `b` rappresenta i bit sintetici codificati;
- `alpha` controlla l'intensità relativa della perturbazione.

Nel progetto sono valutati `alpha=0.16` e `alpha=0.24`. Il decoder ricostruisce i bit dai pesi modificati usando la chiave, la ripetizione e l'identificativo del checkpoint; non ha bisogno dei pesi benigni originali.

Questa implementazione si chiama `e2-keyed-orthogonal-spread-v0-educational`. È ispirata ai principi generali dello spread-spectrum, ma **non è il software originale MaleficNet**: non implementa la stessa pipeline di correzione degli errori (ECC/LDPC), fine-tuning e configurazione del lavoro originale. I messaggi sono sintetici e inerti.

## 2.5 Model X-Ray, rete Siamese e few-shot learning

Il progetto utilizza l'implementazione upstream di **Model X-Ray**, fissata al commit Git `a880e332f556fc71faf8d3753931005d5d019339` come submodule `external/ModelXRay`.

Il metodo trasforma il vettore dei pesi in una rappresentazione 2D di dimensione 100 × 100 e usa una rete Siamese convoluzionale per confrontare rappresentazioni di modelli benigni e modificati.

Una rete **Siamese** è costituita da due rami con la stessa architettura e gli stessi parametri. I rami producono rappresentazioni confrontabili; durante l'apprendimento il sistema impara a collocare vicini gli esempi della stessa classe e più lontani quelli di classi differenti.

Il progetto adotta un regime **few-shot**: ogni fit utilizza soltanto tre identità di checkpoint per l'addestramento, ciascuna con un esempio benigno e uno modificato. Sono quindi 3 coppie, cioè 6 esempi di training per fit.

Il punteggio principale è basato sulla distanza dai centroidi:

- si calcola un centro (*centroid*) delle rappresentazioni benigne;
- si calcola un centro delle rappresentazioni modificate;
- si confronta la distanza del campione da entrambi.

Il punteggio è definito come `distanza_benigno - distanza_stego`: un valore maggiore favorisce la classe modificata. Come metodo secondario viene usato **1-NN** (*one-nearest-neighbour*), che confronta il campione con il singolo esempio di training più vicino.

## 2.6 Relazione con il paper Model X-Ray e perimetro della replica

Il paper Model X-Ray pubblicato nel 2026 descrive la rappresentazione Grayscale-Fourpart (GF), una rete few-shot e una valutazione che include attacchi X-LSB e trasferimento OOD verso MaleficNet. Il repository upstream contiene inoltre una matrice di baseline e altre pipeline di valutazione. Il presente progetto riutilizza componenti upstream del detector Siamese e della pipeline X-LSB, ma adotta un protocollo sperimentale adattato: split congelato per identità sorgente, dieci fit, tre identità di training per fit, payload sintetici deterministici e metriche/controlli aggiuntivi. Il runner E1 stesso dichiara che non si tratta di una riproduzione bit-per-bit dello split 3+3 del paper.

È essenziale non confrontare direttamente i valori X=1, 8, 16 e 23 con le percentuali di *embedding rate* riportate nel paper: X indica quanti bit meno significativi della mantissa vengono modificati, mentre l'embedding rate è una diversa quantità sperimentale. Di conseguenza, il risultato E1 non conferma né smentisce le percentuali di rilevamento pubblicate nel paper.

Anche il confronto OOD è diverso. Il paper valuta il trasferimento verso MaleficNet; E2 valuta `e2-keyed-orthogonal-spread-v0-educational`, un encoder sviluppato per questo progetto e ispirato allo spread-spectrum, ma privo della pipeline originale MaleficNet. Il risultato E2 non contraddice quindi il trasferimento OOD riportato dal paper: riguarda un encoder, una capacità di payload, un'intensità e un protocollo differenti. La formulazione corretta è che il detector non trasferisce il ranking alla specifica variante didattica qui testata.

## 2.7 Metriche: come leggere i numeri

| Metrica | Significato pratico |
|---|---|
| **AUROC** | Misura quanto bene il sistema ordina i campioni modificati sopra quelli benigni considerando tutte le soglie. 1,0 è perfetto; 0,5 è circa casuale. |
| **Accuracy** | Percentuale totale di previsioni corrette a una soglia specifica. |
| **TPR / Recall** | Quota di campioni modificati che il sistema identifica correttamente. |
| **FNR** | Quota di campioni modificati che il sistema non rileva; vale `1 - TPR`. |
| **FPR** | Quota di campioni benigni erroneamente segnalati come modificati. |
| **Precision** | Tra i campioni segnalati come modificati, quanti sono davvero modificati. |
| **F1-score** | Media armonica tra precision e recall. |
| **AUPRC** | Area sotto la curva precision-recall; utile per valutare il compromesso tra precision e richiamo. |
| **Deviazione standard (SD)** | Misura quanto i valori delle diverse ripetizioni variano attorno alla media. |

Un'AUROC di 0,5 indica che il punteggio non ordina in modo utile le due classi. Un valore sotto 0,5 può indicare che, in media, l'ordinamento è invertito rispetto alla direzione attesa; non significa automaticamente che si possa ottenere un rilevatore affidabile semplicemente invertendo il segno, soprattutto senza una valutazione separata e preregistrata.

Per le metriche che richiedono una decisione binaria viene usata, tra le altre, la soglia `val_youden`, scelta sulla validation attraverso l'indice di Youden (`TPR - FPR`). La soglia è selezionata sui dati di validation e poi mantenuta fissa sul test: non viene scelta guardando i risultati OOD del test.

# 3. Dataset, split e provenienza

## 3.1 Collezione dei checkpoint

La ricerca utilizza 1.000 checkpoint di piccole CNN provenienti dalla collezione GHRP/STL10. Ogni checkpoint finale viene rappresentato da 2.864 valori `float32`.

Il riferimento alla collezione è il record Zenodo **6631784**: <https://zenodo.org/records/6631784>.

I checkpoint originali, gli archivi completi e alcuni file intermedi di grandi dimensioni non sono inclusi nella repository pubblica. I dati devono essere ottenuti dalla fonte originaria e utilizzati rispettando i relativi termini. Il progetto non ridistribuisce automaticamente i diritti sui dati di terze parti.

È importante distinguere due file citati nel flusso di preparazione:

- `dataset.pt` contiene immagini e label STL10 pre-elaborate;
- `weights.npy` contiene i pesi numerici estratti dai checkpoint CNN.

Non sono due copie dello stesso dataset: servono a scopi differenti.

## 3.2 Suddivisione dei modelli

Lo split congelato è composto da:

| Partizione | Identità di checkpoint |
|---|---:|
| Training pool | 600 |
| Validation | 200 |
| Test | 200 |
| **Totale** | **1.000** |

La separazione avviene per identità del modello sorgente. Le versioni benigna e modificata dello stesso checkpoint restano nella stessa partizione. Questo evita che una variante del modello finisca nel training e l'altra nel test.

I dettagli sono registrati in `manifests/e1_uniform_v1/protocol.json` e `manifests/e1_uniform_v1/splits.csv`. L'hash SHA-256 dello split è:

`3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f`

L'hash SHA-256 atteso della matrice originale dei pesi è:

`5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad`

Questi hash permettono di verificare che i file utilizzati corrispondano a quelli previsti dal protocollo. Lo split è stato congelato prima delle esecuzioni finali, ma la storia di sviluppo aveva già esplorato la stessa collezione di modelli: non va descritto come un holdout esterno completamente nuovo.

## 3.3 Ripetizioni

Sono eseguiti dieci fit per configurazione e piattaforma. I fit riutilizzano le stesse 200 identità di test, ma cambiano le selezioni few-shot e i semi di addestramento. Le dieci ripetizioni misurano quindi la variabilità tra fit, non dieci dataset di test indipendenti.

Non è corretto interpretare 10 × 200 = 2.000 osservazioni come 2.000 checkpoint sorgente indipendenti.

# 4. Disegno sperimentale

## 4.1 E1 - Baseline in-distribution X-LSB

**Domanda:** il rilevatore few-shot ispirato a Model X-Ray riconosce pesi modificati con X-LSB?

Sono valutati X = 1, 8, 16 e 23. Il rilevatore viene addestrato usando esempi X-LSB e poi valutato sulle identità di test riservate. Il metodo centroid è l'analisi principale; 1-NN è un metodo secondario.

Le esecuzioni sono state effettuate su Ubuntu e replicate su Mac M4, utilizzando la stessa collezione di checkpoint e lo stesso split. La replica Mac è una verifica su una diversa piattaforma di calcolo, non un esperimento su una nuova architettura CNN.

## 4.2 E2 - Trasferimento a una famiglia di embedding diversa

**Domanda:** un rilevatore addestrato e calibrato esclusivamente su X-LSB X=23 riconosce anche la modifica spread-spectrum sintetica?

Il protocollo E2 mantiene:

- training e validation esclusivamente su X-LSB X=23;
- tre coppie benigno/modificato per fit;
- dieci fit per piattaforma;
- soglia scelta sulla validation LSB;
- test appaiato sulle stesse 200 identità sorgente per ID e OOD;
- AUROC centroid come metrica primaria;
- 1-NN, alpha=0.16 e metriche a soglia come analisi secondarie.

La condizione ID è X-LSB X=23. Le condizioni OOD sono spread-spectrum alpha=0.24 (primaria) e alpha=0.16 (secondaria). Lo stesso rilevatore addestrato in ciascun fit valuta le diverse condizioni: non viene riaddestrato tra ID e OOD.

La metrica primaria è la differenza appaiata:

`Delta AUROC = AUROC(spread alpha=0.24) - AUROC(LSB X=23)`

Una differenza negativa indica che il ranking del rilevatore peggiora sulla condizione spread rispetto alla condizione LSB dello stesso fit.

Prima di aprire il test sono stati previsti controlli di integrità, verifica delle soglie e autorizzazione distinta alla fase di test. Il protocollo congelato e il record di autorizzazione sono conservati come documenti di audit separati.

## 4.3 E3 - Controlli matched e analisi retrospettiva

**Domanda:** il calo di E2 può essere spiegato da differenze nei modelli benigni o da metadati associati alle classi?

E3 rianalizza i punteggi prodotti da E2. Per ciascuna identità sorgente controlla la presenza di una versione benigna e una modificata. Verifica inoltre l'equilibrio dei metadati, la stabilità dei punteggi benigni e le metriche ottenute mantenendo fissa la soglia di validation.

E3 non riaddestra il rilevatore e non crea un nuovo insieme di test indipendente. È un'analisi di controllo successiva all'apertura del test E2.

# 5. Risultati E1: baseline X-LSB

## 5.1 AUROC centroid

| X-LSB | Ubuntu AUROC | Ubuntu AUPRC (media ± SD) | Mac M4 AUROC | Mac M4 AUPRC (media ± SD) |
|---:|---:|---:|---:|---:|
| 1 | 0,500150 | 0,504064 ± 0,001444 | 0,500209 | 0,504417 ± 0,001155 |
| 8 | 0,508233 | 0,509345 ± 0,025420 | 0,509388 | 0,510389 ± 0,025776 |
| 16 | 0,501293 | 0,512234 ± 0,021902 | 0,501425 | 0,512511 ± 0,023323 |
| **23** | **0,901863** | **0,902063 ± 0,069213** | **0,904378** | **0,904875 ± 0,065256** |

L'AUPRC è calcolata sui punteggi continui e non dipende dalla soglia binaria; la deviazione standard è quella campionaria tra i dieci fit. Il test contiene 200 esempi benigni e 200 modificati, quindi il riferimento casuale dell'AUPRC è circa 0,50.

A X=1, X=8 e X=16 AUROC e AUPRC rimangono vicine al caso: in queste condizioni il rilevatore non ordina in modo utile i campioni benigni e modificati. A X=23 entrambe le metriche salgono a circa 0,90, indicando una buona capacità di distinguere le due classi nella collezione studiata.

## 5.2 Metriche a soglia

Con la soglia selezionata sulla validation (`val_youden`), a X=23:

| Metrica | Ubuntu | Mac M4 |
|---|---:|---:|
| Accuracy media | 0,82125 | 0,82300 |
| FPR medio | 0,1550 | 0,1605 |

L'accuratezza dipende dalla soglia usata, mentre AUROC misura il ranking su tutte le soglie. Per questo le due metriche vanno lette insieme.

## 5.3 Confronto hardware

L'audit descrittivo E1 ha riportato un tempo medio della sezione misurata di 217,124 secondi su Ubuntu e 104,412 secondi su Mac M4, con un rapporto Ubuntu/Mac di circa 2,079. Non è un benchmark causale della CPU: la macchina Ubuntu era una macchina virtuale e sistema operativo, virtualizzazione, processore, build TensorFlow e memoria sono fattori confondenti. Il timing esclude inoltre alcune fasi iniziali e la scrittura dei CSV.

La conclusione principale di E1 non riguarda la velocità: è la conferma che la condizione X-LSB X=23 è riconoscibile dal rilevatore, mentre le altre intensità testate non lo sono in modo utile.

# 6. Risultati E2: trasferimento OOD

## 6.1 AUROC centroid

| Condizione | Ubuntu AUROC (media ± SD) | Ubuntu AUPRC (media) | Mac M4 AUROC (media ± SD) | Mac M4 AUPRC (media) |
|---|---:|---:|---:|---:|
| ID: X-LSB X=23 | **0,904273 ± 0,063014** | **0,904619** | **0,904300 ± 0,059861** | **0,904341** |
| OOD: spread alpha=0,24 | 0,477620 ± 0,039926 | 0,492045 | 0,474500 ± 0,037686 | 0,488265 |
| OOD: spread alpha=0,16 | 0,494701 ± 0,024164 | 0,497873 | 0,491042 ± 0,022405 | 0,496086 |

Gli aggregati ufficiali pubblicano l'AUPRC media ma non la sua deviazione standard per fit; per questo non viene inventata una SD AUPRC. Anche qui la prevalenza delle classi è bilanciata e l'AUPRC casuale è circa 0,50.

La differenza primaria appaiata OOD-ID (alpha=0,24) è:

| Piattaforma | Delta AUROC medio |
|---|---:|
| Ubuntu | -0,426653 |
| Mac M4 | -0,429800 |

La differenza è negativa in tutte e dieci le ripetizioni su entrambe le piattaforme, secondo i record pubblicati.

## 6.2 Metodo secondario 1-NN

| Condizione | Ubuntu AUROC | Mac M4 AUROC |
|---|---:|---:|
| ID: X-LSB X=23 | 0,820174 | 0,816670 |
| OOD: spread alpha=0,24 | 0,480515 | 0,480939 |

Anche il metodo secondario mostra lo stesso andamento generale. L'evidenza non dipende quindi soltanto dalla scelta del metodo centroid, pur rimanendo il centroid la metrica primaria preregistrata.

## 6.3 Interpretazione

Il rilevatore mantiene un AUROC vicino a 0,90 sulla condizione ID X-LSB, ma scende a 0,475-0,495 sulle condizioni spread-spectrum. Questi valori sono **compatibili con prestazioni al livello del caso** entro la variabilità tra fit: non sono sufficienti per sostenere un ranking inverso affidabile. Il risultato indica che la rappresentazione appresa usando X-LSB non si trasferisce alla particolare famiglia di modifica sintetica testata.

È corretto parlare di **mancato trasferimento nelle condizioni sperimentali considerate**. Non è corretto concludere che ogni tecnica spread-spectrum sia non rilevabile, che il sistema Model X-Ray sia inutile o che il progetto abbia riprodotto MaleficNet.

## 6.4 Accordo tra piattaforme

Le medie ID sono quasi identiche: la differenza Mac-Ubuntu è circa +0,000028. Per spread alpha=0,24 la differenza Mac-Ubuntu è -0,003120; per alpha=0,16 è -0,003659. Anche le differenze primarie OOD-ID sono molto simili: -0,426653 su Ubuntu e -0,429800 su Mac M4.

Questo è un buon accordo a livello aggregato. Non viene rivendicata una riproduzione bit-per-bit dell'addestramento TensorFlow.

# 7. Risultati E3: controlli sui campioni appaiati

Per il metodo centroid e alpha=0,24:

| Metrica | Ubuntu ID | Ubuntu OOD | Mac ID | Mac OOD |
|---|---:|---:|---:|---:|
| AUROC | 0,9043 | 0,4776 | 0,9043 | 0,4745 |
| TPR | 0,8135 | 0,1815 | 0,8190 | 0,1785 |
| FNR | 0,1865 | 0,8185 | 0,1810 | 0,8215 |
| FPR | 0,1820 | 0,1820 | 0,1750 | 0,1750 |
| Concordanza matched | 0,9265 | 0,4765 | 0,9280 | 0,4800 |

**TPR** è la quota di modificati correttamente riconosciuti. Passa da circa 81-82% a circa 18%. **FNR** è la quota di modificati mancati e sale a circa 82%.

La **FPR identica tra ID e OOD non è un risultato indipendente**: il codice di controllo verifica che i punteggi benigni siano esattamente gli stessi tra condizioni (`max_benign_score_difference = 0`) e mantiene la medesima soglia di validation per ogni fit. La FPR invariata è quindi una conseguenza strutturale attesa e va interpretata come controllo di coerenza del pairing, non come prova autonoma di robustezza.

Il controllo sui metadati produce una baseline di maggioranza del 50%, come previsto dalla costruzione con una versione benigna e una modificata per ogni identità. Questo riduce la possibilità che i soli metadati controllati risolvano il compito, ma non esclude qualsiasi possibile scorciatoia di preprocessing o rappresentazione.

La parte informativa di E3 è la caduta della TPR, l'aumento complementare della FNR e la bassa concordanza appaiata per i campioni spread. E3 resta un'analisi post-hoc sui medesimi risultati E2, non un nuovo holdout indipendente.

# 8. Pilot di utilità e intensità delle perturbazioni

Prima del test principale è stato eseguito un piccolo pilot solo su tre checkpoint appartenenti al training pool e su 256 immagini per modello. Le reti CNN originali sono state ricostruite dai parametri e valutate senza fine-tuning.

| Condizione | Accuracy media immagini | Differenza dal benigno | Norma relativa L2 |
|---|---:|---:|---:|
| Benigno originale | 37,2396% | 0,0000 punti percentuali | 0% |
| X-LSB X=23 | 26,0417% | -11,1979 pp | 31,2191% |
| Spread alpha=0,16 | 35,6771% | -1,5625 pp | 16,0000% |
| Spread alpha=0,24 | 31,3802% | -5,8594 pp | 24,0000% |

Nel pilot, il recupero dei 16 bit sintetici è riuscito per tutti e tre i checkpoint in entrambe le condizioni spread. Tuttavia tre modelli e 256 immagini non sono sufficienti per affermare che lo spread-spectrum preservi in generale l'utilità di una rete neurale.

Il pilot riportato in tabella misura una perturbazione relativa media di X-LSB X=23 pari al 31,2191%, contro 16% e 24% per le due condizioni spread. Separatamente, l'audit G2 su 20 checkpoint del training pool ha misurato una norma relativa media X-LSB pari a 0,312615 (31,2615%). I due valori provengono da insiemi di checkpoint differenti e non vanno confusi. Pertanto X-LSB e spread non sono stati confrontati a parità perfetta né di norma relativa né di capacità del payload. Questo è un confondente importante: il calo AUROC non può essere attribuito esclusivamente alla diversa famiglia di embedding come se tutte le altre caratteristiche fossero identiche.

# 9. Limiti e validità delle conclusioni

1. **Una sola collezione di checkpoint.** Non viene dimostrata la generalizzazione a zoo indipendenti, altre architetture o modelli di dimensioni differenti.
2. **Identità di test riutilizzate.** Le dieci ripetizioni riutilizzano le stesse 200 identità; non sono dieci test set indipendenti.
3. **Intensità non perfettamente appaiate.** X-LSB X=23 e spread alpha=0,24/0,16 differiscono per perturbazione relativa e capacità del messaggio.
4. **E3 retrospettivo.** E3 analizza i punteggi di E2 dopo l'apertura del test; non costituisce un nuovo holdout cieco.
5. **Payload sintetici.** Non sono stati incorporati né eseguiti malware o contenuti eseguibili.
6. **Pilot di utilità limitato.** La valutazione di utilità usa tre checkpoint e 256 immagini per modello; non supporta conclusioni generali.
7. **Artefatti raw incompleti.** Non tutti i checkpoint originali, le predizioni per campione e gli intermedi locali sono redistribuiti nella repo.
8. **Riproducibilità numerica.** I risultati aggregati tra Ubuntu e Mac sono vicini, ma non si rivendica identità bitwise tra gli addestramenti.
9. **Storia di sviluppo.** La stessa collezione era stata esplorata durante le fasi preliminari; lo split congelato non equivale a una validazione esterna indipendente.
10. **Shortcut non completamente esclusi.** I controlli E3 riducono alcune spiegazioni alternative, ma non dimostrano che qualsiasi forma di leakage o scorciatoia sia impossibile. La FPR stabile è attesa per costruzione perché gli score benigni non cambiano; non va usata come evidenza autonoma.
11. **Interpretazione dell'AUROC OOD.** Le medie inferiori a 0,50 sono accompagnate da variabilità tra fit e da intervalli descrittivi che attraversano 0,50; la conclusione prudente è “al livello del caso”, non “ranking invertito”.

La conclusione sostenibile è: **per la collezione GHRP/STL10, il rilevatore Siamese few-shot e i livelli di perturbazione testati, un sistema addestrato e calibrato su X-LSB X=23 non trasferisce le proprie prestazioni di ranking alla specifica implementazione spread-spectrum sintetica valutata in E2.**

# 10. Riproducibilità e istruzioni operative

## 10.1 Che cosa è possibile verificare con la repository pubblica

La repo contiene il codice, il submodule fissato, lo split congelato, le configurazioni, le tabelle aggregate e diversi artefatti di audit. Per una verifica leggera del contenuto pubblicato, senza riaddestrare il detector, eseguire dalla radice della repo (su `main` o `ricky`):

```bash
python3 scripts/verify_published_results.py
python3 tests/test_verify_published_results.py
python3 tests/test_repository_layout.py
python3 tests/test_e2_g5_preflight.py
python3 tests/test_e2_g7_release_contract.py
```

Un controllo dei risultati pubblicati completato correttamente stampa:

`PUBLISHED E2/E3 SUMMARY QA OK`

Questa verifica controlla le tabelle aggregate e i rapporti tra i CSV. Non ricalcola ogni AUROC partendo da tutte le predizioni raw, non apre i checkpoint originali e non esegue training. I quattro test presenti sono `test_verify_published_results.py`, `test_repository_layout.py`, `test_e2_g5_preflight.py` e `test_e2_g7_release_contract.py`. La repository non ha una workflow GitHub Actions attiva: i controlli vengono eseguiti manualmente. La finalizzazione documentale non equivale a un nuovo run di questi test né a un nuovo training.

## 10.2 Clonare la repository correttamente

Per scaricare il progetto includendo anche il submodule Model X-Ray:

```bash
git clone --recurse-submodules https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY.git
cd PROGETTO-MACHINE-LEARNING-SECURITY
```

Se la repo è già stata clonata senza submodule:

```bash
git submodule update --init --recursive
```

Verificare lo stato Git:

```bash
git status
git log -1 --oneline
git submodule status
```

Per leggere la consegna si usa il branch `main`. Per rieseguire E1/E2 con i runner congelati, passare invece al branch sperimentale `ricky`: i runner E1 test ed E2 controllano esplicitamente il nome del branch e si fermano se è diverso. Il suo head verificato per questa consegna è `3ef84f73d994fc447b12bb99f265c203548480e4`. I file dei runner e il protocollo E2 congelato hanno gli stessi contenuti su `main` e `ricky`; non rimuovere il controllo sul branch.

```bash
git switch ricky
git rev-parse HEAD
```

## 10.3 Ambiente di riferimento

L'ambiente registrato per gli esperimenti è Ubuntu 24.04 LTS, Python 3.11, Git e `uv`, con dipendenze fissate in `configs/modelxray-ubuntu24-py311.lock.txt`.

Gli script di setup sono:

```bash
./scripts/setup_linux.sh
./scripts/check_setup.sh
```

Il setup crea l'ambiente virtuale in `$HOME/mlsec-local/venvs/modelxray`. Prima di avviarlo, controllare che il percorso sia adatto alla propria macchina. `check_setup.sh` verifica l'importazione delle librerie e del submodule; può anche generare grafici upstream nella cartella del progetto esterno.

## 10.4 Dataset e checkpoint necessari per rifare il training

Il clone Git da solo non basta per ripetere gli esperimenti completi. Servono gli archivi originali dei modelli, i checkpoint e la matrice estratta `weights.npy`. I dati non sono inclusi nella repo per dimensioni e termini di distribuzione.

Gli script predisposti sono:

```bash
export MODELXRAY_GHRP_DIR="$HOME/mlsec-local/datasets/ghrp_zoos"
bash scripts/download_d1_stl10.sh --all
INPUT_ROOT="$(find "$MODELXRAY_GHRP_DIR" -type d -name tune_zoo_stl_small_uniform -print -quit)"
test -n "$INPUT_ROOT"
python3 scripts/extract_d1_real_weights.py \
  --input-root "$INPUT_ROOT" \
  --output-dir "$MODELXRAY_GHRP_DIR/d1_uniform_real" \
  --expected-models 1000
sha256sum "$MODELXRAY_GHRP_DIR/d1_uniform_real/weights.npy"
```

Il download predefinito salva i dati fuori dalla repo in `$HOME/mlsec-local/datasets/ghrp_zoos` (modificabile tramite `MODELXRAY_GHRP_DIR`). Lo script di estrazione richiede la directory `tune_zoo_stl_small_uniform/` che contiene le cartelle `NN_tune_trainable_*` e produce `weights.npy`, `checkpoint_manifest.csv` e `extraction_summary.json`. Il file `weights.npy` deve avere shape `(1000, 2864)`, dtype `float32` e SHA-256 `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad`.

**Non avviare una nuova campagna E1/E2 soltanto per controllare il repository.** Il training richiede i dati originali, l'ambiente compatibile e il rispetto dei protocolli congelati. I runner E2 includono inoltre blocchi di integrità e una distinta autorizzazione al test. Non modificare il protocollo congelato, non sovrascrivere output completati e non usare i risultati OOD per scegliere nuovi parametri.

## 10.5 Comandi di riesecuzione e gate

Dopo aver predisposto ambiente e `weights.npy`, la matrice di validation E1 può essere avviata con:

```bash
export MODELXRAY_PYTHON="$HOME/mlsec-local/venvs/modelxray/bin/python"
export MODELXRAY_GHRP_DIR="$HOME/mlsec-local/datasets/ghrp_zoos"
export E1_V2_OUT_DIR="$HOME/mlsec-local/runs/e1_v2_validation"
bash scripts/run_e1_v2_matrix.sh
```

Il wrapper E1 test usa percorsi locali predefiniti per validation/test; richiede branch `ricky`, working tree pulito, preflight valido e conferma esplicita. Non eseguire `--run` come semplice smoke test. Per E2 la sequenza è più restrittiva: runner sul branch `ricky`, dieci fit di validation, audit G6, file locale di autorizzazione G7 e soltanto dopo test ID/OOD. L'ordine è implementato nei wrapper `e2_g6_run_validation.sh`, `e2_g6_audit_validation_v2.py`, `e2_g7_prepare_test_release.py`, `e2_g7_run_test.sh` ed `e2_g7_audit_test.py`. Non aggirare i blocchi e non riutilizzare output ufficiali.

## 10.6 Entry point degli esperimenti

| Esperimento | Script principale | Scopo |
|---|---|---|
| Preparazione | `extract_d1_real_weights.py` | Estrarre i pesi dai checkpoint originali. |
| E1 | `run_e1_final_v2.py` | Eseguire il baseline X-LSB. |
| E1 matrice | `run_e1_v2_matrix.sh` | Eseguire le configurazioni di validation. |
| E1 test | `run_e1_v2_test_matrix.sh` | Eseguire il test E1 dopo i preflight. |
| E2 embedding | `e2_synthetic_spread.py` | Implementare il payload spread-spectrum didattico. |
| E2 | `run_e2_paired_v0.py` | Eseguire il confronto paired ID/OOD. |
| E2 QA | `e2_g6_audit_validation_v2.py`, `e2_g7_audit_test.py` | Verificare gli output della validation e del test. |
| E3 | `e3_matched_controls.py` | Calcolare i controlli appaiati. |
| E3 confronto | `e3_compare_controls.py` | Confrontare i controlli tra piattaforme. |
| Risultati | `verify_published_results.py` | Verificare le tabelle aggregate pubblicate. |

I runner usano alcuni percorsi predefiniti sotto `$HOME/mlsec-local`. La matrice E1 validation consente override tramite `MODELXRAY_PYTHON`, `MODELXRAY_GHRP_DIR` ed `E1_V2_OUT_DIR`; il wrapper E1 test mantiene invece i percorsi validation/test sotto `$HOME/mlsec-local/runs/`. I wrapper E2 G6/G7 hanno a loro volta percorsi locali predefiniti. Non sono stati modificati perché legati alla provenienza del protocollo; per una riesecuzione conforme bisogna predisporre tali percorsi o seguire il loro `--help`/preflight, senza alterare i controlli di integrità.

Le sigle G3/G4/G5/G6/G7 sono fasi interne di gate: rispettivamente pilot di utilità, congelamento del protocollo, runner/preflight, audit validation e rilascio/audit test. Non sono esperimenti distinti da E1/E2/E3.

## 10.7 Nota sulla precisione CSV

Durante l'audit Mac M4 di E2 è emersa una discrepanza nella lettura di alcuni valori molto vicini alla soglia, pari a un'unità nell'ultima cifra rappresentabile (*ULP*). Il parser pandas predefinito poteva arrotondare un punteggio sulla soglia e alterare una decisione stretta `score > threshold`. L'audit è stato aggiornato usando `pd.read_csv(..., float_precision="round_trip")`.

Il controllo round-trip ha eliminato i mismatch. Non sono stati modificati detector, training, semi, split, punteggi, soglie o metriche preregistrate: è stata corretta la procedura di lettura numerica del CSV.

# 11. Struttura della repository di consegna

La versione ripulita è organizzata per separare documentazione completa, codice, prove dei risultati e registri sperimentali.

| Percorso | Contenuto e motivo per cui è mantenuto |
|---|---|
| `README.md` | Pagina iniziale sintetica con risultati principali, mappa e comandi di verifica. |
| `LICENSE` | Licenza MIT del codice originale del progetto. |
| `.gitignore` | Esclude ambienti locali, checkpoint, dataset e file intermedi grandi. |
| `.gitmodules` | Definisce il submodule Model X-Ray. |
| `configs/modelxray-ubuntu24-py311.lock.txt` | Versioni bloccate delle dipendenze dell'ambiente di riferimento. |
| `manifests/e1_uniform_v1/` | Protocollo e split dei 1.000 checkpoint. |
| `external/ModelXRay/` | Submodule upstream fissato a un commit preciso. |
| `scripts/` | Download, estrazione, setup, runner E1/E2/E3, audit e verifica dei risultati. |
| `tests/` | Controlli essenziali del layout, del verificatore e dei gate E2. |
| `results/test/` | Risultati finali E1 su Ubuntu, con metriche per fit e riepilogo. |
| `results/replicas/` | Risultati E1 su Mac M4, manifest e hash di provenienza. |
| `results/e2_final/` | Tabelle E2, AUROC appaiate, statistiche cross-platform, manifest e grafici. |
| `results/e3_final/` | Tabelle E3 per fit, riepiloghi, confronti tra piattaforme e grafico. |
| `results/figures/e1/` | Figure E1 selezionate, non l'intero archivio esplorativo. |
| `report/final_report.md` | Versione Markdown sintetica mantenuta nella repository. Questa relazione PDF/DOCX è un’edizione estesa con istruzioni operative e mappa dei file più dettagliate; risultati e conclusioni scientifiche restano coerenti. |
| `docs/` | Quattro registri E2: protocollo congelato, avviso di autorizzazione al test e due puntatori storici richiesti dai controlli di integrità. Non sono manuali duplicati. |

## 11.1 File di risultati da consultare

| File | Perché è importante |
|---|---|
| `results/test/e1_uniform_v2/summary.csv` | Tabella riassuntiva finale E1 Ubuntu. |
| `results/test/e1_uniform_v2/metrics_per_run.csv` | Metriche E1 per fit e configurazione. |
| `results/test/e1_uniform_v2/run_config.json` | Configurazione E1 registrata. |
| `results/replicas/e1_mac_m4/summary.csv` | Riepilogo E1 Mac M4. |
| `results/replicas/e1_mac_m4/metrics_per_run.csv` | Metriche E1 Mac M4 per fit. |
| `results/e2_final/ubuntu/summary.csv` e `mac_m4/summary.csv` | Medie E2 per piattaforma, metodo e condizione. |
| `results/e2_final/ubuntu/paired_auroc_per_repeat.csv` e `mac_m4/paired_auroc_per_repeat.csv` | Confronto ID/OOD per ciascun fit. |
| `results/e2_final/e2_cross_platform_statistics.csv` | Statistiche cross-platform e differenze OOD-ID. |
| `results/e2_final/source_manifest.json` | Provenienza e hash delle tabelle E2 pubblicate. |
| `results/e3_final/*/e3_controls_summary.csv` | Riepilogo dei controlli E3. |
| `results/e3_final/*/e3_controls_per_fit.csv` | Dettagli dei controlli per ripetizione. |
| `results/e3_final/cross_platform/` | Confronto E3 tra Ubuntu e Mac M4. |

## 11.2 File di codice principali

**Preparazione e ambiente:** `download_d1_stl10.sh`, `extract_d1_real_weights.py`, `make_e1_frozen_splits.py`, `setup_linux.sh`, `check_setup.sh`.

**E1:** `run_e1_final_v2.py`, `run_e1_v2_matrix.sh`, `run_e1_v2_test_matrix.sh`, `plot_e1_comparison.py`.

**E2:** `e2_synthetic_spread.py`, `run_e2_paired_v0.py`, `e2_intensity_train_audit.py`, `e2_g3_cnn_forward_train.py`, `e2_g3_train_utility.py`, `e2_g6_audit_validation_v2.py`, `e2_g6_run_validation.sh`, `e2_g7_prepare_test_release.py`, `e2_g7_run_test.sh`, `e2_g7_audit_test.py`, `e2_g7_compare_platforms.py`.

**E3 e verifica:** `e3_matched_controls.py`, `e3_compare_controls.py`, `verify_published_results.py`.

Gli script diagnostici ad hoc, i riepiloghi di sviluppo duplicati e gli output esplorativi non necessari alla consegna non fanno parte dell'albero `main`; i quattro registri `docs/` rimasti sono necessari alla provenienza dei gate E2.

# 12. Convenzioni dei registri E2

Le sigle G3, G4, G5, G6 e G7 sono etichette interne dei gate di sviluppo e di integrità E2; non indicano esperimenti scientifici aggiuntivi rispetto a E1, E2 ed E3. In breve: G3 identifica il pilot di utilità; G4 il protocollo congelato; G5 il runner e il preflight; G6 l'audit della validation; G7 l'autorizzazione e l'audit del test.

I quattro file in `docs/` sono mantenuti perché i runner e i test verificano contenuto, percorso o hash di alcuni di essi. In particolare, `docs/E2_PROTOCOL_FROZEN.md` ha hash Git blob `696854c0669964bc92033034af90ec84443d20c3` ed è immutabile nell'ambito dei risultati pubblicati. I due file di poche righe `E2_G3_UTILITY_RESULTS.md` e `E2_PROTOCOL_FINAL_REVIEW.md` sono puntatori storici richiamati dal protocollo: non sono documentazione ridondante da eliminare.

Il branch `main` raccoglie la documentazione descrittiva consolidata nel report e nel README; i risultati sperimentali e i file congelati restano invariati. La repository non contiene una workflow GitHub Actions attiva: i quattro test essenziali vanno quindi eseguiti manualmente.

# 13. Licenze e componenti di terze parti

Il codice originale scritto per questo progetto è distribuito sotto licenza **MIT**, riportata in `LICENSE`. La licenza del codice del progetto non si estende automaticamente ai componenti esterni.

Il submodule Model X-Ray, fissato al commit `a880e332f556fc71faf8d3753931005d5d019339`, dichiara una licenza **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**. Occorre quindi rispettarne attribuzione, limitazione non commerciale e condizioni sulle opere derivate; la licenza MIT del repository principale non modifica quei termini.

Il record Zenodo 6631784 della collezione GHRP/STL10 dichiara **Creative Commons Attribution 4.0 International (CC BY 4.0)**. La collezione può essere consultata e riutilizzata secondo tale licenza, con attribuzione alla fonte e rispetto degli eventuali termini di altri componenti inclusi.

La repository non contiene gli archivi originali né `weights.npy`. Quest'ultimo, se ricostruito correttamente, ha dimensione attesa di circa 10,92 MiB (1000 × 2864 valori `float32`) ed è piccolo abbastanza da poter essere pubblicato in una release dedicata, con manifest e attribuzione. Non lo aggiungiamo qui perché il file non è disponibile nell'ambiente di finalizzazione e non sarebbe corretto ricrearlo o dichiararne l'hash senza averlo verificato.

# 14. Glossario essenziale

| Termine | Spiegazione |
|---|---|
| **AUROC** | Misura la capacità di ordinare correttamente benigni e modificati considerando tutte le soglie. |
| **Checkpoint** | File che contiene lo stato dei parametri di una rete neurale in un determinato momento. |
| **CNN** | Rete neurale convoluzionale, spesso usata per immagini. |
| **Centroid** | Centro delle rappresentazioni di una classe, usato per confrontare le distanze. |
| **Few-shot** | Apprendimento con pochissimi esempi. |
| **FPR / FNR** | Tasso di falsi positivi / tasso di falsi negativi. |
| **ID / OOD** | In-distribution, condizione simile a quella di training / out-of-distribution, condizione diversa. |
| **LSB** | Bit meno significativo di un numero. |
| **Manifest** | File che registra identità, configurazioni, provenienza o hash degli input. |
| **OOD transfer** | Capacità di un sistema di funzionare su una condizione diversa da quella vista in addestramento. |
| **Submodule Git** | Collegamento a un altro repository Git fissato a una versione precisa. |
| **TPR** | Quota di campioni modificati identificati correttamente. |
| **Youden threshold** | Soglia scelta sulla validation per massimizzare `TPR - FPR`. |

# 15. Conclusione

Il progetto fornisce una valutazione controllata di un rilevatore few-shot per modifiche steganografiche dei pesi di reti neurali. E1 mostra che il detector riconosce la condizione X-LSB X=23 nella collezione studiata, ma non le intensità X=1, 8 e 16. E2 mostra che la capacità ID non si trasferisce alla specifica tecnica spread-spectrum sintetica implementata per il progetto: le AUROC OOD sono al livello del caso entro la variabilità osservata. E3 documenta una forte perdita di TPR sui campioni modificati, mentre la FPR invariata è un controllo strutturale atteso perché i punteggi benigni e la soglia restano invariati.

Il contributo richiesto di andare oltre la semplice replica è rappresentato da un encoder keyed a codici ortogonali sviluppato per il progetto e da un protocollo di controlli appaiati. La rivendicazione corretta è un contributo sperimentale e metodologico didattico, non una nuova implementazione di MaleficNet o una superiorità rispetto al paper. Una futura tesi potrebbe trasformare questo scaffold in uno studio più ampio: intensità L2 e capacità di payload appaiate; confronto con la vera pipeline MaleficNet; più architetture e collezioni indipendenti; holdout esterno; metriche di utilità su più task; e controlli/attacchi ulteriori.

Il progetto è quindi una **base sensata per una possibile tesi magistrale**, ma non una tesi già completa. L'approvazione finale dell'impostazione da parte del docente resta una decisione accademica separata dai risultati tecnici.

# Riferimenti

1. D. Gilkarov e R. Dubin, *Model X-Ray: Detection of Hidden Malware in AI Model Weights Using Few Shot Learning*, arXiv:2409.19310 (2024); versione journal in *Journal of Information Security and Applications*, vol. 101, settembre 2026, art. 104517, DOI: `10.1016/j.jisa.2026.104517`. Codice: <https://github.com/danigil/ModelXRay>.
2. D. Hitaj et al., *MaleficNet: Hiding Malware into Deep Neural Networks Using Spread-Spectrum Channel Coding*, ESORICS 2022, DOI: `10.1007/978-3-031-17143-7_21`.
3. D. Hitaj et al., *Do You Trust Your Model? Emerging Malware Threats in the Deep Learning Ecosystem*, arXiv:2403.03593 (2024).
4. GHRP/STL10 checkpoint collection, Zenodo record 6631784, licenza CC BY 4.0: <https://zenodo.org/records/6631784>.
5. Model X-Ray upstream repository, licenza CC BY-NC-ND 4.0: <https://github.com/danigil/ModelXRay>.

**Ambito del lavoro:** progetto universitario di ricerca. I risultati devono essere interpretati entro le condizioni sperimentali e i limiti esplicitati in questa relazione.
