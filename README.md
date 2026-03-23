# LLaMA Factory Test

This project is a sandbox for testing and fine-tuning models using [LLaMA Factory](https://github.com/hiyouga/LLaMA-Factory).

## Notes

- [在 Mac 上运行 LLaMA Factory](notes/mac-setup-and-workflow.md) - 环境配置、训练与推理工作流、模型管理
- [在服务器上部署 LLaMA Factory](notes/server-deployment.md) - 源码安装、启动 Web UI、SSH 端口转发远程访问
- [SFT](notes/sft.md) - 关键参数解释：数据集 size、epoch、batch size、gradient accumulation、step 计算、learning rate
- [LoRA](notes/lora.md) - 原理、低秩矩阵 A/B、参数量对比示例、rank 和 alpha 参数详解
- [DPO](notes/dpo.md) - 原理、数据集格式示例、与 SFT 的对比

## Project Structure

- **data/**: Contains custom datasets and dataset configuration.
  - `dataset_info.json`: Configuration mapping for datasets.
  - `henan_identity.json` / `henan_identity_v2.json`: Custom identity datasets used for training/testing.
- **test_cpu.py**: Python script for testing model inference.
- **saves/**: Directory where model checkpoints and training logs are saved (ignored in git).
- **cache/** & **llamaboard_cache/**: Cache directories for LLaMA Factory and LlamaBoard (ignored in git).
- **notes/**: Learning notes and operational guides.

## Misc Notes

- This repository is set up to ignore large model files and cache directories via `.gitignore`.
