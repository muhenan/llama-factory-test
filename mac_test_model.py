from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

print("🔄 加载模型（Apple GPU - MPS）...")

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"使用设备: {device}")

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    torch_dtype=torch.float16,  # MPS 用 float16 更快
    low_cpu_mem_usage=True
)
model = model.to(device)

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")

print("🔄 加载 LoRA checkpoint...")
model = PeftModel.from_pretrained(
    model, 
    "saves/Qwen2.5-3B-Instruct/lora/train_2026-01-08-02-49-33/checkpoint-10"
)

print("✅ 模型加载完成！\n")

def ask(question):
    messages = [{"role": "user", "content": question}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    inputs = tokenizer([text], return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,         # 减少到 50（更快）
            temperature=0.7,
            do_sample=False,           # 关闭采样（贪心解码，更快）
            pad_token_id=tokenizer.pad_token_id
        )
    
    response = tokenizer.decode(
        outputs[0][len(inputs.input_ids[0]):], 
        skip_special_tokens=True
    )
    return response

# 测试
print("问题：你是谁？")
print(f"回答：{ask('你是谁？')}\n")

print("问题：Who are you?")
print(f"Answer: {ask('Who are you?')}\n")

print("问题：谁创建了你？")
print(f"回答：{ask('谁创建了你？')}")

print("问题：你认识Henan Mu吗？")
print(f"回答：{ask('你认识Henan Mu吗？他做了什么事情？他训练大语言模型吗')}")