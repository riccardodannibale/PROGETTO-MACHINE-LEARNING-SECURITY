# Relazione conclusiva — E1 + E2 + E3

- `PROJECT_REPORT.md` / `.docx`: relazione tecnica integrale, Parte I E1 **conservata**, Parte II E2 e Parte III E3 (controlli matched/metadata e confronto Mac/Ubuntu). **Non sostituisce** l’originale `E1_REPORT.*`.
- `E3_REPORT.md`: sezione E3 leggibile autonomamente.
- `../results/e3_final/e3_cross_platform_means_from_qa_report.csv`: sei righe di metriche E3 **ricostruite dal rapporto QA fornito dall’utente**, non il CSV di 60 fit originali.
- `../results/e3_final/plots/e3_centroid_tpr_fpr.png`: grafico da medie pubblicate nel rapporto E3; niente fit aggiuntivi.

## Provenienza e limite importante

La base E1/E2 è la precedente relazione integrata del 22 ottobre 2026 disponibile negli artifact della conversazione, **non è stata verificata sul branch remoto corrente**. I numeri E3 provengono dall'output dei comandi `e3_matched_controls.py` e `e3_compare_controls.py` eseguiti dall’utente e dal collaboratore sul proprio hardware. Lo script di confronto ha dichiarato 60/60 record per piattaforma, ma questa confezione **non include i due CSV grezzi da 60 righe**: copiarli dalla cartella locale per conservare la provenienza quantitativa completa.

## Integrazione sicura nella repository

Estrarre il pacchetto prima in una directory di staging (non usare `unzip -n` direttamente nella repo se `PROJECT_REPORT.*` esiste già), confrontare l'ultima versione locale del report, poi copiare i file approvati. Si raccomanda una revisione indipendente di Fabrizio di tutta la Parte III e dei riferimenti E1/E2 prima della consegna. I due report d'esame devono contenere gli stessi risultati e non dichiarare di avere svolto esperimenti intensity-matched inesistenti.

La roadmap A6 suggerisce una relazione di circa 10–15 pagine, da verificare col docente. **Questo è il report tecnico esteso**, da cui eventualmente ricavare una versione sintetica; non presumere che la sua lunghezza soddisfi automaticamente i vincoli della consegna.
