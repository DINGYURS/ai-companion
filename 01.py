import streamlit as st
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)
st.set_page_config(
    page_title="AI 智能伴侣",
    page_icon="🤖",
    # 布局
    layout="wide",

    # 侧边栏状态
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
    }
)

# 大标题
st.title("AI 智能伴侣")

# LOGO

# 系统提示词
system_prompt = "你是一个会安慰人的朋友，用户每次和你说话都会感觉好很多。"

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []
    print("初始化聊天历史")

# 显示聊天历史
for message in st.session_state.messages:
    print(f"显示聊天历史消息: {message}")
    st.chat_message(message["role"]).write(message["content"])

# 消息输入框
prompt = st.chat_input("请输入消息...")
if prompt: # 字符串会自动转化成布尔值，如果字符串为非空，则为True
    st.chat_message("user").write(prompt) # 显示用户输入的消息
    print(f"用户输入的消息: {prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt}) # 将用户输入的消息添加到聊天历史中
    res = client.chat.completions.create(
        messages=[
            {"role": "system","content": system_prompt},
            *st.session_state.messages
        ],
        model='qwen3:4b',
        stream=True,
    )

    # 非流式输出
    # st.chat_message("assistant").write(res.choices[0].message.content)
    # st.session_state.messages.append({"role": "assistant", "content": res.choices[0].message.content}) # 将模型生成的消息添加到聊天历史中

    # 流式输出
    res_message = st.empty() # 创建一个空的占位符，用于显示模型生成的消息
    full_response = ""
    for chunk in res:
        if chunk.choices[0].delta.content:
            full_response += chunk.choices[0].delta.content
            res_message.chat_message("assistant").write(full_response) # 显示模型生成的消息

    # 将模型生成的完整消息添加到聊天历史中
    st.session_state.messages.append({"role": "assistant", "content": full_response}) # 将模型生成的消息添加到聊天历史中