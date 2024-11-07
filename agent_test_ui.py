#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

from baselibs import *

# 配置环境变量；如果您已经提前将api-key提前配置到您的运行环境中，可以省略这个步骤
import os
os.environ['DASHSCOPE_API_KEY']="sk-31b195403f6141f9a6aeaa209100929e"

os.environ['AMAP_TOKEN']="98b0d9d5e23e49b53ac0587a8b57515b"

# os.environ['MODELSCOPE_API_TOKEN']="b1efe3e7-f2d0-4917-8678-6863ae199938"
os.environ['MODELSCOPE_API_TOKEN']="0722db7c-c35a-4c00-9a3d-a1d0e5516b01"

# 选用RolePlay 配置agent
from modelscope_agent.agents.role_play import RolePlay  # NOQA
pl()

import streamlit as st

def role_weather(text, role_template):
    '''
    '''
    if role_template == "":
        role_template = '你扮演一个天气预报助手，你需要查询相应地区的天气，并调用给你的画图工具绘制一张城市的图。'
    llm_config = {'model': 'qwen-max', 'model_server': 'dashscope'}

    # input tool name
    function_list = ['amap_weather', 'image_gen']

    st.write('正在创建智能体...')
    bot = RolePlay(
        function_list=function_list, llm=llm_config, instruction=role_template)

    st.write('智能体开始工作...')
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


def role_video(text, role_template):
    ''' 生成视频
    '''
    if role_template == "":
        role_template = '你是一个视频生成助手，你需要根据用户输入的内容，生成宣传文稿，然后将文稿使用女生配音，最后用文稿和配音生成短视频。'

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
    st.write('正在创建智能体...')
    bot = RolePlay(
        function_list=function_list, llm=llm_config, instruction=role_template)

    pl('智能体开始工作...')
    st.write('智能体开始工作...')
    response = bot.run(text)
    return response

def test_role_video():

    query = '智能体为未来生产带来无限的可能，将会极大的改变我们的生活。'
    response = role_video(query)

    text = ''
    for chunk in response:
        text += chunk

    pl()
    print(f'text:{text}')

# -----------------------------------------

# 版本号及应用名称
app_name = "智能体演示"
app_name_en = "Agent Demo"
version = "v0.1.0"

project_title = f"{app_name} {app_name_en}_{version}"

#-----------------------------------------
st.set_page_config(
    page_title= project_title,
    page_icon="favicon.png",
    layout="wide",
    menu_items={
        "About": f"关于{app_name}",
    },
)

# 隐藏右边的菜单以及页脚
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title('智能体Agent演示')
st.caption('功能说明: Agent Demo 智能体功能演示。')
st.write('---')


query_sample_texts = """
厦门海沧区天气怎样？
深圳明天天气
明天的广州
后天上海天气
"""
query_video_texts = """
“科创新视界”，带你看最前沿的科技！
智能体为未来生产带来无限的可能，将会极大的改变我们的生活。
咪宝是一款全新的智能音箱，可以陪你聊天，带你学习。
"""

# -----------------------------------------

role_movie_template = '你是一个视频生成助手，你需要根据用户输入的内容，生成宣传文稿，然后将文稿使用女生配音，最后用文稿和配音生成短视频。'
role_movie_template = '你是一个视频生成助手，你需要根据用户输入的内容，生成简洁的宣传文稿，然后将文稿使用女生配音，最后将文稿(翻译成英文)并和配音一起生成短视频。'
role_movie_template = '你是一个视频生成助手，你需要根据用户输入的内容，生成简洁的宣传文稿，最后将文稿翻译成英文)并生成短视频。'
role_movie_template = '你是一个视频生成助手，你需要根据用户输入的内容，生成简洁的宣传文稿，然后将文稿使用女生配音，最后将文稿(翻译成英文)并和配音一起生成短视频。'


# role_template = '你扮演一个天气预报助手，你需要查询用户提供地区和时间的天气，并调用画图工具绘制一张城市对应天气的图，图像大小800*600。'
# role_template = '你扮演一个天气预报助手，你需要根据用户提供地区和时间查询天气情况，调用画图工具绘制一张城市对应天气的图，并在图上写上城市、日期及天气，图像大小600*400; 并。'
role_template = '你扮演一个天气预报助手，你需要根据用户提供地区和时间查询天气情况，并绘制一张城市对应天气的图，图像大小600*400。'
# st.write(role_template)

col_1, col_2 = st.columns(2)
with col_2:
    role_sample_list = {
        "天气预报助手":role_template,
        "短视频助手":role_movie_template
    }
    role_sample = st.selectbox('选择预置角色:', role_sample_list.keys(), index=0)
with col_1:
    def_role = role_sample_list.get(role_sample, "")
    role_text = st.text_area("请输入角色定义:", def_role)


st.subheader(role_sample)

col1, col2 = st.columns(2)
with col2:
    if role_sample == "天气预报助手":
        query_sample_list = query_sample_texts.splitlines()
    else:
        query_sample_list = query_video_texts.splitlines()

    query_sample = st.selectbox('选择例子试试:', query_sample_list, index=0)

with col1:

    def_query = st.session_state.get('query', query_sample)
    query_text = st.text_area("请输入对话内容:", def_query)

bt_search = st.button("搜索")
if bt_search :
    print(f'role_text:{role_text}')
    if role_sample == "天气预报助手":
        response = role_weather(query_text, role_text)
    else:
        response = role_video(query_text, role_text)

    with st.expander('执行过程细节', expanded=True):
        with st.empty():
            text = ''
            for chunks in response:
                text += chunks
                #print(chunks, end='', flush=True)
                st.text(text)

    st.divider()
    pl()
    print(text)

    # 提取结果
    pl("提取结果")
    # text = text.replace('\n\n', '\n')
    answer_list = []
    keys = ["", "Action:"]
    key = "Answer:"
    last_line = ""

    for line in text.splitlines():
        print(line)
        if line.startswith(key):
            last_line = line
        elif line.startswith("Action:"):
            if last_line != "":
                answer_list.append(last_line[len(key):])
            last_line = ""
        elif line.startswith("Action Input:"):
            if last_line != "":
                answer_list.append(last_line[len(key):])
            last_line = ""
        elif line.startswith("Observation:"):
            if last_line != "":
                answer_list.append(last_line[len(key):])
            last_line = ""
        else:
            last_line += line + "\n\n"

    if last_line != "":
        answer_list.append(last_line[len(key):])

    for answer in answer_list:
        answer = answer.replace("![", "\n\n![")
        print(answer)
        st.write (f'{answer}')

if __name__ == '__main__':
    pass
    # import fire
    # fire.Fire()


