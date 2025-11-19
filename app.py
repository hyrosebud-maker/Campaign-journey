import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ---------------------------------
# 0. 캠페인 데이터 (47개, 한글명)
# ---------------------------------

def build_campaign_data():
    base = datetime(2025, 11, 1)

    raw = [
        ("CMP001", "회원가입 환영 이메일 시리즈",           "Email",        "event", False, "visit",          "common",  "CRM"),
        ("CMP002", "신규 앱 설치 푸시 알림",               "App Push",     "event", False, "visit",          "common",  "CRM"),
        ("CMP003", "주간 디지털 전단지 이메일",             "Email",        "batch", True,  "browse",        "common",  "CRM"),
        ("CMP004", "급여일 할인 프로모션 SMS",              "SMS",          "batch", True,  "purchase_intent","common", "CRM"),
        ("CMP005", "신선식품 가격 인하 푸시 알림",         "App Push",     "event", False, "pdp",            "common", "CRM"),
        ("CMP006", "장바구니 이탈 리마인드 이메일",         "Email",        "event", False, "add_to_cart",   "common",  "CRM"),
        ("CMP007", "장바구니 이탈 카카오톡 알림",           "KakaoTalk",    "event", False, "add_to_cart",   "common",  "CRM"),
        ("CMP008", "결제 이탈 리마인드 이메일",             "Email",        "event", False, "checkout",      "common",  "CRM"),
        ("CMP009", "첫 구매 쿠폰 제공 이메일",              "Email",        "event", False, "purchase",      "common",  "CRM"),
        ("CMP010", "상품 리뷰 작성 요청 이메일",            "Email",        "event", False, "retention",     "common",  "CRM"),
        ("CMP011", "밀키트 교차판매 추천 이메일",           "Email",        "batch", True,  "nth_purchase",  "loyalty", "CRM"),
        ("CMP012", "생필품 재구매 푸시 알림",               "App Push",     "event", False, "nth_purchase",  "loyalty", "CRM"),
        ("CMP013", "30일 비활성 고객 윈백 이메일",          "Email",        "event", False, "churn_risk",    "churn",   "CRM"),
        ("CMP014", "60일 비활성 고객 카카오 윈백",          "KakaoTalk",    "event", False, "churn_risk",    "churn",   "CRM"),
        ("CMP015", "VIP 등급 승급 안내 이메일",             "Email",        "event", False, "loyalty",       "loyalty", "CRM"),
        ("CMP016", "VIP 전용 선공개 푸시 알림",             "App Push",     "batch", True,  "loyalty",       "loyalty", "CRM"),
        ("CMP017", "생일 축하 쿠폰 이메일",                 "Email",        "batch", True,  "retention",     "loyalty", "CRM"),
        ("CMP018", "급여일 정육 묶음 메타 광고",            "Meta Ads",     "batch", True,  "purchase_intent","common","Paid Media"),
        ("CMP019", "브랜드 인지도 유튜브 캠페인",           "YouTube",      "batch", True,  "visit",         "common","Paid Media"),
        ("CMP020", "브랜드 키워드 구글 검색 광고",          "Google Ads",   "batch", True,  "visit",         "common","Paid Media"),
        ("CMP021", "오프라인 매장 오픈 지오 푸시",          "App Push",     "batch", True,  "visit",         "common","CRM"),
        ("CMP022", "비 오는 날 따뜻한 음식 추천 푸시",      "App Push",     "event", False, "pdp",           "common","CRM"),
        ("CMP023", "점심시간 벤토 인앱 배너",               "In-app Banner","batch", True,  "browse",       "common","Onsite"),
        ("CMP024", "야식 시간 푸시 캠페인",                 "App Push",     "event", False, "purchase",      "common","CRM"),
        ("CMP025", "레시피 뉴스레터 이메일",                "Email",        "batch", True,  "browse",       "common","CRM"),
        ("CMP026", "영수증 기반 회원 전환 SMS",             "SMS",          "batch", True,  "visit",         "common","CRM"),
        ("CMP027", "앱 온보딩 튜토리얼 캐러셀",             "In-app Banner","event", False,"visit",         "common","Onsite"),
        ("CMP028", "주말 가족팩 메타 광고",                 "Meta Ads",     "batch", True,  "purchase_intent","common","Paid Media"),
        ("CMP029", "2시간 한정 플래시 세일 푸시",           "App Push",     "event", False, "purchase",      "common","CRM"),
        ("CMP030", "무료 배송 조건 안내 이메일",            "Email",        "event", False, "checkout",      "common","CRM"),
        ("CMP031", "관심상품 가격 인하 푸시",               "App Push",     "event", False, "pdp",           "common","CRM"),
        ("CMP032", "위시리스트 재입고 알림 이메일",         "Email",        "event", False, "add_to_cart",   "common","CRM"),
        ("CMP033", "멤버 전용 화요일 할인 이메일",          "Email",        "batch", True,  "nth_purchase",  "loyalty","CRM"),
        ("CMP034", "스캔 앤 고 기능 안내 푸시",             "App Push",     "event", False, "visit",         "common","CRM"),
        ("CMP035", "냉동식품 리마케팅 디스플레이 광고",    "Display Ads",  "batch", True,  "browse",       "common","Paid Media"),
        ("CMP036", "결제 단계 디저트 업셀 이메일",          "Email",        "event", False, "checkout",      "loyalty","CRM"),
        ("CMP037", "N번째 구매 스탬프 푸시",                "App Push",     "event", False, "nth_purchase",  "loyalty","CRM"),
        ("CMP038", "정기 구독/리필 리마인더 이메일",        "Email",        "event", False, "nth_purchase",  "loyalty","CRM"),
        ("CMP039", "180일 휴면 고객 빅쿠폰 이메일",          "Email",        "event", False, "churned",       "churn","CRM"),
        ("CMP040", "건강한 식단 프로그램 이메일 시리즈",    "Email",        "batch", True,  "browse",       "common","CRM"),
        ("CMP041", "고가 장바구니 교차판매 이메일",         "Email",        "batch", True,  "loyalty",       "loyalty","CRM"),
        ("CMP042", "2차 구매 미발생 신규고객 윈백 이메일",  "Email",        "event", False, "churn_risk",    "churn","CRM"),
        ("CMP043", "상위 5% 고객 서프라이즈 기프트 푸시",  "App Push",     "batch", True,  "loyalty",       "loyalty","CRM"),
        ("CMP044", "주말 브런치 카테고리 추천 이메일",      "Email",        "batch", True,  "browse",       "loyalty","CRM"),
        ("CMP045", "연말연시 선물세트 메타 광고",           "Meta Ads",     "batch", True,  "purchase_intent","common","Paid Media"),
        ("CMP046", "저RFM 고객 업셀 카카오톡",              "KakaoTalk",    "batch", True,  "nth_purchase",  "loyalty","CRM"),
        ("CMP047", "2+1 묶음 프로모션 이메일",              "Email",        "batch", True,  "nth_purchase",  "loyalty","CRM"),
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


# ---------------------------------
# 1. Journey 정의 / 매핑
# ---------------------------------

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
        "onboarding":     "가입",
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


# ---------------------------------
# 2. 라벨 행(row) 자동 배정 (캠페인명)
# ---------------------------------

def assign_label_rows(label_items, base_y=160, char_width=9, row_gap=22):
    rows_right_edge = []
    placements = []
    padding = 8

    for item in sorted(label_items, key=lambda d: d["x"]):
        x = float(item["x"])
        text = str(item["text"])
        width = len(text) * char_width
        left = x - width / 2 - padding
        right = x + width / 2 + padding

        row_idx = 0
        while row_idx < len(rows_right_edge) and left <= rows_right_edge[row_idx]:
            row_idx += 1

        if row_idx == len(rows_right_edge):
            rows_right_edge.append(right)
        else:
            rows_right_edge[row_idx] = right

        y = base_y + row_idx * row_gap
        placements.append((item, row_idx, y))

    max_row = len(rows_right_edge) - 1 if rows_right_edge else 0
    return placements, max_row, row_gap


# ---------------------------------
# 3. Journey SVG 생성
# ---------------------------------

STORY_SEQUENCE = [
    "CMP019", "CMP020", "CMP026",      # 가입 이전
    "CMP021", "CMP002", "CMP027", "CMP001", "CMP034",           # 가입 ~ 탐색
    "CMP003", "CMP025", "CMP040", "CMP023", "CMP035",           # 탐색 ~ 고려
    "CMP022", "CMP005", "CMP031", "CMP032", "CMP006", "CMP007",
    "CMP008", "CMP030", "CMP004", "CMP018", "CMP028", "CMP045",
    "CMP024", "CMP029", "CMP009",                                    # 고려 ~ 첫 구매
    "CMP010",                                                        # 첫 구매 ~ 구매 후 경험
    "CMP012", "CMP011", "CMP033", "CMP047", "CMP037", "CMP038",
    "CMP036", "CMP046",                                             # 구매 후 경험 ~ 재구매
    "CMP015", "CMP016", "CMP043", "CMP041", "CMP044", "CMP017",     # 재구매 ~ 로열티
    "CMP042", "CMP013", "CMP014", "CMP039",                         # 로열티 ~ 휴면/재활성화
]

STORY_INDEX = {cid: i for i, cid in enumerate(STORY_SEQUENCE)}
PRE_SIGNUP_IDS = {"CMP019", "CMP020", "CMP026"}


def build_journey_svg(df: pd.DataFrame) -> str:
    df = df.copy()
    df["journey_stage"] = df.apply(map_row_to_journey_stage, axis=1)
    df = df[df["journey_stage"].notnull()]
    if df.empty:
        return "<p>표시할 여정 캠페인이 없습니다.</p>"

    # --- 스토리 순서 기반 x좌표 ---
    df["story_idx"] = df["campaign_id"].map(STORY_INDEX)
    df = df.sort_values("story_idx").reset_index(drop=True)

    n = len(df)
    if n <= 1:
        n = 2

    # 🔧 폭/마진 조정 (왼쪽 정렬)
    width = 1400
    margin_left = 0       # 컨테이너 왼쪽에 딱 붙게
    margin_right = 40
    baseline_y = 130

    step = (width - margin_left - margin_right) / (n - 1)
    df["x"] = df["story_idx"].apply(lambda i: margin_left + i * step)

    # --- 스테이지 x좌표 (캠페인 분포 기반, 가입은 PRE_SIGNUP 제외) ---
    stage_x = {}
    for stage in JOURNEY_LINE:
        if stage == "onboarding":
            sub = df[(df["journey_stage"] == "onboarding") & (~df["campaign_id"].isin(PRE_SIGNUP_IDS))]
        else:
            sub = df[df["journey_stage"] == stage]

        if not sub.empty:
            stage_x[stage] = sub["x"].mean()

    # 빈 스테이지는 보간
    for i, stage in enumerate(JOURNEY_LINE):
        if stage in stage_x:
            continue
        left = right = None
        for j in range(i-1, -1, -1):
            if JOURNEY_LINE[j] in stage_x:
                left = stage_x[JOURNEY_LINE[j]]
                break
        for j in range(i+1, len(JOURNEY_LINE)):
            if JOURNEY_LINE[j] in stage_x:
                right = stage_x[JOURNEY_LINE[j]]
                break
        if left is not None and right is not None:
            stage_x[stage] = (left + right) / 2
        elif left is not None:
            stage_x[stage] = left + step
        elif right is not None:
            stage_x[stage] = right - step
        else:
            stage_x[stage] = margin_left + i * step

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

    # --- 캠페인 라벨 배치 계산 ---
    label_base_y = baseline_y + 30
    label_items = []
    for _, r in df.iterrows():
        label_items.append({"x": float(r["x"]), "text": str(r["campaign_name"]), "row": r})

    placements, max_row, row_gap = assign_label_rows(
        label_items,
        base_y=label_base_y,
        char_width=9,
        row_gap=22,
    )
    height = label_base_y + (max_row + 1) * row_gap + 60

    svg = []
    # ★ 여기서 preserveAspectRatio 로 SVG 를 항상 왼쪽 기준(xMin)으로 붙임
    svg.append(
        f'<svg width="100%" height="{height}" '
        f'viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMin meet" '
        f'xmlns="http://www.w3.org/2000/svg">'
    )

    # 1) 채널 Legend
    legend_y = 30
    x_cursor = margin_left
    svg.append(
        f'<text x="{margin_left}" y="{legend_y-12}" font-size="12" fill="#111">채널 Legend</text>'
    )
    x_cursor += 90
    legend_x_gap = 120
    for ch, color in channel_colors.items():
        svg.append(
            f'<rect x="{x_cursor}" y="{legend_y-10}" width="12" height="12" fill="{color}" />'
        )
        svg.append(
            f'<text x="{x_cursor+18}" y="{legend_y}" font-size="11" fill="#111">{ch}</text>'
        )
        x_cursor += legend_x_gap

    # 2) 기본 여정 라인
    x_min = df["x"].min()
    x_max = df["x"].max()
    svg.append(
        f'<line x1="{x_min}" y1="{baseline_y}" x2="{x_max}" y2="{baseline_y}" '
        'stroke="#444" stroke-width="4" />'
    )

    # 3) 스테이지 라벨 (겹침 방지)
    stage_char_width = 9
    stage_gap = 20
    outer_margin = 10

    centers = []
    widths = []

    for stage in JOURNEY_LINE:
        label = pretty_stage_name(stage)
        centers.append(stage_x[stage])
        widths.append(len(label) * stage_char_width)

    # 왼쪽->오른쪽
    min_center = x_min + widths[0] / 2 + outer_margin
    centers[0] = max(centers[0], min_center)
    for i in range(1, len(JOURNEY_LINE)):
        min_center = centers[i-1] + (widths[i-1] + widths[i]) / 2 + stage_gap
        if centers[i] < min_center:
            centers[i] = min_center

    # 오른쪽->왼쪽
    max_center = x_max - widths[-1] / 2 - outer_margin
    centers[-1] = min(centers[-1], max_center)
    for i in range(len(JOURNEY_LINE)-2, -1, -1):
        max_center = centers[i+1] - (widths[i+1] + widths[i]) / 2 - stage_gap
        if centers[i] > max_center:
            centers[i] = max_center

    for idx, stage in enumerate(JOURNEY_LINE):
        stage_x[stage] = centers[idx]

    for i, stage in enumerate(JOURNEY_LINE):
        sx = centers[i]
        sy = baseline_y
        label = pretty_stage_name(stage)
        svg.append(
            f'<rect x="{sx-8}" y="{sy-8}" width="16" height="16" fill="#444" rx="3" />'
        )
    #
        svg.append(
            f'<text x="{sx}" y="{sy-22}" text-anchor="middle" '
            f'font-size="13" fill="#111">{label}</text>'
        )

    # 4) 전 여정 영향 화살표
    arrow_specs = [
        {
            "label": "브랜드 인지도/상단 퍼널 (CMP019, CMP020)",
            "color": "#7f7fff",
            "start_stage": "onboarding",
            "end_stage": "consider",
            "row": 0,
        },
        {
            "label": "급여일 프로모션 (CMP004, CMP018, CMP028, CMP045)",
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

    arrow_base_y = baseline_y - 40
    arrow_row_gap = 18

    for spec in arrow_specs:
        y = arrow_base_y - spec["row"] * arrow_row_gap
        sx = stage_x[spec["start_stage"]]
        ex = stage_x[spec["end_stage"]]
        color = spec["color"]
        svg.append(
            f'<line x1="{sx}" y1="{y}" x2="{ex}" y2="{y}" '
            f'stroke="{color}" stroke-width="2" />'
        )
        svg.append(
            f'<path d="M {ex} {y} L {ex-7} {y-3} L {ex-7} {y+3} Z" fill="{color}" />'
        )
        mid = (sx + ex) / 2
        svg.append(
            f'<text x="{mid}" y="{y-3}" text-anchor="middle" '
            f'font-size="10" fill="{color}">{spec["label"]}</text>'
        )

    # 5) 47개 캠페인 점 + 라벨
    for item, row_idx, label_y in placements:
        r = item["row"]
        x = float(item["x"])
        color = channel_colors.get(r["channel"], "#666666")
        line_y2 = label_y - 6

        svg.append(
            f'<line x1="{x}" y1="{baseline_y+8}" x2="{x}" y2="{line_y2}" '
            'stroke="#bbbbbb" stroke-width="1" />'
        )
        svg.append(f'<circle cx="{x}" cy="{baseline_y}" r="4" fill="{color}" />')
        svg.append(
            f'<text x="{x}" y="{label_y}" text-anchor="middle" '
            'font-size="9" fill="#222">'
            f'{r["campaign_name"]}</text>'
        )

    svg.append("</svg>")
    return "".join(svg)


# ---------------------------------
# 4. Streamlit Layout
# ---------------------------------

def main():
    st.set_page_config(page_title="A사 마케팅 캠페인 Journey MAP", layout="wide")

    # 컨테이너 좌우 padding 최소화
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("A사 마케팅 캠페인 Journey MAP")

    df = build_campaign_data()
    last_updated = datetime.now()

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        if st.button("캠페인 가져오기 (API 호출)", help="데모용: 현재는 고정 데이터 사용"):
            st.success("데모용 고정 데이터 기준으로 캠페인 정보를 불러왔습니다.")
    with col_info:
        ts = last_updated.strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"**마지막 캠페인 동기화 시각:** {ts}")

    with st.expander("Raw Campaign List (47개)"):
        st.dataframe(df, use_container_width=True)

    tab1, tab2 = st.tabs(["🧭 Journey View", "📅 Calendar View"])

    # -------- Journey View --------
    with tab1:
        st.subheader("고객 여정 기반 캠페인 맵")

        base_df = df[df["view_assignment"].isin(["Journey", "Both"])].copy()

        with st.expander("필터"):
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

        svg = build_journey_svg(filtered)
        st.markdown(svg, unsafe_allow_html=True)

        st.markdown("### 선택된 캠페인 목록")
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
            ],
            use_container_width=True,
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
            ],
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
