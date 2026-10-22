# E3 — Sezione da completare nel report d'esame dopo l'esecuzione

> **Non includere come risultati completati:** questo file è un modello di scrittura, non contiene numeri E3 osservati.

## Obiettivo
Verificare retrospettivamente, sugli score già prodotti e auditati in E2, l'appaiamento benigno/modificato, la neutralità dei metadati di checkpoint e la stabilità del tasso di falsi positivi (FPR) al cambio di famiglia di embedding.

## Metodo
- Split checkpoint disgiunti 600/200/200 e 10 fit E2 congelati per Ubuntu e Mac M4.
- Un benigno e un modificato per ogni checkpoint nelle tre condizioni ID/OOD, due metodi di scoring.
- Chiave di appaiamento: `repeat`, `method`, `condition`, `row_index`.
- Soglia Youden sempre da LSB validation; nessun nuovo fit né tuning post-test.
- Misure: completezza coppie, uguaglianza `model_id` e checksum, score benigni ID/OOD, FPR/TPR/FNR, concordanza degli score a coppie.

## Risultati — DA INSERIRE dai CSV reali
- Ubuntu: [NON ANCORA ESEGUITO]
- Mac M4: [NON ANCORA ESEGUITO]
- Replicazione hardware: [NON ANCORA ESEGUITA]

## Interpretazione
Se FPR e score benigni sono invariati, un calo nelle prestazioni OOD a soglia fissata è compatibile con una perdita di riconoscimento dei modificati; non con un diverso trattamento dei benigni. Gli identificativi matched non possono separare etichette dato il bilanciamento 1:1. I risultati non dimostrano che l'intera perdita sia dovuta alla famiglia di attacco, perché intensità e payload non sono matched, e non costituiscono un nuovo test blind esterno.

## Materiali da citare
`docs/E3_PROTOCOL_CONTROLS.md`, `results/e2_final/`, `e3_controls_per_fit.csv`, `e3_controls_summary.csv`, confronto Ubuntu/Mac, manifest degli hash.
