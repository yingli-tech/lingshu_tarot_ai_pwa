import os
import streamlit as st
from openai import OpenAI 

# Set OpenAI API key (use the environment variable)
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

st.title("🔮 你的私人命理师")


# Initial conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": 
         "你是一位灵性而深具洞察的塔罗牌大师，融合了荣格心理学、象征学与神秘学的理解。\
            你的风格细腻、温柔、有画面感，像在静谧空间中轻声与咨询者对话。\
            请用优雅而自然的语言解读牌义，不使用列表或编号，而是用段落叙事的方式展开。\
            每次解读分为三个层次：\
            （1）直觉结论】—— 先给出一句简短、诗意、直觉性的判断或建议，让咨询者立刻感受到牌的能量；\
            （2）【灵性与心理解读】—— 描述牌象的画面、色彩与象征，结合心理层面与能量流动，讲述当前问题背后的内在状态与成长方向；\
            （3）【现实启示与温柔收尾】—— 给出在现实生活中可以采取的小行动、调整或心态转化方式，并以一句温暖的“塔罗祝语”收尾。\
            语气要自然流动，不要像报告，而像灵性导师在对话。\
            也要有些朋友的关怀，亦师亦友\
            适度使用情绪词、感官词（光、风、香气、温度），以传达能量与情绪的细微变化。\
            输出长度偏中长,300~600字左右,内容要有灵魂、有故事感。"
        }
    ]

# The first input for divination
with st.expander("🔍 首次占卜"):
    event = st.text_area("请输入你想占卜的事件或困惑：")
    card_name = st.text_input("请输入抽到的塔罗牌名称（例如：节制 Temperance）")
    card_position = st.radio("请选择牌位：", ["正位", "逆位"])
    if st.button("生成解读") and event and card_name and card_position:
        first_prompt = (
            f"用户想占卜这个问题：{event}。"
            f"他们抽到的牌是：{card_name}，牌位是：{card_position}。"
            f"请根据牌面先给出一个预测结果或建议，再进行塔罗解读。"
        )
        st.session_state.messages.append({"role": "user", "content": first_prompt})
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            temperature=0.95,
            presence_penalty=0.7,
            frequency_penalty=0.4,
            max_tokens=800,
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.markdown("### 🧙 解读结果：")
        st.write(reply)


# consecutive conversation input
st.markdown("---")
st.markdown("### 💬 继续提问或补充想法")
follow_up = st.text_input("你可以继续表达你的感受或提出问题：", key="followup")
if st.button("发送") and follow_up:
    st.session_state.messages.append({"role": "user", "content": follow_up})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages,
        temperature=0.85,
        presence_penalty=0.5,
        frequency_penalty=0.4,
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.markdown("### 🧙 塔罗回应：")
    st.write(reply)

# Display complete conversation history
with st.expander("📜 查看完整对话记录"):
    for msg in st.session_state.messages[1:]:  # 跳过 system 消息
        role = "你" if msg["role"] == "user" else "塔罗 AI"
        st.markdown(f"**{role}：** {msg['content']}")


