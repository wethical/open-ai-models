# Open AI Models

收集并维护可开源使用的小型 AI 模型：模型卡、权重、推理配置与可直接运行的示例代码。

当前收录：

| 模型 | 参数规模 | 类型 | 许可证 | 目录 |
| --- | --- | --- | --- | --- |
| Qwen2.5-0.5B-Instruct | 0.49B | 指令微调对话模型（Causal LM） | Apache-2.0 | [`models/qwen2.5-0.5b`](models/qwen2.5-0.5b) |

## 仓库里有什么

- **模型权重**：`model.safetensors`（约 942 MiB，BF16），通过 **Git LFS** 托管
- **模型卡**：官方模型介绍、训练数据、评测结果、使用建议
- **推理配置**：`config.json`、`generation_config.json`、`tokenizer_config.json`、`tokenizer.json`
- **分词器词表**：`merges.txt`、`vocab.json`
- **示例代码**：`transformers` 单轮推理与交互式多轮对话

## 关于权重（Git LFS）

权重文件用 Git LFS 存储，克隆前请先安装 Git LFS，否则只会拿到指针文件：

```bash
git lfs install
git clone https://github.com/wethical/open-ai-models.git
cd open-ai-models
git lfs pull          # 如果克隆时未自动拉取
```

校验完整性（应与官方发布的 SHA256 一致）：

```bash
sha256sum models/qwen2.5-0.5b/model.safetensors
# fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe
```

如果不想拉取权重，也可以直接按官方渠道获取（与仓库内的配置文件放在同一目录即可使用）：

```bash
pip install -U huggingface_hub
# 方式一：Hugging Face（需要能访问 huggingface.co）
huggingface-cli download Qwen/Qwen2.5-0.5B-Instruct --local-dir ./weights/qwen2.5-0.5b

# 方式二：使用镜像（国内网络环境）
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download Qwen/Qwen2.5-0.5B-Instruct --local-dir ./weights/qwen2.5-0.5b
```

## 快速开始

```bash
python -m pip install -r examples/requirements.txt

# 用仓库内的权重直接推理
python examples/infer.py --model models/qwen2.5-0.5b --prompt "用一句话解释什么是混淆器"

# 交互式对话
python examples/chat.py --model models/qwen2.5-0.5b
```

`--model` 既可以是本仓库的本地目录，也可以是 Hugging Face 上的模型 ID（自动下载）。

## 目录结构

```
.
├── .gitattributes               # Git LFS 跟踪规则（*.safetensors）
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
        ├── merges.txt
        ├── model.safetensors    # 权重（Git LFS，942 MiB）
        ├── tokenizer.json
        ├── tokenizer_config.json
        └── vocab.json
```

## 许可证

- 本仓库的代码与文档：Apache License 2.0，见 [LICENSE](LICENSE)
- Qwen2.5-0.5B-Instruct 模型：Apache-2.0，版权归阿里巴巴通义千问团队所有，模型卡、配置文件与权重按其许可证分发

## 免责声明

示例代码仅用于学习与本地实验用途。模型输出可能存在偏差或错误，请勿直接用于高风险决策场景。