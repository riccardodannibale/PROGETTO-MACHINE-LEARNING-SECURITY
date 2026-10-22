# E2 — Protocollo per approvazione congiunta (G4)

**Stato: FROZEN PER VALIDATION E2 — 22 ottobre 2026.** Autorizzata esclusivamente la campagna ufficiale di dieci fit di validation X-LSB. **TEST ID/OOD NON AUTORIZZATO**: richiede audit 10/10 e nuovo atto congiunto. Il precedente singolo fit di validation era una diagnostica, non un risultato ufficiale.
**Data:** 22 ottobre 2026. **Ambito:** progetto d'esame condiviso Riccardo/Fabrizio; base per futura tesi.
**Riferimento evidenze:** `docs/E2_G3_UTILITY_RESULTS.md`, audit E2 G1/G2 su TRAIN, E1 completato.

## 1. Research question e minaccia

Quanto generalizza un detector Siamese Model X-Ray **addestrato e calibrato solo su X-LSB** quando i checkpoint sorgente sono modificati da un embedding *a codici ortogonali di spreading* mai presentato al detector durante training/calibrazione?

- Nuovo metodo: `e2-keyed-orthogonal-spread-v0-educational`, **ispirato ai principi** dello spread-spectrum nella letteratura MaleficNet, **non** l'implementazione originale di MaleficNet (nessun ECC/LDPC, fine-tuning, dataset CIFAR10 o malware reale).
- Payload X-LSB: byte sintetici deterministici già utilizzati in E1; OOD: messaggi sintetici inerti **B=16 bit** per checkpoint/fit.
- Decoder spread: richiede chiave, repeat, identificativo checkpoint; **non** richiede pesi benigni originali.
- Lo shift testato è la **famiglia di modifica dei pesi**, non uno shift di architettura, provenance, checkpoint source o preprocessing.

## 2. Versioni e integrità bloccate

| Elemento | Identificativo |
|---|---|
| Dataset GHRP/STL10 `weights.npy` | SHA-256 `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad` |
| Manifest degli split `splits.csv` | SHA-256 `3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f` |
| Upstream Model X-Ray | commit `a880e332f556fc71faf8d3753931005d5d019339` |
| Runner baseline E1 `run_e1_final_v2.py` | SHA-256 `a75aa3d844bb695a6d6155fe808394025b04c480d74d1e1b856eec5ca6f9c037` |
| Prototype OOD `e2_synthetic_spread.py` | SHA-256 `70d9e0c02fd26dffc7d69f3fbbdb70cd3219844200c625891797eb13ee544edd` |
| Upstream-hook audit `e2_intensity_train_audit.py` | SHA-256 `e3bb2fb669ff3aae36f2a3412fae5e9e3a8d69f4217f9833ec37735c0500e51b` |
| GHRP `dataset.pt` (solo studio utility) | SHA-256 `7afdccfe4d5418d3645e1a42f149c377cdc9088a9283cfd8288924c3a2e0b434` |

Il **nuovo runner E2** deve registrare il proprio SHA-256 ed essere versionato *prima* di aprire la fase test; codice e configurazioni non si cambiano dopo la decisione test.

## 3. Risultati dei gate pre-test (NON risultati del detector E2)

- **G1:** spread v0, 20 checkpoint TRAIN, B=16; α=0,16 BER=0,003125, recupero esatto 19/20; α=0,24 BER=0, recupero esatto 20/20. Audit individuale Ubuntu/Mac passato; self-test e hash invariati.
- **G2:** 20 checkpoint TRAIN, X-LSB X=23 `rel_L2` medio 0,312615; spread α=.16/.24 rispettivamente 0,16 e 0,24; `changed_fraction` circa 1 in tutte le condizioni. Audit **60 righe appaiate** Ubuntu/Mac passato.
- **G3:** 3 checkpoint TRAIN, ricostruzione originale e forward pass validi; dataset STL10 preprocessato trovato e letto con `torch.load(weights_only=True)`; pilot 256 immagini del `valset` originale. Delta accuracy medio vs benign: X-LSB −11,1979 pp; spread .16 −1,5625 pp; spread .24 −5,8594 pp. **Pilot esplorativo su 3 soli modelli**.
- Fabrizio ha confermato gli audit cross-platform e revisionato l'architettura. Ha inoltre approvato esplicitamente senza modifiche il protocollo G4 e i capisaldi E2 (messaggio riportato da Riccardo il 22 ottobre 2026). La revisione separata del codice G3-C non è documentata da quel messaggio: il pilot utility resta esplorativo e non viene trattato come risultato principale E2.

## 4. Disegno sperimentale E2 da congelare

- **Dataset**: gli stessi 1000 checkpoint `float32 (2864,)` di E1, split *per identità di checkpoint sorgente* `600 train / 200 val / 200 test`. Nessuna copia stego della stessa origine fra split.
- **Train**: per ogni fit scegliere **3 identità** solo nel TRAIN pool, come E1 (`np.random.default_rng(42 + repeat).choice(..., 3, replace=False)`), 3 benign + 3 LSB X=23; 10 ripetizioni `repeat=0..9`. `fit_seed = 42 + repeat * 1000 + 23`. Nessun OOD presentato al detector in train.
- **Detector**: Siamese Model X-Ray originale `osl_siamese_cnn`, `imsize=100`, modalità `ub` e identici iperparametri E1.
- **Validation per fit**: su 200 benign e 200 X-LSB X=23, **solo**. Calibrare soglia Youden dai margini centroid validation, con decisione `score>threshold`. Congelare e registrare; nessuna selezione soglia OOD.
- **Test ID e OOD appaiati nello STESSO fit**: usare gli stessi 200 checkpoint test benign e le varianti 200 LSB X=23, 200 spread α=.24 **primario**, 200 spread α=.16 **secondario**. `B=16`, seed spread `42`, `repeat` uguale al fit, `row_index` originale. **Non riaddestrare** tra ID e OOD.
- **Rappresentazione**: per benign e spread, stesso percorso upstream rappresentazione non attaccata `img_pp_xlsb_attack(..., x=0)` sui rispettivi vettori; per LSB, attacco upstream originale con payload E1 e medesima rappresentazione. Tutte le condizioni devono produrre shape/ordine/normalizzazione compatibili; eseguire controlli fail-closed.
- **Test E1 già consultato**: il set di 200 checkpoint riutilizzato non è un *nuovo* holdout blind incontaminato. Dichiarare nella relazione; per la futura tesi/paper prevedere nuovo dataset e holdout indipendente.

### Metrica primaria e secondarie

**Primaria:** `ΔAUROC_centroid = AUROC_centroid(OOD α=.24) - AUROC_centroid(ID X=23)` usando il medesimo fit e le stesse 200 identità di origine. Riportare entrambi gli AUROC assoluti, la differenza per repeat e la distribuzione sui 10 fit.

**Secondarie preregistrate:** AUROC α=.16, AUPRC (prevalenza 50% per confronto), `accuracy`, `FPR`, `F1` sotto soglia `val_youden` del *medesimo fit*, regola originale `score>0`, e 1-NN secondario. Salvataggio score **per checkpoint e condizione**. Bootstrap/IC, se riportati, raggruppati per checkpoint origine e attenti alla riutilizzazione delle identità across repeat; non interpretare 10×200 osservazioni come 2.000 checkpoint indipendenti.

### Audit per esempio e per fit

- Identità/row_index, modello sorgente, hash checkpoint, split, seed/repeat, family, α/X, payload hash, bit errors/BER/exact recovery (per spread), norma perturbazione, max_abs_delta, numero pesi modificati, shape, all-finite.
- Punteggi centroid e 1-NN, etichette, predizioni, soglia val per fit, confusion matrices e metriche aggregate con mean/SD.
- Hash/versioni del runner, protocollo, pesi, split, submodule, ambiente, hardware, start/end e elapsed fit.
- Idempotenza fail-closed: output immutabili, stop su cartella parziale, confronto check di completezza; nessun rerun selettivo per migliorare il risultato.

## 5. Confondenti/limiti da riportare esplicitamente

1. LSB X=23 modifica fino a 23×2864 = **65.872 posizioni di bit** (NON 65.872 bit indipendenti recuperabili garantiti); OOD porta **16 bit** sintetici: capacità diversa.
2. Norme relative diverse (media su 20 TRAIN X-LSB 31,26% vs spread .24 24%); non attribuire ogni delta di AUROC alla sola famiglia in modo causale; il risultato è un confronto con **fattori di aggressività non perfettamente controllati**.
3. Pilot utility sulle sole tre CNN: valori non sufficienti a sostenere *utility preservata in generale* né *stealth*. X-LSB altera significativamente l'accuracy nel pilot.
4. Decoder spread possiede chiave e identificativo del checkpoint; non possiede benign. Non sostenere recupero senza metadati e senza chiave.
5. La storia di sviluppo E1 ha già consultato il medesimo zoo/test; il risultato E2 sarà un confronto interno, non validazione esterna indipendente.
6. E3 dovrà includere perturbazioni benign non-stego matched per intensità e controlli sui metadati per distinguere rilevazione steganografia vs generiche alterazioni numeriche.

## 6. Ordine esecutivo e stop rule

1. Revisione congiunta Riccardo/Fabrizio del protocollo e codice G3-C; archiviare CSV originali G1/G2/G3 + report QA.
2. Implementazione runner E2 **nuovo**, basato sul runner E1 v2, con stadi `validation` e `test`, **test inizialmente chiuso**; test unitari/smoke su train+validation senza checkpoint TEST.
3. Congelare codice E2 runner, configurazione e il presente testo: copiare come `docs/E2_PROTOCOL_FROZEN.md`, annotare commit e SHA-256, ricevere approvazione esplicita di entrambi, push Git.
4. Eseguire 10 fit `validation` (solo LSB), controllare scoring e soglie; NON usare risultati OOD per scegliere alpha, fit o soglie.
5. Soltanto dopo preflight e approvazione aprire lo stadio `test` per 10 nuovi fit `training LSB → calibration LSB → test ID e OOD nello stesso fit`; non ripetere selettivamente esecuzioni riuscite.
6. Aggregare per fit, audit delle previsioni per checkpoint, plot e report; etichettare come `internal E2 attack-family shift` e non come MaleficNet vero.

**STOP** se hash inattesi, leakage di identità, variazione di protocollo non approvata, mismatch dei punteggi del Siamese, payload OOD in train/validation, unblind prematuro del test o cartelle parziali. Le modifiche dopo il freeze richiedono un protocol amendment datato.

## 7. Freeze, approvazioni e ambito

- [x] **Riccardo:** approvazione esplicita del presente freeze **solo validation**, data 2026-10-22, confermata digitando `APPROVO` nel comando di congelamento.
- [x] **Fabrizio:** approvazione integrale, senza modifiche, di `docs/E2_PROTOCOL_FINAL_REVIEW.md` e di tutti i capisaldi E2, comunicata a Riccardo il 22 ottobre 2026 (fonte: messaggio condiviso da Riccardo; non una firma digitale).
- [x] **Runner G5:** SHA-256 `4719e6d947c5c5f7acba09f464ec0d2e5abf5182c642af8a063789ca217849ac`; sintassi e preflight superati su Ubuntu, test unitario e revisione su Mac; un fit diagnostico di validation Ubuntu superato con QA.
- [x] **Documento sorgente G4:** SHA-256 `c822e5a27146b6fc00a568e0b094a777227b542aaf24b6dda3cd4733a7cb4b05`.
- [ ] **Autorizzazione al TEST:** NON concessa. Sarà oggetto di una revisione distinta dopo 10/10 fit e audit. Nessun file `approved_for_e2_test` deve essere creato ora.

Il **commit del freeze** sarà identificato dal log Git dopo il commit, per evitare un riferimento circolare al commit che contiene questo stesso documento. **Non modificare il presente file per registrare il suo commit**: conservarne invece l'hash e il commit in un registro separato.

### Vincolo di immutabilità

Seed, attacchi, alpha, metrica primaria, sorgenti, split, runner e condizioni di test sono fissati. Qualsiasi correzione dopo il freeze richiede un *amendment* esplicito e documentato, prima di aprire il test.
