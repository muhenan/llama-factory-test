# LLaMA Factory Test

This project is a sandbox for testing and fine-tuning models using [LLaMA Factory](https://github.com/hiyouga/LLaMA-Factory).

## Project Structure

- **data/**: Contains custom datasets and dataset configuration.
  - `dataset_info.json`: Configuration mapping for datasets.
  - `henan_identity.json` / `henan_identity_v2.json`: Custom identity datasets used for training/testing.
- **test_cpu.py**: Python script for testing model inference (likely on CPU).
- **saves/**: Directory where model checkpoints and training logs are saved (ignored in git).
- **cache/** & **llamaboard_cache/**: Cache directories for LLaMA Factory and LlamaBoard (ignored in git).

## Getting Started

1. Ensure you have LLaMA Factory installed.
2. Place your datasets in the `data/` folder and update `dataset_info.json`.
3. Run training scripts or use the LLaMA Board UI.

## Notes

- This repository is set up to ignore large model files and cache directories.

