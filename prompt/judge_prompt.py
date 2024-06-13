judge_prompt = """
你是一个答案判断助手，根据下列题目和参考答案判断某个模型输出是否是同一答案。判断时请按照以下格式给出详细的分析过程。
注意, 对于多选题目, 只有输出所有的对应的选项时候才算正确.(例如:参考答案为: A\nC\n时, 模型响应: C\n的答案一致性为: No)
注意, 如果模型响应未给出具体的选项，无法确定其正确性, 则输出答案一致性为: No。

题目是: 如下数表是由从$$1$$开始的连续自然数组成的，则第$$10$$行各数之和为 $$\\underline{}$$ ．. 
参考答案: 1729.
模型响应: 根据对于图像的观察可以得到, $$10$$行各数之和为1600.
判断结果: 参考答案1729是一个数值型答案，模型响应相应中给出的输出是1600。答案一致性是: No

题目是: 下列图形中，对称轴的条数最少的图形是 $$\\underline{}$$ （只填序号）．\n ．. 
参考答案: ②
模型响应: 首先观察图形1，它是一个椭圆形，有一个对称轴，即通过椭圆的长轴的直线。 <STEP1>\n然后观察图形2，它是由两个三角形组成的图形，有两个对称轴，即通过每个三角形的高的直线。 <STEP2>\n接着观察图形3，它是一个正方形对角线相交形成的图形，有四个对称轴，即每条对角线和每条边的中垂线。 <STEP3>\n最后观察图形4，它是一个由四个半圆组成的图形，有两个对称轴，即通过每对相对的半圆中心的直线。 <STEP4>\n比较所有图形的对称轴数量，图形1的对称轴数量最少，只有一个。 <STEP5>\n所以最终的答案为图形1的序号，即1。 <STEP6>.
判断结果: 参考答案②是一个数值型答案，模型响应中给出的输出是序号1。答案一致性是: No

题目是: 甲、乙两名同学在一次用频率去估计概率的实验中，绘出了某一结果出现的频率的折线图，则符合这一结果的实验可能是（   ）\n\nA.掷一枚正六面体的骰子，出现1点的概率\nB.抛一枚硬币，出现正面的概率\nC.任意写一个整数，它能被2整除的概率\nD.从一个装有2个白球和1个红球的袋子中任取一球，取到红球的概率\n
参考答案: D
模型响应: 求解步骤:\n首先，我们需要理解频率与概率的关系。频率是指在一系列重复实验中，某个结果出现的次数与总实验次数的比值。当实验次数足够多时，频率可以作为概率的估计。 <STEP1>\n\n接着，我们观察折线图。图中显示的频率在20%到40%之间波动。 <STEP2>\n\n现在我们分析每个选项:\nA.掷一枚正六面体的骰子，出现1点的概率是1/6，约等于16.67%，这个值低于图中的频率波动范围。 <STEP3>\nB.抛一枚硬币，出现正面的概率是1/2，即50%，这个值高于图中的频率波动范围。 <STEP4>\nC.任意写一个整数，它能被2整除的概率是1/2，即50%，这个值同样高于图中的频率波动范围。 <STEP5>\nD.从一个装有2个白球和1个红球的袋子中任取一球，取到红球的概率是1/3，约等于33.33%，这个值在图中的频率波动范围内。 <STEP6>\n\n综上所述，只有选项D的概率与图中的频率波动范围相匹配。 <STEP7>\n\n所以最终的答案为B. <STEP8>
判断结果: 参考答案是一个选项型答案, 模型响应中给出的输出是B, 答案一致性是: No
"""


cross_lingual_judge_prompt = """
You are an answer evaluation assistant. Based on the following questions and reference answers, determine if the model's output is the same answer. When making the determination, please provide the analysis process in the following format.
Note, for multiple-choice questions, it is only correct if the output includes all the corresponding options. (For example: If the reference answer is: A\nC\n, and the model response is: C\n, the answer consistency is: No)
Note, if the model response does not specify a particular option, and its correctness cannot be determined, the answer consistency should be: No.

Chinese Problem: 如下数表是由从$$1$$开始的连续自然数组成的，则第$$10$$行各数之和为 $$\\underline{}$$ ．. 
Reference Answer: 1729.
Model Response: 根据对于图像的观察可以得到, $$10$$行各数之和为1600.
Judge Result: First, understand the question in Chinese. The Chinese model response means:
According to the observation of the image, the sum of the numbers in each of the 10 lines is 1600.
Next, let’s analyze whether the correct answer has been given.
The reference answer 1729 is a numerical answer, and the output given in the model response is 1600. The consistency of the answers is: No.

Chinese Problem: 下列图形中，对称轴的条数最少的图形是 $$\\underline{}$$ （只填序号）．\n ．. 
Reference Answer: ②
Model Response: 首先观察图形1，它是一个椭圆形，有一个对称轴，即通过椭圆的长轴的直线。 <STEP1>\n然后观察图形2，它是由两个三角形组成的图形，有两个对称轴，即通过每个三角形的高的直线。 <STEP2>\n接着观察图形3，它是一个正方形对角线相交形成的图形，有四个对称轴，即每条对角线和每条边的中垂线。 <STEP3>\n最后观察图形4，它是一个由四个半圆组成的图形，有两个对称轴，即通过每对相对的半圆中心的直线。 <STEP4>\n比较所有图形的对称轴数量，图形1的对称轴数量最少，只有一个。 <STEP5>\n所以最终的答案为图形1的序号，即1。 <STEP6>.
Judge Result: First, understand the question in Chinese. The Chinese model response means: 
First, observe Figure 1, which is an oval with one axis of symmetry, which is the line passing through the major axis of the ellipse. Then, observe Figure 2, which is a shape composed of two triangles and has two axes of symmetry, which are the lines passing through the heights of each triangle. Next, observe Figure 3, which is a shape formed by the intersection of the diagonals of a square and has four axes of symmetry, which are the lines along each diagonal and the perpendicular bisectors of each side. Finally, observe Figure 4, which is a shape made up of four semicircles and has two axes of symmetry, which are the lines passing through the centers of each pair of opposite semicircles. Comparing the number of axes of symmetry of all the figures, Figure 1 has the fewest, with only one. Therefore, the final answer is the number of Figure 1, which is 1. 
Next, let’s analyze whether the correct answer has been given.
The reference answer ② is a numerical answer, and the output given in the model response is the serial number 1. The consistency of the answers is: No.

Chinese Problem: 甲、乙两名同学在一次用频率去估计概率的实验中，绘出了某一结果出现的频率的折线图，则符合这一结果的实验可能是（   ）\n\nA.掷一枚正六面体的骰子，出现1点的概率\nB.抛一枚硬币，出现正面的概率\nC.任意写一个整数，它能被2整除的概率\nD.从一个装有2个白球和1个红球的袋子中任取一球，取到红球的概率\n
Reference Answer: D
Model Response: 求解步骤:\n首先，我们需要理解频率与概率的关系。频率是指在一系列重复实验中，某个结果出现的次数与总实验次数的比值。当实验次数足够多时，频率可以作为概率的估计。 <STEP1>\n\n接着，我们观察折线图。图中显示的频率在20%到40%之间波动。 <STEP2>\n\n现在我们分析每个选项:\nA.掷一枚正六面体的骰子，出现1点的概率是1/6，约等于16.67%，这个值低于图中的频率波动范围。 <STEP3>\nB.抛一枚硬币，出现正面的概率是1/2，即50%，这个值高于图中的频率波动范围。 <STEP4>\nC.任意写一个整数，它能被2整除的概率是1/2，即50%，这个值同样高于图中的频率波动范围。 <STEP5>\nD.从一个装有2个白球和1个红球的袋子中任取一球，取到红球的概率是1/3，约等于33.33%，这个值在图中的频率波动范围内。 <STEP6>\n\n综上所述，只有选项D的概率与图中的频率波动范围相匹配。 <STEP7>\n\n所以最终的答案为B. <STEP8>
Judge Result: First, understand the question in Chinese. The Chinese model response means: 
Firstly, we need to understand the relationship between frequency and probability. Frequency refers to the ratio of the number of times a certain result appears in a series of repeated experiments to the total number of experiments. When the number of experiments is sufficiently large, frequency can be used as an estimate of probability.
Next, we observe the line graph. The frequency shown in the graph fluctuates between 20% and 40%.
Now let’s analyze each option:
A. The probability of rolling a 1 on a fair six-sided die is 1/6, which is approximately 16.67%, and this value is lower than the range of frequency fluctuations in the graph.
B. The probability of getting heads when flipping a coin is 1/2, which is 50%, and this value is higher than the range of frequency fluctuations in the graph.
C. The probability of writing an integer that is divisible by 2 is 1/2, which is 50%, and this value is also higher than the range of frequency fluctuations in the graph.
D. The probability of drawing a red ball from a bag containing 2 white balls and 1 red ball is 1/3, which is approximately 33.33%, and this value falls within the range of frequency fluctuations in the graph.
In summary, only the probability of option D matches the range of frequency fluctuations in the graph.
Therefore, the final answer is B.

Next, let’s analyze whether the correct answer has been given.
The reference answer is an option-based answer, and the output given in the model response is B. The consistency of the answers is: No.
"""

englist_judge_prompt = """
You are an answer evaluation assistant. Based on the following questions and reference answers, determine if the model's output is the same answer. When making the determination, please provide the analysis process in the following format.
Note, for multiple-choice questions, it is only correct if the output includes all the corresponding options. (For example: If the reference answer is: A\nC\n, and the model response is: C\n, the answer consistency is: No)
Note, if the model response does not specify a particular option, and its correctness cannot be determined, the answer consistency should be: No.

Question: Among the following figures, the one with the fewest axes of symmetry is ___?.
Reference Answer: ②
Model Response: First, observe figure 1, which is an ellipse with one axis of symmetry, namely the line through the major axis of the ellipse. <STEP1>\nThen observe figure 2, which is a figure composed of two triangles, with two axes of symmetry, namely the lines through the heights of each triangle. <STEP2>\nNext, observe figure 3, which is a figure formed by the intersection of the diagonals of a square, with four axes of symmetry, namely each diagonal and the perpendicular bisectors of each side. <STEP3>\nFinally, observe figure 4, which is a figure composed of four semicircles, with two axes of symmetry, namely the lines through the centers of each pair of opposite semicircles. <STEP4>\nComparing the number of axes of symmetry of all figures, figure 1 has the fewest axes of symmetry, only one. <STEP5>\nTherefore, the final answer is the number of figure 1, which is 1. <STEP6>.
Judgment Result: The reference answer ② is a numerical answer, and the model response given is the number 1. The answer consistency is: No

Question: Students A and B conducted an experiment to estimate probability using frequency, and plotted the frequency of a certain result as a line chart. The experiment that matches this result is ( )
A. Rolling a fair six-sided die, the probability of getting a 1
B. Tossing a coin, the probability of getting heads
C. Writing any integer, the probability that it is divisible by 2
D. Drawing a ball from a bag containing 2 white balls and 1 red ball, the probability of drawing a red ball
Reference Answer: D
Model Response: Solution steps:\nFirst, we need to understand the relationship between frequency and probability. Frequency refers to the ratio of the number of times a certain result occurs to the total number of experiments in a series of repeated experiments. When the number of experiments is sufficiently large, frequency can be used as an estimate of probability. <STEP1>\n\nNext, we observe the line chart. The frequency shown in the chart fluctuates between 20% and 40%. <STEP2>\n\nNow we analyze each option:\nA. Rolling a fair six-sided die, the probability of getting a 1 is 1/6, approximately 16.67%, which is below the fluctuation range shown in the chart. <STEP3>\nB. Tossing a coin, the probability of getting heads is 1/2, which is 50%, higher than the fluctuation range shown in the chart. <STEP4>\nC. Writing any integer, the probability that it is divisible by 2 is 1/2, which is 50%, also higher than the fluctuation range shown in the chart. <STEP5>\nD. Drawing a ball from a bag containing 2 white balls and 1 red ball, the probability of drawing a red ball is 1/3, approximately 33.33%, within the fluctuation range shown in the chart. <STEP6>\n\nIn summary, only option D's probability matches the fluctuation range shown in the chart. <STEP7>\n\nTherefore, the final answer is B. <STEP8>
Judgment Result: The reference answer is an option-based answer, and the output given in the model response is B. The consistency of the answers is: No.
"""

cross_lingual_templete = """
Question: {problem}
Reference Answer: {answer}
Model Response: {model_response}
Judgment Result: 
"""

test_judge_prompt = """
你是一个答案判断助手，根据下列题目和参考答案判断某个模型输出是否是同一答案。判断时请按照以下格式给出分析过程
"""

english_templete_prompt = """
Question: {problem}
Reference Answer:{answer}
Model Response: {model_response}
Judgment Result:
"""

templete_prompt = """
题目是: {problem}
参考答案: {answer}
模型响应: {model_response}
判断结果:
"""

simple_judge_prompt = """
你是一个答案判断助手，根据下列题目和参考答案判断某个模型输出是否是同一答案。判断时请按照以下格式给出分析过程。
注意, 对于多选题目, 只有输出所有的对应的选项时候才算正确.(例如:参考答案为: A\nC\n时, 模型响应: C\n的答案一致性为: No)
注意, 如果模型响应未给出具体的选项，无法确定其正确性, 则输出答案一致性为: No。
"""

simple_templete_prompt = """
参考答案: {answer}
模型响应: {model_response}
判断结果:
"""

cross_lingual_judge_prompt = """
You are an answer evaluation assistant. Based on the following questions and reference answers, determine if the model's output is the same answer. When making the determination, please provide the analysis process in the following format.
Note, for multiple-choice questions, it is only correct if the output includes all the corresponding options. (For example: If the reference answer is: A\nC\n, and the model response is: C\n, the answer consistency is: No)
Note, if the model response does not specify a particular option, and its correctness cannot be determined, the answer consistency should be: No.

Chinese Problem: 如图所示，$$AD$$是$$\\bigtriangleup ABC$$的中线，点$$E$$在$$AC$$上，$$BE$$交$$AD$$于点$$F$$．当$$\\frac{AF}{FD}=\\frac{1}{2}$$时，$$\\frac{AE}{AC}= \\underline{}$$ 
Reference Answer: $$\\frac{1}{5}$$
Model Response: 首先，我们需要找到中线AD，然后找到点E在AC上的位置。\n\n找到中线AD，可以通过勾股定理求解，AD^2 = AD \\* AC^2。\n\n设AD = x，AC = y，则有 x^2 = x \\* y^2。\n\n解这个方程，我们得到 y = √x。\n\n现在我们知道点E在AC上，所以E的横坐标为y，纵坐标为x。\n\n接下来，我们需要找到点F在BD上的位置。\n\n由于F点在BD上，我们可以设F点在BD的一半，即F = (x + y) / 2。\n\n现在我们可以计算AF和FD的长度。\n\nAF = x - F\n\nFD = FD - F\n\n将已知的x和y代入公式，得到：\n\nAF = x - (x + y) / 2\n\nFD = (x + y) / 2 - (x + y) / 2\n\n简化得到：\n\nAF = x - x\n\nFD = x - x\n\n这意味着AF = FD。\n\n现在我们可以求解题目中的条件：\n\nAE / AC = 1 / 2\n\n将已知的AF和FD代入公式，得到：\n\nAE / AC = (x - x) / (√x \\* y)\n\n化简得到：\n\nAE / AC = 1 / 2\n\n所以，答案为AE / AC = 1 / 2。
Judge Result: The relevant paragraph in the Model Response that provides the answer is 
所以，答案为AE / AC = 1 / 2
Understand the question in Chinese. The Chinese model response means:
Therefore, the answer is AE / AC = 1 / 2.
Next, let’s analyze whether the correct answer has been given.
The reference answer $$\\frac{1}{5}$$ is a numerical answer, and the output given in the model response is 1/2. The consistency of the answers is: No.

Chinese Problem: 下列图形中，对称轴的条数最少的图形是 $$\\underline{}$$ （只填序号）．\n ．. 
Reference Answer: ②
Model Response: 首先观察图形1，它是一个椭圆形，有一个对称轴，即通过椭圆的长轴的直线。 <STEP1>\n然后观察图形2，它是由两个三角形组成的图形，有两个对称轴，即通过每个三角形的高的直线。 <STEP2>\n接着观察图形3，它是一个正方形对角线相交形成的图形，有四个对称轴，即每条对角线和每条边的中垂线。 <STEP3>\n最后观察图形4，它是一个由四个半圆组成的图形，有两个对称轴，即通过每对相对的半圆中心的直线。 <STEP4>\n比较所有图形的对称轴数量，图形1的对称轴数量最少，只有一个。 <STEP5>\n所以最终的答案为图形1的序号，即1。 <STEP6>.
Judge Result: The relevant paragraph in the Model Response that provides the answer is 
所以最终的答案为图形1的序号，即1。
Understand the question in Chinese. The Chinese model response means:
Therefore, the final answer is the number of Figure 1, which is 1.
Next, let’s analyze whether the correct answer has been given.
The reference answer ② is a option-based answer, and the output given in the model response is 1. The consistency of the answers is: No.

Chinese Problem: 甲、乙两名同学在一次用频率去估计概率的实验中，绘出了某一结果出现的频率的折线图，则符合这一结果的实验可能是（   ）\n\nA.掷一枚正六面体的骰子，出现1点的概率\nB.抛一枚硬币，出现正面的概率\nC.任意写一个整数，它能被2整除的概率\nD.从一个装有2个白球和1个红球的袋子中任取一球，取到红球的概率\n
Reference Answer: D
Model Response: 求解步骤:\n首先，我们需要理解频率与概率的关系。频率是指在一系列重复实验中，某个结果出现的次数与总实验次数的比值。当实验次数足够多时，频率可以作为概率的估计。 <STEP1>\n\n接着，我们观察折线图。图中显示的频率在20%到40%之间波动。 <STEP2>\n\n现在我们分析每个选项:\nA.掷一枚正六面体的骰子，出现1点的概率是1/6，约等于16.67%，这个值低于图中的频率波动范围。 <STEP3>\nB.抛一枚硬币，出现正面的概率是1/2，即50%，这个值高于图中的频率波动范围。 <STEP4>\nC.任意写一个整数，它能被2整除的概率是1/2，即50%，这个值同样高于图中的频率波动范围。 <STEP5>\nD.从一个装有2个白球和1个红球的袋子中任取一球，取到红球的概率是1/3，约等于33.33%，这个值在图中的频率波动范围内。 <STEP6>\n\n综上所述，只有选项D的概率与图中的频率波动范围相匹配。 <STEP7>\n\n所以最终的答案为B. <STEP8>
Judge Result: The relevant paragraph in the Model Response that provides the answer is 
所以最终的答案为B.
Understand the question in Chinese. The Chinese model response means:
Therefore, the final answer is B.
Next, let’s analyze whether the correct answer has been given.
The reference answer D is a option-based answer, and the output given in the model response is B. The consistency of the answers is: No.
"""
# /mnt/pfs/jinfeng_team/MMGroup/lzz/code/GradeGPT_A/sft_output/output_0515_2010/checkpoint-50