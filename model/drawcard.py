import streamlit as st
import random
from datetime import datetime

# 78张塔罗牌示例（可自行补全）
tarot_deck = [
    "愚者", "魔术师", "女祭司", "皇后", "皇帝", "教皇", "恋人", "战车",
    "力量", "隐者", "命运之轮", "正义", "倒吊人", "死神", "节制",
    "恶魔", "高塔", "星星", "月亮", "太阳", "审判", "世界"
    # ……补全至78张
]

st.title("🔮 塔罗牌占卜 🔮")

# 选择抽牌方式
st.write("### 选择抽牌方式")
mode = st.radio("", ["我有实体塔罗牌", "使用线上抽牌"])

# 选择抽牌数量
num_cards = st.selectbox("选择抽牌数量：", [1, 3, 6, 10])

if mode == "我有实体塔罗牌":
    st.write(f"您选择抽 {num_cards} 张牌。")
    if num_cards == 1:
        card = st.text_input("请输入您抽到的牌名（含正位/逆位）：")
    else:
        card = st.text_area("请输入您抽到的多张牌名（每张牌用逗号或空格分隔，含正位/逆位）：")
    if card:
        st.success(f"您输入的牌是：{card}")

else:
    st.write("请在心中默念您的问题……")
    if st.button("抽牌"):
        # 使用时间微秒作为随机种子
        random.seed(datetime.now().microsecond)

        # 抽出若干不重复的牌
        cards = random.sample(tarot_deck, num_cards)

        st.markdown("### 🌟 宇宙为您选择的牌是：")
        for i, c in enumerate(cards, 1):
            orientation = random.choice(["正位", "逆位"])
            st.markdown(f"**{i}. {c}（{orientation}）**")