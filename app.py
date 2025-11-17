import streamlit as st
from streamlit.components.v1 import html
import pandas as pd

# ----------------------------------------------------------------------
# 1) 더미 캠페인 데이터 (총 47개)
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
    (f"C{100+i}", f"CRM 캠페인 {i+1}", "Email", "탐색") for i in range(24)
]

campaigns = campaigns[:47]
df_campaign = pd.DataFrame(campaigns, columns=["ID", "캠페인명", "채널", "주요 조건"])

# ----------------------------------------------------------------------
# 2) Streamlit 기본 세팅
# ----------------------------------------------------------------------
st.set_page_config(page_title="CRM Journey Mapper", layout="wide")

st.markdown(
    """
<style>
    body { background-color:#f8f9fc; }
    .section-box {
        background:white; padding:20px; border-radius:12px;
        border:1px solid #e5e7eb; margin-bottom:20px;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("CRM Journey Mapper")
st.caption("Salesforce 등에서 실행 중인 CRM 캠페인을 불러와, 고객 여정 기준으로 한눈에 시각화하는 서비스입니다.")

# ----------------------------------------------------------------------
# 3) 캠페인 불러오기 (API 시뮬레이션)
# ----------------------------------------------------------------------
st.subheader("1. 캠페인 가져오기 (API 연동 시나리오)")

if st.button("🔄 현재 실행 중인 캠페인 불러오기", use_container_width=True):
    st.session_state["campaign_loaded"] = True
    st.success("47개 캠페인을 성공적으로 불러왔습니다.")

if "campaign_loaded" in st.session_state:
    st.markdown("### 📋 불러온 캠페인 리스트 (총 47개)")
    st.dataframe(df_campaign, use_container_width=True, height=280)

# ----------------------------------------------------------------------
# 4) 여정 단계 정의 & 캠페인 매핑
# ----------------------------------------------------------------------
st.subheader("2. 고객 여정 기준 캠페인 배치")

stages = ["회원가입", "탐색", "구매", "재구매", "이탈임박", "휴면"]

# 캠페인을 단계별로 grouping (Entry 기준)
stage_mapping = {s: [] for s in stages}
for _, row in df_campaign.iterrows():
    cond = row["주요 조건"]
    stage = {
        "신규가입": "회원가입",
        "첫구매": "구매",
        "탐색": "탐색",
        "재구매": "재구매",
        "이탈임박": "이탈임박",
        "휴면": "휴면",
        "고객세분화": "탐색",
    }.get(cond, "탐색")

    stage_mapping[stage].append(f"{row['캠페인명']} ({row['채널']})")

# 인접 단계 간 span(영향 구간) 집계: Entry가 i번째 단계인 캠페인은 i→i+1 구간 영향으로 표현
span_counts = {}
for i in range(len(stages) - 1):
    entry_stage = stages[i]
    span_counts[(i, i + 1)] = len(stage_mapping.get(entry_stage, []))

# ----------------------------------------------------------------------
# 5) Journey 레이어 + 타임라인 (검은 박스 안에 모두 배치)
# ----------------------------------------------------------------------
st.markdown("### 🎯 고객 여정 타임라인 & 레이어별 캠페인 영향")

n = len(stages)
positions = [i / (n - 1) * 100 for i in range(n)]  # 0~100% 위치

timeline_html = """
<div style="background:#020617; padding:28px 26px 36px 26px; border-radius:16px;
            color:#e5e7eb; font-family:-apple-system, BlinkMacSystemFont, 'Pretendard', system-ui;">

  <style>
    .cj-line     { height:4px; background:linear-gradient(90deg,#22c55e,#06b6d4);
                   margin:32px 0 26px 0; border-radius:999px; }
    .cj-stage-row{ display:flex; justify-content:space-between; align-items:flex-start; }
    .cj-stage    { text-align:center; width:150px; }
    .cj-dot      { width:22px; height:22px; border-radius:999px; background:#22c55e;
                   border:3px solid #020617; margin:0 auto;
                   box-shadow:0 0 0 2px rgba(34,197,94,0.9); }
    .cj-label    { margin-top:8px; font-size:14px; font-weight:600; color:#f9fafb; }

    .cj-layer-row  { display:flex; justify-content:space-between; margin-bottom:6px;
                     font-size:12px; color:#a5b4fc; }
    .cj-layer-pill { flex:1; text-align:center; padding:4px 0; border-radius:999px;
                     background:rgba(129,140,248,0.13); margin:0 4px;
                     border:1px solid rgba(129,140,248,0.35); }

    .cj-span-row { position:relative; height:54px; margin-top:6px; }
    .cj-span     { position:absolute; top:12px; height:18px; border-radius:999px;
                   background:linear-gradient(90deg,rgba(45,212,191,0.35),
                                                rgba(129,140,248,0.70));
                   border:1px solid rgba(59,130,246,0.9);
                   display:flex; align-items:center; padding:0 11px;
                   font-size:11px; color:#e5e7eb; white-space:nowrap; }
  </style>

  <div style="text-align:center; font-size:15px; margin-bottom:10px; color:#e5e7eb;">
    고객 여정 위에서 각 캠페인의 <b>진입 지점</b>과 <b>영향 구간</b>을 레이어로 확인합니다.
  </div>

  <!-- Journey Layer -->
  <div class="cj-layer-row">
    <div class="cj-layer-pill">온보딩 · 회원가입 → 탐색 → 구매</div>
    <div class="cj-layer-pill">성장 · 구매 이후 재구매 / N차 구매</div>
    <div class="cj-layer-pill">이탈 관리 · 이탈임박 → 휴면</div>
  </div>

  <!-- 메인 타임라인 -->
  <div class="cj-line"></div>

  <!-- 단계 마커 -->
  <div class="cj-stage-row">
"""

# 단계 마커 추가
for s in stages:
    timeline_html += f"""
    <div class="cj-stage">
      <div class="cj-dot"></div>
      <div class="cj-label">{s}</div>
    </div>
    """

timeline_html += """
  </div>  <!-- /cj-stage-row -->

  <!-- 영향 구간 하이라이트 레이어 -->
  <div class="cj-span-row">
"""

# span bar 그리기 (회원가입→탐색, 탐색→구매, …)
for i in range(len(stages) - 1):
    count = span_counts.get((i, i + 1), 0)
    if count <= 0:
        continue
    left = positions[i]
    right = positions[i + 1]
    width = right - left
    # 살짝 안쪽으로 줄여서 좌우 여백 확보
    left += 3
    width -= 6
    label = f"{stages[i]} → {stages[i+1]} · {count}개 캠페인"
    timeline_html += f"""
    <div class="cj-span" style="left:{left:.2f}%; width:{width:.2f}%;">
      {label}
    </div>
    """

timeline_html += """
  </div> <!-- /cj-span-row -->

</div>  <!-- /wrapper -->
"""

html(timeline_html, height=260)

# ----------------------------------------------------------------------
# 6) (옵션) 단계별 상세 캠페인 – 접을 수 있는 리스트
# ----------------------------------------------------------------------
st.markdown("### 🔍 단계별 상세 캠페인 (옵션 보기)")

for s in stages:
    with st.expander(f"{s} 구간에 진입하는 캠페인", expanded=False):
        items = stage_mapping.get(s, [])
        if not items:
            st.write("- 해당 여정에 진입하는 캠페인 없음")
        else:
            for c in items:
                st.write(f"- {c}")
