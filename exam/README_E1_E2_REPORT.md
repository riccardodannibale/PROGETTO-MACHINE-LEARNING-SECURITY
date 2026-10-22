# Relazione d'esame integrata — E1 + E2

**Documento principale aggiornato:** `exam/PROJECT_REPORT.md` oppure `exam/PROJECT_REPORT.docx`.

È una nuova relazione **continua** dalla baseline E1 già esistente nel repository fino a tutto E2, con 23 sezioni principali/sottosezioni, figure incorporate, bibliografia e limiti metodologici. Il report originale E1 resta conservato **senza sovrascrittura** come `exam/E1_REPORT.md` e `exam/E1_REPORT.docx`.

## Istruzioni Ubuntu (Riccardo)

Dalla radice del repository:

```bash
cd ~/PROGETTO-MACHINE-LEARNING-SECURITY
unzip -n ~/Scaricati/EXAM_REPORT_E1_E2_COMPLETO.zip -d .
ls -lh exam/PROJECT_REPORT.md exam/PROJECT_REPORT.docx
```

**Prima del commit**, aprire `exam/PROJECT_REPORT.md` per rivedere l'introduzione e confrontare, se necessario, la Parte I con la **versione effettiva** di `exam/E1_REPORT.md` già presente su `ricky`. La versione E1 sorgente della relazione integrata è una copia completa locale con audit Ubuntu/Mac disponibile durante la redazione; la versione remota corrente non era direttamente consultabile. Non cancellare il report E1 originale.

Per archiviare soltanto i nuovi file:

```bash
git add -- exam/PROJECT_REPORT.md exam/PROJECT_REPORT.docx exam/README_E1_E2_REPORT.md
git diff --cached --check
git diff --cached --stat
git commit -m "docs(exam): integrate E1 and full E2 experimental report"
git push origin ricky
```

Se `git diff --cached --check` segnala *trailing whitespace* Markdown sulle righe di metadati, sono spazi di line break Markdown; correggere solo se lo si desidera, **senza modificare dati dei CSV**. Se Git o la revisione mostrano differenze rilevanti fra la Parte I e l'originale su `ricky`, **non pubblicare finché non le abbiamo verificate**.

## Per Fabrizio

Dopo il push, può revisionare il Markdown con:

```bash
cd ~/PROGETTO-MACHINE-LEARNING-SECURITY
git fetch origin ricky
git show origin/ricky:exam/PROJECT_REPORT.md
```

Può anche aprire il `.docx` condiviso, senza dover ripetere E1 o E2.

## Distinzioni metodologiche fondamentali

- Il detector è addestrato e calibrato **solo su X-LSB X=23**. Lo spread sintetico è usato **solo come OOD in test**, non sostituisce X-LSB nel training.
- L'algoritmo `SPREAD_v0` **si ispira al principio spread-spectrum di MaleficNet**, ma **non è MaleficNet, non è una replica, non include malware, ECC o fine-tuning**.
- La differenza di AUROC osservata è interna allo zoo condiviso, e il confronto non è matched per payload rate/perturbazione L2.
- E2 è **concluso**; E3 è **proposto ma non eseguito**. L'eventuale paper scientifico è futuro e separato dal progetto d'esame.
- Tutti gli esperimenti di detection sono sui pesi numerici autentici; il dump delle immagini STL10 è usato solo per il pilot utility delle CNN.

## Fonti principali dei numeri

- `docs/E2_G7_FINAL_RESULTS.md`
- `results/e2_final/`
- `results/pilots/e2_g3_utility_train_v0/`
- `docs/E2_PROTOCOL_FROZEN.md`
- `exam/E1_REPORT.md`

Versione report: 22 ottobre 2026.
