# E2 G6 — Amendment QA 01: ricostruzione float64 da CSV

Data: 22 ottobre 2026
Classificazione: **correzione del controllo di integrità dei risultati** dopo il freeze; il modello, training, seed, split, soglie e metriche preregistrate rimangono immutati.

## Incidente

Ubuntu: dieci validation e QA originali superati. Mac M4: dieci validation completate ma QA originale fallisce al controllo `bad threshold application 1/nn`. La discrepanza potrebbe derivare dal parser float64 predefinito di pandas applicato a margini e soglie che differiscono di un solo ULP.

## Modifica verificabile

In `scripts/e2_g6_audit_validation_v2.py`, rispetto al controllo QA originario, la lettura di `predictions_validation.csv` utilizza `pd.read_csv(..., float_precision='round_trip')`. Tutte le altre invarianti e i confronti stretti `score_margin > threshold` sono invariati. Viene conservato anche il controllo originale. Il diagnostico confronta i due parser su ogni repeat e metodo.

Non usare tolleranze che modificano la classificazione e non rigenerare i training. Il test non va aperto finché l'audit Mac v2 non passa senza mismatch a precisione piena e i risultati non sono esaminati.

## Validazione richiesta

- Test unitario con soglia a distanza di un ULP.
- Diagnostica su ciascuna piattaforma: zero mismatch con lettura round-trip.
- Audit G6 v2 completo 10/10 su Ubuntu e Mac M4.
- Registrazione hash del nuovo audit e del diagnostico in commit separato; runner originale intoccato.

**Questo documento non contiene né concede autorizzazione di apertura del test.**
