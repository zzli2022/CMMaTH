GRADEGPT_WEIGHT="./GradeGPT/path2weight"
# /mnt/pfs/jinfeng_team/MMGroup/lzz/code/GradeGPT_A/sft_output/output_0526_1334_JoT
current_time=$(date +"%m%d_%H%M")
MODEL_NAME=llava_v15
python tool/compare_answer_gradegpt.py \
     --weight_path $GRADEGPT_WEIGHT  \
     --output_json_file  ./result/$MODEL_NAME/eval_result.json  \
     --report_file_path ./result/$MODEL_NAME/correct_report_${current_time}.json \
     --batch_size 1