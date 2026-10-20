# E1 — Appendice finale: integrità e analisi hardware (20/10/2026)

**Stato: verifiche di integrità e confronto descrittivo completati.** Questo documento supporta `exam/E1_REPORT.md` e non sostituisce i CSV originali. I risultati Mac sono una replica su altro **ambiente di calcolo**, non su nuova architettura neurale.

## Evidenze e livelli di verifica

| Oggetto | Evidenza | Giudizio |
|---|---|---|
| Runner E1 v2 | SHA-256 `a75aa3d844bb695a6d6155fe808394025b04c480d74d1e1b856eec5ca6f9c037`, verificato nella copia di lavoro e confermato da Fabrizio | Concordanza del runner; diff dei file esecutivi riferito da Fabrizio come nullo (log non allegato) |
| Pesi e split | SHA-256 identici nei due `run_config` Mac, uguali a Ubuntu | Identici a livello di hash |
| Upstream Model X-Ray | `a880e332f556fc71faf8d3753931005d5d019339` | Identico |
| Payload `repeat=0, X=23` | 403 manifest: 3 train + 200 val + 200 test; 403/403 SHA ricreati | Riproducibilità dei byte dimostrata per questa condizione |
| Mac CSV campagna test | 320 righe metriche, 40 fit, 32 righe summary | Medie originali verificate |
| Mac validation stand-alone | 16 righe, 10 run dichiarati per configurazione | Summary ricevuto; per-run non forniti |
| Ambiente Mac | Apple M4 ARM64 10 core, 16 GB, macOS 27.0.1 | Campi presenti nel file; recupero software incompleto |

## Confronto quantitativo E1 v2

| X-LSB | AUROC Ubuntu centroid | AUROC Mac centroid | Δ Mac−Ubuntu | Tempo Mac `elapsed_sec`, media ± SD (s) |
|---:|---:|---:|---:|---:|
| 1 | 0.500150 | 0.500209 | +0.000059 | 102.76 ± 5.97 |
| 8 | 0.508232 | 0.509388 | +0.001156 | 104.22 ± 2.36 |
| 16 | 0.501293 | 0.501425 | +0.000132 | 105.12 ± 1.73 |
| 23 | 0.901863 | 0.904378 | +0.002515 | 105.54 ± 1.41 |

**Mac validation separata X23 AUROC centroid:** 0.882700. **Mac validation durante i fit test X23:** 0.883028. **Ubuntu validation separata X23:** 0,882645. Le tre misure sono *campagne distinte*: non fonderle.

## Costi di esecuzione registrati

- Ubuntu VirtualBox: media `elapsed_sec` **217,124 s** per fit (dato dall'audit locale comunicato da Riccardo). Totale dei 40 intervalli misurati ~144,75 min.
- Mac M4 CPU: media `elapsed_sec` **104,412 s** (ricontrollata dal CSV ricevuto). Totale dei 40 intervalli misurati ~69,61 min.
- Rapporto delle medie Ubuntu/Mac: **2,079**. Non è uno speedup causale del chip: virtualizzazione, OS, CPU, build TF, threading e disponibilità RAM cambiano insieme.
- `elapsed_sec` non include avvio Python e tutto il preprocessing; non sono state misurate misure end-to-end uniformi né picco RAM comparabile.

## Riproducibilità e analisi delle 10 coppie

I 40 fit totali per piattaforma condividono la griglia `(repeat, X, fit_seed)`. L'audit `scripts/audit_e1_platforms.py`, già eseguito sulla macchina Ubuntu, ha prodotto **40 coppie** in `paired_per_run.csv`. Le medie delle differenze sono già note, ma i **CSV delle differenze individuali non facevano parte del materiale caricato in questa conversazione**: non inventiamo deviazioni standard o intervalli di confidenza delle differenze paired. Il comando seguente li materializza usando i CSV GitHub locali:

```bash
python3 scripts/audit_e1_platforms.py --out-dir results/analysis/e1_hardware
```

Archiviare quindi `results/analysis/e1_hardware/` se si desiderano anche i dati per ogni coppia. Non occorre alcun nuovo training. Nota: ricontrollare `git status` e tenere gli output raw immutati.

## Stato, limiti e decisione

**E1 chiuso:** baseline in-distribution LSB su stesso zoo, test per identità disgiunte e replica Mac coerente. Rimangono fuori dall'evidenza: valutazione esterna, payload recovery, utility del modello dopo embedding, causalità dei tempi CPU, equivalenza bitwise dei training e validazione cross-architecture delle CNN. Il mini-benchmark CPU/RAM prospettico è **opzionale** e non blocca E2.

**Artefatti:** `results/replicas/e1_mac_m4/audit/`, `results/figures/e1/E1_grafici.xlsx`, figure `e1_hw_*.png`, `exam/E1_REPORT.md`. Dataset e payload binari non sono distribuiti dentro Git.
