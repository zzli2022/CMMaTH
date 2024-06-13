

import json

def read_jsonl(file_path):

    json_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            json_obj = json.loads(line.strip())
            json_list.append(json_obj)
    return json_list

def read_json(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        json_obj = json.load(file)
    return json_obj


def list_to_dict_by_key(input_list, key):

    output_dict = {}
    for item in input_list:
        item_key = item.get(key)
        if item_key:
            output_dict[item_key] = item
    return output_dict

def dict_to_list(input_dict):

    output_list = []
    for key, value in input_dict.items():
        value[key] = key
        output_list.append(value)
    return output_list

import json

def save_list_to_json(data_list, file_path):

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data_list, file, ensure_ascii=False, indent=4)

read_json_path = "/mnt/pfs/jinfeng_team/MMGroup/lzz/code/CMMaTH/result/yi_vl_34b/eval_result.jsonl"
merge_data_json = "/mnt/pfs/jinfeng_team/MMGroup/lzz/code/CMMaTH/cmmath_v3.json"
eval_result = read_jsonl(read_json_path)
data_dict = list_to_dict_by_key(read_json(merge_data_json), 'problem_id')
for data_item in eval_result:
    question_id = data_item["question_id"]
    text = data_item["text"]
    data_dict[question_id].update({"model_response":text})

data_list = dict_to_list(data_dict)
save_list_to_json(data_list, file_path="/mnt/pfs/jinfeng_team/MMGroup/lzz/code/CMMaTH/result/yi_vl_34b/gpt4eval/eval_result_gpt4.json")