## Tesseract
### 安装
最常见方式是通过 pip：

```powershell
pip install pytesseract pillow
```

也可以直接安装 Tesseract 引擎：

+ **Windows**：下载 Tesseract 官方安装包
+ **Linux (Ubuntu/Debian)**：

```bash
sudo apt install tesseract-ocr libtesseract-dev
```

### 使用
#### 脚本
```python
import pytesseract
from PIL import Image

img = Image.open("test.png")
text = pytesseract.image_to_string(img, lang="chi_sim")
print(text.strip())
```

#### 命令行
```powershell
tesseract test.png out.txt -l chi_sim
```

### 特点
+ 免费开源，Google 维护，社区大。
+ 支持 100+ 语言（含中文），但对复杂背景、扭曲图片稍弱。
+ 提供 `tesseract` CLI 和 Python 封装库 `pytesseract`。
+ 对 CPU 友好，不依赖 GPU。



### 示例
![](https://cdn.nlark.com/yuque/0/2025/png/49693855/1755678064894-e4da8611-8c4c-4747-ab44-ce6fba90600c.png)

---

## PaddleOCR
### 安装
```powershell
pip install paddleocr paddlepaddle
```

GPU 用户建议提前安装对应版本的 PaddlePaddle：

```bash
pip install paddlepaddle-gpu==2.5.0.post117 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
```

### 使用
#### 脚本
```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="ch")
img_path = r"C:\\Users\\yuzhe\\Desktop\\test\\test.png"
result = ocr.ocr(img_path, cls=True)

print("识别结果：\n")
for line in result[0]:
    print(line[1][0])
```

#### 命令行
```powershell
paddleocr --image_dir test.png --lang=ch
```

### 特点
+ 中文识别准确率高，支持竖排、手写体。
+ 提供快速模型与高精度模型，灵活选择。
+ Python API 完善，社区活跃，文档齐全。
+ 可调用 **表格识别、版面分析** 模块。



### 示例
![](https://cdn.nlark.com/yuque/0/2025/png/49693855/1755701068852-21ebd50d-22b2-4cbe-bdd6-2b06b1941aff.png)

---

## EasyOCR
### 安装
```powershell
pip install easyocr
```

需要确保 **PyTorch** 已安装，否则需先安装：

```bash
pip install torch torchvision torchaudio
```

### 使用
#### 脚本
```python
import easyocr

reader = easyocr.Reader(['ch_sim','en'])
results = reader.readtext("test.png")

for _, text, _ in results:
    print(text)
```

#### 命令行
虽然 EasyOCR 主要提供 Python API，但也可以封装成简单脚本实现 CLI 功能。

### 特点
+ 使用 PyTorch，支持 80+ 语言。
+ 易上手，几行代码即可完成 OCR。
+ 识别率不如 PaddleOCR，但比 Tesseract 对复杂背景友好。
+ GPU 支持好，速度快。



### 示例
![](https://cdn.nlark.com/yuque/0/2025/png/49693855/1755709529663-ae750526-bf11-417f-bf92-09e649977805.png)

---

## Kraken OCR
### 安装
```powershell
pip install kraken
```

源码安装：

```bash
git clone https://github.com/mittagessen/kraken.git
cd kraken
pip install -e .
```

### 使用
#### 脚本
```python
from kraken import rpred
from PIL import Image

im = Image.open("test.png")
model = rpred.load_any("en-default.mlmodel")
predictions = rpred.rpred(model, im)

print("识别结果：")
for line in predictions:
    print(line.text)
```

#### 命令行
```powershell
kraken -i test.png out.txt binarize segment ocr --model en-default.mlmodel
```

### 特点
+ 专注历史文献、古籍 OCR。
+ 内置版面分析（layout analysis），支持多栏、复杂排版。
+ 支持用户自定义训练模型，适合特殊字体和语言。
+ 社区较小，学习曲线高于 Tesseract/EasyOCR。



 

