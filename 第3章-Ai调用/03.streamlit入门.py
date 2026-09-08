import streamlit as st

# 页面设置
st.set_page_config(
    page_title="Toping助手",
    layout="wide",
)
st.header("我是标题")
st.text("我是文本内容")
st.write("我是内容")
with st.chat_message("user"):
    st.write("你好，你是谁")

