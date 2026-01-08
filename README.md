# LLaMA Factory Test

This project is a sandbox for testing and fine-tuning models using [LLaMA Factory](https://github.com/hiyouga/LLaMA-Factory).

## Project Structure

- **data/**: Contains custom datasets and dataset configuration.
  - `dataset_info.json`: Configuration mapping for datasets.
  - `henan_identity.json` / `henan_identity_v2.json`: Custom identity datasets used for training/testing.
- **test_cpu.py**: Python script for testing model inference.
- **saves/**: Directory where model checkpoints and training logs are saved (ignored in git).
- **cache/** & **llamaboard_cache/**: Cache directories for LLaMA Factory and LlamaBoard (ignored in git).

## Setup & Installation

**Prerequisite**: Python 3.10 is required.

1. **Install Python 3.10** (if not already installed):
   ```bash
   brew install python@3.10
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   /opt/homebrew/bin/python3.10 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install LLaMA Factory**:
   ```bash
   uv pip install llamafactory
   ```
   *(Note: Ensure you have `uv` installed, or use `pip install llamafactory`)*

4. **Launch the Web UI**:
   ```bash
   llamafactory-cli webui
   ```

## Workflow

### 1. Training
We use **LLaMA Factory** exclusively for model training.
1. Start the Web UI (`llamafactory-cli webui`).
2. Upload your training dataset via the UI (updating `dataset_info.json` in `data/`).
3. Configure your training parameters and start fine-tuning.

### 2. Inference & Testing
We use our own custom script for model testing, not the built-in LLaMA Factory inference tools.

Run the testing script:
```bash
python test_cpu.py
```

> **Note**: Ensure the model path in `test_cpu.py` points to your latest checkpoint in the `saves/` directory.

## Architecture & Artifacts

### LLaMA Factory's Role
- Provides training framework and Web UI.
- Simplifies dataset processing.
- Configures LoRA training.
- Generates checkpoints.

### Model Files
You have two main components:
1. **Base Model**: Stored in `~/.cache/huggingface/` (approx. 6GB for 3B models).
2. **LoRA Checkpoint**: Stored in `saves/xxx/checkpoint-2/` (approx. tens of MB).

These two components are all you need.

### Testing Script (`test_cpu.py`)
- Uses `transformers` + `peft` libraries only.
- Loads the base model + LoRA checkpoint directly.
- Runs completely independently of LLaMA Factory.

## Model Management (Hugging Face)

### Inspecting Local Model Cache
Check what models are downloaded from Hugging Face on your machine:

```bash
# Check the hub directory
ls -lh ~/.cache/huggingface/hub

# Check specific model folder
ls -lh ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct/

# Inspect snapshots
ls -lh ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct/snapshots/*/

# Check file size
du -sh ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct/
```

### Manual Model Download
If you need to download a model manually:

```bash
# Install huggingface_hub
pip install huggingface_hub

# Download model to a specific directory
huggingface-cli download \
    Qwen/Qwen2.5-3B-Instruct \
    --local-dir ./models/qwen-3b \
    --local-dir-use-symlinks False
```

## Notes

- This repository is set up to ignore large model files and cache directories via `.gitignore`.
