# CMMaTH: A Chinese Multi-modal Math Skill Evaluation Benchmark for Foundition Models
Code  and Data for paper: "CMMaTH: A Chinese Multi-modal Math Skill Evaluation Benchmark for
Foundation Models". 
To systematically evaluate the capability of multimodal large models in solving Chinese multimodal mathematical problems, we propose the CMMaTH Benchmark, contraining 23k multimodal K12 math related question, the largest Chinese multimodal mathematical problem benchmark to date. CMMaTH includes questions from elementary to high school levels, providing increased diversity in problem types, solution objectives, visual elements, detailed knowledge points, and standard solution annotations. We have constructed an open-source GradeGPT integrated with the CMMaTH dataset, facilitating stable, rapid, and cost-free model evaluation and iteration.

<div align=center>
	<img width="400" src="figures\lidar_cmmath_dataset.png">
</div>
<div align=center>
	Figure 1. Performance of LMMs/LLMs.
</div>

<div align=center>
	<img width="300" src="figures\kn_graph.png">
</div>
<div align=center>
	Figure 2. Overview of Knowledge Point Graph.
</div>

<div align=center>
	<img width="400" src="figures\ssr_rate.png">
</div>
<div align=center>
	Figure 3. SSR of LMMs/LLMs.
</div>

## Data Prepartion
When conducting an evaluation, the user needs to create a folder named model_name/eval under the result directory and place the eval_result.json file containing the model's output into the eval folder.
For Example, for LMM LLaVA-v1.5
```
result/
└── llava-v1.5/
    └── eval/
        └── eval_result.json
```
The file structure of eval_result.json is shown below.
```
    {
        "problem_id": "00014",
        "question": "如图，在矩形$$ABCD$$中，$$\\angle DBC=30{}^\\circ $$，$$DC=2$$，$$E$$为$$AD$$上一点，以点$$D$$为圆心，以$$DE$$为半径画弧，交$$BC$$于点$$F$$，若$$CF=CD$$，则图中的阴影部分面积为 $$\\underline{}$$ ．（结果保留$$ \\pi $$）\n",
        "image": [
            "00014_img.png"
        ],
        "is_multi_img": false,
        "answer": "$$4\\sqrt{3}-2- \\pi $$\n",
        "answer_type": "free_form",
        "grade_id": 9,
        "grade_group": 2,
        "knowledge_point": "圆(与圆有关的计算(弧长、扇形面积应用(与圆有关的不规则图形的周长与面积计算)))",
        "skill": "运算能力",
        "analysis": ,
        "metadata": {
            "multimodal-category": "Plane Geometry",
            "img_info": [
                {
                    "height": "123",
                    "width": "194"
                }
            ]
        },
        "model_response": "解：如图，连接$DF$，∵$∠D=\\frac{1}{2}∠C=15^{\\circ}$，$CD=2$，$CF=CD$，∴$DF=DC+CF=4$，$S_{\\bigtriangleup CDF}=\\frac{1}{2}×CD×DF=\\frac{1}{2}×2×4=4$，∴阴影部分的面积$S=\\frac{1}{2}S_{矩形ABCD}=8$．故选：$B$．",
    }
]
```
## GradeGPT 
To quickly perform model evaluation, we can run the shell script: `bash sh_files/gradegpt_compare_result.sh`. In that script, specify `GRADEGPT_WEIGHT` as the path to the trained GradeGPT model.

The complete data for GradeGPT training and the model weights will be released after the review process is completed.
```
bash sh_files/gradegpt_compare_result.sh
```

For all models, you can run the following command: gpt4_result_correct.sh.
```
bash sh_files/model_result_correct.sh
```

## Detailed Analysis tools
We also provide various program tools for fine-grained category analysis. You can run the following command to perform fine-grained analysis.
```
model_names=(
    "cogagent_18b"
    "baichuan2_13b"
    "qwen_14b"
    #"mathgpt"
    "gpt4v"
    "yi_vl_34b"
    "intern_vl_xcomposer"
    "qwen_14b"
    "MetaMath-70B-V1.0"
    "deepseek-math-7b-instruct"
    "llama2_70b"
)

for model_name in "${model_names[@]}"; do
    python3 tools/statics_acc.py --model_name "$model_name" --eval_mode visual_subject
    echo "Current Model Name: $model_name"
done
```

## Dataset Explanation
To facilitate the reviewers' understanding, we have released part of the CMMaTH dataset `./cmmath.json` and part of the instruction data `./instruction_cross_lingual_finetune.json` for GradeGPT.
After the review process is completed, we will open source all the instruction data and the complete dataset.