# Data, Third-Party Components, and Licenses

## Project code

The original project code is distributed under the license in the repository-root `LICENSE` file. That license applies to the project's own code only and does not override third-party terms.

## Model X-Ray upstream

The upstream Model X-Ray implementation is included as the `external/ModelXRay/` Git submodule. The project records a pinned upstream commit. Preserve attribution and comply with the upstream repository's license; do not copy upstream source files into the project's MIT-licensed tree unless the applicable license permits it.

## Dataset and checkpoints

The experiments use an original model/checkpoint collection and preprocessed STL10 images and labels. Large source checkpoints and intermediate `.pt`/`.npy` artifacts are not necessarily redistributed. Obtain them from the original source and check the applicable terms before downloading, sharing, or publishing them.

The file `dataset.pt` refers to preprocessed images and labels; the extracted `weights.npy` represents neural-network checkpoint parameters. They are different artifacts and must not be conflated.

## Synthetic payloads and security

The experimental payloads are synthetic and inert. No executable malware is embedded, activated, or distributed. Do not publish transient payload bytes or large model artifacts without checking source permissions and distribution terms.

## Reproducibility

See [`REPRODUCING.md`](../REPRODUCING.md) for the distinction between published-summary verification, auditing existing source-host artifacts, and full experiment recreation.
