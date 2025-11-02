import os
import random
from datetime import datetime
import streamlit as st
from openai import OpenAI

# --------------------
# 基础配置
# --------------------
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

st.title("🔮 您的私人命理师")

# --------------------
# 塔罗牌列表（示例，可自行补全）
# --------------------


tarot_deck = [
    "愚者", "魔术师", "女祭司", "皇后", "皇帝", "教皇", "恋人", "战车",
    "力量", "隐者", "命运之轮", "正义", "倒吊人", "死神", "节制",
    "恶魔", "高塔", "星星", "月亮", "太阳", "审判", "世界",
    "权杖一", "权杖二", "权杖三", "权杖四", "权杖五", "权杖六",
    "权杖七", "权杖八", "权杖九", "权杖十", "权杖侍从", "权杖骑士",
    "权杖皇后", "权杖国王",
    "圣杯一", "圣杯二", "圣杯三", "圣杯四", "圣杯五", "圣杯六",
    "圣杯七", "圣杯八", "圣杯九", "圣杯十", "圣杯侍从", "圣杯骑士",
    "圣杯皇后", "圣杯国王",
    "宝剑一", "宝剑二", "宝剑三", "宝剑四", "宝剑五", "宝剑六",
    "宝剑七", "宝剑八", "宝剑九", "宝剑十", "宝剑侍从", "宝剑骑士",
    "宝剑皇后", "宝剑国王",
    "星币一", "星币二", "星币三", "星币四", "星币五", "星币六",
    "星币七", "星币八", "星币九", "星币十", "星币侍从", "星币骑士",
    "星币皇后", "星币国王"
]


# --------------------
# 初始化对话历史
# --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content":
            "你是一位灵性而深具洞察的塔罗牌大师，融合了荣格心理学、象征学与神秘学的理解。\
            你的风格细腻、温柔、有画面感，像在静谧空间中轻声与咨询者对话。\
            请用优雅而自然的语言解读牌义，不使用列表或编号，而是用段落叙事的方式展开。\
            每次解读分为三个层次：\
            （1）先给出一句针对这个事情结果的简短、诗意、直觉性的判断或建议，让咨询者立刻感受到牌的能量；\
            （2）【灵性与心理解读】—— 描述牌象的意象，结合心理层面与能量流动，讲述当前问题背后的内在状态与成长方向；\
            （3）给出在现实生活中可以采取的小行动、调整或心态转化方式，并以一句温暖的“塔罗祝语”收尾。\
            语气要自然流动，不要像报告。\
            也要有些朋友的关怀，亦师亦友，适度使用感官词（光、风、香气、温度）以传达能量与情绪变化。\
            输出长度偏中长（300~600字左右），内容要有灵魂、有故事感。"
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

num_cards = {
    "单牌占卜（1张）": 1,
    "三张牌阵": 3,
    "六张牌阵（全局能量）": 6,
    "十张牌阵（凯尔特十字阵）": 10
}[spread_type]

# --------------------
# 选择抽牌方式
# --------------------
st.write("### 🃏 选择抽牌方式")
draw_mode = st.radio("", ["我有实体塔罗牌", "使用线上抽牌"])

card_inputs = []

# --------------------
# 用户输入或系统抽牌
# --------------------
if draw_mode == "我有实体塔罗牌":
    st.info("请输入您抽到的每张牌与正/逆位：")
    for i in range(num_cards):
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input(f"第 {i+1} 张牌名称", key=f"card_{i}")
        with col2:
            pos = st.radio(f"牌位 {i+1}", ["正位", "逆位"], key=f"pos_{i}", horizontal=True)
        if name:
            card_inputs.append((name, pos))

elif draw_mode == "使用线上抽牌":
    st.info("请在心中默念您的问题，然后点击下方按钮。")
    if st.button("🌌 抽牌"):
        random.seed(datetime.now().microsecond)
        selected = random.sample(tarot_deck, num_cards)
        for i, card in enumerate(selected, 1):
            orientation = random.choice(["正位", "逆位"])
            card_inputs.append((card, orientation))
            st.markdown(f"**第{i}张：{card}（{orientation}）**")

# --------------------
# 占卜问题输入
# --------------------
event = st.text_area("💭 请输入你想占卜的事件或困惑：")

# --------------------
# 生成解读
# --------------------
if st.button("生成塔罗解读") and event and len(card_inputs) == num_cards:
    card_summary = "\n".join(
        [f"第{i+1}张：{name}（{pos}）" for i, (name, pos) in enumerate(card_inputs)]
    )
    user_prompt = (
        f"用户的问题是：{event}\n"
        f"他们使用的牌阵是：{spread_type}\n"
        f"抽到的牌如下：\n{card_summary}\n\n"
        f"请给出塔罗解读。"
    )

    st.session_state.messages.append({"role": "user", "content": user_prompt})

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
# 继续对话
# --------------------
st.markdown("---")
follow_up = st.text_input("💬 想进一步交流或提问吗？", key="followup")
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
# 查看对话记录
# --------------------
with st.expander("📜 查看完整对话记录"):
    for msg in st.session_state.messages[1:]:
        role = "你" if msg["role"] == "user" else "AI命理师"
        st.markdown(f"**{role}：** {msg['content']}")