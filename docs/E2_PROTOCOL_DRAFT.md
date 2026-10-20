# E2 — Bozza di protocollo condiviso (NON congelato)

**Stato:** pianificazione; nessun nuovo training autorizzato da questo documento. **Prerequisito:** revisione Riccardo + Fabrizio del protocollo e del costo computazionale.

## Domanda

*Un detector Model X-Ray addestrato a distinguere checkpoint LSB può rilevare su identità test le modifiche prodotte da una famiglia di embedding diversa e mai vista in training/validation?*

## Disegno desiderato (attack-family shift, un fattore alla volta)

1. Conservare zoo GHRP/STL10, split originari 600/200/200, pesi (1000,2864), stessi ID sorgente benigni, seed, rappresentazione, Siamese e definizione di score.
2. Formare training **esclusivamente con LSB**, calibration/validation **esclusivamente su LSB**; scegliere la soglia Youden su validation LSB, una volta per fit.
3. Utilizzare **lo stesso modello addestrato** per due valutazioni abbinate sul test: LSB in-distribution (controllo contemporaneo) e nuovo embedding OOD; non riaddestrare due detector differenti per il confronto. Il vecchio E1 funge da benchmark storico, non necessariamente da controllo paired dello stesso nuovo fit.
4. Predefinire metrica primaria **AUROC centroid**, analisi secondaria AUPRC, accuracy, FPR, 1-NN; reportare 10 fit × intensità, se la fattibilità lo consente.
5. Per ogni checkpoint originale costruire benign, ID-LSB e OOD con elaborazioni equivalenti, evitando confondenti di serializzazione/provenance. Registrare rate e **norme delle perturbazioni**; confrontare livelli di aggressività plausibilmente analoghi, non assumere che un parametro X dell'altra tecnica equivalga automaticamente a X-LSB.
6. Mantenere payload **sintetici e inerti**. Non eseguire o distribuire codice malevolo o payload eseguibili.
7. **Nessun tuning sul test OOD.** Qualunque parametro della nuova trasformazione deve essere congelato tramite proprietà dell'algoritmo o prove tecniche su unità non riservate. Il test E1 è già stato consultato: un riuso degli stessi ID in E2 non è un nuovo holdout incontaminato e va dichiarato chiaramente; per una valutazione strettamente blind sarebbe necessario riservare ID nuovi prima di E2.

## Scelta della seconda famiglia: gate di fattibilità

Valutare il percorso MaleficNet esistente nell'upstream **solo come candidato**, dopo ispezione del codice e verifica compatibilità con vettori float32 da 2.864 pesi, ambiente CPU, riproducibilità e costi. Se non implementabile senza cambiare simultaneamente architettura/checkpoint, scegliere una seconda tecnica di embedding chiaramente distinta, documentando threat model e implementazione. Non usare soltanto payload casuali differenti nella stessa procedura LSB: non sarebbe uno shift di famiglia.

## Gate E2-0 (da superare prima di qualsiasi training)

- Revisione del codice di embedding candidato e sua determinazione matematica, più corrispondente schema riproducibile.
- Smoke su pochi checkpoint del pool train: integrità output, dimensione, rate, perturbazione, assenza di NaN/Inf; no esecuzione malware.
- Documento `docs/E2_PROTOCOL_FROZEN.md` con codici/hash/seed, budget e protocollo di threshold; review con Fabrizio.
- Decisione esplicita su riuso del test E1 vs nuovo holdout, con claim coerenti.
- Solo dopo: validation/controlli, quindi test secondo preflight analogo a E1.

**Le conclusioni OOD e gli eventuali risultati E2 saranno redatti esclusivamente dopo i dati.**
