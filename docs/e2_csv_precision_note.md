# E2 validation audit: CSV floating-point precision

During the Mac M4 validation audit, the original threshold check reported mismatches for 1-NN. The discrepancy was traced to CSV parsing near a threshold. In a few cases, the score and threshold differed by one unit in the last place (ULP); the default pandas parser could remove that difference.

The audit was amended to use `pd.read_csv(path, float_precision="round_trip")`. A regression test compares the standard parser with round-trip parsing. The audit then found zero mismatches with round-trip parsing; the Ubuntu audit also reported zero mismatches.

The detector, training, seeds, split, scores, thresholds and preregistered metrics were not changed. This was a correction to the CSV audit procedure, not a change to the experiment.
