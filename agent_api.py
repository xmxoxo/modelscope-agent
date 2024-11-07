#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

from baselibs import *
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse

from modelscope import AutoModelForCausalLM, AutoTokenizer
from modelscope import GenerationConfig

from typing import List
import base64
from pydantic import BaseModel, Field

model_path = '/mnt/sda1/models/ModelScope-Agent-7B'
device_map = 'cuda:0' # 'auto'

print('正在加载模型...')
tokenizer = AutoTokenizer.from_pretrained(model_path, 
        revision = 'v1.0.0',trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, 
        revision = 'v1.0.0', device_map=device_map, 
        trust_remote_code=True, fp16=True).eval()
model.generation_config = GenerationConfig.from_pretrained(model_path, 
        revision = 'v1.0.0', trust_remote_code=True) # 可指定不同的生成长度、top_p等相关超参

print('模型加载成功...')

system = """
 <|system|>:当前对话可以使用的插件信息如下，请自行判断是否需要调用插件来解决当前用户问题。
 若需要调用插件，则需要将插件调用请求按照json格式给出，必须包含api_name、url、parameters字段，
 并在其前后使用<|startofthink|>和<|endofthink|>作为标志。然后你需要根据插件API调用结果生成合理的答复；
 若无需调用插件，则直接给出对应回复即可：

1. {"name": "modelscope_image-generation", "url":"http://127.0.0.1:9860/txt2image", "description": "图片生成服务，针对文本输入，生成对应的图片，插图等", "parameters": [{"name": "text", "description": "用户输入的文本信息", "required": true}]}

2. {"name": "modelscope_speech-generation", "url":"http://127.0.0.1:9860/tts", "description": "朗读文本内容，将文本转语音服务，将文字转换为自然而逼真的语音，可配置男声/女声", "parameters": [{"name": "input", "description": "要转成语音的文本", "required": true}, {"name": "gender", "description": "用户身份", "required": true}]}
"""


def test_a():
        
    pl()
    query = "根据龟兔赛跑的故事情节内容,生成一张插图。"
    query = "根据龟兔赛跑的故事情节内容，生成一个新的故事，然后为它生成一张插图。"
    query = "生成一张插图，根据故事情节一的内容。"
    print(f'query:{query}')
    response, history = model.chat(tokenizer, query, history=None, system=system)
    print(response)
    pl()

    query = "假如你是李清照，现在和我对话，你最喜欢的词是哪一首，语音回复我。"
    print(f'query:{query}')
    response, history = model.chat(tokenizer, query, history=history, system=system)
    print(response)

app = FastAPI(title="Agent API接口", description="AI Agent API", version="0.1.0")

# 定义查询数据的实体类
class AgentQuery(BaseModel):
    query: str

@app.post("/agent", description="Agent推理") #, response_model=UploadResult
async def agent_predict(agent_query:AgentQuery):
    global model, tokenizer, system
    query = agent_query.query
    response, history = model.chat(tokenizer, query, history=None, system=system)
    
    return JSONResponse(content={"code": 200, "result": response})

def main(args):
    import uvicorn

    # 设置运行参数，比如端口、主机地址等 
    uvicorn.run(app, host=args.host, port=args.port, reload=args.debug, workers=args.workers) #

if __name__ == '__main__':
    pass
    parser = argparse.ArgumentParser(description='API接口服务端')
    parser.add_argument('--host', type=str, default="0.0.0.0", help='host')
    parser.add_argument('--port', type=int, default=9850, help='port')
    parser.add_argument('--workers', type=int, default=1, help='workers')
    parser.add_argument('--debug', type=int, default=0, help='debug')
    #parser.add_argument('--debug', action='store_true', help="Enable debug mode.")

    args = parser.parse_args()
    #print(args)
    main(args)

'''
python agent_api.py --host --port --workers --debug

http://192.168.15.111:9850/docs

'''
