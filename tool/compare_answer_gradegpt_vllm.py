from opensource_tool import get_opensource_llm_reponse, get_opensource_llm_reponse_batch, get_opensource_llm_reponse_batch_vllm
import os
import sys
from vllm import LLM, SamplingParams
current_file_path = os.path.abspath(__file__)
parent_dir_path = os.path.dirname(os.path.dirname(current_file_path))
sys.path.insert(0, parent_dir_path)

from prompt.judge_prompt import judge_prompt, templete_prompt
import argparse 
import os
from tool import read_json, save_json, create_model_tokenizer
from tqdm import tqdm
from copy import deepcopy
dataset_list = ['CMMaTH']
type_list = ['api_model', 'opensource_model']
model_list = ['gemin-pro']

def concatenate_responses(responses_list):
    concatenated_responses = []
    for response in responses_list:
        concatenated_responses.extend(response)
    return concatenated_responses

def transform_data(problem_data):
    problem_dict = {}
    # import pdb; pdb.set_trace()
    for idx, problem in enumerate(problem_data):
        problem_dict[idx] = problem
    return problem_dict

def compare_answer_batch(args):
    compare_result_data = read_json(args.output_json_file) 
    compare_result_data_dict = transform_data(compare_result_data) 
    result_report_dict = {}
    cnt = 0
    right_dict = {}
    false_dict = {}
    unjudge_dict = {}
    times = 0
    compare_prompts = []
    for problem_id, data in tqdm(compare_result_data_dict.items()):
        templete_prompt_cur = deepcopy(templete_prompt)
        problem, answer, response = compare_result_data_dict[problem_id]["question"], compare_result_data_dict[problem_id]["answer"], compare_result_data_dict[problem_id]["model_response"]
        compare_prompt = judge_prompt+templete_prompt_cur.format_map(dict(problem=problem, answer=answer, response=response))
        compare_prompts.append(compare_prompt)
    # Split compare_prompts into smaller parts of length batch_size
    compare_prompts_parts = [compare_prompts[i:i+args.batch_size] for i in range(0, len(compare_prompts), args.batch_size)]
    responses_list = []

    vllm_model = LLM(model=args.weight_path, tensor_parallel_size=args.vllm_gpu_num, gpu_memory_utilization=0.8, trust_remote_code=True)
    for part in tqdm(compare_prompts_parts):
        # import pdb; pdb.set_trace()
        responses_list.append(get_opensource_llm_reponse_batch_vllm(args, vllm_model, part))
    compare_prompts_all = concatenate_responses(responses_list)
    for judge_data_item, compare_result in zip(compare_result_data, compare_prompts_all):
        problem_id = judge_data_item["question"]
        response = judge_data_item["model_response"]
        result_report_dict[problem_id] = {"compare_result":compare_result, 'answer': judge_data_item["answer"]}
        if "Yes" in compare_result:
            right_dict[problem_id] = (response, judge_data_item["answer"], compare_result)
            if judge_data_item["wrong_index"]==None:
                cnt+=1
        elif "No" in compare_result:
            false_dict[problem_id] = (response, judge_data_item["answer"], compare_result)
            if judge_data_item["wrong_index"]!=None:
                cnt+=1
        else:
            unjudge_dict[problem_id] = (response, judge_data_item["answer"], compare_result)
    result_dict  = {"right_len":len(right_dict), "false_len":len(false_dict), "total_num":len(compare_result_data), "cnt":cnt, "right_id":right_dict, "right_dict":right_dict, "false_dict":false_dict, "unjudge_dict":unjudge_dict}
    save_json(result_dict, args.report_file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt_type", default="general", choices=["general", "few-shot"], type=str) # prompt_type
    # parser.add_argument("--eval_dataset_path", default="./cmmath_testclass_v3.json", type=str)
    parser.add_argument("--output_json_file", default="result", type=str)
    parser.add_argument("--batch_size", default=100, type=int)
    parser.add_argument("--weight_path", default="", type=str)
    parser.add_argument("--report_file_path", default="./{output_json_dir}/{model_name}/result_testclass_report.json", type=str)
    parser.add_argument("--from_local", default=True, type=bool)
    parser.add_argument("--eval_result_file", default="eval_result_testmini.json", type=str)
    parser.add_argument("--vllm_gpu_num", default=4, type=int)
    parser.add_argument("--use_ocr", default=False, type=bool)
    
    
    args = parser.parse_args()
    # args.report_file_path = args.report_file_path.format_map(dict(output_json_dir=args.output_json_dir, model_name=args.model_name))
    # compare_answer(args)  
    compare_answer_batch(args=args)