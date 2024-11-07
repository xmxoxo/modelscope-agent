#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

from baselibs import *

# 配置环境变量；如果您已经提前将api-key提前配置到您的运行环境中，可以省略这个步骤
import os
os.environ['DASHSCOPE_API_KEY']="sk-31b195403f6141f9a6aeaa209100929e"
os.environ['AMAP_TOKEN']="98b0d9d5e23e49b53ac0587a8b57515b"
os.environ['MODELSCOPE_API_TOKEN']="b1efe3e7-f2d0-4917-8678-6863ae199938"
os.environ['MODELSCOPE_API_TOKEN']="0722db7c-c35a-4c00-9a3d-a1d0e5516b01"


# 选用RolePlay 配置agent
from modelscope_agent.agents.role_play import RolePlay  # NOQA

pl()
def role_weather(text):
    '''
    '''

    role_template = '你扮演一个天气预报助手，你需要查询相应地区的天气，并调用给你的画图工具绘制一张城市的图。'
    llm_config = {'model': 'qwen-max', 'model_server': 'dashscope'}

    # input tool name
    function_list = [
        "amap_weather",
        "image_gen",
        "text-address",
    ]

    bot = RolePlay(
        function_list=function_list, llm=llm_config, instruction=role_template)

    response = bot.run(text)
    return response

def test_role_weather():

    query = '厦门海沧区天气怎样？'
    response = role_weather(query)

    text = ''
    for chunk in response:
        text += chunk
        #print(chunk, end='', flush=True)

    #print()
    pl()
    print(f'text:{text}')


def role_video(text):
    ''' 生成视频
    '''

    role_template = '你是一个视频生成助手，你需要根据用户输入的内容，生成简洁的宣传文稿，然后将文稿使用女生配音，最后将文稿和配音一起生成短视频，注意：在调用短视频生成工具时，要将文稿翻译成英文输入视频生成工具。'
    role_template = '你是一个视频生成助手，你需要根据用户输入的内容，生成简洁的宣传文稿，然后将文稿使用女生配音，最后将文稿(翻译成英文)并和配音一起生成短视频。'

    #llm_config = {'model': 'modelscope-agent-llm-v1', 'model_server': 'dashscope'}
    llm_config = {'model': 'qwen-max', 'model_server': 'dashscope'}

    # input tool name
    function_list = [
                    'video-generation',
                    #'text-translation-en2zh',
                    #'text-translation-zh2en',
                    'web_browser',
                    'speech-generation',
                    'image_gen',
                    "amap_weather",
                    "text-address",
                    ]
    pl('正在创建智能体...')
    bot = RolePlay(function_list=function_list, llm=llm_config, instruction=role_template)

    pl('智能体开始工作...')
    response = bot.run(text)
    return response

def test_role_video():

    query = '智能体为未来生产带来无限的可能，将会极大的改变我们的生活。'
    response = role_video(query)

    text = ''
    for chunk in response:
        text += chunk
        print(chunk, end='', flush=True)

    print()

    pl()
    print(f'text:{text}')

if __name__ == '__main__':
    pass
    import fire
    fire.Fire()


