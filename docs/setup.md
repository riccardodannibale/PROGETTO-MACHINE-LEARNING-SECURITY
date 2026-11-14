# Development environment setup

## Recorded environment
- Ubuntu 24.04 LTS
- Python 3.11
- Git and `uv`
- CPU-based experiment setup

The pinned package list is `configs/modelxray-ubuntu24-py311.lock.txt`.

## Clone the repository
```bash
git clone --recurse-submodules https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY.git
cd PROGETTO-MACHINE-LEARNING-SECURITY
```

## Install system tools
```bash
sudo apt update
sudo apt install -y git curl ca-certificates build-essential
```

Install `uv` using its official installation instructions: https://docs.astral.sh/uv/getting-started/installation/.

## Create the Python environment
```bash
./scripts/setup_linux.sh
./scripts/check_setup.sh
```

The helper creates the environment under `$HOME/mlsec-local/venvs/modelxray`. Review the scripts before running them and check that this path is suitable for your machine.

## Data
Model checkpoints and datasets are not included in Git. Obtain the original model collection from its source and follow its licensing terms. The project scripts for downloading and extracting weights are in `scripts/`.
