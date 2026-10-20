# Handoff Completato: Replica Esperimento E1 su Mac M4

Ciao Riccardo,
ti confermo di aver completato con successo l'intera replica dell'esperimento E1 sulla mia macchina (Mac Apple Silicon M4), eseguendo il protocollo v2 in maniera isolata come descritto nel report di allineamento.

Di seguito il resoconto completo con i dettagli dell'ambiente, le verifiche di integrità e il confronto quantitativo.

## 1. Informazioni sull'Ambiente
La pipeline è stata eseguita interamente su macOS con architettura ARM (M4). TensorFlow ha girato su CPU (Metal non attivato per questo specifico run), sollevando i warning standard riguardo all'ottimizzatore Adam legacy, ma senza impattare la stabilità.

* **Piattaforma:** Mac Apple Silicon M4
* **Python:** 3.11.17
* **NumPy:** 1.26.4
* **TensorFlow:** 2.15.1
* **PyTorch:** 2.4.0
* **TF GPU visibili:** `[]` (Esecuzione su CPU)

## 2. Conferma dell'Origine (Dati e Versioning)
Ho verificato di utilizzare il dataset reale (non immagini) e che i protocolli di split siano identici a quelli usati su Ubuntu. Gli hash coincidono perfettamente.

**Integrità Dati:**
* `weights.npy` SHA-256: `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad` (OK)
* `splits.csv` SHA-256: `3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f` (OK)

**Versioning GitHub:**
* Esecuzione locale (Branch `ricky`): HEAD `59f556c`
* Submodule Upstream (`external/ModelXRay`): HEAD `a880e332f556fc71faf8d3753931005d5d019339` (OK)

## 3. Stato dell'Esecuzione e QA
* **Smoke test pre-validation:** Eseguito (203 payload verificati, determinismo confermato).
* **Validation v2:** 40/40 fit completati con script a matrice.
* **Test E1 (reserved):** 40/40 fit completati.
* **QA CSV Test:** Lo script di check ha confermato `validation 40/40` e `test 40/40`.

## 4. Confronto Quantitativo (Test - Metodo Centroid)
I risultati mostrano un allineamento eccellente tra il run su Ubuntu e la replica su Mac M4 CPU. Le metriche non sono bitwise-identical (come ci aspettavamo, a causa delle differenze tra backend TF/hardware), ma il comportamento del detector è invariato: non discrimina a X ≤ 16 e rileva accuratamente a X=23. 

| X-LSB | AUROC Riccardo (Ubuntu) | AUROC Fabrizio (Mac M4) | Accuracy (val_youden) Riccardo | Accuracy (val_youden) Fabrizio |
|-------|-------------------------|-------------------------|--------------------------------|--------------------------------|
| **1** | 0.500150                | 0.500209                | 0.50025                        | 0.50075                        |
| **8** | 0.508232                | 0.509388                | 0.50375                        | 0.50350                        |
| **16**| 0.501293                | 0.501425                | 0.49850                        | 0.50125                        |
| **23**| 0.901863                | 0.904378                | 0.82125                        | 0.82300                        |

*Nota: l'FPR su X=23 calcolato sui miei log è intorno allo 0.1605 rispetto al tuo 0.1550.*

## 5. Note Operative su Mac M4
* **Tempi:** Circa 100-110 secondi mediamente per ogni singolo `repeat/X` per lo stage test.
* **Memoria:** L'uso dello script bash a matrice `run_e1_v2_matrix.sh` ha funzionato perfettamente. Non c'è stato alcun errore "Out Of Memory" (OOM) o crash del kernel.
* **Gestione Standby:** Il tool `caffeinate` ha impedito lo sleep di macOS, permettendo al job notturno di concludersi autonomamente.

## 6. Allegati in Consegna
Come richiesto, provvedo a girarti (o a caricare nel repo) i seguenti materiali:
1. `summary.csv` e `metrics_per_run.csv` estratti da `~/mlsec-local/runs/e1_v2_test/`
2. I log completi testuali generati dal run (`e1_v2_test.log`, `e1_v2_validation.log`, smoke).

Adesso che abbiamo verificato la riproducibilità su entrambe le piattaforme, sono pronto a iniziare a ragionare con te sul protocollo per E2/E3.

A presto,
Fabrizio