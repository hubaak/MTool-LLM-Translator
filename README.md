# MTool LLM Translator
这个项目是为了适配[MTool](https://mtool.app/?lang=chs)进行更优质的翻译。

本项目的目标：
* 统一的名词翻译
* 连贯的上下文翻译
* 我用着爽

哦顺带一提，现在也支持兼容[XUnity.AutoTranslator](https://github.com/bbepis/XUnity.AutoTranslator)的`CustomTranslate`接口的服务了。

未来可能更新：
* Ollama
* 本地LLM直接从模型加载

*如果有上面使用需求，可以直接提在issue里，这会有点懒了。*


## 为什么要写这个项目？
之前我自己写了个很简单的脚本用LLM翻译MTool导出的文本，但是使用的时候发现几个问题：
1. 上下文联系差，因为是逐条的
2. 专有名词比如人物、道具经常出现不同的翻译
3. 有时候把一些不是需要翻译的文本比如纯数字也扔进去翻译了

所以对于上面的三个问题，对应的解决方法是：
1. MTool导出的json总体文本顺序还是正确的，所以可以用FIFO保留上文以及它们对应翻译，以增加上下文连续性以及翻译的一致性
2. 用一个专有名词列表专门存储专有名词和它们的翻译。不用担心这个列表过程影响翻译，因为只有待翻译文本中出现对应的专有名词，prompt里才会把它放进去
3. 加了个简单的filter，把不用翻译的部分提前退出了

## 配置环境
本项目依赖`Python`进行运行，所以在开始之前，需要安装python，并下载需要的包。
总之先安装一下项目运行要的包：
```bash
pip install -r requirements.txt
```

## api设置
目前项目只支持使用openai格式的api，你可以从大模型厂商购买，或者是用[vllm](https://docs.vllm.ai/en/stable/)以及[ollama](https://ollama.com/?utm_source=chatgpt.com)在本地部署并提供api服务。
api需要在`config.yaml`中进行设置，主要是`url`，`key`以及`model`。

如果需要更改模型推理的细节，如最大token和温度等等，可以直接在`inference`中更改，格式是:
```yaml
LLM_Backend: openai

OpenAI_api:
  url: 你的openai格式url
  key: 对应的key
  model: 你想使用的模型

  inference:
    max_tokens: 2048
    temperature: 0.2
    <openai格式的任意输入参数>: <对应的值>

Translate_Config:
  max_attempts: 3
  context_num: 5
```

其中`Translate_Config`控制翻译器自身的一些行为，比如：
* `max_attempts`：设置单个文本的最大尝试翻译次数（防止有时候大模型抽风，我本地部署的Qwen3.6-27B试了下3基本足够）
* `context_num`：设置上下文管理器记录的上文数量，越大上文越多但是越消耗token

## MTool翻译开跑！
准备好python环境和大模型的api之后，就可以直接开跑了

```bash
python main.py \
    --input 输入文件，默认是repo主目录下的ManualTransFile.json \
    --output 输出文件，默认是Translation.json
```

默认情况下，会在repo的主目录下生成一个`Translation.json`的文件。
本项目是支持中途断了接着跑的，所以`Translation.json`中会有一些用于断点继续的东西，这些内容不会影响MTool对翻译文件的读取，所以使用的时候直接忽略掉就行。


## XUnity.AutoTranslator的CustomTranslate服务
突然遇上俩没翻译的Unity游戏，于是又搓了个简单的翻译服务。

### 开启server
server的设置和MTool使用的翻译一样也在`config.yaml`中进行设置，请在下面的操作开始前保证已经进行了api相关的配置。

```bash
python AutoTranslator_server.py \
  --host 0.0.0.0 \
  --port 3280 \
  -s xxx
```
按照上面设置，翻译服务就会运行在`http://ip:3280/translate`这个接口上。

`-s`或者`--session`参数主要用于上下文和名词表的保存，这样下次翻译的时候就能从保存的配置中恢复，配置json会保存在`sessions/<session_name>.json`中。
如果不想占空间手动删掉就行（虽然文本也要不了多大空间）。


### 在AutoTranslator中进行配置
首先需要遵循[XUnity.AutoTranslator](https://github.com/bbepis/XUnity.AutoTranslator)项目的指引，安装AutoTranslator。
然后需要在AutoTranlator的配置文件`AutoTranslatorConfig.ini`中进行如下配置：

```yaml
[Service]
Endpoint=CustomTranslate
FallbackEndpoint=

...

[Custom]
Url=http://127.0.0.1:3280/translate
```

这里演示的是本机运行翻译服务，如果不是本机的话把上面ip换一下就可以了。