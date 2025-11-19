import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# -----------------------------
# 0. 기본 데이터 세팅
# -----------------------------

def build_campaign_data():
    base = datetime(2025, 11, 1)

    # id, 한국어 캠페인명, 채널, 트리거, 배치여부, primary_objective, journey_branch, 캠페인 타입
    raw = [
        ("CMP001", "회원가입 환영 이메일 시리즈", "Email",       "event", False, "visit",          "common",  "CRM"),
        ("CMP002", "신규 앱 설치 푸시 알림",       "App Push",    "event", False, "visit",          "common",  "CRM"),
        ("CMP003", "주간 디지털 전단지 이메일",     "Email",       "batch", True,  "browse",        "common",  "CRM"),
        ("CMP004", "급여일 할인 프로모션 SMS",      "SMS",         "batch", True,  "purchase_intent","common", "CRM"),
        ("CMP005", "신선식품 가격 인하 푸시 알림", "App Push",    "event", False, "pdp",            "common", "CRM"),
        ("CMP006", "장바구니 이탈 리마인드 이메일", "Email",       "event", False, "add_to_cart",   "common",  "CRM"),
        ("CMP007", "장바구니 이탈 카카오톡 알림",   "KakaoTalk",   "event", False, "add_to_cart",   "common",  "CRM"),
        ("CMP008", "결제 이탈 리마인드 이메일",     "Email",       "event", False, "checkout",      "common",  "CRM"),
        ("CMP009", "첫 구매 쿠폰 제공 이메일",      "Email",       "event", False, "purchase",      "common",  "CRM"),
        ("CMP010", "상품 리뷰 작성 요청 이메일",    "Email",       "event", False, "retention",     "common",  "CRM"),
        ("CMP011", "밀키트 교차판매 추천 이메일",   "Email",       "batch", True,  "nth_purchase",  "loyalty", "CRM"),
        ("CMP012", "생필품 재구매 푸시 알림",       "App Push",    "event", False, "nth_purchase",  "loyalty", "CRM"),
        ("CMP013", "30일 비활성 고객 윈백 이메일",  "Email",       "event", False, "churn_risk",    "churn",   "CRM"),
        ("CMP014", "60일 비활성 고객 카카오 윈백",  "KakaoTalk",   "event", False, "churn_risk",    "churn",   "CRM"),
        ("CMP015", "VIP 등급 승급 안내 이메일",     "Email",       "event", False, "loyalty",       "loyalty", "CRM"),
        ("CMP016", "VIP 전용 선공개 푸시 알림",     "App Push",    "batch", True,  "loyalty",       "loyalty", "CRM"),
        ("CMP017", "생일 축하 쿠폰 이메일",         "Email",       "batch", True,  "retention",     "loyalty", "CRM"),
        ("CMP018", "급여일 정육 묶음 메타 광고",    "Meta Ads",    "batch", True,  "purchase_intent","common", "Paid Media"),
        ("CMP019", "브랜드 인지도 유튜브 캠페인",   "YouTube",     "batch", True,  "visit",         "common", "Paid Media"),
        ("CMP020", "브랜드 키워드 구글 검색 광고",  "Google Ads",  "batch", True,  "visit",         "common", "Paid Media"),
        ("CMP021", "오프라인 매장 오픈 지오 푸시", "App Push",    "batch", True,  "visit",         "common", "CRM"),
        ("CMP022", "비 오는 날 따뜻한 음식 추천 푸시","App Push","event", False, "pdp",          "common", "CRM"),
        ("CMP023", "점심시간 벤토 인앱 배너",       "In-app Banner","batch", True, "browse",       "common", "Onsite"),
        ("CMP024", "야식 시간 푸시 캠페인",         "App Push",    "event", False, "purchase",      "common", "CRM"),
        ("CMP025", "레시피 뉴스레터 이메일",        "Email",       "batch", True,  "browse",       "common", "CRM"),
        ("CMP026", "영수증 기반 회원 전환 SMS",     "SMS",         "batch", True,  "visit",         "common", "CRM"),
        ("CMP027", "앱 온보딩 튜토리얼 캐러셀",     "In-app Banner","event", False,"visit",        "common", "Onsite"),
        ("CMP028", "주말 가족팩 메타 광고",         "Meta Ads",    "batch", True,  "purchase_intent","common","Paid Media"),
        ("CMP029", "2시간 한정 플래시 세일 푸시",   "App Push",    "event", False, "purchase",      "common", "CRM"),
        ("CMP030", "무료 배송 조건 안내 이메일",    "Email",       "event", False, "checkout",      "common", "CRM"),
        ("CMP031", "관심상품 가격 인하 푸시",       "App Push",    "event", False, "pdp",           "common", "CRM"),
        ("CMP032", "위시리스트 재입고 알림 이메일","Email",       "event", False, "add_to_cart",   "common", "CRM"),
        ("CMP033", "멤버 전용 화요일 할인 이메일",  "Email",       "batch", True,  "nth_purchase",  "loyalty", "CRM"),
        ("CMP034", "스캔 앤 고 기능 안내 푸시",     "App Push",    "event", False, "visit",         "common", "CRM"),
        ("CMP035", "냉동식품 리마케팅 디스플레이 광고","Display Ads","batch",True,"browse","common","Paid Media"),
        ("CMP036", "결제 단계 디저트 업셀 이메일",  "Email",       "event", False, "checkout",      "loyalty","CRM"),
        ("CMP037", "N번째 구매 스탬프 푸시",        "App Push",    "event", False, "nth_purchase",  "loyalty","CRM"),
        ("CMP038", "정기 구독/리필 리마인더 이메일","Email",       "event", False, "nth_purchase",  "loyalty","CRM"),
        ("CMP039", "180일 휴면 고객 빅쿠폰 이메일","Email",       "event", False, "churned",       "churn", "CRM"),
        ("CMP040", "건강한 식단 프로그램 이메일 시리즈","Email","batch",True,"browse","common","CRM"),
        ("CMP041", "고가 장바구니 교차판매 이메일","Email",       "batch", True,  "loyalty",       "loyalty","CRM"),
        ("CMP042", "2차 구매 미발생 신규고객 윈백 이메일","Email","event",False,"churn_risk","churn","CRM"),
        ("CMP043", "상위 5% 고객 서프라이즈 기프트 푸시","App Push","batch",True,"loyalty","loyalty","CRM"),
        ("CMP044", "주말 브런치 카테고리 추천 이메일","Email",    "batch", True,  "browse",        "loyalty","CRM"),
        ("CMP045", "연말연시 선물세트 메타 광고",  "Meta Ads",    "batch", True,  "purchase_intent","common","Paid Media"),
        ("CMP046", "저RFM 고객 업셀 카카오톡",      "KakaoTalk",   "batch", True,  "nth_purchase",  "loyalty","CRM"),
        ("CMP047", "2+1 묶음 프로모션 이메일",      "Email",       "batch", True,  "nth_purchase",  "loyalty","CRM"),
    ]

    records = []
    for idx, row in enumerate(raw):
        cid, name, channel, trigger, is_batch, obj, branch, ctype = row
        start = base + timedelta(days=idx)
        end = start + timedelta(days=7 if is_batch else 1)

        if trigger == "event" and obj in [
            "visit","browse","pdp","add_to_cart","checkout","purchase",
            "retention","nth_purchase","churn_risk","churned","loyalty"
        ]:
            journey = True
        else:
            journey = False

        view_assignment = "Both" if (journey and is_batch) else ("Journey" if journey else "Calendar")

        records.append({
            "campaign_id": cid,
            "campaign_name": name,
            "channel": channel,
            "trigger_type": trigger,
            "is_batch_campaign": is_batch,
            "primary_objective": obj,
            "journey_branch": branch,
            "campaign_type": ctype,
            "start_datetime": start,
            "end_datetime": end,
            "view_assignment": view_assignment,
        })

    return pd.DataFrame(records)


# -----------------------------
# 1. Journey 정의 / 매핑
# -----------------------------

JOURNEY_LINE = [
    "onboarding",
    "explore",
    "consider",
    "first_purchase",
    "post_purchase",
    "repeat",
    "loyalty",
    "reactivation",
]

def pretty_stage_name(stage_key: str) -> str:
    mapping = {
        "onboarding":     "가입 & 온보딩",
        "explore":        "탐색",
        "consider":       "고려",
        "first_purchase": "첫 구매",
        "post_purchase":  "구매 후 경험",
        "repeat":         "재구매 (N차)",
        "loyalty":        "로열티",
        "reactivation":   "휴면/재활성화",
    }
    return mapping.get(stage_key, stage_key)

def map_row_to_journey_stage(row):
    obj = row["primary_objective"]
    branch = row["journey_branch"]

    if obj == "visit":
        return "onboarding"
    if obj == "browse":
        return "explore"
    if obj == "pdp":
        return "consider"
    if obj in ["add_to_cart", "checkout", "purchase"]:
        return "repeat" if branch == "loyalty" else "first_purchase"
    if obj == "retention":
        return "post_purchase"
    if obj == "nth_purchase":
        return "repeat"
    if obj == "loyalty":
        return "loyalty"
    if obj in ["churn_risk", "churned"]:
        return "reactivation"
    if obj == "purchase_intent":
        return "consider"
    return None

def campaign_group(row):
    obj = row["primary_objective"]
    branch = row["journey_branch"]

    if obj == "visit":
        return "온보딩/가입 캠페인"
    if obj in ["browse", "pdp"]:
        return "탐색/상품 관심 캠페인"
    if obj == "add_to_cart":
        return "장바구니 캠페인"
    if obj == "checkout":
        return "체크아웃/결제 직전 캠페인"
    if obj == "purchase" and branch == "common":
        return "첫 구매 유도 캠페인"
    if obj == "retention":
        return "구매 후 경험/리뷰 리텐션"
    if obj == "nth_purchase":
        return "재구매/구독/스탬프 캠페인"
    if obj == "loyalty":
        return "VIP/충성 고객 캠페인"
    if obj in ["churn_risk", "churned"]:
        return "이탈 임박/휴면 윈백 캠페인"
    if obj == "purchase_intent":
        return "프로모션/가격 혜택 캠페인"
    return "기타 캠페인"


# -----------------------------
# 2. Journey SVG 생성
#    - 여정 라인 위: 스테이지 + 전여정 화살표
#    - 여정 라인 아래: 그룹 라벨(굵게) + 캠페인명 세로 배치
# -----------------------------

def build_journey_svg(df: pd.DataFrame) -> str:
    df = df.copy()
    df["journey_stage"] = df.apply(map_row_to_journey_stage, axis=1)
    df = df[df["journey_stage"].notnull()]
    if df.empty:
        return "<p>표시할 여정 캠페인이 없습니다.</p>"

    # 스테이지 index
    stage_pos = {s: i for i, s in enumerate(JOURNEY_LINE)}
    df["stage_idx"] = df["journey_stage"].map(stage_pos)

    # 그룹 라벨 및 우선순위
    df["group_label"] = df.apply(campaign_group, axis=1)
    group_priority = {
        "온보딩/가입 캠페인": 0,
        "탐색/상품 관심 캠페인": 1,
        "장바구니 캠페인": 2,
        "체크아웃/결제 직전 캠페인": 3,
        "첫 구매 유도 캠페인": 4,
        "구매 후 경험/리뷰 리텐션": 5,
        "재구매/구독/스탬프 캠페인": 6,
        "VIP/충성 고객 캠페인": 7,
        "이탈 임박/휴면 윈백 캠페인": 8,
        "프로모션/가격 혜택 캠페인": 9,
        "기타 캠페인": 10,
    }

    info = df[["journey_stage", "group_label"]].drop_duplicates()
    info["priority"] = info["group_label"].map(lambda g: group_priority.get(g, 99))

    # 스테이지별 그룹 index
    group_index_map = {}
    for stage in JOURNEY_LINE:
        rows = info[info["journey_stage"] == stage].copy()
        if rows.empty:
            continue
        rows = rows.sort_values(["priority", "group_label"])
        for i, (_, r) in enumerate(rows.iterrows()):
            group_index_map[(stage, r["group_label"])] = i

    df["group_index"] = df.apply(
        lambda r: group_index_map.get((r["journey_stage"], r["group_label"]), 0),
        axis=1,
    )

    # 그룹 내 캠페인 순번
    df["lane_index"] = df.groupby(["journey_stage", "group_label"]).cumcount()

    max_group_index = int(df["group_index"].max())
    max_lane = int(df["lane_index"].max())

    # SVG 레이아웃
    width = 1300
    margin_left = 140
    margin_right = 40
    baseline_y = 80  # 여정 라인
    group_gap = 55   # 그룹 간 세로 간격
    line_to_group_gap = 30
    label_line_gap = 12

    height = (
        baseline_y
        + line_to_group_gap
        + (max_group_index + 1) * group_gap
        + (max_lane + 3) * label_line_gap
        + 20
    )

    n_stage = len(JOURNEY_LINE)
    if n_stage <= 1:
        gap = 200
    else:
        gap = (width - margin_left - margin_right) / (n_stage - 1)

    # 채널 색상
    channel_colors = {
        "Email": "#1f77b4",
        "App Push": "#ff7f0e",
        "KakaoTalk": "#ffcc00",
        "SMS": "#2ca02c",
        "Meta Ads": "#d62728",
        "YouTube": "#c61c29",
        "Google Ads": "#17becf",
        "In-app Banner": "#9467bd",
        "Display Ads": "#8c564b",
    }

    # 스테이지별 캠페인 수
    stage_counts = df.groupby("journey_stage")["campaign_id"].nunique().to_dict()

    svg = []
    svg.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')

    # 여정 라인
    x0 = margin_left
    x1 = margin_left + gap * (n_stage - 1)
    svg.append(
        f'<line x1="{x0}" y1="{baseline_y}" x2="{x1}" y2="{baseline_y}" '
        'stroke="#444" stroke-width="4" />'
    )

    # 스테이지 노드 + 텍스트
    for s in JOURNEY_LINE:
        idx = stage_pos[s]
        sx = margin_left + gap * idx
        sy = baseline_y
        count = stage_counts.get(s, 0)
        label = pretty_stage_name(s)

        svg.append(
            f'<rect x="{sx-7}" y="{sy-7}" width="14" height="14" fill="#444" rx="2" />'
        )
        svg.append(
            f'<text x="{sx}" y="{sy-20}" text-anchor="middle" '
            f'font-size="12" fill="#111">{label} ({count} 캠페인)</text>'
        )

    # 전 여정 영향 화살표 (스토리라인용)
    arrow_specs = [
        {
            "label": "브랜드 인지도/상단 퍼널 캠페인 (CMP019, CMP020)",
            "color": "#7f7fff",
            "start_stage": "onboarding",
            "end_stage": "consider",
            "row": 0,
        },
        {
            "label": "급여일 프로모션 캠페인 (CMP004, CMP018, CMP028, CMP045)",
            "color": "#ff7f7f",
            "start_stage": "consider",
            "end_stage": "repeat",
            "row": 1,
        },
        {
            "label": "식단/레시피 프로그램 (CMP025, CMP040)",
            "color": "#55aa77",
            "start_stage": "onboarding",
            "end_stage": "repeat",
            "row": 2,
        },
    ]

    arrow_base_y = baseline_y - 35
    arrow_row_gap = 16

    for spec in arrow_specs:
        y = arrow_base_y - spec["row"] * arrow_row_gap
        sx = margin_left + gap * stage_pos[spec["start_stage"]]
        ex = margin_left + gap * stage_pos[spec["end_stage"]]
        color = spec["color"]
        svg.append(
            f'<line x1="{sx}" y1="{y}" x2="{ex}" y2="{y}" '
            f'stroke="{color}" stroke-width="2" />'
        )
        # 화살촉
        svg.append(
            f'<path d="M {ex} {y} L {ex-6} {y-3} L {ex-6} {y+3} Z" fill="{color}" />'
        )
        mid = (sx + ex) / 2
        svg.append(
            f'<text x="{mid}" y="{y-2}" text-anchor="middle" '
            f'font-size="10" fill="{color}">{spec["label"]}</text>'
        )

    # 그룹 라벨 (굵게) + 캠페인 세로 배치
    # 그룹 라벨은 색/폰트 다르게
    for (stage, group), ginfo in df.groupby(["journey_stage", "group_label"]):
        idx = stage_pos[stage]
        sx = margin_left + gap * idx
        g_idx = int(ginfo["group_index"].iloc[0])
        group_top_y = baseline_y + line_to_group_gap + g_idx * group_gap

        svg.append(
            f'<text x="{sx}" y="{group_top_y}" text-anchor="middle" '
            f'font-size="11" fill="#aa0033" font-weight="bold">{group}</text>'
        )

    # 개별 캠페인들
    for _, row in df.iterrows():
        stage = row["journey_stage"]
        idx = stage_pos[stage]
        sx = margin_left + gap * idx
        g_idx = int(row["group_index"])
        lane_idx = int(row["lane_index"])
        group_top_y = baseline_y + line_to_group_gap + g_idx * group_gap
        # 첫 캠페인 라벨 y 위치
        label_y = group_top_y + 15 + lane_idx * label_line_gap
        line_y2 = label_y - 6

        color = channel_colors.get(row["channel"], "#666666")

        # 세로선
        svg.append(
            f'<line x1="{sx}" y1="{baseline_y+7}" x2="{sx}" y2="{line_y2}" '
            'stroke="#bbbbbb" stroke-width="1" />'
        )
        # 여정 선 상의 점
        svg.append(
            f'<circle cx="{sx}" cy="{baseline_y}" r="4" fill="{color}" />'
        )
        # 캠페인명 라벨
        svg.append(
            f'<text x="{sx}" y="{label_y}" text-anchor="middle" '
            'font-size="10" fill="#222">'
            f'{row["campaign_name"]}</text>'
        )

    # 채널 Legend (왼쪽 상단)
    legend_x = 20
    legend_y = 40
    svg.append(
        f'<text x="{legend_x}" y="{legend_y-10}" font-size="12" '
        'fill="#111">채널 Legend</text>'
    )
    ly = legend_y
    for ch, color in channel_colors.items():
        svg.append(
            f'<rect x="{legend_x}" y="{ly-9}" width="12" height="12" fill="{color}" />'
        )
        svg.append(
            f'<text x="{legend_x+18}" y="{ly}" font-size="11" fill="#111">{ch}</text>'
        )
        ly += 16

    svg.append("</svg>")
    return "".join(svg)


# -----------------------------
# 3. Streamlit Layout
# -----------------------------

def main():
    st.set_page_config(page_title="A사 마케팅 캠페인 Journey MAP", layout="wide")
    st.title("A사 마케팅 캠페인 Journey MAP")

    if "campaign_df" not in st.session_state:
        st.session_state["campaign_df"] = build_campaign_data()
        st.session_state["last_updated"] = datetime.now()

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        if st.button("캠페인 가져오기 (API 호출)"):
            st.session_state["campaign_df"] = build_campaign_data()
            st.session_state["last_updated"] = datetime.now()
            st.success("캠페인 메타데이터를 최신 상태로 갱신했습니다.")

    with col_info:
        ts = st.session_state["last_updated"].strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"**마지막 캠페인 동기화 시각:** {ts}")

    df = st.session_state["campaign_df"]

    with st.expander("Raw Campaign List (47개)"):
        st.dataframe(df)

    tab1, tab2 = st.tabs(["🧭 Journey View", "📅 Calendar View"])

    # -------- Journey View --------
    with tab1:
        st.subheader("고객 여정 기반 캠페인 맵")

        base_df = df[df["view_assignment"].isin(["Journey", "Both"])].copy()

        col1, col2 = st.columns([2, 1])

        with col1:
            svg = build_journey_svg(base_df)
            st.markdown(svg, unsafe_allow_html=True)

        with col2:
            st.markdown("### 필터 (테이블용)")
            channel_filter = st.multiselect(
                "채널 선택",
                sorted(base_df["channel"].unique()),
                default=sorted(base_df["channel"].unique()),
                key="channel_filter_journey",
            )
            branch_filter = st.multiselect(
                "브랜치 선택",
                ["common", "churn", "loyalty"],
                default=["common", "churn", "loyalty"],
                format_func=lambda x: {"common": "공통", "churn": "이탈", "loyalty": "충성"}[x],
                key="branch_filter_journey",
            )

            filtered = base_df[
                (base_df["channel"].isin(channel_filter))
                & (base_df["journey_branch"].isin(branch_filter))
            ].copy()

            st.markdown("### 선택된 조건의 캠페인 목록")
            st.dataframe(
                filtered[
                    [
                        "campaign_id",
                        "campaign_name",
                        "channel",
                        "primary_objective",
                        "journey_branch",
                        "is_batch_campaign",
                        "start_datetime",
                        "end_datetime",
                    ]
                ]
            )

    # -------- Calendar View --------
    with tab2:
        st.subheader("배치성 마케팅 캘린더 (테이블)")

        channel_filter_cal = st.multiselect(
            "채널 선택",
            sorted(df["channel"].unique()),
            default=sorted(df["channel"].unique()),
            key="channel_filter_calendar",
        )
        branch_filter_cal = st.multiselect(
            "브랜치 선택",
            ["common", "churn", "loyalty"],
            default=["common", "churn", "loyalty"],
            format_func=lambda x: {"common": "공통", "churn": "이탈", "loyalty": "충성"}[x],
            key="branch_filter_calendar",
        )

        calendar_df = df[
            (df["is_batch_campaign"])
            & (df["channel"].isin(channel_filter_cal))
            & (df["journey_branch"].isin(branch_filter_cal))
        ].copy()

        st.markdown("### 배치성 캠페인 목록")
        st.dataframe(
            calendar_df[
                [
                    "campaign_id",
                    "campaign_name",
                    "channel",
                    "primary_objective",
                    "journey_branch",
                    "start_datetime",
                    "end_datetime",
                ]
            ]
        )


if __name__ == "__main__":
    main()
