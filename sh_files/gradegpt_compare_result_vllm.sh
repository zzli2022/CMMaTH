current_time=$(date +"%m%d_%H%M")

python3 tool/compare_answer_gradegpt.py \
     --weight_path /mnt/pfs/jinfeng_team/MMGroup/lzz/code/GradeGPT_A/sft_output/output_0606_0847_agent \
     --output_json_file  ./process_eval_bench_result/process_correct_eval_v1.json \
     --report_file_path ./process_eval_bench_result/result_gradegpt_${current_time}.json \
     --vllm_gpu_num 1
