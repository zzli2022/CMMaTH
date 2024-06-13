from tool.api_tool import get_chat_response, get_chat_vllm_response
from tool.opensource_tool import get_opensource_llm_reponse
from tool import save_json, read_json
from tool import create_model_tokenizer
from tqdm import tqdm
import argparse 
import os
from argparse import Namespace
from torch.utils.data import DataLoader
from tool.dataloader import CMMaTH_APIDataset, image_to_base64, CMMaTHDataset, CMMaTH_vLLMDataset
from vllm import LLM, SamplingParams
import os

dataset_list = ['CMMaTH']
type_list = ['api_model', 'opensource_model']
model_list = ['gemin-pro']

def eval(args, dataset_path, output_json_file):
    if args.model_type == "vllm":
        eval_opensource_model_vllm(args, dataset_path, output_json_file)
    if args.model_type == 'api_model':
        eval_api_model(args, dataset_path, output_json_file)
    if args.model_type == 'opensource_model':
        eval_opensource_model(args, dataset_path, output_json_file)

def eval_opensource_model_vllm(args, dataset_path, output_json_file):
    dataset = CMMaTH_vLLMDataset(
        dataset_path=dataset_path,
        args=args,
    )
    sampling_params = SamplingParams(temperature=0.2, top_p=0.95, max_tokens=2048)
    vllm_model = LLM(model=args.model_name, tensor_parallel_size=args.vllm_gpu_num, gpu_memory_utilization=0.7)
    data_loader = DataLoader(dataset, batch_size=args.bsz, collate_fn=dataset.collate_fn)
    answer_dict = {}
    times = 0
    for data_iter in tqdm(data_loader):
        model_input = data_iter["model_input"] # question with prompt
        instance_ids = data_iter['prob_id']  # instances_id
        ocr_results  = data_iter['ocr'] # img_paths
        answer_result = get_chat_vllm_response(args, vllm_model, model_input, ocr_results, sampling_params) # batch result 
        for i in range(len(answer_result)):
            answer_dict[instance_ids[i]] = answer_result[i] 
        times +=1
    save_json(answer_dict, output_json_file)
    return 
    
def eval_opensource_model(args, dataset_path, output_json_file):
    model, tokenizer, config = create_model_tokenizer(args, from_local=args.from_local)
    dataset = CMMaTHDataset(
        dataset_path=dataset_path,
        max_seq_length=args.max_seq_length,
        tokenizer=tokenizer,
        args=args,
    )
    data_loader = DataLoader(dataset, batch_size=args.bsz, collate_fn=dataset.collate_fn)
    answer_result = get_opensource_llm_reponse(data_loader, model, tokenizer, args.sample_number)
    save_json(answer_result, output_json_file, indent=2)

def eval_api_model(args, dataset_path, output_json_file):
    dataset = CMMaTH_APIDataset(
        dataset_path=dataset_path,
        args=args,
    )
    data_loader = DataLoader(dataset, batch_size=1, collate_fn=dataset.collate_fn)
    answer_dict = {}
    times = 0
    for data_iter in tqdm(data_loader):
        model_input = data_iter["model_input"] # question with prompt
        instance_ids = data_iter['prob_id']  # instances_id
        img_paths    = data_iter['img_path'] # img_paths
        for i in range(args.bsz):
            image_url = image_to_base64(os.path.join(args.img_dir, img_paths[i]))
            answer_result = get_chat_response(args, model_input[i], image_url)
            answer_dict[instance_ids[i]] = answer_result
        times +=1
    save_json(answer_dict, output_json_file)

def get_filename_from_path(path):
    # 判断是否为路径
    filename = os.path.basename(path)
    filename_without_extension = os.path.splitext(filename)[0]
    return filename_without_extension
     
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt_type", default="general", choices=["general", "fewshot"], type=str) # prompt_type
    parser.add_argument("--eval_dataset_path", default="./cmmath_v3.json", type=str)
    parser.add_argument("--img_dir", default="/mnt/pfs/jinfeng_team/MMGroup/lzz/code/CMMaTH/images", type=str)
    parser.add_argument("--output_json_dir", default="result", type=str)
    parser.add_argument("--model_name", default="/mnt/pfs/jinfeng_team/MMGroup/lzz/huggingface_checkpoint/WizardMath-7B-V1.1", type=str)
    parser.add_argument("--model_type", default="vllm", choices=["api_model", "opensource", "vllm"], type=str)
    parser.add_argument("--bsz", default=1000, type=int)
    parser.add_argument("--vllm_gpu_num", default=1, type=int)
    parser.add_argument("--use_ocr", default=False, action='store_true')
    
    args = parser.parse_args()
    if args.use_ocr:
        args.eval_dataset_path = args.eval_dataset_path.replace("cmmath_v3.json", "cmmath_v3_ocr.json")
    output_json_dir = os.path.join(args.output_json_dir, get_filename_from_path(args.model_name))
    output_json_file = os.path.join(output_json_dir, f"eval_result.json") if not args.use_ocr else os.path.join(output_json_dir, f"eval_result_with_ocr.json")
    eval(args, args.eval_dataset_path, output_json_file) # 