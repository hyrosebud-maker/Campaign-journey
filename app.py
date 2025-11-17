import streamlit as st
import pandas as pd
import random

# -----------------------------
# 1) PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="CRM Journey Mapper",
    page_icon="✨",
    layout="wide"
)

# -----------------------------
# 2) CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

body {
    font-family: 'Inter', sans-serif;
}

/* Header Section */
.header-box {
    background: linear-gradient(90deg, #0f172a, #1e293b);
    padding: 32px;
    border-radius: 12px;
    color: white;
    margin-bottom: 25px;
}

.header-title {
    font-size: 30px;
    font-weight: 700;
}

.header-desc {
    font-size: 16px;
    margin-top: 6px;
    opacity: 0.9;
}

/* Section Titles */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 10px;
}

/* Timeline Container */
.timeline-container {
    position: relative;
    background: #0f172a;
    padding: 40px 20px;
    border-radius: 14px;
    margin-top: 20px;
    color: white;
}

/* Horizontal Arrow Line */
.arrow-line {
    height: 4px;
    background: linear-gradient(90deg, #38bdf8, #34d399);
    position: relative;
    margin-top: 50px;
    margin-bottom: 60px;
}

/* Journey Stage Marker */
.stage-marker {
    position: relative;
    text-align: center;
    width: 150px;
    display: inline-block;
}

.stage-dot {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #34d399;
    margin: 0 auto;
    border: 3px solid white;
}

.stage-label {
    margin-top: 6px;
    font-size: 15px;
    font-weight: 600;
}

/* Campaign Cards */
.campaign-card {
    background: #1e293b;
    padding: 10px 12px;
    margin: 6px 0;
    border-radius: 8px;
    color: #f1f5f9;
    font-size: 13px;
    border-left: 3px solid #38bdf8;
}

.campaign-card:hover {
    background: #0f172a;
    transition: 0.2s;
}

/* Grid for campaign zone */
.campaign-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 14px;
    margin-top: 30px;
}

.stage-col-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 8px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 3) HEADER
# -----------------------------
st.markdown("""
<div class="header-box">
    <div class="header-title">✨ CRM Journey Mapper</div>
    <div class="header-desc">
        Salesforce·Braze 등에서 운영 중인 캠페인을 불러와  
        고객 여정(회원가입 → 탐색 → 구매 → 재구매 → N차 구매 → 이탈임박 → 휴면) 상에  
        어떤 시점에 어떤 캠페인이 맞닿는지 한눈에 시각화해주는 도구입니다.
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# 4) Dummy Campaign Generation (47개)
# -----------------------------
campaign_titles = [
    "가입 완료 웰컴 이메일", "신규회원 첫구매 Push", "장바구니 이탈 리마인드",
    "최근 본 상품 기반 추천", "카테고리 관심 기반 추천", "재구매 유도 쿠폰",
    "고객 등급 상승 알림", "이탈임박 리마인드", "휴면 방지 캠페인", 
    "구매후기 작성 유도", "멤버십 프로모션", "첫 배송 완료 안내",
    "카카오 알림톡 웰컴", "이벤트 참여 독려", "VIP 리워드 안내",
    "신규 카테고리 추천", "대체 상품 추천", "최근 구매 기반 Cross-Sell",
    "N차 구매 딥러닝 추천", "유사 관심상품 추천", "핵심 상품 할인 안내",
    "봄 시즌 프로모션", "여름 시즌 프로모션", "가을 시즌 프로모션",
    "겨울 시즌 프로모션", "장바구니 재진입 할인", "브랜드 스토리 소개",
    "고객 생일 축하 캠페인", "기념일 쿠폰 지급", "리뷰 기반 상세 추천",
    "배송 완료 후 케어 콘텐츠", "신규 런칭 소식", "장기 미구매 리마인드",
    "지난 관심상품 모음", "최근 탐색 기반 추천", "찜한상품 리마인드",
    "이탈 예상 고객 Push", "찜상품 할인 알림", "후기 많은 상품 추천",
    "가격인하 알림", "구매 후 경품 추첨 이벤트", "매장 방문 유도",
    "친구 추천 이벤트", "기획전 알림", "포인트 소멸 알림", "고객 등급 갱신"
]

campaign_titles = campaign_titles[:47]  # 47개로 고정

channels = ["Email", "Push", "Kakao", "SMS"]
stages = ["회원가입", "탐색", "구매", "재구매", "N차 구매", "이탈임박", "휴면"]

campaign_list = []
for idx, title in enumerate(campaign_titles):
    campaign_list.append({
        "ID": f"C{idx+1:03}",
        "캠페인명": title,
        "채널": random.choice(channels),
        "주요 타겟": random.choice(stages)
    })

df = pd.DataFrame(campaign_list)

# -----------------------------
# 5) CAMPAIGN LIST VIEW
# -----------------------------
st.markdown("<div class='section-title'>📋 불러온 캠페인 리스트 (총 47개)</div>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True, height=350)


# -----------------------------
# 6) JOURNEY VISUAL TIMELINE (컨설팅 스타일)
# -----------------------------
st.markdown("<div class='section-title'>🧭 고객 여정 타임라인 & 캠페인 매핑</div>", unsafe_allow_html=True)

# 캠페인 분류
stage_groups = {s: [] for s in stages}
for _, row in df.iterrows():
    stage_groups[row["주요 타겟"]].append(row["캠페인명"])

# -----------------------------
# 7) TIMELINE RENDERING
# -----------------------------
# 타임라인 HTML 구조
timeline_html = """
<div class="timeline-container">
    <div style="text-align: center; font-size:18px; margin-bottom:20px; opacity:0.85;">
        전체 고객 여정에 배치된 캠페인을 한 눈에 파악하세요.
    </div>

    <div class="arrow-line"></div>

    <div style="display:flex; justify-content: space-between; margin-top:-40px;">
"""

# 스테이지 노드
for s in stages:
    timeline_html += f"""
    <div class="stage-marker">
        <div class="stage-dot"></div>
        <div class="stage-label">{s}</div>
    </div>
    """

timeline_html += "</div></div>"

st.markdown(timeline_html, unsafe_allow_html=True)


# -----------------------------
# 8) 캠페인 카드를 Journey 단계 아래에 배치
# -----------------------------
st.markdown("""
<div style='margin-top:20px; font-size:17px; font-weight:600;'>🔎 단계별 캠페인 상세 보기</div>
""", unsafe_allow_html=True)

cols = st.columns(7)

for idx, stage in enumerate(stages):
    with cols[idx]:
        st.markdown(f"<div class='stage-col-title'>{stage}</div>", unsafe_allow_html=True)
        if len(stage_groups[stage]) == 0:
            st.markdown("<div style='opacity:0.5;'>등록된 캠페인 없음</div>", unsafe_allow_html=True)
        else:
            for camp in stage_groups[stage]:
                st.markdown(f"<div class='campaign-card'>{camp}</div>", unsafe_allow_html=True)

