import streamlit as st

st.markdown(
    """
    <link rel="manifest" href="/static/manifest.json">
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/static/service-worker.js');
            });
        }
    </script>
    """,
    unsafe_allow_html=True
)



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

tarot_name_map = {
    # 大阿卡纳
    "愚者": "fool",
    "魔术师": "magician",
    "女祭司": "high_priestess",
    "皇后": "empress",
    "皇帝": "emperor",
    "教皇": "hierophant",
    "恋人": "lovers",
    "战车": "chariot",
    "力量": "strength",
    "隐者": "hermit",
    "命运之轮": "wheel_of_fortune",
    "正义": "justice",
    "倒吊人": "hanged_man",
    "死神": "death",
    "节制": "temperance",
    "恶魔": "devil",
    "高塔": "tower",
    "星星": "star",
    "月亮": "moon",
    "太阳": "sun",
    "审判": "judgement",
    "世界": "world",

    # 权杖
    "权杖一": "wands1",
    "权杖二": "wands2",
    "权杖三": "wands3",
    "权杖四": "wands4",
    "权杖五": "wands5",
    "权杖六": "wands6",
    "权杖七": "wands7",
    "权杖八": "wands8",
    "权杖九": "wands9",
    "权杖十": "wands10",
    "权杖侍从": "page_of_wands",
    "权杖骑士": "knight_of_wands",
    "权杖皇后": "queen_of_wands",
    "权杖国王": "king_of_wands",

    # 圣杯
    "圣杯一": "cups1",
    "圣杯二": "cups2",
    "圣杯三": "cups3",
    "圣杯四": "cups4",
    "圣杯五": "cups5",
    "圣杯六": "cups6",
    "圣杯七": "cups7",
    "圣杯八": "cups8",
    "圣杯九": "cups9",
    "圣杯十": "cups10",
    "圣杯侍从": "page_of_cups",
    "圣杯骑士": "knight_of_cups",
    "圣杯皇后": "queen_of_cups",
    "圣杯国王": "king_of_cups",

    # 宝剑
    "宝剑一": "swords1",
    "宝剑二": "swords2",
    "宝剑三": "swords3",
    "宝剑四": "swords4",
    "宝剑五": "swords5",
    "宝剑六": "swords6",
    "宝剑七": "swords7",
    "宝剑八": "swords8",
    "宝剑九": "swords9",
    "宝剑十": "swords10",
    "宝剑侍从": "page_of_swords",
    "宝剑骑士": "knight_of_swords",
    "宝剑皇后": "queen_of_swords",
    "宝剑国王": "king_of_swords",

    # 星币
    "星币一": "pents1",
    "星币二": "pents2",
    "星币三": "pents3",
    "星币四": "pents4",
    "星币五": "pents5",
    "星币六": "pents6",
    "星币七": "pents7",
    "星币八": "pents8",
    "星币九": "pents9",
    "星币十": "pents10",
    "星币侍从": "page_of_pents",
    "星币骑士": "knight_of_pents",
    "星币皇后": "queen_of_pents",
    "星币国王": "king_of_pents"
}

# --------------------
# 初始化 session_state
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
            （1）先给出一句针对这个事情结果的简短、直觉性的判断或建议，让咨询者立刻感受到牌的能量；\
            （2）【灵性与心理解读】—— 描述牌象的意象，结合心理层面与能量流动，讲述当前问题背后的内在状态与成长方向；\
            （3）给出在现实生活中可以采取的小行动、调整或心态转化方式，并以一句温暖的“塔罗祝语”收尾。\
            语气要自然流动，不要像报告。\
            也要有些朋友的关怀，亦师亦友，适度使用感官词（光、风、香气、温度）以传达能量与情绪变化。\
            输出长度偏中长（300~600字左右），内容要有灵魂、有故事感。"
        }
    ]

# 用于保存线上抽牌结果（格式：[(牌名, 正/逆位), ...]）
if "drawn_cards" not in st.session_state:
    st.session_state.drawn_cards = []

# 记录上一次抽牌模式，便于切换时清理
if "last_draw_mode" not in st.session_state:
    st.session_state.last_draw_mode = None

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

# 如果抽牌方式发生变化，清空之前线上抽牌结果（避免混淆）
if st.session_state.last_draw_mode is None:
    st.session_state.last_draw_mode = draw_mode
elif st.session_state.last_draw_mode != draw_mode:
    st.session_state.drawn_cards = []
    st.session_state.last_draw_mode = draw_mode

# --------------------
# 用户输入或系统抽牌（UI）
# --------------------
manual_card_inputs = []  # 临时收集用户手动输入（不会覆盖线上抽牌）
if draw_mode == "我有实体塔罗牌":
    st.info("请输入您抽到的每张牌与正/逆位：")
    for i in range(num_cards):
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input(f"第 {i+1} 张牌名称", key=f"manual_card_{i}")
        with col2:
            pos = st.radio(f"牌位 {i+1}", ["正位", "逆位"], key=f"manual_pos_{i}", horizontal=True)
        if name:
            manual_card_inputs.append((name, pos))

elif draw_mode == "使用线上抽牌":
    st.info("请在心中默念您的问题，然后点击下方按钮。")
    if st.button("🌌 抽牌"):
        random.seed(datetime.now().microsecond)
        selected = random.sample(tarot_deck, num_cards)
        st.session_state.drawn_cards = []  # Cover the previous online draw
        for i, card in enumerate(selected, 1):
            orientation = random.choice(["正位", "逆位"])
            st.session_state.drawn_cards.append((card, orientation))
        # Display the drawn cards
        st.success("抽牌完成 — 已载入以下牌位（将用于解读）：")
    
    if st.session_state.drawn_cards:
        st.markdown("### 🎴 您抽到的牌是：")
        
        cols = st.columns(len(st.session_state.drawn_cards))  # 横向排列牌面

        for i, (card, pos) in enumerate(st.session_state.drawn_cards):
            with cols[i]:
            # 获取英文文件名
                eng_filename = tarot_name_map.get(card, None)
                if eng_filename:
                    image_path = f"images/{eng_filename}.jpg"

                    # 检查图片是否存在
                    if os.path.exists(image_path):
                        from PIL import Image
                        if pos == "逆位":
                            img = Image.open(image_path).rotate(180)
                            st.image(img, use_container_width=True)
                        else:
                            st.image(image_path, use_container_width=True)
                    else:
                        st.warning(f"未找到牌图：{eng_filename}.jpg")
                else:
                    st.warning(f"未找到牌名对应数据：{card}")

            # 显示中文牌名 + 正逆位
            st.markdown(f"**{card}**")
            st.caption(f"（{pos}）")
        

        
        for i, (card, pos) in enumerate(st.session_state.drawn_cards, 1):
            st.markdown(f"**第{i}张：{card}（{pos}）**")
        st.caption("这些牌将用于生成塔罗解读。")

# --------------------
# Input the divination question
# --------------------
event = st.text_area("💭 请输入你想占卜的事件或困惑：")

# --------------------
# Generate the interpretation (using persistent online draw or manual input)
# --------------------
if st.button("生成塔罗解读"):
    # 先决定使用哪组牌：优先使用线上抽牌（若存在），否则使用手动输入
    if draw_mode == "使用线上抽牌":
        card_inputs = st.session_state.drawn_cards
    else:
        card_inputs = manual_card_inputs

    # 校验
    if not event:
        st.warning("请先输入你想占卜的事件或困惑。")
    elif len(card_inputs) != num_cards:
        st.warning(f"牌数不符合：期望 {num_cards} 张，目前提供 {len(card_inputs)} 张。请补全牌位或重新抽牌。")
    else:
        # 构建 prompt
        card_summary = "\n".join(
            [f"第{i+1}张：{name}（{pos}）" for i, (name, pos) in enumerate(card_inputs)]
        )
        user_prompt = (
            f"用户的问题是：{event}\n"
            f"他们使用的牌阵是：{spread_type}\n"
            f"抽到的牌如下：\n{card_summary}\n\n"
            f"请给出塔罗解读，遵循系统设定的风格和结构。"
        )

        st.session_state.messages.append({"role": "user", "content": user_prompt})

        # 调用模型
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            temperature=0.92,
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
        temperature=0.92,
        presence_penalty=0.7,
        frequency_penalty=0.4,
        max_tokens=600,
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
