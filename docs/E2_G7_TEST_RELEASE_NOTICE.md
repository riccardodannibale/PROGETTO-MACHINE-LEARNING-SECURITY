# E2 — G7 autorizzazione documentata del test ID/OOD

**APPROVAL: E2 TEST AUTHORIZED — 22 ottobre 2026.**

Questa autorizzazione costituisce un **atto separato** dal protocollo `docs/E2_PROTOCOL_FROZEN.md` per la sola validation. Non modifica il documento congelato, il suo hash o il runner `scripts/run_e2_paired_v0.py` (SHA-256 `4719e6d947c5c5f7acba09f464ec0d2e5abf5182c642af8a063789ca217849ac`).

## Evidenza della decisione

- **Ubuntu, Riccardo**: i 10 fit ufficiali LSB validation sono terminati. Audit v2 superato: 10 fit, 40 metriche, 8.000 predizioni e 2.030 payload manifest; nessuno score test esaminato. AUROC centroid media 0,88170875, SD 0,08349493.
- **Mac M4, Fabrizio**: dopo il controllo del parser CSV round-trip, diagnostica riferita con tre mismatch del parser standard e zero mismatch del parser round-trip; audit v2 comunicato come superato: 10 fit, 40 metriche, 8.000 predizioni e 2.030 manifest. AUROC centroid riferita ~0,88183.
- **Approvazioni**: Riccardo ha autorizzato esplicitamente il proseguimento delle attività senza richieste ripetute; Fabrizio ha espresso approvazione integrale del protocollo e, dopo l'audit Mac, ha chiesto espressamente di procedere allo sblocco ID/OOD. L'evidenza è costituita da messaggi trasmessi da Riccardo in data 22 ottobre 2026: **non è una firma digitale** e i dati Mac sono riferiti, non letti direttamente dall'autore di questo registro.

## Scope irrevocabile del test

1. **10 nuovi fit per piattaforma**, ciascuno su 3 checkpoint TRAIN benign + X-LSB X=23, calibrato esclusivamente sui 200 checkpoint VALIDATION in versione benign/LSB.
2. **Per ciascun fit, lo stesso modello** valuta i 200 checkpoint TEST benign/LSB-ID e benign/spread OOD α=0,24 (primario) e α=0,16 (secondario).
3. La **metrica primaria** è `AUROC_centroid(SPREAD_0.24) - AUROC_centroid(LSB_ID)`, calcolata appaiando per repeat le medesime 200 identità di origine.
4. Conservare predizioni e soglie per checkpoint, registro payload, manifest, log e test di integrità. Nessun tuning dei parametri o selezione delle ripetizioni in base agli score test.
5. **Non ripetere selettivamente** i fit completati; in caso di errore sospendere, conservare log e applicare un emendamento tracciato se indispensabile.
6. Un test interno al medesimo zoo GHRP/STL10 già impiegato in E1: **non un holdout esterno blind** e **non MaleficNet originale**. Capacità e intensità delle due famiglie non sono matched.

L'autorizzazione **non** pre-approva ulteriori ottimizzazioni su test, cambi di algoritmo o altri esperimenti. Ogni piattaforma produce un proprio JSON locale di abilitazione **solo dopo un nuovo audit dei dieci fit validation locali**. Il file JSON è un record machine-readable, non una firma crittografica.
