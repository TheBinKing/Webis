Webis是一款旨在“**高效且低价**地提取网页数据”的**数据净化流水线工具**，其核心竞争力来源于以下关键技术：

### 1. DOM节点噪声标签标记算法

根据用户提供HTML文件，对文件对应DOM树节点进行标签标记。

Webis设计了一款高效的DOM-Validator内容过滤器，由该过滤器提取出——由位置特征与内容特征组成的DOM节点特征向量：

![img](https://weboffice.ks3-cn-beijing.wpscdn.cn/shapes/386898879627/eae11522f2475db6bbe8dcf8703c628b4d206331?Expires=1746622800&KSSAccessKeyId=AKLT0EQocIWQWiSieayovaig&Signature=Y8vKuDS8D%2BZlTz%2Bdvp1brzrOXb8%3D&response-cache-control=public%2Cmax-age%3D86400)

- **content**：节点包含内容，内容特征。
- **lastTag**：节点当前标签，内容特征。
- **riskTag**：节点PATH的风险标签，位置特征。
- **depth**：节点深度，位置特征。
- **confidence**：节点置信度，位置特征。

```json
{
    "instruction": "Determine if the node is noise.",
    "input": "content:'Art Nouveau' | last_tag:<option>[M] | risk_tags: aside[H], section[M] | confidence: 0.87",
    "output": 0
}
```

风险标签由小模型产生：Webis**小模型**在经过百万级DOM节点数据集训练后，根据标签噪声概率，生成 **[H]**、**[M]**、**[L]** 三种风险的风险标签标识。

置信度由动态权重算法产生：**置信度计算以节点末位标签的噪声概率为基础，结合其风险等级调整系数进行加权，同时累加同节点上所有风险标签的概率均值作为辅助判定依据**。在融合节点深度权重后，产出节点置信度。

### 2. 基于DOM树的反向着色算法

该算法通过构建层次化统计模型，结合深度感知的动态决策机制，实现对网页噪声内容的精准识别与结构化清除。反向着色算法分为两步：着色与剪裁还原。

![img](https://weboffice.ks3-cn-beijing.wpscdn.cn/shapes/386898879627/81aac09047fba0e21e2fec064f6fdb2e2b2072d8?Expires=1746626400&KSSAccessKeyId=AKLT0EQocIWQWiSieayovaig&Signature=GUdqWZlWVFRCUbCLf66PsGkt%2BEg%3D&response-cache-control=public%2Cmax-age%3D86400)

DOM树采用**动态决策机制**，根据节点深度等特征计算决策参数，实现“**护根裁枝**”的剪裁效果。以后序遍历的顺序，首先处理子节点，当节点噪声值超过深度权重下的噪声阈值时，节点会被识别为噪声节点。该过程称为**反向着色**。

当处理完一个子树后，算法将对其进行**剪裁还原**。当该子树的噪声节点比例超过阈值后，整个子树将被移除。反之，整个子树的节点将会被保留，噪声节点的标记也随之移除。

### 3. 多维度上升的过滤模式

Webis采用**多维度上升**的过滤模式，结合微观、中观、宏观三个维度对文本进行过滤。

![img](https://weboffice.ks3-cn-beijing.wpscdn.cn/shapes/386898879627/e91a16a846ba02ddd974bda6374eb82a906a10b8?Expires=1746626400&KSSAccessKeyId=AKLT0EQocIWQWiSieayovaig&Signature=%2F0KeL85FgLAKe588rRydKaH4Fb8%3D&response-cache-control=public%2Cmax-age%3D86400)

- **微观维度**：对节点信息进行分析过滤。
- **中观维度**：子树级分析过滤。
- **宏观维度**：引入大模型，在语义级别进行宏观过滤。

Webis引入了**大小模型协同过滤**的概念，在低处理成本的基础上，保证了文本过滤效果的高质量。

