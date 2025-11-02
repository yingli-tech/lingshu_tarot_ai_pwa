import os
import streamlit as st
from openai import OpenAI 

# Set OpenAI API key (use the environment variable)
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

st.title("🔮 你的私人塔罗师")

# the user inputs
event = st.text_area("请输入你想占卜的事件或困惑：")
card_name = st.text_input("请输入抽到的塔罗牌名称（例如：节制 Temperance）")
card_position = st.radio("请选择牌位：", ["正位", "逆位"])

# button to generate the reading
if st.button("生成解读") and event and card_name and card_position:
    prompt = (
        f"你是一位塔罗牌大师。用户想占卜这个问题：{event}。"
        f"他们抽到的牌是：{card_name}，牌位是：{card_position}。"
        f"请根据牌面先给出一个预测结果或建议，再进行塔罗解读。"
    )

    # Call GPT-4o-mini model to generate the reading
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    result = response.choices[0].message.content
    st.markdown("### 🧙 解读结果：")
    st.write(result)


