# MTool LLM Translator
这个项目是为了适配[MTool](https://mtool.app/?lang=chs)进行更优质的翻译。


## 为什么要写这个项目？
之前我自己写了个很简单的脚本用LLM翻译MTool导出的文本，但是使用的时候发现几个问题：
1. 上下文联系差，因为是逐条的
2. 专有名词比如人物、道具经常出现不同的翻译
3. 有时候把一些不是需要翻译的文本比如纯数字也扔进去翻译了

所以对于上面的三个问题，对应的解决方法是：
1. MTool导出的json总体文本顺序还是正确的，所以可以用FIFO保留上文以及它们对应翻译，以增加上下文连续性以及翻译的一致性
2. 用一个专有名词列表专门存储专有名词和它们的翻译。不用担心这个列表过程影响翻译，因为只有待翻译文本中出现对应的专有名词，prompt里才会把它放进去
3. 加了个简单的filter，把不用翻译的部分提前退出了

## 使用方法
### 配置环境
本项目依赖`Python`进行运行，所以在开始之前，需要安装python，并下载需要的包。
总之先安装一下项目运行要的包：
```bash
pip install -r requirements.txt
```

### api设置
目前项目只支持使用openai格式的api，你可以从大模型厂商购买，或者是用[vllm](https://docs.vllm.ai/en/stable/)以及[ollama](https://ollama.com/?utm_source=chatgpt.com)在本地部署并提供api服务。
api需要在`config.yaml`中进行设置，主要是`url`，`key`以及`model`。

如果需要更改模型推理的细节，如最大token和温度等等，可以直接在`inference`中更改，格式是:
```yaml
OpenAI_api:
  url: 你的openai格式url
  key: 对应的key
  model: 你想使用的模型

  inference:
    max_tokens: 2048
    temperature: 0.2
    <openai格式的任意输入参数>: <对应的值>
```

### 开跑！
准备好python环境和大模型的api之后，就可以直接开跑了

```bash
python main.py \
    --input 输入文件，默认是repo主目录下的ManualTransFile.json \
    --output 输出文件，默认是Translation.json
```

默认情况下，会在repo的主目录下生成一个`Translation.json`的文件。
本项目是支持中途断了接着跑的，所以`Translation.json`中会有一些用于断点继续的东西，这些内容不会影响MTool对翻译文件的读取，所以使用的时候直接忽略掉就行。