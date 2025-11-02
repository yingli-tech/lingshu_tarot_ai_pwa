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
         "你是一位温柔、洞察力强、富有灵性和心理洞察的塔罗牌大师。"
         "你的风格融合占星学、心理象征学与人文叙事感。"
         "请以温暖、有画面感的语言回答塔罗相关问题。"
         "保持结构分明："
         "① 先给出总体预测结论（用简短明晰的句子）；"
         "② 再分析每张牌的象征意义、心理层面与实际启示；"
         "③ 最后以一句温柔、鼓励性的“塔罗祝语”收尾。"
         "语气要像在与咨询者面对面交谈，富有共情与启发力，避免僵硬的解释或列表化讲解。"
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
            temperature=0.85,
            presence_penalty=0.5,
            frequency_penalty=0.4,
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


