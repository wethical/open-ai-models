# Open AI Models

收集并维护可开源使用的小型 AI 模型：模型卡、推理配置与可直接运行的示例代码。

当前收录：

| 模型 | 参数规模 | 类型 | 许可证 | 目录 |
| --- | --- | --- | --- | --- |
| Qwen2.5-0.5B-Instruct | 0.49B | 指令微调对话模型（Causal LM） | Apache-2.0 | [`models/qwen2.5-0.5b`](models/qwen2.5-0.5b) |

## 仓库里有什么

- **模型卡**：官方模型介绍、训练数据、评测结果、使用建议
- **推理配置**：`config.json`、`generation_config.json`、`tokenizer_config.json`、`tokenizer.json`
- **示例代码**：`transformers` 单轮推理与交互式多轮对话

## 关于权重

本仓库**不包含模型权重**（`*.safetensors` 单文件通常数百 MB 以上，不适合直接进 Git）。权重请按官方渠道获取：

```bash
# 方式一：Hugging Face（需要能访问 huggingface.co）
pip install -U huggingface_hub
huggingface-cli download Qwen/Qwen2.5-0.5B-Instruct --local-dir ./weights/qwen2.5-0.5b

# 方式二：使用镜像（国内网络环境）
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download Qwen/Qwen2.5-0.5B-Instruct --local-dir ./weights/qwen2.5-0.5b
```

拿到权重后，把它和本仓库 `models/qwen2.5-0.5b` 下的配置文件放在同一目录即可直接加载。

## 快速开始

```bash
python -m pip install -r examples/requirements.txt

# 单轮推理
python examples/infer.py --model Qwen/Qwen2.5-0.5B-Instruct --prompt "用一句话解释什么是混淆器"

# 交互式对话
python examples/chat.py --model ./weights/qwen2.5-0.5b
```

`--model` 既可以是 Hugging Face 上的模型 ID（自动下载），也可以是本地权重目录。

## 目录结构

```
.
├── LICENSE                      # Apache-2.0
├── README.md
├── examples
│   ├── chat.py                  # 交互式多轮对话
│   ├── infer.py                 # 单轮/批量推理
│   └── requirements.txt
└── models
    └── qwen2.5-0.5b
        ├── README.md            # 官方模型卡
        ├── config.json
        ├── generation_config.json
        ├── tokenizer.json
        └── tokenizer_config.json
```

## 许可证

- 本仓库的代码与文档：Apache License 2.0，见 [LICENSE](LICENSE)
- Qwen2.5-0.5B-Instruct 模型：Apache-2.0，版权归阿里巴巴通义千问团队所有，模型卡与配置文件按其许可证分发

## 免责声明

示例代码仅用于学习与本地实验用途。模型输出可能存在偏差或错误，请勿直接用于高风险决策场景。