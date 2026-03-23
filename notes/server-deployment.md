# 在服务器上部署 LLaMA Factory

## 部署步骤

### 1. 克隆源代码

```bash
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
```

### 2. 安装依赖

```bash
pip install -e ".[torch,metrics]"
```

> 如果需要其他可选依赖（如 bitsandbytes、vllm 等），可按需添加：
> ```bash
> pip install -e ".[torch,metrics,bitsandbytes,vllm]"
> ```

### 3. 启动 Web UI

```bash
llamafactory-cli webui
```

默认监听 `0.0.0.0:7860`，如需指定端口：

```bash
GRADIO_SERVER_PORT=7860 llamafactory-cli webui
```

### 4. 远程访问

如果服务器没有公网直接暴露，可以用 SSH 端口转发在本地访问：

```bash
ssh -L 7860:localhost:7860 user@your-server-ip
```

然后在本地浏览器打开 `http://localhost:7860`。
