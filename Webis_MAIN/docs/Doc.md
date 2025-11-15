##  LangChain （一般配合文档加载器（Document Loaders）使用）  
[**https://www.langchain.com/**](https://www.langchain.com/)

**特点**：

+ 开源框架，生态庞大，支持 docx、pdf、markdown、html 等几十种格式。
+ 能把文档转成 `Document` 对象，再切分（Chunk）和向量化，配合向量数据库做检索增强。
+ 灵活，可嵌入任意 LLM（OpenAI、Ollama、本地大模型等）。

```python
from langchain.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 加载 docx
loader = Docx2txtLoader("sample.docx")
documents = loader.load()

# 切分文档
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = splitter.split_documents(documents)

# texts 就可以送进向量库或直接问答
print(texts[0].page_content)

```

**优缺点：**生态最大，社区插件、文档 loader、工具接口非常多。灵活性高，可以接大模型（OpenAI、本地 LLM）、向量数据库（FAISS、Chroma、Milvus）、代理等。而且轻量，只要 Python 环境就能跑，常见的 doc/pdf loader 本地可用 。但是对新手来说调试门槛稍高  

### 1.安装环境
```python
#新建虚拟环境
python -m venv venvLC
# Linux/macOS:
source venvLC/bin/activate
# Windows:
# venvLC\Scripts\activate

# 安装 LangChain 及常用组件
pip install -U langchain langchain-community langchain-text-splitters langchain-huggingface langchain-openai langchain-ollama chromadb faiss-cpu pypdf python-docx docx2txt sentence-transformers


# 如果打算用 OpenAI：
# export OPENAI_API_KEY={key}         # Linux/macOS
# setx OPENAI_API_KEY {key}            # Windows（新开终端生效）

# 如果你打算用本地 Ollama（推荐纯本地）：
# 1。安装 Ollama
# 2。首次拉取任一模型，例如：
#    ollama pull llama3

```

**<font style="color:rgb(38, 38, 38);">2.文档准备</font>**<font style="color:rgb(38, 38, 38);">  
</font><font style="color:rgb(38, 38, 38);">建议在环境目录底下创建一个docs文件夹，把源文件放进去</font>

### <font style="color:rgb(38, 38, 38);">3.运行</font>
支持的功能很多，比如一键清洗保存为同名的txt文件

![](https://cdn.nlark.com/yuque/0/2025/png/49023023/1755711593686-27c682e1-52ad-413a-ae88-1b1c54ebe25b.png)

![](https://cdn.nlark.com/yuque/0/2025/png/49023023/1755711850161-41cd35b5-d1c9-4d0d-a68f-c668c2509510.png)

还可以检索文档中的内容，与使用者交互，比如使用者可以问文档中的问题或总结文档内容

```python
import os
import pathlib
from typing import List
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# LLM 适配：OpenAI 或 Ollama
def get_llm():
    use_openai = os.getenv("USE_OPENAI", "0") == "1"
    if use_openai and os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        print("使用 OpenAI LLM（可通过 USE_OPENAI=0 改回本地）")
        return ChatOpenAI(model="gpt-4o-mini", temperature=0)
    else:
        from langchain_ollama import ChatOllama
        # 需本地已安装并运行 ollama，且已 pull 对应模型
        print("使用本地 Ollama（默认模型：llama3）")
        return ChatOllama(model="llama3", temperature=0)

INPUT_DIR = "docs"
PERSIST_DIR = "storage"

def load_docs(root: str):
    files = []
    for r, _, fns in os.walk(root):
        for fn in fns:
            ext = pathlib.Path(fn).suffix.lower()
            if ext in {".docx", ".pdf", ".md", ".txt"}:
                files.append(os.path.join(r, fn))
    if not files:
        raise RuntimeError(f"在 {root}/ 未找到文档（支持 .docx/.pdf/.md/.txt）")

    all_docs = []
    for fp in files:
        ext = pathlib.Path(fp).suffix.lower()
        if ext == ".docx":
            docs = Docx2txtLoader(fp).load()
        elif ext == ".pdf":
            docs = PyPDFLoader(fp).load()
        else:
            docs = TextLoader(fp, encoding="utf-8").load()
        # 标注来源，方便回溯
        for d in docs:
            d.metadata = d.metadata or {}
            d.metadata["source"] = fp
        all_docs.extend(docs)
    return all_docs

def build_or_load_vectorstore():
    # 嵌入模型：体积小、中文友好
    embed = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh")
    if os.path.isdir(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        print(f"发现持久化向量库，加载：{PERSIST_DIR}/")
        vs = Chroma(persist_directory=PERSIST_DIR, embedding_function=embed)
        return vs

    print("首次构建向量库：加载文档…")
    docs = load_docs(INPUT_DIR)
    print(f"共加载 {len(docs)} 条文档片段（未切分）")

    # 切分
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.split_documents(docs)
    print(f"切分后共 {len(chunks)} 个块")

    # 构建 & 持久化
    vs = Chroma.from_documents(chunks, embedding=embed, persist_directory=PERSIST_DIR)
    print(f"已持久化到：{PERSIST_DIR}/")
    return vs

def main():
    llm = get_llm()
    vectorstore = build_or_load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
    )

    print("\nRAG 已就绪。输入问题开始检索问答；输入 `exit` 退出。\n")
    while True:
        q = input("你：").strip()
        if q.lower() in {"exit", "quit"}:
            break
        out = qa.invoke({"query": q})
        print("\n—— 回答 ——")
        print(out["result"].strip())
        print("\n—— 参考来源 ——")
        for i, sd in enumerate(out.get("source_documents", []), 1):
            src = sd.metadata.get("source", "unknown")
            page = sd.metadata.get("page", None)
            page_info = f" (page {page})" if page is not None else ""
            print(f"{i}. {src}{page_info}")
        print()

if __name__ == "__main__":
    main()

```

![](https://cdn.nlark.com/yuque/0/2025/png/49023023/1755712997825-4783d1bd-2547-42af-9cfb-40dd29118c6e.png)

##  LlamaIndex
[https://docs.llamaindex.ai/en/stable/](https://docs.llamaindex.ai/en/stable/)

[https://docs.llamaindex.org.cn/en/stable/](https://docs.llamaindex.org.cn/en/stable/)

**特点**：

+ 专注文档问答，API 友好。
+ 提供 “索引” 抽象，支持树形索引、向量索引、关键词索引等多种方式。
+ 可以直接将 doc/pdf 等作为输入构建知识库。

```python
from llama_index import Document, VectorStoreIndex, SimpleDirectoryReader

# 加载文件
documents = SimpleDirectoryReader("docs/").load_data()

# 建立索引
index = VectorStoreIndex.from_documents(documents)

# 查询
query_engine = index.as_query_engine()
response = query_engine.query("这份文档讲了什么？")
print(response)

```

**优缺点：**

api设计更专注于“问答”，核心优势是可以建立各种索引，根据索引对目标文档进行查找，清洗，且核心依赖少，本地环境能直接跑。但是生态不如 LangChain 广，扩展性差一点  

### 1.环境准备
```python
# 创建虚拟环境
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

# 安装 LlamaIndex
pip install llama-index
# 安装常用依赖
pip install openai chromadb faiss-cpu

```

### 2.文档准备
建议在环境目录底下创建一个docs文件夹，把源文件放进去

### 3.运行
可以对这些文档进行各种操作，比如提取主体保存为.txt、按索引查找、按关键字排序等，这里只搞了一个简单的保存为.txt的程序

```python
import os
from llama_index.core import SimpleDirectoryReader

def main():
    inputdir = "docs"
    outputdir = "outputs"

    os.makedirs(outputdir, exist_ok=True)

    documents = SimpleDirectoryReader(inputdir).load_data()

    for i, doc in enumerate(documents):
        filename = f"document_{i+1}.txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(doc.text)

        print("=" * 40)
        print(f"文档 {i+1} 已保存为: {filepath}")
        print("内容预览:\n")
        print(doc.text[:500])  
        print("\n...（已截断）")

if __name__ == "__main__":
    main()

```

![](https://cdn.nlark.com/yuque/0/2025/png/49023023/1755709861441-bd72bc4f-4254-4b10-a5a9-b87e5041be78.png)

![运行结果](https://cdn.nlark.com/yuque/0/2025/png/49023023/1755709876904-d3977cc8-f197-403c-88d5-ab4322ef8503.png)

##  Haystack 
[https://haystack.deepset.ai/overview/intro](https://haystack.deepset.ai/overview/intro)

**特点**：

+ 德国 deepset 团队开发，企业级信息检索框架。
+ 支持 pipeline 化：文档读取 → 索引 → 检索 → QA。
+ 集成多种后端（Elasticsearch、Weaviate、FAISS）。

```python
from haystack.nodes import TextConverter, PreProcessor
from haystack.document_stores import InMemoryDocumentStore

doc_store = InMemoryDocumentStore()

# 读取 docx
converter = TextConverter(remove_numeric_tables=True)
docs = converter.convert(file_path="sample.docx", meta=None)

preprocessor = PreProcessor(split_length=200, split_overlap=20)
processed_docs = preprocessor.process(docs)

doc_store.write_documents(processed_docs)

```

**优缺点：**这是一个企业级文档工具，强调可扩展性，pipeline 概念清晰，适合大规模检索和生产部署。具有强大的检索能力，支持 Elasticsearch、Weaviate、Milvus 等重型数据库。而且社区和文档不错，由deepset 团队维护，有很多实战案例。但是部署相对复杂，如果只用内存型 `InMemoryDocumentStore`，本地跑很轻量；但如果要用 Elasticsearch/Weaviate，那就要额外部署服务。更偏向“做个公司内部知识库/问答系统”。

