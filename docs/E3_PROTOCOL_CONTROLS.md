# E3 — Benign matched, metadata e negative controls (progetto d'esame)

**Stato: protocollo di diagnostica E3 — nessun risultato E3 ancora misurato.** 22 ottobre 2026.  
**Fonte di scope:** roadmap 15 ottobre 2026, work package A4: "E3: controllo con benigni matched e controlli sui metadati". A5: metriche/QA, A6: relazione.  
**Tipo di studio:** analisi **retrospettiva** dei risultati del test E2 già aperti su GHRP/STL10. Non è un nuovo blind holdout; non vi è tuning, training o cambio di soglia/attacco.

## Quesiti E3

1. **E3-C1 — benigni veramente appaiati?** Per ogni checkpoint, replicate, metodo e famiglia (`LSB_ID`, `SPREAD_0.24`, `SPREAD_0.16`), esiste un benigno e un modificato tracciabili allo **stesso checkpoint sorgente**? Il benigno ha lo stesso score sui tre rami valutati con **lo stesso fit Siamese**?
2. **E3-C2 — scorciatoie da metadati osservati?** `row_index`, `model_id`, `checkpoint_sha256`, `repeat`, `fit_seed`, `X`, `stage` sono uguali per benigni e modificati entro coppia? Resta quindi esattamente 50/50 la distribuzione delle etichette per ogni identità? Questo controllo matematico **non addestra un classificatore di metadata**: l'accuratezza majority-only teorica è 0,5 con un esempio per classe a parità di identità.
3. **E3-C3 — il calo OOD è imputabile a un cambio di FPR o ai positivi?** Poiché le immagini e gli score dei benigni sono identici fra rami, con la stessa soglia Youden da validation LSB deve coincidere l'**FPR**, mentre si misura la differenza in TPR/FNR e la concordanza *entro coppia* (score modificato > score benigno).
4. **E3-C4 — riproducibilità hardware:** ricostruire questi controlli dai **CSV grezzi locali** di ogni piattaforma, confrontando fit appaiati 0–9.

## Dati e design

- Sorgente: `~/mlsec-local/runs/e2_test_official_ubuntu_v1` e `~/mlsec-local/runs/e2_test_official_mac_m4_v1` (nomi standard; percorso Mac da verificare). I CSV in `results/e2_final/` **non** includono le predizioni per checkpoint sufficienti per E3.
- Frozen weights digest `5a03ff...60ad`, split digest `3f4236...6e4b93a6f` (SHA integrali verificati via script), detector digest `4719e6...849ac`.
- 10 repeat × 200 identità checkpoint test × 3 condizioni × 2 metodi = **12.000 coppie benigno/modificato** come unità di confronto all'interno dei fit, non 12.000 checkpoint indipendenti.
- Soglia Youden **solo** dalla validation LSB di ogni fit: nessuna ri-calibrazione OOD, nessuna scelta α post-test.
- Audit fail-closed sullo schema dati, coppie, sha dei checkpoint, score, soglie, AUROC registrata, FPR e recupero di payload/alpha; lettura CSV con `float_precision='round_trip'`.
- Risultati E3: `e3_controls_per_fit.csv`, `e3_controls_summary.csv`, `e3_source_manifest.json`, `E3_CONTROLS_REPORT.md`; stesso schema per Ubuntu e Mac; aggregazione incrociata soltanto dopo entrambi gli audit.

## Limiti e confondenti

- X-LSB X=23 e il nostro spread sintetico 16-bit hanno **capacitá, distribuzioni e intensità relative di perturbazione diverse**. E2/G2 ha misurato ~0,313 rel-L2 per X-LSB e 0,16/0,24 per i due spread sul campione TRAIN: non sono attacchi intensity-matched. Non inferiamo un effetto causale isolato della famiglia di embedding.
- Il campo `X=23` viene ereditato da `prediction_rows` di E1 anche per i record spread: è **metadata del protocollo/runner**, non prova che X-LSB sia stato applicato agli esempi OOD. La vera famiglia è `condition`, corroborata dal codice `test_evaluation` e dal `payload_manifest`.
- Il test E2 è già stato esaminato. E3 non può essere descritto come verifica blind indipendente, e non si devono sviluppare nuove scelte sperimentali sugli score OOD già visti.
- Appaiamento degli identificativi non esclude tutte le scorciatoie da rappresentazione (pixel/normalizzazione/serializzazione). I punteggi benigni identici escludono una differenza **sul ramo benigno** generata dall'algoritmo di embedding, ma non spiegano ogni segnale nei modificati.
- I fit sono correlati perché valutano sempre gli stessi 200 checkpoint test; si riportano medie/SD su repeat a titolo descrittivo, senza considerare i 2.000 conteggi per condizione come indipendenti.

## Gate e criteri di chiusura

- G3-1: script e self-test superati su Ubuntu e Mac; runner E2 SHA invariato.
- G3-2: audit Ubuntu `E3 MATCHED/METADATA CONTROLS QA OK`, risultati locale **read-only**.
- G3-3: audit Mac con stesso script e fonti raw, risultati locale **read-only**.
- G3-4: confronto 60 righe per fit/metodo/condizione, evidenze in `results/e3_final/` **solo dopo i due audit**; aggiornare `exam/PROJECT_REPORT.md` e `.docx` con risultati reali e limiti; rigenerare grafici a partire dai CSV.
- G3-5: check struttura report contro roadmap A0–A6, revisione Fabrizio, presentazione, licenze e versione di consegna. Il suggerimento di 10–15 pagine della roadmap può richiedere una **versione sintetica** del report (la bozza E1+E2 attuale è più lunga).

**STOP per test incompleto o sorgenti discordanti:** non cancellare output E2 originali, non alterare CSV/labels/thresholds per fare passare QA, non ripetere training selettivamente.
