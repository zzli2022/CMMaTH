from tool.gpt_agent import submit_question, get_batch_result, resemble_data
from prompt.subject_prompt import class_prompt 
import re
import json
from tool.gpt_agent import resemble_data
import json
import time
from tqdm import tqdm

easy_cnt = 0
middle_cnt = 0
hard_cnt = 0

def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

def compute_score(diagram_description, question, analysis, max_T_D_len, min_T_D_len, max_s_len, min_s_len):
    alpha = 0.5
    return alpha*(len(diagram_description)+len(question)-min_T_D_len)/(max_T_D_len-min_T_D_len)+(1-alpha)*(len(analysis)-min_s_len)/(max_s_len-min_s_len)
    
def quickselect(arr, k):
    if arr:
        pivot = arr[0]
        left = [x for x in arr if x > pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x < pivot]

        if k <= len(left):
            return quickselect(left, k)
        elif k <= len(left) + len(middle):
            return middle[0]
        else:
            return quickselect(right, k - len(left) - len(middle))
    else:
        return None

def judge_complexity(diagram_description, question, analysis, max_T_D_len, min_T_D_len, max_s_len, min_s_len):
    score = compute_score(diagram_description, question, analysis, max_T_D_len, min_T_D_len, max_s_len, min_s_len)
    global easy_cnt
    global middle_cnt
    global hard_cnt
    if score<=0.1:
        easy_cnt += 1
        return "Easy"
    if score>0.1 and score<=0.3:
        middle_cnt += 1
        return "Middle"
    if score>0.3:
        hard_cnt += 1
        return "Hard"

def label_complexity(data):
    len_T_D = []
    len_S = []
    for data_item in data:
        len_T_D.append(len(data_item["ocr"])+len(data_item["question"]))
        len_S.append(len(data_item["analysis"]))
    # import pdb; pdb.set_trace()  
    max_T_D_len = quickselect(len_T_D, 10)
    min_T_D_len = min(len_S)
    max_s_len = max(len_S)
    min_s_len = min(len_S)
    # import pdb; pdb.set_trace()  
    for data_item in data:
        data_item["complex_type"] = judge_complexity(diagram_description=data_item["ocr"], question=data_item["question"], analysis=data_item["analysis"], max_T_D_len=max_T_D_len, min_T_D_len=min_T_D_len, max_s_len=max_s_len, min_s_len=min_s_len)
    print(easy_cnt, middle_cnt, hard_cnt)
    return data

cmmath_data = read_json('./cmmath.json')
labeled_data = label_complexity(cmmath_data)
save_to_json(labeled_data, "./cmmath_complex.json")
