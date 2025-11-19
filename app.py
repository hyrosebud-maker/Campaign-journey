import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# -----------------------------
# 0. 기본 데이터 세팅
# -----------------------------

def build_campaign_data():
    """
    47개 캠페인 메타데이터 예시 생성 함수.
    실제 환경에서는 여기 대신 SFMC / Adobe / 기타 솔루션 API 호출 결과를 매핑해서 사용.
    """
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
# 2. Journey Chart (Altair 1차원 화살표)
# -----------------------------

def build_journey_chart(df: pd.DataFrame) -> alt.Chart:
    df = df.copy()
    df["journey_stage"] = df.apply(map_row_to_journey_stage, axis=1)
    df = df[df["journey_stage"].notnull()]
    if df.empty:
        dummy = pd.DataFrame({"x":[0], "y":[0], "text":["데이터 없음"]})
        return alt.Chart(dummy).mark_text().encode(x="x:Q", y="y:Q", text="text")

    # stage index
    stage_pos = {s: i for i, s in enumerate(JOURNEY_LINE)}
    df["stage_idx"] = df["journey_stage"].map(stage_pos)

    # stage 내에서 좌우로만 분산
    df["rank_in_stage"] = df.groupby("journey_stage").cumcount()
    df["count_in_stage"] = df.groupby("journey_stage")["campaign_id"].transform("count")

    def calc_offset(row):
        n = row["count_in_stage"]
        r = row["rank_in_stage"]
        if n <= 1:
            return 0.0
        return (r / (n - 1) - 0.5) * 0.5  # -0.25 ~ +0.25

    df["x_offset"] = df.apply(calc_offset, axis=1)
    df["x_pos"] = df["stage_idx"] + df["x_offset"]
    df["y_pos"] = 0.0

    # stage summary
    stage_counts = df.groupby("journey_stage")["campaign_id"].nunique().to_dict()
    stage_df = pd.DataFrame({
        "journey_stage": JOURNEY_LINE,
        "stage_idx": [stage_pos[s] for s in JOURNEY_LINE],
        "y": 0.0,
        "label": [
            f"{pretty_stage_name(s)} ({stage_counts.get(s,0)} 캠페인)"
            for s in JOURNEY_LINE
        ],
    })

    # 라인용 데이터 (좌→우 화살표 느낌)
    line_df = pd.DataFrame({
        "x": [min(stage_df["stage_idx"]), max(stage_df["stage_idx"])],
        "y": [0.0, 0.0],
    })

    line = alt.Chart(line_df).mark_line(strokeWidth=4).encode(
        x=alt.X("x:Q", axis=alt.Axis(title="", grid=False)),
        y=alt.Y("y:Q", axis=None),
    )

    nodes = alt.Chart(stage_df).mark_square(size=150).encode(
        x="stage_idx:Q",
        y="y:Q",
        tooltip=["label:N"],
    )

    labels = alt.Chart(stage_df).mark_text(dy=-20).encode(
        x="stage_idx:Q",
        y="y:Q",
        text="label:N",
    )

    campaigns = alt.Chart(df).mark_circle(size=60).encode(
        x="x_pos:Q",
        y=alt.Y("y_pos:Q", axis=None),
        color=alt.Color("channel:N", title="채널"),
        tooltip=[
            "campaign_id",
            "campaign_name",
            "channel",
            "journey_stage",
            "primary_objective",
            "journey_branch",
        ],
    )

    chart = (line + nodes + labels + campaigns).properties(
        height=450,
    ).configure_view(
        strokeWidth=0,
    )

    return chart


# -----------------------------
# 3. Calendar Chart (Altair Gantt)
# -----------------------------

def build_calendar_chart(df: pd.DataFrame) -> alt.Chart:
    batch_df = df[df["is_batch_campaign"]].copy()
    if batch_df.empty:
        dummy = pd.DataFrame({"x":[0], "y":[0], "text":["배치 캠페인 없음"]})
        return alt.Chart(dummy).mark_text().encode(x="x:Q", y="y:Q", text="text")

    batch_df["Start"] = batch_df["start_datetime"]
    batch_df["Finish"] = batch_df["end_datetime"]
    batch_df["Campaign"] = batch_df["campaign_name"]
    batch_df["Channel"] = batch_df["channel"]

    chart = alt.Chart(batch_df).mark_bar().encode(
        x=alt.X("Start:T", title="시작"),
        x2="Finish:T",
        y=alt.Y("Campaign:N", sort="-x", title="캠페인"),
        color=alt.Color("Channel:N", title="채널"),
        tooltip=[
            "campaign_id",
            "campaign_name",
            "channel",
            "primary_objective",
            "journey_branch",
            "Start",
            "Finish",
        ],
    ).properties(
        height=650,
    ).configure_view(
        strokeWidth=0,
    )

    return chart


# -----------------------------
# 4. Streamlit Layout
# -----------------------------

def main():
    st.set_page_config(page_title="A사 마케팅 캠페인 Journey MAP", layout="wide")
    st.title("A사 마케팅 캠페인 Journey MAP")

    # 세션 상태 초기화
    if "campaign_df" not in st.session_state:
        st.session_state["campaign_df"] = build_campaign_data()
        st.session_state["last_updated"] = datetime.now()

    # 상단 버튼
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

    # Journey View
    with tab1:
        st.subheader("고객 여정 기반 캠페인 맵")

        base_df = df[df["view_assignment"].isin(["Journey", "Both"])].copy()

        col1, col2 = st.columns([2, 1])

        with col1:
            chart = build_journey_chart(base_df)
            st.altair_chart(chart, use_container_width=True)

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

            filtered["journey_stage"] = filtered.apply(map_row_to_journey_stage, axis=1)
            filtered["journey_label"] = filtered["journey_stage"].apply(
                lambda x: pretty_stage_name(x) if pd.notnull(x) else ""
            )

            st.markdown("### 선택된 조건의 캠페인 목록")
            st.dataframe(
                filtered[
                    [
                        "campaign_id",
                        "campaign_name",
                        "channel",
                        "primary_objective",
                        "journey_branch",
                        "journey_label",
                        "is_batch_campaign",
                        "start_datetime",
                        "end_datetime",
                    ]
                ]
            )

    # Calendar View
    with tab2:
        st.subheader("배치성 마케팅 캘린더")

        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown("### 필터")
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

            st.markdown("### 배치성 캠페인 테이블")
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

        with col2:
            cal_chart = build_calendar_chart(calendar_df)
            st.altair_chart(cal_chart, use_container_width=True)


if __name__ == "__main__":
    main()
