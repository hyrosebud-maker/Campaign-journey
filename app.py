import streamlit as st
import pandas as pd
import random

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="CRM Journey Mapper",
    page_icon="✨",
    layout="wide"
)

# -----------------------------
# CSS (HTML 렌더링 안정 버전)
# -----------------------------
st.markdown("""
<style>

html, body {
    font-family: 'Inter', sans-serif;
}

/* HEADER BOX */
.header-box {
    background: linear-gradient(90deg, #0f172a, #1e293b);
    padding: 30px 32px;
    border-radius: 14px;
    color: white;
    margin-bottom: 25px;
}

.header-title {
    font-size: 28px;
    font-weight: 700;
}

.header-desc {
    font-size: 15px;
    opacity: 0.85;
}

/* SECTION TITLE */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin: 25px 0 10px 0;
}

/* TIMELINE CONTAINER */
.timeline-container {
    background: #0f172a;
    padding: 40px 30px;
    border-radius: 16px;
    margin-top: 20px;
    color: white;
}

/* HORIZONTAL ARROW */
.arrow-line {
    height: 5px;
    background: linear-gradient(90deg, #38bdf8, #34d399);
    margin: 35px 0 50px 0;
    border-radius: 3px;
}

/* STAGE NODE */
.stage-wrapper {
    display: flex;
    justify-content: space-between;
    margin-top: -45px;
}

.stage-marker {
    text-align: center;
    width: 130px;
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

/* CAMPAIGN CARDS */
.stage-col-title {
    text-align: center;
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 12px;
}

.campaign-card {
    background: #1e293b;
    padding: 10px 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 13px;
    border-left: 3px solid #38bdf8;
}

.campaign-card:hover {
    background: #0f172a;
    transition: 0.25s;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="header-box">
    <div class="header-title">✨ CRM Journey Mapper</div>
    <div class="header-desc">
        운영 중인 CRM 마케팅 캠페인을 여정 단계(회원가입 → 탐색 → 구매 → 재구매 → N차 구매 → 이탈임박 → 휴면)에 자동 배치하여  
        고객이 어떤 시점에 어떤 메시지를 받는지 한눈에 분석할 수 있는 시각화 도구입니다.
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# 47개 캠페인 생성
# -----------------------------
campaign_titles = [
    "가입 완료 웰컴 이메일","신규회원 첫구매 Push","장바구니 이탈 리마인드",
    "최근 본 상품 기반 추천","카테고리 관심 기반 추천","재구매 유도 쿠폰",
    "고객 등급 상승 알림","이탈임박 리마인드","휴면 방지 캠페인",
    "구매후기 작성 유도","멤버십 프로모션","첫 배송 완료 안내",
    "카카오 알림톡 웰컴","이벤트 참여 독려","VIP 리워드 안내",
    "신규 카테고리 추천","대체 상품 추천","최근 구매 기반 Cross-Sell",
    "N차 구매 딥러닝 추천","유사 관심상품 추천","핵심 상품 할인 안내",
    "봄 시즌 프로모션","여름 시즌 프로모션","가을 시즌 프로모션",
    "겨울 시즌 프로모션","장바구니 재진입 할인","브랜드 스토리 소개",
    "고객 생일 축하 캠페인","기념일 쿠폰 지급","리뷰 기반 상세 추천",
    "배송 완료 후 케어 콘텐츠","신규 런칭 소식","장기 미구매 리마인드",
    "지난 관심상품 모음","최근 탐색 기반 추천","찜상품 리마인드",
    "이탈 예상 고객 Push","찜상품 할인 알림","후기 많은 상품 추천",
    "가격인하 알림","구매 후 경품 이벤트","매장 방문 유도",
    "친구 추천 이벤트","기획전 알림","포인트 소멸 알림",
    "고객 등급 갱신"
]

campaign_titles = campaign_titles[:47]
channels = ["Email", "Push", "Kakao", "SMS"]
stages = ["회원가입", "탐색", "구매", "재구매", "N차 구매", "이탈임박", "휴면"]

campaigns = []
for idx, t in enumerate(campaign_titles):
    campaigns.append({
        "ID": f"C{idx+1:03}",
        "캠페인명": t,
        "채널": random.choice(channels),
        "주요 타겟": random.choice(stages)
    })

df = pd.DataFrame(campaigns)

# -----------------------------
# 캠페인 리스트 출력
# -----------------------------
st.markdown("<div class='section-title'>📋 불러온 캠페인 리스트 (총 47개)</div>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True, height=350)

# -----------------------------
# JOURNEY TIMELINE
# -----------------------------
st.markdown("<div class='section-title'>🧭 고객 여정 타임라인 & 캠페인 매핑</div>", unsafe_allow_html=True)

timeline_html = """
<div class="timeline-container">

    <div style="text-align:center; font-size:17px; margin-bottom:20px;">
        전체 고객 여정에 배치된 캠페인을 한눈에 확인하세요.
    </div>

    <div class="arrow-line"></div>

    <div class="stage-wrapper">
"""

for s in stages:
    timeline_html += f"""
        <div class="stage-marker">
            <div class="stage-dot"></div>
            <div class="stage-label">{s}</div>
        </div>
    """

timeline_html += """
    </div>
</div>
"""

st.markdown(timeline_html, unsafe_allow_html=True)

# -----------------------------
# 단계별 캠페인 카드 출력
# -----------------------------
st.markdown("### 🔎 단계별 캠페인 상세")

cols = st.columns(7)

grouped = {s: [] for s in stages}

for _, row in df.iterrows():
    grouped[row["주요 타겟"]].append(row["캠페인명"])

for idx, stg in enumerate(stages):
    with cols[idx]:
        st.markdown(f"<div class='stage-col-title'>{stg}</div>", unsafe_allow_html=True)
        if not grouped[stg]:
            st.markdown("<div style='opacity:0.5;'>해당 캠페인 없음</div>", unsafe_allow_html=True)
        else:
            for c in grouped[stg]:
                st.markdown(f"<div class='campaign-card'>{c}</div>", unsafe_allow_html=True)
