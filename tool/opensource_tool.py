import torch
from tqdm import tqdm
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

import time
from api_tool import get_chat_vllm_response
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig, GenerationConfig
from argparse import ArgumentParser
import os
from typing import Tuple
from vllm import LLM, SamplingParams

import sys
sys.path.append("../")
from tool.qwen_generation_utils import make_context, decode_tokens, get_stop_words_ids
from prompt.judge_prompt import agent_judge_prompt

import os
import io
import regex
import pickle
import traceback
import copy
import datetime
import dateutil.relativedelta
import multiprocess
from multiprocess import Pool
from typing import Any, Dict, Optional
from pebble import ProcessPool
from tqdm import tqdm
from concurrent.futures import TimeoutError
from functools import partial
from timeout_decorator import timeout
from contextlib import redirect_stdout
from executor import PythonExecutor

from transformers.generation.stopping_criteria import StoppingCriteria, StoppingCriteriaList, \
    STOPPING_CRITERIA_INPUTS_DOCSTRING, add_start_docstrings
    
class AgentStopCriteria(StoppingCriteria):
    def __init__(self, token_id_list=None):
        """
        :param token_id_list: 停止生成的指定token的id的列表
        """
        self.token_id_list = token_id_list# [13874, 3989, 32804, 75117, 59151, 17714]
        
    @add_start_docstrings(STOPPING_CRITERIA_INPUTS_DOCSTRING)
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        # return np.argmax(scores[-1].detach().cpu().numpy()) in self.token_id_list
        # 储存scores会额外占用资源，所以直接用input_ids进行判断
        return input_ids[0][-1].detach().cpu().numpy() in self.token_id_list

def extract_program(result: str, last_only=True):
    """
    extract the program after "```python", and before "```"
    """
    program = ""
    start = False
    for line in result.split("\n"):
        if line.startswith("```python"):
            if last_only:
                program = "" # only extract the last program
            else:
                program += "\n# ========\n"
            start = True
        elif line.startswith("```"):
            start = False
        elif start:
            program += line + "\n"
    return program

def create_model_tokenizer(args: ArgumentParser, from_local: bool=True) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
    if from_local:
        assert os.path.exists(args.weight_path), f"cannot find weight path: {args.weight_path}"
        model = AutoModelForCausalLM.from_pretrained(
            args.weight_path, pad_token_id=tokenizer.pad_token_id, device_map="auto", trust_remote_code=True).to(device)
        model.generation_config = GenerationConfig.from_pretrained(args.weight_path, pad_token_id=tokenizer.pad_token_id)
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=args.weight_path, pad_token='<|extra_0|>', eos_token='<|endoftext|>',
                                                  padding_side='left', trust_remote_code=True).to(device)
        config = AutoConfig.from_pretrained(pretrained_model_name_or_path=args.weight_path, trust_remote_code=True)
        
    else:      
        model = AutoModelForCausalLM.from_pretrained(
            args.model_name,  device_map="auto", token="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"
        )
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained(args.model_name, token="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")
        config = AutoConfig.from_pretrained(args.model_name)
        
    return model, tokenizer, config

def get_opensource_llm_reponse(compare_prompt, model, tokenizer):
    model.to(device)
    inputs_test = tokenizer(compare_prompt, return_tensors="pt").to(model.device)
    inputs = inputs_test["input_ids"].to(model.device)
    pred = model.generate(inputs,
                    max_length=1024,
                    do_sample=True,
                    top_k=50,
                    top_p=0.1,
                    num_return_sequences=1,
                    pad_token_id=tokenizer.eos_token_id)
    return_text = tokenizer.decode(pred.cpu()[0], skip_special_tokens=True)[len(inputs[0]):]
    return return_text

def get_opensource_llm_reponse_batch(all_raw_texts, model, tokenizer):
    # import pdb; pdb.set_trace()
    batch_raw_text = []
    for q in all_raw_texts:
        raw_text, _ = make_context(
            tokenizer,
            q,
            system="You are a helpful assistant.",
            max_window_size=6144, # model.generation_config.max_window_size,
            chat_format="chatml",
        )
        batch_raw_text.append(raw_text)

    # stop_token = "```output"
    # stop_token_id = tokenizer.encode(stop_token)[0] # for debug
    # stopping_criteria = StoppingCriteriaList()
    # stopping_criteria.append(AgentStopCriteria([32804, 75117, 59151, 17714]))

    batch_input_ids = tokenizer(batch_raw_text, padding='longest')
    batch_input_ids = torch.LongTensor(batch_input_ids['input_ids']).to(model.device)
    batch_out_ids = model.generate(
        batch_input_ids,
        return_dict_in_generate=False,
        generation_config=model.generation_config,
        repetition_penalty=1.0
        #stopping_criteria=stopping_criteria
    )
    padding_lens = [batch_input_ids[i].eq(tokenizer.pad_token_id).sum().item() for i in range(batch_input_ids.size(0))]

    batch_response = [
        decode_tokens(
            batch_out_ids[i][padding_lens[i]:],
            tokenizer,
            raw_text_len=len(batch_raw_text[i]),
            context_length=(batch_input_ids[i].size(0)-padding_lens[i]),
            chat_format="chatml",
            verbose=False,
            errors='replace'
        ) for i in range(len(all_raw_texts))
    ]
    return batch_response

def get_opensource_llm_agent_reponse_batch(args, response_parts, all_raw_texts, model, tokenizer):
    ## implement agent_inference
    executor = PythonExecutor(get_answer_from_stdout=True)
    samples = all_raw_texts
    init_samples = response_parts
    remain_prompts = [sample for sample in samples for _ in range(args.n_sampling)]
    remain_prompts = [(i, prompt) for i, prompt in enumerate(remain_prompts)]
    end_prompts = []
    
    max_func_call = 5
    # measure time use
    start_time = time.time()
    for epoch in range(max_func_call):
        print("=" * 50, "Epoch", epoch)
        current_prompts = remain_prompts
        if len(current_prompts) == 0:
            break
        prompts = [item[1] for item in current_prompts]
        outputs = get_opensource_llm_reponse_batch(prompts, model, tokenizer)
        # process all outputs
        remain_prompts = []
        remain_codes = []
        out_inputs = []
        # stop_tokens = ["</s>", "```\n函数执行结果为:"]
        for (i, query), output, init_sample in zip(current_prompts, outputs, init_samples):
            output = output.rstrip()
            query += output # 
            replace_newlines = lambda s: s.replace('\n', '\\n')
            # if (("Yes" not in output) and ("No" not in output) and output.endswith("```")): # end with code but there no final answer
            if (("Yes" not in output) and ("No" not in output) and output.endswith("```")): # 在推理时候额外的有的
                program = extract_program(query) # get the latested program
                # import pdb; pdb.set_trace()
                out_inputs.append('''model_response="{}"'''.format(replace_newlines(init_sample[0])))
                # program = "model_response=\"{}\"\n".format(init_sample) + program # query 
                remain_prompts.append((i, query))
                remain_codes.append(program) # get the latested program
            elif (("Yes" not in output) and ("No" not in output)): # end condtion box in output.give defined result
                remain_prompts.append((i, query))
            else:
                end_prompts.append((i, query)) 
        # execute the remain prompts
        # import pdb; pdb.set_trace()
        # remain_codes = executor.process_generation_to_code(remain_codes)
        remain_results = executor.batch_apply(remain_codes, out_inputs)
        
        for k in range(len(remain_prompts)): # concat the execute result into prompt
            i, query = remain_prompts[k]
            try:
                res, report = remain_results[k]
                exec_result = res if res else report
            
                exec_result = f"\n```函数执行结果为: {exec_result}\n"
                query += exec_result
            except:
                pass
            # not end
            if epoch == max_func_call - 1:
                query += "\nReach max function call limit."
            remain_prompts[k] = (i, query)
        
    end_prompts.extend(remain_prompts)
    # sort by idx
    end_prompts = sorted(end_prompts, key=lambda x: x[0])
    output_judge = []
    for end_response in end_prompts:
        output_judge.append(end_response[1].replace(agent_judge_prompt, ""))
    return output_judge

def get_opensource_llm_reponse_batch_vllm(args, vllm_model, all_raw_texts): # Self-General
    sampling_params = SamplingParams(temperature=0.2,  max_tokens=2048)
    answer_result = get_chat_vllm_response(args, vllm_model, all_raw_texts, ocr_result=None, sampling_parameter=sampling_params) # list2list
    return answer_result
