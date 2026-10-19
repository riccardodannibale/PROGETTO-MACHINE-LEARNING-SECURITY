# Beyond the X-Ray — progetto di Machine Learning Security

**Stato del documento:** introduzione e impostazione sperimentale del progetto d'esame (ottobre–dicembre 2026).  
**Collaborazione:** Riccardo e Fabrizio.  
**Riferimento metodologico:** [Model X-Ray](https://github.com/danigil/ModelXRay).  
**E1:** concluso il 19 ottobre 2026, commit dei risultati `d35f8f2`; **E2, E3:** da svolgere.  
**Ambito:** esclusivamente progetto condiviso dell'esame; eventuale tesi individuale e paper costituiscono percorsi successivi e separati.

## 1. Background e motivazione

Il *machine learning supply chain* comprende acquisizione, distribuzione, caricamento, riutilizzo e aggiornamento di checkpoint di reti neurali. I pesi dei modelli sono artefatti numerici che possono essere condivisi e consumati senza che sia evidente quali modifiche siano state introdotte rispetto a una versione affidabile. In uno scenario di **steganografia/stegomalware nei pesi**, un avversario nasconde informazioni dentro i valori floating-point del checkpoint. La presenza di byte incorporati non implica automaticamente che questi siano eseguiti: *occultamento, recupero ed esecuzione del codice sono proprietà diverse*, e qui valutiamo soltanto il **rilevamento** di alterazioni sintetiche.

Gli attacchi *least significant bits* (LSB) sostituiscono un numero controllato di bit della mantissa dei pesi float32. Minore è l'intensità, più la perturbazione tende a essere numericamente sottile; intensità elevate possono alterare sensibilmente i pesi e rendere il riconoscimento più facile. L'obiettivo del detector è distinguere un checkpoint originale (*benign/cover*) da una sua versione modificata (*stego*), senza affidarsi all'identità del checkpoint stesso.

**Model X-Ray**, lavoro e codice di riferimento, studia il rilevamento di stegomalware nei parametri di modelli neurali e include metodi di few-shot learning e baseline. Il nostro studio **non presenta Model X-Ray come un metodo ideato da noi**: usa la pipeline e il Siamese originali, adattando gli esperimenti a split controllati, coppie checkpoint-matched, payload inerti tracciabili e metriche complete. Gli scenari out-of-distribution (OOD) sono già parte della letteratura di riferimento; un semplice esperimento OOD non è automaticamente una novità scientifica.

Letture di riferimento da discutere nella relazione finale: [Model X-Ray](https://github.com/danigil/ModelXRay), [MaleficNet](https://doi.org/10.1007/978-3-031-17143-7_21), [Do You Trust Your Model?](https://doi.org/10.1109/TDSC.2025.3586703). Questa è una breve cornice, non una literature review esaustiva.

## 2. Obiettivo e domanda di ricerca

**Domanda del progetto d'esame:** *un detector basato su Model X-Ray mostra un comportamento verificabile in distribuzione e come reagisce a una famiglia di embedding non vista, adottando controlli corretti contro leakage e fattori confondenti?*

Gli obiettivi operativi sono: (i) costruire una baseline riproducibile su **veri pesi neurali**, non sulle immagini del dataset di classificazione; (ii) separare gli originali tra training, validation e test; (iii) evitare che la calibrazione della soglia usi il test; (iv) misurare AUROC, AUPRC, accuracy, F1 e FPR, con ripetizioni e tracciabilità; (v) testare successivamente generalizzazione e spiegazioni alternative.

### Threat model e perimetro

Un attaccante ha accesso in scrittura ai pesi float32 di un checkpoint e può alterare bit della mantissa per incorporarvi **payload sintetici casuali non eseguibili**. Il difensore riceve una rappresentazione derivata dai pesi del checkpoint e assegna un punteggio di anomalia/stego. **Non** si esegue codice malevolo, non si prova il successo di esecuzione di malware e non si misura, in E1, la persistenza/recuperabilità del payload o l'accuracy dei CNN originali dopo l'attacco. Il valore numerico dell'alterazione non va quindi interpretato automaticamente come un attacco funzionalmente stealth.

## 3. Piano sperimentale E1–E3

| Esperimento | Configurazione | Domanda specifica | Stato al 19/10/2026 |
|---|---|---|---|
| **E1 — In-distribution (ID)** | Train LSB, validation e test LSB su checkpoint sorgente **distinti**; intensità X = 1, 8, 16, 23. | Il detector distingue benign da stego su nuove identità dello stesso zoo? | **Concluso:** validation 40/40 e test 40/40, risultati pubblicati. |
| **E2 — Attack-family shift (OOD)** | Train come E1 (LSB), test su una **seconda famiglia di embedding non osservata durante lo sviluppo**, mantenendo quanto possibile stesso modello/split. | Quanto diminuisce o cambia la detection quando cambia la famiglia di embedding? | **Da progettare ed eseguire**; famiglia alternativa e fattibilità da verificare. |
| **E3 — Confound e leakage checks** | Coppie benign/stego matched, controllo origine/serializzazione/metadati/precisione e bilanciamento; falsi positivi. | Il detector sfrutta l'attacco o scorciatoie del dataset/pipeline? | **Parziale**: matching e split di E1 già implementati; verifiche sistematiche da svolgere. |

E2 ed E3 **non sono stati completati**: non attribuire loro risultati, numeri o conclusioni. L'ordine di lavoro suggerito dalla roadmap è replica controllata → confronto ID/OOD → audit dei confondenti → relazione e presentazione.

## 4. Dataset e separazione dei dati in E1

- **Sorgente:** zoo GHRP/STL10 di checkpoint di CNN; file originali e provenance conservati localmente. Il file chiamato `dataset.pt` contiene anche dati immagine STL10: le immagini **non sono** i pesi neurali da classificare con Model X-Ray.
- **Campione sperimentale:** 1.000 checkpoint CNN reali estratti dai trial; `weights.npy` ha forma **(1000, 2864)** e dtype `float32`, ossia 2.864 parametri per CNN.
- **Split congelati:** 600 modelli nel pool train, 200 modelli validation e 200 modelli test; split per checkpoint sorgente, non per derivato cover/stego. Il detector usa **3 identità dal pool train in ogni replica** (= 3 benign + 3 stego = 6 campioni di addestramento).
- **Valutazione:** per ciascuno dei 200 checkpoint di validation/test vengono costruite entrambe le versioni, benign e stego, producendo **400 osservazioni appaiate** per partizione e replica (200 positive, 200 negative). Le 10 repliche variano le identità estratte dal pool di training e i seed di addestramento/payload.
- **Provenance verificabile:** `manifests/e1_uniform_v1/{splits.csv,protocol.json}`; il runner controlla SHA-256 e unicità di ID/hashes; non c'è sovrapposizione train/validation/test.

### Distinzione cruciale: holdout interno vs. validazione esterna

Il test E1 è *identity-disjoint* e la soglia viene fissata senza etichette del test. Tuttavia **tutti i checkpoint provengono dalla stessa famiglia/zoo** e alcune esplorazioni iniziali hanno riguardato lo stesso zoo prima del congelamento definitivo. Per rigore va chiamato **test interno riservato a livello di identità**, non benchmark completamente esterno né holdout integralmente incontaminato dall'esplorazione preliminare.

## 5. Approccio, strumenti e riproducibilità

- **Upstream Model X-Ray:** commit `a880e332f556fc71faf8d3753931005d5d019339`, incluso come submodule senza modificarne i file sorgente.
- **Ambiente:** Ubuntu 24.04 in VM VirtualBox; Python 3.11 in virtualenv; TensorFlow su CPU (senza GPU); ~11 GiB RAM e 4 GiB swap. Freeze dipendenze in `configs/modelxray-ubuntu24-py311.lock.txt`.
- **Codice specifico E1:** `scripts/extract_d1_real_weights.py`, `scripts/make_e1_frozen_splits.py`, `scripts/run_e1_final_v2.py`, `scripts/run_e1_v2_matrix.sh`, `scripts/run_e1_v2_test_matrix.sh`, `scripts/diagnose_e1_v2_centroid.py`.
- **Archivi metriche:** `results/validation/e1_uniform_v2/` e `results/test/e1_uniform_v2/`; ogni directory contiene `metrics_per_run.csv`, `summary.csv`, `run_config.json`.
- **Payload:** file binari temporanei con byte sintetici uniformi e inerti, **distinti per checkpoint**, generati determinicamente usando SHA-256 + NumPy PCG64 a partire da seed, replica, X e riga sorgente; 16.384 byte per payload. I file temporanei vengono rimossi dopo l'embedding e resta il manifest locale con gli hash.

## 6. Collaborazione e tracciabilità

Il lavoro è un **progetto universitario condiviso con Fabrizio**. La roadmap proponeva inizialmente: Riccardo — provenance, dataset, payload e pipeline; Fabrizio — replica upstream, baseline, metriche e grafici; entrambi — threat model, revisioni incrociate, split, relazione e discussione orale. Questa è una **proposta di ripartizione**, non una certificazione dei contributi finali: per il resoconto conclusivo bisognerà consultare issue, PR e commit di ciascun partecipante. Non attribuire a uno dei due attività non documentate.

## 7. Confini rispetto a tesi e paper

La fase ottobre–dicembre 2026 mira al **progetto d'esame**: replica, esperimenti E1–E3 sostenibili e report indicativamente di 10–15 pagine, subordinati alle indicazioni del docente. La possibile **tesi magistrale individuale** e una eventuale pubblicazione scientifica sono fasi successive, non risultati già raggiunti e non un requisito per concludere E1. Prima di rivendicare novità o contributi pubblicabili occorre confrontarsi con la letteratura e con il relatore.

## 8. Navigazione

- [Relazione tecnica dettagliata E1](../exam/E1_REPORT.md)
- [Guida di riproducibilità e audit E1](E1_REPRODUCIBILITY.md)
- [Risultati validation](../results/validation/e1_uniform_v2/summary.csv)
- [Risultati test](../results/test/e1_uniform_v2/summary.csv)
- [Grafici E1 e cartella Excel](../results/figures/e1/E1_grafici.xlsx)
- Fonte di pianificazione: `Roadmap_Progetto_Tesi_Paper_IEEE_con_Letture(7).docx` (documento fornito al gruppo; non necessariamente da aggiungere al repository).
