# DPO

## 什么是 DPO

DPO（Direct Preference Optimization）是一种对齐训练方法，目标是让模型的输出更符合人类偏好。

传统的对齐方式是 RLHF（Reinforcement Learning from Human Feedback），流程较重：先训练一个独立的 Reward Model 对输出打分，再用 PPO 强化学习优化模型。DPO 将这两步合并为一步，直接用偏好数据优化模型，不需要单独的 Reward Model，训练更简单稳定。

**核心思想**：给定同一个问题，数据集中标注了一个"好回答"（chosen）和一个"差回答"（rejected），模型通过对比学习，提高生成 chosen 的概率，降低生成 rejected 的概率。

## 数据集格式

DPO 数据集常用 **ShareGPT 格式**，每条样本包含三部分：
- **conversations**：对话上下文（用户的输入）
- **chosen**：偏好的回答（好的）
- **rejected**：不偏好的回答（差的）

### 示例

```json
{
  "conversations": [
    {
      "from": "human",
      "value": "详细说明：在这个任务中，我们要求您回答一个关于某个事件之前或之后可能发生的事件的问题。例如，"赚钱"通常会出现在"花钱"之前。请注意，许多问题可能有多个正确答案。我们只需要一个最有可能的答案。请尽量保持您的"答案"尽可能简单。简洁明了的"答案"优于复杂冗长的回答。\n问题：句子：自然堤防 洪水泛滥的河流通常会在河岸形成自然堤防。\n问题：一旦形成堤防会发生什么？\n解决方案："
    }
  ],
  "chosen": {
    "from": "gpt",
    "value": "答案：堤坝阻止了河水水位上涨，减少了洪水。"
  },
  "rejected": {
    "from": "gpt",
    "value": "一旦堤坝形成，它可以通过提高河岸和引导水流远离相邻的土地区域来防止未来的洪水。"
  }
}
```

可以看到，chosen 的回答简洁直接，rejected 的回答虽然也正确但过于冗长——这正是这条数据想教给模型的偏好：**简洁优于冗长**。

### 与 Chat Template 的关系

ShareGPT 格式只是**训练数据文件的存储格式**，与模型本身无关。LLaMA Factory 在训练时，会自动将 ShareGPT 格式（`from: human` / `from: gpt`）转换成当前模型对应的 chat template，再喂给模型训练。你只需要准备好 ShareGPT 格式的数据文件，chat template 的转换由框架自动处理。

## DPO vs SFT

| | SFT | DPO |
|---|---|---|
| 数据格式 | 问题 + 标准答案 | 问题 + 好答案 + 差答案 |
| 训练目标 | 学会怎么回答 | 学会回答得更好 |
| 典型用途 | 能力注入、格式学习 | 对齐人类偏好、风格优化 |
| 训练阶段 | 通常在 DPO 之前 | 通常在 SFT 之后 |

实践中两者经常组合使用：先 SFT 让模型学会基本能力，再 DPO 进一步对齐偏好。
