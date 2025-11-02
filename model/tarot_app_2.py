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
    prompt2 = (
        f"你是一位温柔、洞察力强、富有灵性和心理洞察的塔罗牌大师。"
        f"你的风格融合占星学、心理象征学与人文叙事感。"
        f"请以温暖、有画面感的语言回答塔罗相关问题。"
        f"保持结构分明："
        f"① 先给出总体预测结论（用简短明晰的句子）；"
        f"② 再分析每张牌的象征意义、心理层面与实际启示；"
        f"③ 最后以一句温柔、鼓励性的“塔罗祝语”收尾。"
        f"语气要像在与咨询者面对面交谈，富有共情与启发力，避免僵硬的解释或列表化讲解。"
    )

    # Call GPT-4o-mini model to generate the reading
    response = client.chat.completions.create(
        model = "gpt-4o",  
        temperature = 0.85,
        presence_penalty = 0.5,
        frequency_penalty = 0.4,
        messages=[
            {"role": "system", "content": prompt2},
            {"role": "user", "content": prompt}],

    )

    result = response.choices[0].message.content
    st.markdown("### 🧙 解读结果：")
    st.write(result)

