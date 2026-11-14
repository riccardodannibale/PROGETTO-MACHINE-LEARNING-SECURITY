# Data, third-party components and licenses

## Project code
The project's own code is distributed under the MIT License in the repository-root `LICENSE` file. This license does not override third-party terms.

## Model X-Ray
The upstream implementation is included as the Git submodule `external/ModelXRay/`, pinned to commit `a880e332f556fc71faf8d3753931005d5d019339`. Preserve upstream attribution and follow its license. Its terms are separate from this project's MIT license.

## Dataset and checkpoints
The experiments use the GHRP/STL10 checkpoint collection, available from [Zenodo record 6631784](https://zenodo.org/records/6631784). The original zoo, large checkpoint files and intermediate `.pt`/`.npy` artifacts are not included. Obtain them from the original source and check the applicable distribution terms.

The preprocessed `dataset.pt` contains STL10 images and labels; it is not the extracted neural-network weight matrix. The extracted `weights.npy` contains checkpoint parameters. These files serve different purposes.

## Synthetic payloads
The project uses synthetic, inert byte messages. No executable malware was embedded, executed or distributed. The custom spread-spectrum method is an educational implementation, not the original MaleficNet software.

## Reproducibility
Public result summaries and selected audit artifacts are included. Not every raw prediction, original checkpoint or locally generated intermediate file is redistributed. See `../REPRODUCING.md`.
