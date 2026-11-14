# E1 platform comparison and audit

## Platforms
The final E1 comparison uses Ubuntu 24.04 in VirtualBox (x86_64 CPU, 6 vCPUs) and macOS on Apple M4 (ARM64 CPU). These are two computing platforms, not two CNN architectures. The source-checkpoint collection, weight representation and split are the same.

## Centroid test results

| X-LSB | Ubuntu AUROC | Mac M4 AUROC | Mac - Ubuntu |
|---:|---:|---:|---:|
| 1 | 0.500150 | 0.500209 | +0.000059 |
| 8 | 0.508232 | 0.509388 | +0.001156 |
| 16 | 0.501293 | 0.501425 | +0.000132 |
| 23 | 0.901863 | 0.904378 | +0.002515 |

At X=23, mean test accuracy using the validation Youden threshold is 0.82125 on Ubuntu and 0.82300 on Mac M4. The corresponding FPR values are 0.1550 and 0.1605.

The two environments report matching hashes for weights, the frozen split and the upstream submodule. The Mac replication manifest records 403 payload entries for repeat 0 at X=23; the payload hashes were regenerated and matched.

The Mac operator reported an empty diff of the experiment files against the Ubuntu runner, but the diff output was not included in the shared archive. The comparison is descriptive and does not establish bitwise equality, statistical equivalence or a controlled hardware benchmark.
