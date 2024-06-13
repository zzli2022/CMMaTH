import os
import json
import pickle
import yaml
import codecs
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
from argparse import ArgumentParser
import os
from typing import Tuple


def create_model_tokenizer(args: ArgumentParser, from_local: bool=True) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
    if from_local:
        assert os.path.exists(args.weight_path), f"cannot find weight path: {args.weight_path}"
        model = AutoModelForCausalLM.from_pretrained(
             args.weight_path, device_map="auto", trust_remote_code=True)
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=args.weight_path, trust_remote_code=True, padding_side='left', pad_token="<|endoftext|>")
        config = AutoConfig.from_pretrained(pretrained_model_name_or_path=args.weight_path, trust_remote_code=True)
        
    else:      
        model = AutoModelForCausalLM.from_pretrained(
            args.model_name,  device_map="auto", token="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"
        ).cuda()
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained(args.model_name, token="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")
        config = AutoConfig.from_pretrained(args.model_name)
        
    return model, tokenizer, config

def read_json(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

def save_json(data, output_file, indent=True):
    # get the dir path
    directory = os.path.dirname(output_file)
    # if the dir path don't exit, mkdir the dir
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(output_file, 'w', encoding="utf-8") as wr_file:
        if not indent:
            json.dump(data, wr_file, ensure_ascii=False)
        else:
            json.dump(data, wr_file, indent=4, ensure_ascii=False)

def read_pickle(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def read_yaml(yaml_path: str) -> dict:
    # @Jiaxin: this file is used for loading configurations from yaml.
    with codecs.open(yaml_path, "r", "utf-8") as file:
        config = yaml.safe_load(file)
    return config

def read_jsonl(file_path):
    records = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            record = json.loads(line.strip())
            records.append(record)
    return records