# 对 `manuscript.tex` 的检查与修改建议

## 1. 已修复的 LaTeX 问题

我已直接修改 `E:/Downloads/manuscript.tex` 并新增必要文件，使其可以正常编译。

已修复内容：

1. 图片不显示  
   原文图片路径写成：
   `../nn_supply_chain_figures/figures/fig1_sample_facts.pdf`  
   从 `E:/Downloads` 编译时，LaTeX 实际查找的是 `E:/nn_supply_chain_figures/...`，路径不存在。  
   我已把 6 张图复制到：
   `E:/Downloads/ce_figures/`  
   并把所有 `\includegraphics` 改成：
   `ce_figures/fig1_sample_facts.pdf` 等相对路径。

2. 文中引用和参考文献显示 `?`  
   原因是缺少 `references.bib`，而文中使用了 `\bibliography{references}`。  
   我已新增：
   `E:/Downloads/references.bib`

3. 公式中的 `\bm` 报错  
   原因是导言区没有加载 `bm` 包。  
   我已加入：
   `\usepackage{bm}`

4. 编译验证  
   已运行：
   `pdflatex -> bibtex -> pdflatex -> pdflatex -> pdflatex`  
   当前 `E:/Downloads/manuscript.pdf` 已生成，图片正常显示，日志中没有 undefined citation/reference 和图片 not found。

需要注意：
`references.bib` 中部分条目，尤其 `original2024climate` 和中文神经网络稳定性论文，属于根据 PDF 内容和现有材料整理的编译版条目。投稿前必须核对正式卷期、页码、英文刊名和 DOI。

## 2. 最严重的内容问题：变量解释有硬伤

这是当前稿件最大风险，必须优先修改。

### 2.1 `Affected` 被解释错了

当前稿件多处把 `Affected` 写成：
`climate-finance exposure`，甚至解释为银行贷款暴露、银行对气候敏感行业的敞口。

但原始数据中 `Affected` 的变量标签是：
`上游焦点公司同时满足：(1)面临融资约束；(2)受到极端降水影响`

也就是说，`Affected` 不是银行气候金融敞口，而是上游焦点公司同时遭遇极端降水和融资约束的暴露变量。

建议统一改名为：

- `Affected upstream exposure`
- `Climate-constrained upstream exposure`
- `Exposure to climate-shocked and financially constrained upstream firms`

不要再使用 `climate-finance exposure`，除非重新证明它确实来自银行气候金融敞口。

需要修改位置：

- 摘要第 1 段中的 `climate-finance exposure`
- Introduction 中所有 `climate-finance exposure`
- Data section 的 `Climate and Exposure Variables`
- Table 1 feature labels
- Figure captions 1、5、6
- Risk surface discussion

### 2.2 `Climate_CityC` 解释不精确

当前稿件说它是 “normalized to empirical support”。原始变量标签是：
`客户所在城市极端降水`

它更像是客户所在城市的极端降水强度，通常是极端降水天数加 1 取对数。不要写成 normalize，除非代码中确实做了归一化。

建议改为：
`the log intensity of extreme precipitation in the customer's city`

### 2.3 `C_Frequency` 被误写成 stock trading frequency

当前 Table 1 写的是：
`Stock trading frequency`

但原始变量标签是：
`客户交易频次` 或 `季度平均交易次数`

这里应改成：
`Customer-supplier trading frequency`
或
`Relationship trading frequency`

这属于容易被审稿人抓住的低级变量解释错误。

### 2.4 被解释变量定义需要更诚实

当前写法：
`Ter_q_qh equals one if the customer-firm terminates at least one major supplier relationship`

但实际 `Ter_q_q1` 等变量不是简单 0/1，原始数据里有负值和正值。你构造的标签是：
`BreakRisk4Q = 1{Ter_q_q1 + Ter_q_q2 + Ter_q_q3 + Ter_q_q4 > 0}`

更准确的定义应是：

> The prediction target equals one if the net change in terminated focal-company relationships over the next four quarters is positive.

或者：

> We classify an observation as high-risk when the sum of the four forward termination measures is positive.

不要写成 “at least one relationship is terminated”，因为正负值可能抵消。

## 3. 结果解释是否合理

当前稿件最好的地方是没有夸大神经网络预测效果。这个方向是对的。

真实结果是：

- MLP AUC = 0.536
- Logit AUC = 0.544
- MLP AP = 0.598
- Holdout positive rate = 0.560
- MLP 并没有优于 logit

所以结论必须保持：

> The neural network is structurally stable but only weakly predictive.

可以保留的核心贡献：

1. 将神经网络参数稳定性框架用于供应链气候风险预测。
2. 用真实断链标签评估样本外预测能力。
3. 发现当前静态财务、治理、气候变量的预测信号有限。
4. 说明“模型稳定”和“预测准确”不是同一个概念。

不能写的结论：

- “Neural networks improve prediction of supply chain disruption risk.”
- “Climate exposure is a dominant predictor.”
- “The model provides actionable early-warning signals.”
- “The MLP captures mechanisms that linear models cannot capture.”

最后一句尤其要弱化。线性模型加上交互项和二次项也可以捕捉类似曲率。更稳妥写法：

> The baseline MLP reveals nonlinear patterns that are not represented in the simple logit benchmark unless comparable interaction or spline terms are added.

## 4. AI 味过浓的位置和改法

整体判断：目前稿件 AI 味比较明显，尤其在 Introduction、Discussion 和 Conclusion。问题不是英文不流畅，而是太“模板化”、太满、太像自动生成的综述。

高 AI 味短语包括：

- `has emerged as a central concern`
- `offers a natural framework`
- `addresses a gap in the literature`
- `we are the first to`
- `stability-first evaluation paradigm`
- `actionable information`
- `direct implications`
- `operational deployment`
- `high-heterogeneity economic environments`
- `structurally stable representation`

建议：

1. 删除或弱化自我评价词  
   把 `first`, `novel`, `validates`, `demonstrates`, `actionable` 改为更朴素的动词：  
   `apply`, `test`, `document`, `show`, `report`, `compare`。

2. Introduction 第一段不要泛泛谈气候变化  
   现在开头太像模板。建议直接开门见山：

   > Can a neural network forecast which supply-chain relationships break after climate shocks? In our Chinese listed-firm sample, the answer is only partly yes. A two-layer MLP is structurally stable across rolling samples, but its 2022--2023 holdout AUC is only 0.536, slightly below a logit benchmark.

3. Abstract 太长  
   当前 abstract 约 300+ 词，像一个压缩版全文。建议压到 180-220 词。Computational Economics 不需要在摘要中塞入所有窗口、所有变量、所有指标。

4. Conclusion 太长  
   当前 conclusion 约 1000 词，远超一般论文结论。建议压到 450-600 词，避免重复 Introduction 和 Results。

5. Literature Review 像“文献清单”  
   需要变成“缺口叙事”：  
   climate supply chain 文献说明风险存在；ML 文献说明预测可行；稳定性文献说明准确率之外还要看参数稳定；本文把三者连接起来。

## 5. 发表水平判断

当前稿件还没有达到 Computational Economics 的可投稿水平，但已经有一个可以发展的骨架。

### 当前优点

1. 主题适合 Computational Economics  
   期刊关注 computational methods、machine learning、economic applications。神经网络稳定性 + 气候供应链风险预测是合适方向。

2. 结果诚实  
   没有强行包装 MLP 优于 logit，这一点反而增加可信度。

3. 图表完整  
   ROC/PR、校准、残差、稳定性、变量重要性、风险曲面都有，已经像一个计算经济学实证框架。

4. 有可复现代码基础  
   这是机器学习类投稿的重要优势。

### 当前硬伤

1. 变量定义错位  
   `Affected`、`C_Frequency`、`Climate_CityC` 和目标变量解释必须修正。

2. 预测贡献偏弱  
   AUC 0.536 本身不足以支撑一篇“神经网络预测论文”。必须把论文定位为“可靠性/稳定性诊断框架”，而不是“高精度预测模型”。

3. 机器学习实验不够充分  
   只有 MLP 和 logit，不够 Computational Economics 审稿人的期待。

4. 稳定性框架还不够严谨  
   现在的稳定性检验只比较参数距离和随机种子扰动。还需要补充：
   - bootstrap confidence intervals for AUC
   - DeLong or bootstrap test comparing MLP and logit AUC
   - sensitivity to hidden layer size
   - sensitivity to target construction
   - alternative forecast horizons: q+1, q+2, q+3, q+4
   - calibration metrics by year

5. 缺少真正的供应链网络特征  
   如果目标是“供应链风险”，最好加入：
   - supplier/customer concentration
   - relationship duration history
   - lagged terminations
   - number of active suppliers/customers
   - province/industry exposure
   - network centrality
   - geographic dispersion

如果没有网络特征，审稿人可能会问：这到底是供应链预测，还是普通客户财务变量预测？

## 6. 建议的重大修改路线

### 第一优先级：修正变量定义

先统一术语：

- `Affected` -> exposure to climate-shocked and financially constrained upstream firms
- `S_FC` -> upstream supplier financing constraint
- `Affected_x_S_FC` -> interaction between affected upstream exposure and supplier financing constraint
- `Climate_CityC` -> customer-city extreme precipitation intensity
- `C_Frequency` -> relationship trading frequency
- `BreakRisk4Q` -> positive net forward termination risk

### 第二优先级：改写摘要

建议结构：

1. 一句话提出问题。
2. 一句话说明数据和标签。
3. 一句话报告 MLP 和 logit 的真实结果。
4. 一句话报告稳定性结果。
5. 一句话说明贡献是“稳定性诊断”，不是“预测优越性”。

### 第三优先级：重写 Introduction

建议 5 段：

1. 开门见山：神经网络能否预测气候冲击下断链风险？结果有限但稳定。
2. 数据和任务：A 股供应链、极端降水、融资约束、四季度断链标签。
3. 样本外结果：MLP AUC 0.536，logit 0.544，预测增益有限。
4. 稳定性结果：参数距离 0.337-0.490，低于 null threshold 1.534。
5. 贡献：把预测准确率和模型稳定性分开评估，为 climate-supply-chain ML 提供诊断框架。

### 第四优先级：增强实验

最少补充：

1. Random forest
2. Gradient boosting / XGBoost 或 HistGradientBoosting
3. SVM 或 regularized logit
4. MLP architecture sensitivity: `(8,)`, `(12,6)`, `(32,16)`, `(64,32)`
5. Bootstrap confidence intervals for AUC/AP/Brier
6. Ablation table:
   - finance only
   - climate only
   - supply-chain only
   - all features

如果这些结果依旧弱，也不要怕。论文可以更强地论证：

> supply-chain disruption risk is hard to predict from static observables, and model stability diagnostics prevent overclaiming in weak-signal environments.

### 第五优先级：删掉过强机制解释

比如风险曲面中这些解释要弱化：

- `screening or hedging effect`
- `mutual dependence`
- `direct implications for targeted risk assessment`

建议改成：

> These patterns are descriptive model-implied associations. They suggest possible heterogeneity in how financing constraints condition climate exposure, but they should not be interpreted as causal mechanisms.

## 7. 结论

这篇稿件目前是“有潜力但未达发表水平”。技术编译问题已经解决；真正需要大修的是变量定义、贡献定位和实验深度。

最稳妥的投稿定位不是：

> Neural networks predict supply-chain disruption better.

而是：

> Neural networks provide a structurally stable but only weakly discriminative diagnostic tool for climate-related supply-chain disruption risk; the weak predictive gain itself is informative about the limits of static firm-level observables in high-heterogeneity supply-chain environments.

这个定位更诚实，也更符合 Computational Economics 对计算方法可靠性和经济解释的期待。
