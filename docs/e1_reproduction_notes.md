# E1 reproduction notes

E1 v2 is the final in-distribution experiment. Exploratory v1 outputs are retained separately and must not be combined with v2 metrics.

| Item | Recorded value |
|---|---|
| Upstream Model X-Ray commit | `a880e332f556fc71faf8d3753931005d5d019339` |
| Weight matrix | 1,000 CNNs x 2,864 `float32` values |
| Source split | 600 train / 200 validation / 200 test |
| Main random seed | 42 |
| X-LSB settings | 1, 8, 16 and 23 |
| Repetitions | 10 per X setting |
| Few-shot training examples | 3 benign + 3 modified |
| Primary metric | Centroid AUROC |

`weights.npy` SHA-256: `5a03ff6349010405fd05c7c27aee746143259fdf0a000acb4c9e05cbc8dd60ad`.

`manifests/e1_uniform_v1/splits.csv` SHA-256: `3f4236bf2b3e7a91e11dd67037c5dc3262382fd8c77ce333b49f30d6e4b93a6f`.

At X=23, mean centroid AUROC is 0.901863 on Ubuntu and 0.904378 on Mac M4. At X=1, 8 and 16, AUROC is close to 0.5. The Mac experiment is a computational replication using the same checkpoint collection, not a new CNN architecture.

Payload generation is deterministic for a given checkpoint and protocol configuration. TensorFlow training is not claimed to be bitwise deterministic. The threshold is selected on validation data only.
