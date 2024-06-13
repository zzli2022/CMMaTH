#!/bin/bash

# 定义模型名称列表
model_names=(
    "cogagent_18b"
    "baichuan2_13b"
    "qwen_14b"
    #"mathgpt"
    "gpt4v"
    "yi_vl_34b"
    "intern_vl_xcomposer"
    "qwen_14b"
    "MetaMath-70B-V1.0"
    "deepseek-math-7b-instruct"
    "llama2_70b"
)

for model_name in "${model_names[@]}"; do
    python3 tools/statics_acc.py --model_name "$model_name" --eval_mode visual_subject
    echo "当前模型名字: $model_name"
done
