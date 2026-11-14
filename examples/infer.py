#!/usr/bin/env python3
"""单轮 / 批量推理示例：Qwen2.5-0.5B-Instruct

用法:
    python infer.py --prompt "你好，介绍一下你自己"
    python infer.py --model ./weights/qwen2.5-0.5b --prompt "写一句关于秋天的诗"
    python infer.py --prompt "1+1=?" --max-new-tokens 64 --temperature 0.2

说明:
    --model 可以是 Hugging Face 模型 ID（自动下载），也可以是本地权重目录。
    国内网络可先设置环境变量 HF_ENDPOINT=https://hf-mirror.com 再运行。
"""

import argparse
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

DEFAULT_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"


def pick_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Qwen2.5 小模型推理示例")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型 ID 或本地权重目录")
    parser.add_argument("--prompt", default="你好，请用一句话介绍你自己。", help="用户输入")
    parser.add_argument("--system", default=None, help="可选的 system 提示词")
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--device", default="auto", help="auto / cpu / cuda / mps")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    device = pick_device() if args.device == "auto" else args.device

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype="auto" if device != "cpu" else torch.float32,
    ).to(device)
    model.eval()

    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": args.prompt})

    # apply_chat_template 负责套用官方的对话格式，不要自己拼 <|im_start|> 等特殊标记
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=args.max_new_tokens,
            do_sample=args.temperature > 0,
            temperature=args.temperature,
            top_p=args.top_p,
            pad_token_id=tokenizer.eos_token_id,
        )

    # 只取新生成的部分，避免把 prompt 原样回显
    generated = output_ids[:, inputs.input_ids.shape[1]:]
    reply = tokenizer.batch_decode(generated, skip_special_tokens=True)[0].strip()

    print("=" * 60)
    print(f"用户: {args.prompt}")
    print(f"模型: {reply}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())