# Development Environment Setup

## Tested environment

- Ubuntu 24.04 LTS
- Python 3.11
- Git
- uv package manager
- CPU-compatible setup

## 1. Clone the repository

```bash
git clone --recurse-submodules \
  https://github.com/riccardodannibale/PROGETTO-MACHINE-LEARNING-SECURITY.git

cd PROGETTO-MACHINE-LEARNING-SECURITY
```

The repository is private. GitHub access is required.

## 2. Install system dependencies

```bash
sudo apt update

sudo apt install -y \
  git \
  curl \
  ca-certificates \
  build-essential
```

## 3. Install uv

Follow the official installation instructions:

https://docs.astral.sh/uv/getting-started/installation/

## 4. Install the Python environment

```bash
./scripts/setup_linux.sh
```

This installs Python 3.11 and the locked dependencies.

## 5. Verify Model X-Ray

```bash
./scripts/check_setup.sh
```

## 6. Development

The original Model X-Ray code is available in:

`external/ModelXRay/`

Project-specific code belongs in:

- `src/`
- `scripts/`
- `configs/`
- `tests/`

## Data

Model checkpoints and datasets are not included in Git.

Their provenance, download instructions and generation procedures
must be documented.

Experiments use synthetic non-executable payloads.

## Upstream

https://github.com/danigil/ModelXRay

The upstream software retains its original license.
