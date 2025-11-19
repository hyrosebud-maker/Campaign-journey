import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# -----------------------------
# 0. 기본 데이터 세팅
# -----------------------------

def build_campaign_data():
    base = datetime(2025, 11, 1)

    raw = [
        ("CMP001", "Welcome Email Series", "Email", "event", False, "visit", "common", "CRM"),
        ("CMP002", "New App Install Push", "App Push", "event", False, "visit", "common", "CRM"),
        ("CMP003", "Weekly Digital Flyer Email", "Email", "batch", True, "browse", "common", "CRM"),
        ("CMP004", "Payday Payday Promo SMS", "SMS", "batch", True, "purchase_intent", "common", "CRM"),
        ("CMP005", "Fresh Produce Price Drop Push", "App Push", "event", False, "pdp", "common", "CRM"),
        ("CMP006", "Cart Abandonment Email", "Email", "event", False, "add_to_cart", "common", "CRM"),
        ("CMP007", "Cart Abandonment Kakao", "KakaoTalk", "event", False, "add_to_cart", "common", "CRM"),
        ("CMP008", "Checkout Abandonment Email", "Email", "event", False, "checkout", "common", "CRM"),
        ("CMP009", "First Purchase Coupon Email", "Email", "event", False, "purchase", "common", "CRM"),
        ("CMP010", "Review Request Email", "Email", "event", False, "retention", "common", "CRM"),
        ("CMP011", "Cross-sell Ready Meal Email", "Email", "batch", True, "nth_purchase", "loyalty", "CRM"),
        ("CMP012", "Replenishment Staple Reminder Push", "App Push", "event", False, "nth_purchase", "loyalty", "CRM"),
        ("CMP013", "30-day Inactive Winback Email", "Email", "event", False, "churn_risk", "churn", "CRM"),
        ("CMP014", "60-day Inactive Winback Kakao", "KakaoTalk", "event", False, "churn_risk", "churn", "CRM"),
        ("CMP015", "VIP Tier Upgrade Email", "Email", "event", False, "loyalty", "loyalty", "CRM"),
        ("CMP016", "VIP Early Access Push", "App Push", "batch", True, "loyalty", "loyalty", "CRM"),
        ("CMP017", "Birthday Coupon Email", "Email", "batch", True, "retention", "loyalty", "CRM"),
        ("CMP018", "Payday Meat Bundle Meta Ads", "Meta Ads", "batch", True, "purchase_intent", "common", "Paid Media"),
        ("CMP019", "Brand Awareness YouTube Campaign", "YouTube", "batch", True, "visit", "common", "Paid Media"),
        ("CMP020", "Search Brand Keyword Google Ads", "Google Ads", "batch", True, "visit", "common", "Paid Media"),
        ("CMP021", "Store Opening Geo Push", "App Push", "batch", True, "visit", "common", "CRM"),
        ("CMP022", "Rainy Day Hot Food Push", "App Push", "event", False, "pdp", "common", "CRM"),
        ("CMP023", "Lunch-time Bento App Banner", "In-app Banner", "batch", True, "browse", "common", "Onsite"),
        ("CMP024", "Night Snack Push Campaign", "App Push", "event", False, "purchase", "common", "CRM"),
        ("CMP025", "Recipe Newsletter Email", "Email", "batch", True, "browse", "common", "CRM"),
        ("CMP026", "In-store Receipt Coupon Enrollment SMS", "SMS", "batch", True, "visit", "common", "CRM"),
        ("CMP027", "App Onboarding Tutorial Carousel", "In-app Banner", "event", False, "visit", "common", "Onsite"),
        ("CMP028", "Weekend Family Pack Meta Ads", "Meta Ads", "batch", True, "purchase_intent", "common", "Paid Media"),
        ("CMP029", "Flash Sale Push 2hr", "App Push", "event", False, "purchase", "common", "CRM"),
        ("CMP030", "Free Delivery Threshold Reminder Email", "Email", "event", False, "checkout", "common", "CRM"),
        ("CMP031", "Price Drop Alert on Favorited Item Push", "App Push", "event", False, "pdp", "common", "CRM"),
        ("CMP032", "Wishlist Back-in-stock Email", "Email", "event", False, "add_to_cart", "common", "CRM"),
        ("CMP033", "Member-only Tuesday Discount Email", "Email", "batch", True, "nth_purchase", "loyalty", "CRM"),
        ("CMP034", "Scan & Go Feature Education Push", "App Push", "event", False, "visit", "common", "CRM"),
        ("CMP035", "Frozen Food Category Remarketing Ads", "Display Ads", "batch", True, "browse", "common", "Paid Media"),
        ("CMP036", "Dessert Upsell at Checkout Email", "Email", "event", False, "checkout", "loyalty", "CRM"),
        ("CMP037", "Nth Purchase Stamp Card Push", "App Push", "event", False, "nth_purchase", "loyalty", "CRM"),
        ("CMP038", "Subscription Refill Reminder Email", "Email", "event", False, "nth_purchase", "loyalty", "CRM"),
        ("CMP039", "Churned 180-day Big Comeback Coupon Email", "Email", "event", False, "churned", "churn", "CRM"),
        ("CMP040", "Healthy Eating Program Email Series", "Email", "batch", True, "browse", "common", "CRM"),
        ("CMP041", "High-Value Basket Cross-sell Email", "Email", "batch", True, "loyalty", "loyalty", "CRM"),
        ("CMP042", "Lost Newcomer (No 2nd Purchase) Email", "Email", "event", False, "churn_risk", "churn", "CRM"),
        ("CMP043", "LTV Top 5% Surprise Gift Push", "App Push", "batch", True, "loyalty", "loyalty", "CRM"),
        ("CMP044", "Weekend Brunch Category Recommendation Email", "Email", "batch", True, "browse", "loyalty", "CRM"),
        ("CMP045", "Holiday Season Gift Basket Meta Ads", "Meta Ads", "batch", True, "purchase_intent", "common", "Paid Media"),
        ("CMP046", "RFM Low-Value Upsell Kakao", "KakaoTalk", "batch", True, "nth_purchase", "loyalty", "CRM"),
        ("CMP047", "Multi-buy (2+1) Promo Email", "Email", "batch", True, "nth_purchase", "loyalty", "CRM"),
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
        "onboarding": "가입 & 온보딩",
        "explore": "탐색",
        "consider": "고려",
        "first_purchase": "첫 구매",
        "post_purchase": "구매 후 경험",
        "repeat": "재구매 (N차)",
        "loyalty": "로열티",
        "reactivation": "휴면/재활성화",
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


# -----------------------------
# 2. Journey SVG 생성 (1차원 타임라인)
# -----------------------------

def build_journey_svg(df: pd.DataFrame) -> str:
    df = df.copy()
    df["journey_stage"] = df.apply(map_row_to_journey_stage, axis=1)
    df = df[df["journey_stage"].notnull()]
    if df.empty:
        return "<p>표시할 여정 캠페인이 없습니다.</p>"

    # stage index
    stage_pos = {s: i for i, s in enumerate(JOURNEY_LINE)}
    df["stage_idx"] = df["journey_stage"].map(stage_pos)

    # stage 내 rank / count
    df["rank_in_stage"] = df.groupby("journey_stage").cumcount()
    df["count_in_stage"] = df.groupby("journey_stage")["campaign_id"].transform("count")

    def calc_offset(row):
        n = row["count_in_stage"]
        r = row["rank_in_stage"]
        if n <= 1:
            return 0.0
        return (r / (n - 1) - 0.5) * 20.0  # -20 ~ +20px

    df["x_offset"] = df.apply(calc_offset, axis=1)

    # SVG 사이즈 & 베이스라인
    width = 1200
    height = 260
    margin_left = 80
    margin_right = 40
    baseline_y = 140

    n_stage = len(JOURNEY_LINE)
    if n_stage <= 1:
        gap = 200
    else:
        gap = (width - margin_left - margin_right) / (n_stage - 1)

    # 채널별 색상 (없으면 기본 회색)
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

    # stage별 캠페인 개수
    stage_counts = df.groupby("journey_stage")["campaign_id"].nunique().to_dict()

    svg_parts = []
    svg_parts.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')

    # 메인 라인
    x0 = margin_left
    x1 = margin_left + gap * (n_stage - 1)
    svg_parts.append(
        f'<line x1="{x0}" y1="{baseline_y}" x2="{x1}" y2="{baseline_y}" '
        'stroke="#444" stroke-width="4" />'
    )

    # 스테이지 노드 + 라벨
    for s in JOURNEY_LINE:
        idx = stage_pos[s]
        sx = margin_left + gap * idx
        sy = baseline_y
        count = stage_counts.get(s, 0)
        label = pretty_stage_name(s)

        # 노드 (사각형)
        svg_parts.append(
            f'<rect x="{sx-7}" y="{sy-7}" width="14" height="14" fill="#444" rx="2" />'
        )
        # 라벨
        svg_parts.append(
            f'<text x="{sx}" y="{sy-20}" text-anchor="middle" font-size="12">'
            f'{label} ({count} 캠페인)</text>'
        )

    # 캠페인 점
    for _, row in df.iterrows():
        idx = row["stage_idx"]
        sx = margin_left + gap * idx + row["x_offset"]
        sy = baseline_y
        color = channel_colors.get(row["channel"], "#666666")
        title = (
            f"{row['campaign_name']} / {row['channel']} / "
            f"{row['campaign_id']} / {row['primary_objective']}"
        )
        svg_parts.append(
            f'<circle cx="{sx}" cy="{sy}" r="5" fill="{color}">'
            f'<title>{title}</title></circle>'
        )

    # 간단 채널 legend
    legend_x = margin_left
    legend_y = 30
    svg_parts.append(f'<text x="{legend_x}" y="{legend_y-10}" font-size="12">채널 Legend</text>')
    lx = legend_x
    for ch, color in channel_colors.items():
        svg_parts.append(
            f'<rect x="{lx}" y="{legend_y}" width="12" height="12" fill="{color}" />'
        )
        svg_parts.append(
            f'<text x="{lx+18}" y="{legend_y+10}" font-size="11">{ch}</text>'
        )
        legend_y += 18
        if legend_y > 220:  # 너무 길어지면 2열로
            legend_y = 30
            lx += 120

    svg_parts.append("</svg>")
    return "".join(svg_parts)


# -----------------------------
# 3. Streamlit Layout
# -----------------------------

def main():
    st.set_page_config(page_title="A사 마케팅 캠페인 Journey MAP", layout="wide")
    st.title("A사 마케팅 캠페인 Journey MAP")

    # 세션 상태 초기화
    if "campaign_df" not in st.session_state:
        st.session_state["campaign_df"] = build_campaign_data()
        st.session_state["last_updated"] = datetime.now()

    # 상단 버튼 + 동기화 시각
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

    # ------------------ Journey View ------------------
    with tab1:
        st.subheader("고객 여정 기반 캠페인 맵")

        base_df = df[df["view_assignment"].isin(["Journey", "Both"])].copy()

        col1, col2 = st.columns([2, 1])

        with col1:
            # 필터 적용 전 전체 맵
            svg = build_journey_svg(base_df)
            st.markdown(svg, unsafe_allow_html=True)

        with col2:
            st.markdown("### 필터")
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

    # ------------------ Calendar View ------------------
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
