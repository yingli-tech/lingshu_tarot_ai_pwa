import os
import streamlit as st
from openai import OpenAI 

# --------------------
# 基础配置
# --------------------
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

st.title("🔮 您的私人命理师")

# --------------------
# 初始化对话历史
# --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": 
            "你是一位充满灵性、温柔且有生活感的塔罗牌大师。\
            你的语言风格要像真实聊天——轻松、自然、有点俏皮，但始终带着温度与洞察力。\
            你喜欢用 emoji 来表达情绪，例如 🌙、✨、💫、☕、🌿 等，但使用得体，不要太多。\
            你会先以一句简洁有力的话给出直觉预测（带一点仪式感，比如“这杯咖啡是小小的圆满”）。\
            然后进入第二部分，用温柔、有画面感的文字解释塔罗象征（结合生活、心理与灵性层面）。\
            描述牌象的象征，结合心理层面与能量流动，讲述当前问题背后的内在状态与成长方向；\
            最后以一段短短的“塔罗小语”或“祝福语”收尾，让读者感觉被理解、被鼓励。\
            请避免学术化或报告式的语气，使用口语、共情、轻叙事风格，像朋友间聊天又有灵性洞见。\
            你的目标：让读者读完后，感觉温暖、释然、被理解。"
            "你也融合了荣格心理学、象征学与神秘学的理解。\
            你的风格细腻、温柔、有画面感，像在静谧空间中轻声与咨询者对话。\
            语气要自然流动\
            也要有些朋友的关怀，亦师亦友\
            适度使用情绪词、感官词（光、风、香气、温度），以传达能量与情绪的细微变化。\
            输出长度偏中长,300~600字左右,内容要有灵魂、句式节奏要有起伏，有停顿、有呼吸。"
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
        "三张牌阵",
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
    num_cards = {"单牌占卜（1张）": 1, "三张牌阵": 3,
                 "六张牌阵（全局能量）": 6, "十张牌阵（凯尔特十字阵）": 10}[spread_type]

    for i in range(num_cards):
        col1, col2 = st.columns([2, 1])
        # input for card name and position
        with col1:
            card_name = st.text_input(f"第 {i+1} 张牌名称", key=f"card_{i}")
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
            f"请先给出一个预测结果或建议，再进行塔罗解读。"
        )

        st.session_state.messages.append({"role": "user", "content": first_prompt})

        # 调用模型
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

        st.markdown("### 🧙 塔罗解读：")
        st.write(reply)

# --------------------
# 继续对话区
# --------------------
st.markdown("---")
st.markdown("### 💬 继续提问或补充想法")

follow_up = st.text_input("如需要，请继续表达你的感受或提出问题：", key="followup")

if st.button("发送") and follow_up:
    st.session_state.messages.append({"role": "user", "content": follow_up})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state.messages,
        temperature=0.9,
        presence_penalty=0.7,
        frequency_penalty=0.4,
        max_tokens=400,
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
        role = "你" if msg["role"] == "user" else "AI命理师"
        st.markdown(f"**{role}：** {msg['content']}")