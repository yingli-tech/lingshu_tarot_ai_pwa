import os
import streamlit as st
from openai import OpenAI 

# --------------------
# 基础配置
# --------------------
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

st.title("🔮 你的私人塔罗师")

# --------------------
# 初始化对话历史
# --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "你是一位灵性而深具洞察的塔罗牌大师，融合荣格心理学、象征学与神秘学。"
                "请用优雅、叙事的方式解读牌义，每次解读包含："
                "【直觉结论】【灵性与心理解读】【现实启示与温柔收尾】。"
                "语气温柔、有画面感，文字自然流动。"
            ),
        }
    ]

# --------------------
# 选择牌阵模板
# --------------------
st.markdown("## ✨ 选择你的牌阵")

spread_type = st.selectbox(
    "请选择一个牌阵模板：",
    [
        "单牌占卜（1张）",
        "三张牌阵（过去-现在-未来）",
        "六张牌阵（全局能量）",
        "十张牌阵（凯尔特十字阵）",
    ]
)

# --------------------
# 塔罗输入区域
# --------------------
with st.expander("🔍 输入占卜内容"):
    event = st.text_area("请输入你想占卜的事件或困惑：")

    # 根据牌阵类型动态生成输入框
    card_inputs = []
    num_cards = {"单牌占卜（1张）": 1, "三张牌阵（过去-现在-未来）": 3,
                 "六张牌阵（全局能量）": 6, "十张牌阵（凯尔特十字阵）": 10}[spread_type]

    for i in range(num_cards):
        col1, col2 = st.columns([2, 1])
        with col1:
            card_name = st.text_input(f"第 {i+1} 张牌名称（如：恋人 The Lovers）", key=f"card_{i}")
        with col2:
            position = st.radio(f"牌位 {i+1}", ["正位", "逆位"], key=f"pos_{i}", horizontal=True)
        if card_name:
            card_inputs.append((card_name, position))

    # --------------------
    # 生成解读按钮逻辑
    # --------------------
    if st.button("生成解读") and event and len(card_inputs) == num_cards:
        # 构建 prompt
        card_summary = "\n".join(
            [f"第{i+1}张：{name}（{pos}）" for i, (name, pos) in enumerate(card_inputs)]
        )
        first_prompt = (
            f"用户的问题是：{event}\n"
            f"他们使用的牌阵是：{spread_type}\n"
            f"抽到的牌如下：\n{card_summary}\n\n"
            f"请综合每张牌的能量、位置与相互关系，"
            f"给出一段完整的塔罗解读，包含三个部分："
            f"【直觉结论】【灵性与心理解读】【现实启示与温柔收尾】。"
        )

        st.session_state.messages.append({"role": "user", "content": first_prompt})

        # 调用模型
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            temperature=0.95,
            presence_penalty=0.7,
            frequency_penalty=0.4,
            max_tokens=1000,
        )

        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

        st.markdown("### 🧙 塔罗解读：")
        st.write(reply)

# --------------------
# 继续对话区
# --------------------
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

# --------------------
# 查看完整对话
# --------------------
with st.expander("📜 查看完整对话记录"):
    for msg in st.session_state.messages[1:]:  # 跳过 system
        role = "你" if msg["role"] == "user" else "塔罗 AI"
        st.markdown(f"**{role}：** {msg['content']}")