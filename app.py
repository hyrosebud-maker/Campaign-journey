import streamlit as st
import pandas as pd

# =========================================
# 0. 기본 설정 & 스타일
# =========================================
st.set_page_config(
    page_title="CRM Journey Mapper Prototype",
    page_icon="🧭",
    layout="wide"
)

# 트렌디한 컬러 & 카드 스타일 (간단 버전)
CUSTOM_CSS = """
<style>
/* 전체 폭 */
.block-container {max-width: 1400px !important;}

/* 상단 헤더 */
.app-header {
    padding: 12px 18px;
    border-radius: 14px;
    background: linear-gradient(135deg, #111827, #1e293b);
    color: #f9fafb;
    margin-bottom: 18px;
}
.app-header h1 {
    margin: 0;
    font-size: 26px;
    font-weight: 800;
}
.app-header p {
    margin: 4px 0 0 0;
    font-size: 13px;
    color: #e5e7eb;
}

/* 카드 공통 */
.card {
    border-radius: 14px;
    padding: 14px 16px;
    background: #0f172a;
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e5e7eb;
    border: 1px solid #1f2937;
    box-shadow: 0 12px 40px rgba(15,23,42,0.4);
    margin-bottom: 16px;
}
.card-light {
    border-radius: 14px;
    padding: 14px 16px;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 30px rgba(15,23,42,0.08);
    margin-bottom: 16px;
}
.card-title {
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 4px;
}
.card-sub {
    font-size: 12px;
    color: #9ca3af;
}

/* Journey 단계 박스 */
.journey-row {
    display: flex;
    gap: 10px;
    margin-top: 8px;
}
.journey-stage {
    flex: 1;
    border-radius: 12px;
    padding: 10px 10px 12px 10px;
    background: #020617;
    border: 1px solid rgba(148,163,184,0.4);
    position: relative;
}
.journey-stage-label {
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .04em;
    color: #9ca3af;
    margin-bottom: 4px;
}
.journey-stage-name {
    font-size: 14px;
    font-weight: 800;
    color: #e5e7eb;
}
.journey-stage-chip {
    position: absolute;
    right: 8px;
    top: 8px;
    font-size: 11px;
    padding: 2px 7px;
    border-radius: 999px;
    background: rgba(15,118,110,0.15);
    color: #5eead4;
    border: 1px solid rgba(45,212,191,0.4);
}
.journey-arrow {
    align-self: center;
    color: #64748b;
    font-size: 18px;
}

/* 캠페인 태그 */
.campaign-tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    padding: 3px 7px;
    border-radius: 999px;
    background: rgba(59,130,246,0.08);
    color: #60a5fa;
    border: 1px solid rgba(59,130,246,0.5);
    margin: 2px 4px 2px 0;
}
.campaign-tag span.channel {
    font-size: 10px;
    opacity: 0.8;
}

/* 단계별 캠페인 카드 내부 */
.campaign-list {
    margin-top: 6px;
    max-height: 220px;
    overflow-y: auto;
}
.campaign-item-title {
    font-size: 12px;
    font-weight: 700;
    color: #e5e7eb;
}
.campaign-item-meta {
    font-size: 10px;
    color: #9ca3af;
}

/* 메타 정보 */
.meta-pill {
    display: inline-block;
    padding: 3px 8px;
    margin-right: 6px;
    margin-bottom: 6px;
    font-size: 11px;
    border-radius: 999px;
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =========================================
# 1. Journey 정의
# =========================================
JOURNEY_STAGES = [
    {"key": "signup", "name": "회원가입", "label": "Stage 1"},
    {"key": "explore", "name": "탐색", "label": "Stage 2"},
    {"key": "first_purchase", "name": "첫 구매", "label": "Stage 3"},
    {"key": "second_purchase", "name": "2차 구매", "label": "Stage 4"},
    {"key": "loyal", "name": "활성 / 충성", "label": "Stage 5"},
    {"key": "churn_risk", "name": "이탈임박", "label": "Stage 6"},
    {"key": "churned", "name": "휴면 / 이탈", "label": "Stage 7"},
]

STAGE_NAME_MAP = {s["key"]: s["name"] for s in JOURNEY_STAGES}


# =========================================
# 2. 더미 캠페인 데이터 생성
#    (실제로는 Salesforce API 응답 자리)
# =========================================
def load_dummy_campaigns():
    """
    실제로는 Salesforce 등에서 API 호출로 가져올 부분.
    지금은 프로토타입이라 더미 50개 생성.
    """

    campaigns = []

    # --- 핵심 10개: 앞에서 논의한 현실적인 예시들 ---
    campaigns.append({
        "id": "C01",
        "name": "가입 환영 온보딩 이메일",
        "channel": "Email",
        "goal": "온보딩",
        "entry_stage": "signup",
        "applicable_stages": ["signup", "explore"],
        "trigger_condition": "회원가입 완료 직후 (signup_completed == true, within 24h)",
        "target_condition": "신규 가입 고객 전체"
    })
    campaigns.append({
        "id": "C02",
        "name": "첫 구매 유도 Push",
        "channel": "Push",
        "goal": "첫 구매 유도",
        "entry_stage": "explore",
        "applicable_stages": ["explore", "first_purchase"],
        "trigger_condition": "purchase_count == 0 AND last_login 후 48시간 미구매",
        "target_condition": "가입 이후 탐색만 하고 구매 없는 고객"
    })
    campaigns.append({
        "id": "C03",
        "name": "장바구니 이탈 리마인드",
        "channel": "Email",
        "goal": "장바구니 복귀",
        "entry_stage": "explore",
        "applicable_stages": ["explore", "first_purchase"],
        "trigger_condition": "cart_item_count >= 1 AND 12시간 경과 AND 구매 미완료",
        "target_condition": "장바구니 이탈 고객"
    })
    campaigns.append({
        "id": "C04",
        "name": "첫 구매 감사 & 리뷰 요청",
        "channel": "Email",
        "goal": "리뷰 확보",
        "entry_stage": "first_purchase",
        "applicable_stages": ["first_purchase"],
        "trigger_condition": "첫 구매 배송완료 3일 후",
        "target_condition": "purchase_count == 1 고객"
    })
    campaigns.append({
        "id": "C05",
        "name": "동일 카테고리 재구매 리마인드",
        "channel": "Push",
        "goal": "재구매 유도",
        "entry_stage": "second_purchase",
        "applicable_stages": ["second_purchase", "loyal"],
        "trigger_condition": "동일 카테고리 구매 후 30일 경과",
        "target_condition": "최근 구매 카테고리 재구매 가능성이 높은 고객"
    })
    campaigns.append({
        "id": "C06",
        "name": "크로스셀 추천 캠페인",
        "channel": "Email",
        "goal": "Cross-sell",
        "entry_stage": "second_purchase",
        "applicable_stages": ["second_purchase", "loyal"],
        "trigger_condition": "특정 상품 A 구매 후 10일 뒤",
        "target_condition": "상품 A 구매 고객"
    })
    campaigns.append({
        "id": "C07",
        "name": "휴면임박 Push 알림",
        "channel": "Push",
        "goal": "이탈 방지",
        "entry_stage": "churn_risk",
        "applicable_stages": ["churn_risk"],
        "trigger_condition": "days_since_last_purchase >= 90 AND days_since_last_login < 180",
        "target_condition": "3개월 이상 미구매 고객"
    })
    campaigns.append({
        "id": "C08",
        "name": "휴면 방지 재방문 이메일",
        "channel": "Email",
        "goal": "휴면 고객 재활성",
        "entry_stage": "churned",
        "applicable_stages": ["churned"],
        "trigger_condition": "days_since_last_login >= 180",
        "target_condition": "6개월 이상 미로그인 고객"
    })
    campaigns.append({
        "id": "C09",
        "name": "VIP 전용 10% 쿠폰",
        "channel": "Email",
        "goal": "충성 고객 리워드",
        "entry_stage": "loyal",
        "applicable_stages": ["loyal"],
        "trigger_condition": "purchases_last_12m >= 5",
        "target_condition": "연간 다회 구매 VIP 고객"
    })
    campaigns.append({
        "id": "C10",
        "name": "관심 카테고리 개인화 추천",
        "channel": "Push",
        "goal": "관심 기반 탐색 강화",
        "entry_stage": "explore",
        "applicable_stages": ["explore"],
        "trigger_condition": "특정 카테고리 조회 3회 이상 AND 미구매",
        "target_condition": "관심 카테고리만 보고 떠나는 고객"
    })

    # --- 추가 더미: 패턴 기반으로 40개 더 생성 (이름/조건만 약간씩 변경) ---
    # Stage 라운딩용 리스트
    stage_cycle = ["signup", "explore", "first_purchase", "second_purchase", "loyal", "churn_risk", "churned"]
    channels = ["Email", "Push", "Kakao", "SMS"]

    for i in range(11, 51):
        stage_key = stage_cycle[(i - 11) % len(stage_cycle)]
        # representative applicable stages: entry + 하나 확장
        stage_index = [s["key"] for s in JOURNEY_STAGES].index(stage_key)
        applicable = [stage_key]
        if stage_index + 1 < len(JOURNEY_STAGES):
            applicable.append(JOURNEY_STAGES[stage_index + 1]["key"])

        campaigns.append({
            "id": f"C{i:02d}",
            "name": f"Generic CRM Campaign #{i}",
            "channel": channels[(i - 11) % len(channels)],
            "goal": "Generic Nurture" if stage_key in ["signup", "explore"] else "Retention",
            "entry_stage": stage_key,
            "applicable_stages": applicable,
            "trigger_condition": f"(더미) Stage={stage_key}, rule set #{i}",
            "target_condition": "(더미) Segment rule 정의됨"
        })

    return campaigns


# =========================================
# 3. Journey 매핑 헬퍼
# =========================================
def map_campaigns_by_stage(campaigns):
    """
    entry_stage 기준으로 캠페인들을 묶어줌.
    또, stage_key가 정의 밖이면 무시.
    """
    result = {s["key"]: [] for s in JOURNEY_STAGES}
    for c in campaigns:
        key = c.get("entry_stage")
        if key in result:
            result[key].append(c)
    return result


# =========================================
# 4. 상단 헤더
# =========================================
st.markdown(
    """
<div class="app-header">
  <h1>🧭 CRM Journey Mapper — Prototype</h1>
  <p>Salesforce 등에서 캠페인을 불러와 고객 여정(회원가입 → 탐색 → 구매 → 재구매 → 이탈/휴면) 상에 어떻게 배치되는지 한눈에 보여주는 프로토타입입니다.</p>
</div>
""",
    unsafe_allow_html=True,
)

# 세션 상태 초기화
if "campaigns" not in st.session_state:
    st.session_state["campaigns"] = None
if "analyzed" not in st.session_state:
    st.session_state["analyzed"] = False


# =========================================
# 5. 레이아웃 구성 (좌: 가져오기 / 우: Journey)
# =========================================
left_col, right_col = st.columns([1.1, 1.9])

# -----------------------------
# 왼쪽: 캠페인 가져오기 영역
# -----------------------------
with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">1. 캠페인 가져오기 (API 시뮬레이션)</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-sub">실제 운영 시에는 Salesforce/CRM API에서 현재 활성 캠페인 리스트를 가져오는 영역입니다. 지금은 더미 50개를 불러옵니다.</div>',
        unsafe_allow_html=True
    )

    if st.button("🔄 캠페인 가져오기", type="primary", use_container_width=True):
        st.session_state["campaigns"] = load_dummy_campaigns()
        st.session_state["analyzed"] = False
        st.success("현재 활성 캠페인 50개를 불러왔습니다. 아래 리스트를 확인하세요.")

    campaigns = st.session_state["campaigns"]

    if campaigns:
        st.markdown("<hr style='border:0;border-top:1px solid #374151;margin:10px 0 8px 0;'>", unsafe_allow_html=True)
        st.markdown("##### 📋 불러온 캠페인 리스트", unsafe_allow_html=True)

        df = pd.DataFrame([
            {
                "ID": c["id"],
                "캠페인명": c["name"],
                "채널": c["channel"],
                "대표 여정 단계(entry)": STAGE_NAME_MAP.get(c["entry_stage"], c["entry_stage"]),
                "목적(goal)": c["goal"],
                "트리거 조건": c["trigger_condition"],
                "타겟 조건": c["target_condition"],
            }
            for c in campaigns
        ])

        st.dataframe(df, use_container_width=True, height=320)

        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("📊 이 캠페인들로 Journey 분석하기", type="secondary", use_container_width=True):
            st.session_state["analyzed"] = True

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# 오른쪽: Journey 분석 영역
# -----------------------------
with right_col:
    st.markdown('<div class="card-light">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">2. 고객 여정 상의 캠페인 배치</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-sub">회원가입 → 탐색 → 구매 → 재구매 → 활성/충성 → 이탈임박 → 휴면/이탈 여정 위에, 각 캠페인이 어디서 시작되고 어떤 구간까지 영향을 미치는지 시각화합니다.</div>',
        unsafe_allow_html=True
    )

    campaigns = st.session_state["campaigns"]
    analyzed = st.session_state["analyzed"]

    if not campaigns:
        st.info("왼쪽에서 먼저 캠페인을 가져온 뒤, 분석 버튼을 눌러주세요.")
    elif not analyzed:
        st.info("캠페인 리스트 아래의 **[📊 이 캠페인들로 Journey 분석하기]** 버튼을 눌러 여정 분석을 실행하세요.")
    else:
        # --- Journey 상단 메타 ---
        total = len(campaigns)
        by_stage = map_campaigns_by_stage(campaigns)
        st.markdown("<br/>", unsafe_allow_html=True)

        meta_cols = st.columns(3)
        with meta_cols[0]:
            st.markdown(f'<div class="meta-pill">총 캠페인 수: <b>{total}</b></div>', unsafe_allow_html=True)
        with meta_cols[1]:
            stage_counts = ", ".join([
                f"{STAGE_NAME_MAP[k]} {len(v)}개"
                for k, v in by_stage.items()
                if len(v) > 0
            ]) or "매핑된 캠페인 없음"
            st.markdown(f'<div class="meta-pill">단계별 분포: {stage_counts}</div>', unsafe_allow_html=True)
        with meta_cols[2]:
            st.markdown('<div class="meta-pill">시각화 방식: Entry 기준 + 영향 범위</div>', unsafe_allow_html=True)

        st.markdown("<hr style='border:0;border-top:1px solid #e5e7eb;margin:10px 0 12px 0;'>", unsafe_allow_html=True)

        # --- Journey 타임라인 (상단 라인) ---
        st.markdown("###### 🔍 Journey 타임라인 (Anchor 기준)")
        st.markdown('<div class="journey-row">', unsafe_allow_html=True)

        for idx, stage in enumerate(JOURNEY_STAGES):
            key = stage["key"]
            name = stage["name"]
            label = stage["label"]
            cnt = len(by_stage.get(key, []))

            st.markdown(
                f"""
<div class="journey-stage">
  <div class="journey-stage-label">{label}</div>
  <div class="journey-stage-name">{name}</div>
  <div class="journey-stage-chip">{cnt}개 캠페인</div>
</div>
""",
                unsafe_allow_html=True
            )

            # 단계 사이 화살표
            if idx < len(JOURNEY_STAGES) - 1:
                st.markdown('<div class="journey-arrow">➜</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        # --- 단계별 상세 캠페인 카드 ---
        st.markdown("###### 🧩 단계별 캠페인 상세 (Entry 기준)")

        for stage in JOURNEY_STAGES:
            key = stage["key"]
            name = stage["name"]
            stage_campaigns = by_stage.get(key, [])

            if not stage_campaigns:
                # 캠페인 없는 단계도 보여주고 싶으면 아래 주석 제거
                # st.markdown(f"**{name}** 단계: 매핑된 캠페인 없음")
                continue

            st.markdown(f"**{name}** 단계", unsafe_allow_html=True)
            cols = st.columns(2)

            # 왼쪽: 간단 요약
            with cols[0]:
                st.write(f"- Entry 기준 캠페인 수: **{len(stage_campaigns)}개**")
                # 영향을 받는 후행 스테이지 집계
                affected = set()
                for c in stage_campaigns:
                    for s in c.get("applicable_stages", []):
                        if s != key:
                            affected.add(STAGE_NAME_MAP.get(s, s))
                if affected:
                    st.write(f"- 이 단계에서 시작해 영향을 주는 후행 구간: {', '.join(sorted(affected))}")
                else:
                    st.write("- 이 단계에서만 작동하는 캠페인")

            # 오른쪽: 캠페인 리스트
            with cols[1]:
                st.markdown('<div class="campaign-list">', unsafe_allow_html=True)
                for c in stage_campaigns:
                    tag_html = f"""
<div class="campaign-tag">
  <span>{c['id']}</span>
  <span>|</span>
  <span>{c['channel']}</span>
</div>
"""
                    st.markdown(
                        f"""
<div>
  <div class="campaign-item-title">{c['name']}</div>
  <div class="campaign-item-meta">
    {tag_html}
    <br/>🎯 목적: {c['goal']}
    <br/>⚙️ 트리거: {c['trigger_condition']}
    <br/>👥 타겟: {c['target_condition']}
    <br/>📍 영향 범위: {", ".join([STAGE_NAME_MAP.get(s, s) for s in c.get("applicable_stages", [])])}
  </div>
  <hr style="border:0;border-top:1px dashed #4b5563; margin:7px 0 6px 0;"/>
</div>
""",
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
