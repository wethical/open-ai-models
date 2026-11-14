#!/usr/bin/env python3
"""交互式多轮对话示例：Qwen2.5-0.5B-Instruct

用法:
    python chat.py
    python chat.py --model ./weights/qwen2.5-0.5b
    python chat.py --system "你是一个简洁的中文助手"

输入 /reset 清空上下文，/exit 或 Ctrl+C 退出。
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
    parser = argparse.ArgumentParser(description="Qwen2.5 交互式对话")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--system", default="你是一个乐于助人的中文助手，回答尽量简洁。")
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.7)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    device = pick_device()

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype="auto" if device != "cpu" else torch.float32,
    ).to(device)
    model.eval()

    history = [{"role": "system", "content": args.system}]
    print(f"模型: {args.model} (device={device})")
    print("输入 /reset 清空上下文，/exit 退出。\n")

    while True:
        try:
            user_input = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input == "/exit":
            break
        if user_input == "/reset":
            history = [{"role": "system", "content": args.system}]
            print("（上下文已清空）\n")
            continue

        history.append({"role": "user", "content": user_input})

        text = tokenizer.apply_chat_template(
            history,
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
                pad_token_id=tokenizer.eos_token_id,
            )

        generated = output_ids[:, inputs.input_ids.shape[1]:]
        reply = tokenizer.batch_decode(generated, skip_special_tokens=True)[0].strip()
        print(f"AI: {reply}\n")

        history.append({"role": "assistant", "content": reply})

    return 0


if __name__ == "__main__":
    sys.exit(main())