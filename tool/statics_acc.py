import json
import glob
import argparse

def read_json_cmmath(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("文件未找到")
    except json.JSONDecodeError:
        print("JSON文件格式错误")
    except Exception as e:
        print(f"读取JSON文件时发生错误: {e}")
        
def interval_map(num):
    if num >= 0 and num < 30:
        return "0-30"
    elif num >= 30 and num < 60:
        return "30-60"
    elif num >= 60 and num < 90:
        return "60-90"
    elif num >= 90 and num < 120:
        return "90-120"
    elif num >= 120 and num < 150:
        return "120-150"
    elif num >= 150 and num < 180:
        return "150-180"
    elif num >= 180 and num < 210:
        return "180-210"
    else:
        return ">210"
    
def extract_innermost_parent_parent_knowledge(sentence):
    stack = []
    knowledge_start = None
    for i, char in enumerate(sentence):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                knowledge_start = stack.pop()
                knowledge = sentence[knowledge_start+1:i]
                # 查找父节点的父节点的位置
                grandparent_start = None
                for j in range(knowledge_start - 1, -1, -1):
                    if sentence[j] == '(':
                        grandparent_start = j
                        break
                if grandparent_start is not None:
                    grandparent_knowledge = sentence[grandparent_start+1:knowledge_start]
                    return grandparent_knowledge
                else:
                    return ""  # 如果找不到父节点的父节点，则返回空字符串
            else:
                raise ValueError("右括号没有匹配的左括号")
    raise ValueError("没有找到括号匹配的知识点")

def extract_innermost_parent_knowledge(sentence):
    stack = []
    knowledge_start = None
    for i, char in enumerate(sentence):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                knowledge_start = stack.pop()
                knowledge = sentence[knowledge_start+1:i]
                # 查找该父节点的父节点字符串
                parent_start = None
                for j in range(knowledge_start - 1, -1, -1):
                    if sentence[j] == '(':
                        parent_start = j
                        break
                if parent_start is not None:
                    parent_knowledge = sentence[parent_start+1:knowledge_start]
                    return parent_knowledge
                else:
                    return ""  # 如果找不到父节点，则返回空字符串
            else:
                raise ValueError("右括号没有匹配的左括号")
    raise ValueError("没有找到括号匹配的知识点")

def count_chinese_chars(string):
    count = 0
    for char in string:
        if '\u4e00' <= char <= '\u9fff':
            count += 1
    return count
# # 示例调用
def extract_innermost_knowledge(sentence):
    stack = []
    knowledge_start = None
    for i, char in enumerate(sentence):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                knowledge_start = stack.pop()
                knowledge = sentence[knowledge_start+1:i]
                return knowledge
            else:
                raise ValueError("右括号没有匹配的左括号")
    raise ValueError("没有找到括号匹配的知识点")

def check_string(string):
    patterns = {"A\n", "B\n", "C\n", "D\n"}
    if string in patterns:
        return "single"
    else:
        return "multi"

def statics_function(args):
    model_name = args.model_name
    input_json = "./result/{model_name}/gpt4eval/gpt4_correct_report_*.json".format_map(dict(model_name=model_name))

    subject_class = {"Flow Chart": 0, "Bar Chart": 0, "Scatter Plot": 0,\
            "Line Plot": 0, "Fan Chart":0, "LiDAR Chart":0, \
            "Visual-Table":0, "Three View":0, "Three View":0, \
            "Folded Image":0, "Analytic Geometry":0, "Solid Geometry":0,
            "Plane Geometry":0, "Venn diagram":0, "Abtract Analogy diagram":0, "UnKnown":0}

    subject_right = {"Flow Chart": 0, "Bar Chart": 0, "Scatter Plot": 0,\
            "Line Plot": 0, "Fan Chart":0, "LiDAR Chart":0, \
            "Visual-Table":0, "Three View":0, "Three View":0, \
            "Folded Image":0, "Analytic Geometry":0, "Solid Geometry":0,
            "Plane Geometry":0, "Venn diagram":0, "Abtract Analogy diagram":0, "UnKnown":0}

    def read_json(file_path):
        file_paths = glob.glob(input_json)
        # import pdb; pdb.set_trace()
        all_data = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data.extend(data)
            except FileNotFoundError:
                print(f"文件 '{file_path}' 不存在")
            except json.JSONDecodeError:
                print(f"无法解析文件 '{file_path}' 中的 JSON 数据")
        return all_data


    correct_data = read_json(input_json)

    for item in correct_data:
        mm_cls = item["metadata"]["multimodal-category"]
        if mm_cls in subject_class.keys():
            subject_class[mm_cls] += 1
        else:
            subject_class["UnKnown"] += 1

    # print(subject_class)

    for item in correct_data:
        mm_cls = item["metadata"]["multimodal-category"]
        if (mm_cls in subject_right.keys()) and (item["output_correct"]=="Yes"):
            subject_right[mm_cls] += 1

    # print(subject_right)

    category_scores = {category: round((subject_right[category]/(count+1))*100,1) for category, count in subject_class.items()}

    # 计算总的分数
    total_score = round(sum(subject_right.values())/sum(subject_class.values())*100, 1)

    with open("./result/{model_name}/report.txt".format_map(dict(model_name=model_name)), 'w') as file:
        file.write("各个类别的分数：\n")
        for category, score in category_scores.items():
            file.write(f"{category}: {score}\n")
        file.write(f"\n总的分数: {total_score}\n")
    
def statics_grade_function(args):
    # import pdb; pdb.set_trace()
    model_name = args.model_name
    input_json = "./result/{model_name}/gpt4eval/gpt4_correct_report_*.json".format_map(dict(model_name=model_name))

    subject_class = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0,\
        7:0, 8:0, 9:0, 10:0, 11:0, 12:0, "UnKnown":0}
    # subject_right = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0,\
    #     "7":0, "8":0, "9":0, "10":0, "11":0, "12":0, "UnKnown":0}  
    subject_right = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0,\
        7:0, 8:0, 9:0, 10:0, 11:0, 12:0, "UnKnown":0}
    
    def read_json(file_path):
        file_paths = glob.glob(input_json)
        # import pdb; pdb.set_trace()
        all_data = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data.extend(data)
            except FileNotFoundError:
                print(f"文件 '{file_path}' 不存在")
            except json.JSONDecodeError:
                print(f"无法解析文件 '{file_path}' 中的 JSON 数据")
        return all_data

    correct_data = read_json(input_json)
    for item in correct_data:
        grade_num = item["grade_id"]
        if grade_num in subject_class.keys():
            subject_class[grade_num] += 1
        else:
            subject_class["UnKnown"] += 1

    for item in correct_data:
        grade_num = item["grade_id"]
        if (grade_num in subject_right.keys()) and (item["output_correct"]=="Yes"):
            subject_right[grade_num] += 1

    category_scores = {category: round((subject_right[category]/(count+1))*100,1) for category, count in subject_class.items()}
    total_score = round(sum(subject_right.values())/sum(subject_class.values())*100, 1)

    with open("./result/{model_name}/report_grade.txt".format_map(dict(model_name=model_name)), 'w') as file:
        file.write("各个年级的分数：\n")
        for category, score in category_scores.items():
            file.write(f"{category}: {score}\n")
        file.write(f"\n总的分数: {total_score}\n")
    return 

def statics_question_type_function(args):
    model_name = args.model_name
    input_json = "./result/{model_name}/gpt4eval/gpt4_correct_report_*.json".format_map(dict(model_name=model_name))

    subject_class = {"choice": 0, "free_form": 0, "single_choice":0, "multi_choice":0, "UnKnown": 0}
    subject_right = {"choice": 0, "free_form": 0, "single_choice":0, "multi_choice":0, "UnKnown": 0}
    def read_json(file_path):
        file_paths = glob.glob(input_json)
        # import pdb; pdb.set_trace()
        all_data = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data.extend(data)
            except FileNotFoundError:
                print(f"文件 '{file_path}' 不存在")
            except json.JSONDecodeError:
                print(f"无法解析文件 '{file_path}' 中的 JSON 数据")
        return all_data


    correct_data = read_json(input_json)

    for item in correct_data:
        q_type = item["answer_type"]
        # import pdb; pdb.set_trace()
        if q_type == "choice" and check_string(item["answer"])=="single":
            q_type = "single_choice"
        elif q_type == "choice" and check_string(item["answer"])!="single":
            q_type = "multi_choice"
        if q_type in subject_class.keys():
            subject_class[q_type] += 1
        else:
            # import pdb; pdb.set_trace()
            subject_class["UnKnown"] += 1

    # print(subject_class
    for item in correct_data:
        q_type = item["answer_type"]
        if q_type == "choice" and check_string(item["answer"])=="single":
            q_type = "single_choice"
        elif q_type == "choice" and check_string(item["answer"])!="single":
            q_type = "multi_choice"
        if (q_type in subject_right.keys()) and (item["output_correct"]=="Yes"): 
            subject_right[q_type] += 1

    # print(subject_right)
    # import pdb; pdb.set_trace()
    category_scores = {category: round((subject_right[category]/(count+1))*100,1) for category, count in subject_class.items()}

    # 计算总的分数
    total_score = round(sum(subject_right.values())/sum(subject_class.values())*100, 1)

    with open("./result/{model_name}/report_question_type.txt".format_map(dict(model_name=model_name)), 'w') as file:
        file.write("各个类别的分数：\n")
        for category, score in category_scores.items():
            file.write(f"{category}: {score}\n")
        file.write(f"\n总的分数: {total_score}\n")
    return 

def statics_knowledge_complete_rate(args):
    model_name = args.model_name
    input_json = "./result/{model_name}/gpt4eval/gpt4_correct_report_*.json".format_map(dict(model_name=model_name))
    def read_json(file_path):
        file_paths = glob.glob(input_json)
        # import pdb; pdb.set_trace()
        all_data = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data.extend(data)
            except FileNotFoundError:
                print(f"文件 '{file_path}' 不存在")
            except json.JSONDecodeError:
                print(f"无法解析文件 '{file_path}' 中的 JSON 数据")
        return all_data

    correct_data = read_json(input_json)
    # extract_innermost_knowledge()
    kn_dict = {}
    for item in correct_data:
        if item["knowledge_point"]==None:
            continue
        try:
            kn_point = extract_innermost_parent_parent_knowledge(item["knowledge_point"])
            if kn_point not in kn_dict:
                kn_dict[kn_point] = 1
            else:       
                kn_dict[kn_point] += 1
        except:
            pass
    
    # import pdb; pdb.set_trace()
    kn_complete_rate = {}
    for item in correct_data:
        if item["knowledge_point"]==None:
            continue
        try:
            # import pdb; pdb.set_trace()
            kn_point = extract_innermost_parent_parent_knowledge(item["knowledge_point"])
            if kn_point not in kn_complete_rate:
                kn_complete_rate[kn_point] = 0
        except:
            pass
        
    # import pdb; pdb.set_trace()
    for item in correct_data:
       if item["knowledge_point"]==None:
           continue
       try:
           # import pdb; pdb.set_trace()
           kn_point = extract_innermost_parent_parent_knowledge(item["knowledge_point"])
           if (kn_point in kn_dict.keys()) and (item["output_correct"]=="Yes"):
                kn_complete_rate[kn_point] += 1
       except:
           pass
    
    kn_complete_rate = {kn:kn_complete_rate[kn]/(kn_dict[kn]+1) for kn in kn_complete_rate.keys()}
    # knowledge_scores = {category: round((subject_right[category]/(count+1))*100,1) for category, count in subject_class.items()}
    # total_score = round(sum(subject_right.values())/sum(subject_class.values())*100, 1)
    # import pdb; pdb.set_trace()
    def count_values_above_half(my_dict, threahold=0):
        return sum(value > threahold for value in my_dict.values())
    
    complete_rate_dict  = {0:None, 0.1:None, 0.2:None, 0.3:None, 0.4:None, 0.5:None, 0.6:None, 0.7:None, 0.8:None}
    for rate in complete_rate_dict.keys():
        complete_rate_dict[rate] = count_values_above_half(kn_complete_rate, rate)
        
    with open("./result/{model_name}/report_skill_complete_rate.txt".format_map(dict(model_name=model_name)), 'w') as file:
        file.write("各个年级的分数：\n")
        for rate_category, score in complete_rate_dict.items():
            file.write(f"{rate_category}: {score/len(kn_dict)}\n")
    return 

def count_length_intervals(lengths):
    intervals = {"0-30": 0, "30-60": 0, "60-90": 0, "90-120": 0, "120-150": 0, "150-180": 0, "180-210": 0, "210-240":0, ">240":0}
    
    for length in lengths:
        if length >= 0 and length <= 30:
            intervals["0-30"] += 1
        elif length > 30 and length <= 60:
            intervals["30-60"] += 1
        elif length > 60 and length <= 90:
            intervals["60-90"] += 1
        elif length > 90 and length <= 120:
            intervals["90-120"] += 1
        elif length > 120 and length <= 150:
            intervals["120-150"] += 1
        elif length > 150 and length <= 180:
            intervals["150-180"] += 1
        elif length > 180 and length <= 210:
            intervals["180-210"] += 1
        elif length > 210 and length <= 240:
            intervals["210-240"] += 1
        else:
            intervals[">240"] += 1
            
    return intervals

def statics_question_length_function(args):
    model_name = args.model_name
    input_json = "./result/{model_name}/gpt4eval/gpt4_correct_report_*.json".format_map(dict(model_name=model_name))
    
    def read_json(file_path):
        file_paths = glob.glob(input_json)
        # import pdb; pdb.set_trace()
        all_data = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data.extend(data)
            except FileNotFoundError:
                print(f"文件 '{file_path}' 不存在")
            except json.JSONDecodeError:
                print(f"无法解析文件 '{file_path}' 中的 JSON 数据")
        return all_data
        
    data_list = read_json(input_json)
    total_elements = len(data_list)
    question_len = []
    for item in data_list:
        len_cur = count_chinese_chars(item["question"])
        question_len.append(len_cur)
    subject_class = count_length_intervals(question_len)
    subject_right = {key:0 for key in subject_class.keys()}
    for item in data_list:
        question_len = count_chinese_chars(item["question"])
        if ((interval_map(question_len)) in subject_class.keys()) and (item["output_correct"]=="Yes"): 
            subject_right[interval_map(question_len)] += 1
        category_scores = {category: round((subject_right[category]/(count+1))*100,1) for category, count in subject_class.items()}

    # 计算总的分数
    total_score = round(sum(subject_right.values())/sum(subject_class.values())*100, 1)
    # import pdb; pdb.set_trace()
    with open("./result/{model_name}/report_question_length.txt".format_map(dict(model_name=model_name)), 'w') as file:
        file.write("各个类别的分数：\n")
        for category, score in category_scores.items():
            file.write(f"{category}: {score}\n")
        file.write(f"\n总的分数: {total_score}\n")

def statics_complex_type_function(args):
    model_name = args.model_name
    input_json = "./result/{model_name}/gpt4eval/gpt4_correct_report_*.json".format_map(dict(model_name=model_name))

    subject_class = {"Easy": 0, "Middle": 0, "Hard":0, "UnKnown": 0}
    subject_right = {"Easy": 0, "Middle": 0, "Hard":0, "UnKnown": 0}
    def read_json(file_path):
        file_paths = glob.glob(input_json)
        # import pdb; pdb.set_trace()
        all_data = []
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    all_data.extend(data)
            except FileNotFoundError:
                print(f"文件 '{file_path}' 不存在")
            except json.JSONDecodeError:
                print(f"无法解析文件 '{file_path}' 中的 JSON 数据")
        return all_data

    correct_data = read_json(input_json)
    c_type_data = read_json_cmmath("/mnt/pfs/jinfeng_team/MMGroup/lzz/code/CMMaTH/cmmath_v3_ocr_complex.json")
    c_map = {} # get map: id 2 c_type
    for data_item in c_type_data:
        # import pdb; pdb.set_trace()
        c_map[data_item["problem_id"]] = data_item["complex_type"]
    for item in correct_data:
        c_type = c_map[item["problem_id"]]
        # import pdb; pdb.set_trace()
        if c_type == "Easy":
            subject_class["Easy"] += 1
        elif c_type == "Middle":
            subject_class["Middle"] += 1
        elif c_type == "Hard":
            subject_class["Hard"] += 1
        else:
            # import pdb; pdb.set_trace()
            subject_class["UnKnown"] += 1
    # print(subject_class
    import pdb; pdb.set_trace()
    for item in correct_data:
        c_type = c_map[item["problem_id"]]
        if (c_type in subject_right.keys()) and ("Yes" in item["output_correct"]): 
            subject_right[c_type] += 1

    # print(subject_right)
    # import pdb; pdb.set_trace()
    category_scores = {category: round((subject_right[category]/(count+1))*100,1) for category, count in subject_class.items()}

    # 计算总的分数
    total_score = round(sum(subject_right.values())/sum(subject_class.values())*100, 1)

    with open("./result/{model_name}/report_ctype_type.txt".format_map(dict(model_name=model_name)), 'w') as file:
        file.write("各个类别的分数：\n")
        for category, score in category_scores.items():
            file.write(f"{category}: {score}\n")
        file.write(f"\n总的分数: {total_score}\n")
    return 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", default="llava_v15", type=str) # prompt_type
    args = parser.parse_args()
    statics_complex_type_function(args)