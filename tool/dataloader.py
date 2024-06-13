import torch
from argparse import ArgumentParser
from torch.utils.data import Dataset
from transformers import AutoTokenizer

from . import read_json
import urllib.parse

prompt_templete = {
    "general": "要求解的问题: {question}。 求解过程以及答案是:",
    "fewshot": "你是一个数学题解题助手，你的输入是一道数学题，以及这道题目的图像，你的任务是以中文输出这道题目的求解思路以及答案. 输出格式是一步一步的方式. 例如:问题: 小明有2000元, 一个苹果2元, 小明买了10个苹果。小明还有多少钱。求解步骤: 首先计算小明买苹果的开销为2乘10等于20元. <STEP1>用2000元减去所有的开销, 2000-20=1980. <STEP2>所以最终的答案为1980元. <STEP3> 问题:{question}, 求解步骤:"
}

import base64
# /mnt/pfs/jinfeng_team/MMGroup/lzz/code/CMMaTH/images/s_00001_img_1.png
def image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        base64_datas = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/png;base64,{base64_datas}"

# print(file_path_to_url("/mnt/pfs/jinfeng_team/MMGroup/lzz/code/CMMaTH/images/s_00001_img_1.png"))
class CMMaTH_APIDataset(Dataset):
    def __init__(self, dataset_path: str, args: ArgumentParser):
        self.dataset_path = dataset_path
        self.args = args
        
        # load data from json file
        raw_datas = read_json(dataset_path)
        print(f"load {len(raw_datas)} original data")
        
        self.datas = []
        self.instances = []
        self.prob_ids = []
        for instance in raw_datas:
            instance_processed = self._process_per_instance(
                instance=instance,
                prompt_type=args.prompt_type,
            )
            self.datas.append(instance_processed)
            self.instances.append(instance)
            self.prob_ids.append(instance["problem_id"])
        print(f"processed {len(self.datas)} data")
        
    def _process_per_instance(self, instance: dict, prompt_type: str="general") -> dict:
        quesntion_with_prompt = prompt_templete[prompt_type].format_map(dict(question=instance["question"]))
        return quesntion_with_prompt

    def __len__(self) -> int:
        return len(self.datas)

    def __getitem__(self, index: int) -> dict:
        model_input = self.datas[index]
        instance = self.instances[index]
        prob_id     = self.prob_ids[index]
        img_path = self.instances[index]["image"][0]
        return model_input, prob_id, img_path, instance

    def collate_fn(self, batch: list) -> dict:
        model_inputs = []
        prob_ids = []
        instances = []
        img_paths = []
        for sample in batch: 
            model_input, prob_id, img_path, instance = sample 
            model_inputs.append(model_input)
            instances.append(instance)
            prob_ids.append(prob_id)
            img_paths.append(img_path)
        return dict(model_input=model_inputs, prob_id=prob_ids, img_path=img_paths, instance=instances)
    
class CMMaTHDataset(Dataset):
    def __init__(self, dataset_path: str, args: ArgumentParser):
        self.dataset_path = dataset_path
        self.args = args


class CMMaTH_vLLMDataset(Dataset):
    def __init__(self, dataset_path: str, args: ArgumentParser):
        self.dataset_path = dataset_path
        self.args = args
        
        # load data from json file
        raw_datas = read_json(dataset_path)
        print(f"load {len(raw_datas)} original data")
        
        self.datas = []
        self.instances = []
        self.prob_ids = []
        for instance in raw_datas:
            instance_processed = self._process_per_instance(
                instance=instance,
                prompt_type=args.prompt_type,
            )
            self.datas.append(instance_processed)
            self.instances.append(instance)
            self.prob_ids.append(instance["problem_id"])
        print(f"processed {len(self.datas)} data")
        
    def _process_per_instance(self, instance: dict, prompt_type: str="general") -> dict:
        quesntion_with_prompt = prompt_templete[prompt_type].format_map(dict(question=instance["question"]))
        return quesntion_with_prompt

    def __len__(self) -> int:
        return len(self.datas)

    def __getitem__(self, index: int) -> dict:
        model_input = self.datas[index]
        instance = self.instances[index]
        prob_id     = self.prob_ids[index]
        ocr =  self.instances[index]["ocr"] # TODO: input data append_ocr
        return model_input, prob_id, ocr, instance

    def collate_fn(self, batch: list) -> dict:
        model_inputs = []
        prob_ids = []
        instances = []
        ocrs = []
        for sample in batch: 
            model_input, prob_id, ocr, instance = sample 
            model_inputs.append(model_input)
            instances.append(instance)
            prob_ids.append(prob_id)
            ocrs.append(ocr)
        return dict(model_input=model_inputs, prob_id=prob_ids, ocr=ocrs, instance=instances)