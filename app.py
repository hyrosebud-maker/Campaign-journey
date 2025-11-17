import streamlit as st
from streamlit.components.v1 import html
import pandas as pd

# ----------------------------------------------------------------------
# 1) 더미 캠페인 데이터 (47개)
# ----------------------------------------------------------------------
campaigns = [
    ("C001", "가입 완료 웰컴 이메일", "Email", "신규가입"),
    ("C002", "가입 후 웰컴 Push", "Push", "신규가입"),
    ("C003", "첫구매 유도 리마인드", "Email", "첫구매"),
    ("C004", "첫구매 기념 감사 메시지", "SMS", "첫구매"),
    ("C005", "신규 카테고리 추천", "Email", "탐색"),
    ("C006", "최근 본 상품 기반 Cross-Sell", "Push", "탐색"),
    ("C007", "장바구니 방치 알림", "Push", "탐색"),
    ("C008", "가격 인하 알림", "Email", "탐색"),
    ("C009", "카테고리 관심 기반 추천", "Kakao", "탐색"),
    ("C010", "구매 완료 감사 메시지", "Email", "구매"),
    ("C011", "배송 완료 알림", "SMS", "구매"),
    ("C012", "리뷰 작성 유도", "Kakao", "구매"),
    ("C013", "재구매 리마인드 7일", "Email", "재구매"),
    ("C014", "재구매 리마인드 14일", "Email", "재구매"),
    ("C015", "VIP 라인업 안내", "Push", "고객세분화"),
    ("C016", "신규 카테고리 추천", "Kakao", "탐색"),
    ("C017", "대체 상품 추천", "Email", "탐색"),
    ("C018", "최근 구매 기반 Cross-Sell", "SMS", "재구매"),
    ("C019", "N차 구매 리마인드", "Email", "재구매"),
    ("C020", "유사 상품 추천", "Kakao", "탐색"),
    ("C021", "핵심 상품 프로모션", "Push", "탐색"),
    ("C022", "이탈 방지 프로모션", "SMS", "이탈임박"),
    ("C023", "휴면 방지 안내", "Email", "이탈임박"),
] + [
    # 추가 24개를 자동 생성
    (f"C{100+i}", f"CRM 캠페인 {i+1}", "Email", "탐색") for i in range(24)
]

campaigns = campaigns[:47]
df_campaign = pd.DataFrame(campaigns, columns=["ID", "캠페인명", "채널", "주요 조건"])


# ----------------------------------------------------------------------
# 2) Streamlit 기본 세팅
# ----------------------------------------------------------------------
st.set_page_config(page_title="CRM Journey Mapper", layout="wide")

st.markdown("""
<style>
    body { background-color:#f8f9fc; }
    .section-box {
        background:white; padding:20px; border-radius:12px;
        border:1px solid #e5e7eb; margin-bottom:20px;
    }
    .journey-title {
        font-size:20px; font-weight:700; margin-bottom:10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 CRM Journey Mapper – Prototype")
st.caption("Salesforce 등에서 실행 중인 캠페인을 불러와 고객 여정 기준으로 매핑해주는 프로토타입입니다.")


# ----------------------------------------------------------------------
# 3) 캠페인 불러오기 (API 시뮬레이션)
# ----------------------------------------------------------------------
st.subheader("1. 캠페인 가져오기 (API 시뮬레이션)")

if st.button("🔄 캠페인 불러오기", use_container_width=True):
    st.session_state["campaign_loaded"] = True
    st.success("47개 캠페인을 성공적으로 불러왔습니다!")

if "campaign_loaded" in st.session_state:
    st.markdown("### 📋 불러온 캠페인 리스트 (총 47개)")
    st.dataframe(df_campaign, use_container_width=True, height=300)


# ----------------------------------------------------------------------
# 4) Journey 단계 설정
# ----------------------------------------------------------------------
st.subheader("2. 고객 여정상 캠페인 매핑")

st.markdown("""
여정 기준:
- **회원가입**
- **탐색**
- **구매**
- **재구매**
- **이탈임박**
- **휴면**
""")

stages = ["회원가입", "탐색", "구매", "재구매", "이탈임박", "휴면"]

# 캠페인을 단계별로 grouping
stage_mapping = {s: [] for s in stages}
for _, row in df_campaign.iterrows():
    cond = row["주요 조건"]
    target = {
        "신규가입": "회원가입",
        "첫구매": "구매",
        "탐색": "탐색",
        "재구매": "재구매",
        "이탈임박": "이탈임박",
        "휴면": "휴면",
        "고객세분화": "탐색",
    }.get(cond, "탐색")

    stage_mapping[target].append(f"{row['캠페인명']} ({row['채널']})")


# ----------------------------------------------------------------------
# 5) Journey Timeline (컨설팅 장표형, st.html로 렌더링)
# ----------------------------------------------------------------------
st.markdown("### 🎯 고객 여정 타임라인 & 캠페인 매핑")

timeline_html = """
<div style="background:#0f172a; padding:40px 30px; border-radius:16px; color:white;">
    <div style='text-align:center; font-size:18px; margin-bottom:20px;'>
        고객 여정을 기준으로 현재 캠페인이 어떻게 배치되는지 확인하세요
    </div>

    <div style="height:5px; background:linear-gradient(90deg,#38bdf8,#34d399); margin:40px 0;"></div>

    <div style="display:flex; justify-content:space-between; margin-top:-25px;">
"""

for s in stages:
    timeline_html += f"""
    <div style="text-align:center; width:150px;">
        <div style="width:22px; height:22px; border-radius:50%; background:#34d399; border:3px solid white; margin:0 auto;"></div>
        <div style="margin-top:8px; font-size:15px; font-weight:700;">{s}</div>
    </div>
    """

timeline_html += "</div></div>"

html(timeline_html, height=260)


# ----------------------------------------------------------------------
# 6) 단계별 매핑 결과 출력
# ----------------------------------------------------------------------
st.markdown("### 📌 단계별 캠페인 상세")

cols = st.columns(len(stages))

for idx, s in enumerate(stages):
    with cols[idx]:
        st.markdown(f"#### 🟢 {s}")
        if len(stage_mapping[s]) == 0:
            st.write("- 해당 여정에 배치된 캠페인 없음")
        else:
            for c in stage_mapping[s]:
                st.write(f"- {c}")

