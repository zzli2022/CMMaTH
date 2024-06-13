GRADEGPT_WEIGHT="./GradeGPT/path2weight"

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=baichuan2_13b
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=cogagent_18b
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=deepseek-math-7b-instruct
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=gpt4v
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=intern_vl_xcomposer
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=llama2_70b
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=llava_v15
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=MetaMath-70B-V1.0
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=qwen_14b
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=llava_v15
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=WizardMath-7B-V1.1
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1

current_time=$(date +"%m%d_%H%M")
MODEL_NAME=yi_vl_34b
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1