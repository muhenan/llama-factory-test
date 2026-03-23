# SFT

## 数据集格式示例

SFT 数据集常用 **Alpaca 格式**，每条样本包含三部分：
- **instruction**：任务描述
- **input**：额外的上下文或输入内容（可为空）
- **output**：期望的标准回答

```json
{
  "instruction": "比较以下两位著名人物，使用特征列表并以句子形式提供输出。",
  "input": "人物1：阿尔伯特·爱因斯坦\n人物2：斯蒂芬·霍金\n特征：智力、教育、对世界的影响",
  "output": "阿尔伯特·爱因斯坦和斯蒂芬·霍金都是拥有极其出色智力的人物。两人都取得过非常高的教育成就，他们推进了科学发展并在世界范围内产生了深远的影响。爱因斯坦以其相对论和质能关系公式而闻名，而霍金以其关于黑洞和宇宙的发现而著称。两位科学家都以其深厚的学识和非凡的贡献影响了世界。"
}
```

模型的训练目标就是：给定 instruction + input，学会生成 output。

### 与 Chat Template 的关系

Alpaca 格式只是**训练数据文件的存储格式**，与模型本身无关。LLaMA Factory 在训练时，会自动将 Alpaca 格式的数据转换成当前模型对应的 chat template（如 Qwen 的 ChatML 格式），再喂给模型训练。你只需要准备好 Alpaca 格式的数据文件，chat template 的转换由框架自动处理。

---

## SFT 的关键参数

### 数据集 Size

训练集中的样本条数。Size 越大，模型见到的样本越多，通常效果越好，但训练时间也越长。

### Epoch

对整个训练集完整遍历一次为 1 个 epoch。Epoch 越多，模型对数据学习的次数越多，但过多容易过拟合。

### Batch Size

每次前向 + 反向传播时，一次性喂给模型的样本数。Batch size 越大，显存占用越高，梯度估计越稳定。

### Gradient Accumulation

梯度累积步数。设为 N 表示每做 N 次前向/反向传播，才执行一次参数更新（optimizer step）。

作用：在显存不足时，用多次小 batch 模拟一次大 batch 的效果。
等效 batch size = batch size × gradient accumulation。

**硬件充足时，Gradient Accumulation 设 1 即可。**

Gradient Accumulation 本质上是显存不足时的 workaround。当显存充足时，直接用大 batch size、accumulation 设 1 是更好的选择——效果等价，但 GPU 并行利用率更高，不需要等多次前向传播才更新一次。

但"accumulation = 1"不等于"batch size 越小越好"：
- batch size 太小（如 1、2）→ 每次梯度估计噪声大 → 参数更新方向抖动 → 训练不稳定
- batch size 过大 → 梯度方向过于"平均" → 容易陷入较差的局部最优，泛化能力反而下降（large batch training 的经典问题）

**最佳实践**：硬件充足时，accumulation 设 1，batch size 本身调到合适范围（SFT 常见 4～32）。

### 如何计算 Step 数（参数更新次数）

$$\text{每个 epoch 的 step 数} = \frac{\text{数据集 size}}{\text{batch size} \times \text{gradient accumulation}}$$

$$\text{总 step 数} = \text{每个 epoch 的 step 数} \times \text{epoch 数}$$

**示例**：训练集 size = 1000，epoch = 2，batch size = 2，gradient accumulation = 2

- 等效 batch size = 2 × 2 = 4
- 每个 epoch 的 step 数 = 1000 / 4 = 250
- 总 step 数 = 250 × 2 = **500 次参数更新**

> 这里的"step"指的是 optimizer step，即真正更新一次模型参数。

### Learning Rate

控制每次参数更新的幅度。

- 太大：训练不稳定，loss 震荡甚至发散
- 太小：收敛极慢，容易陷入局部最优

SFT 常用范围：`1e-5` ～ `5e-4`，LoRA 微调通常取 `1e-4` 左右。一般配合学习率调度器（如 cosine）使用，训练初期 warmup，之后逐渐衰减。
