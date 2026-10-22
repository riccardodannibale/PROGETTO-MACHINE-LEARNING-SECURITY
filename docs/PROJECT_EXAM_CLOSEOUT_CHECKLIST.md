# Beyond the X-Ray — Checklist per chiudere il progetto d'esame (A0–A6)

> La roadmap dell'utente del 15 ottobre 2026 separa progetto condiviso **ottobre–dicembre 2026**, futura tesi individuale **2027**, e un eventuale paper successivo. Questa checklist è per il **solo progetto d'esame**.

## E1 ed E2: evidenze disponibili

- E1: dataset GHRP/STL10 da 1.000 checkpoint, split disgiunti 600/200/200, codice e risultati E1 archiviati in repo.
- E2: spread sintetico a 16 bit ispirato ai principi MaleficNet ma non replica dell'attacco originale; confronto LSB ID vs spread OOD su 10 fit per piattaforma, audit e risultati in `results/e2_final/`.
- Report unificato `exam/PROJECT_REPORT.md` e `.docx` preparato sulla copia E1+E2. **Verificare che sia effettivamente aggiunto e versionato in `ricky`** prima di integrarlo con E3; non presumere che un file generato in chat sia già su GitHub.

## E3 e chiusura sperimentale

- [ ] Test script E3 superati su Ubuntu e Mac, stesso SHA E3.
- [ ] Audit sui CSV di predizioni grezze E2 Ubuntu PASS (no training).
- [ ] Audit sui CSV grezzi Mac PASS (no training).
- [ ] Confronto 60 righe appaiate per piattaforma, statistiche e grafico generati; revisione incrociata Fabrizio.
- [ ] Report E3 dichiara analisi **retrospettiva** e i limiti (non intensity-matched, non nuovo blind test, stessi checkpoint nel 10 fit).
- [ ] In `results/e3_final/` solo aggregate, manifest SHA, plot e report verificati. Raw score per-checkpoint non richiesti in repository pubblica; custodire localmente le cartelle E2.

## Consegna secondo la roadmap

- [ ] **A0** Riscontro dei docenti sullo scope del progetto e criteri di valutazione: non risultano qui prove di un'approvazione formale.
- [ ] **A1** Literature matrix/gap audit: verificare presenza in repository e controllare claim di originalità (Model X-Ray include già scenari OOD; non definire automaticamente E2 "novità").
- [ ] **A2/A3** Provenienza, submodule SHA, licenze, environment, dati/seed/manifest e split checkpoint-disjoint verificabili da terzi.
- [ ] **A4/A5** E1–E3: CSV, grafici derivati, audit, FPR, AUPRC con prevalenza 50%, incertezza e confondenti espliciti.
- [ ] **A6** `exam/PROJECT_REPORT.md` e `.docx` integrati con i numeri **E3 reali**, revisione collaborativa, indice, tabelle e immagini, riferimenti alle evidenze; produrre eventualmente **versione sintetica 10–15 pagine** perché l'attuale Word E1+E2 è ~29 pp (scope docente da verificare).
- [ ] **A6** Slide e simulazione orale per entrambi; potete spiegare modello Siamese, split, threat model, spread sintetico, metriche e limiti.
- [ ] **A6** Preparare export PDF del report e delle slide per la consegna, se richiesto. Controllare licenze Model X-Ray e dataset prima di redistribuire derivati e pesi.
- [ ] Tag Git (ad es. `exam-v1`) **solo quando la consegna è revisionata e approvata**, non oggi in anticipo.

## Non fanno parte della consegna di dicembre

Nuovo architecture shift, lifecycle shift, studio fattoriale completo, difesa nuova e paper IEEE; sono possibili sviluppi **di tesi 2027**, da approvare con relatore. Il paper non è un output obbligatorio dell'esame.
