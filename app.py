import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta

# -----------------------------
# 0. 기본 데이터 세팅
# -----------------------------

def build_campaign_data():
    """
    위에서 정의한 47개 캠페인을 코드 상 DataFrame으로 구성하고,
    날짜/기간(캘린더용)은 예시로 생성한다.
    """
    base = datetime(2025, 11, 1)

    raw = [
        # id, name, channel, trigger_type, is_batch, primary_objective, journey_branch, campaign_type
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
        cid, name, channel, trigger, is_batch, objective, branch, ctype = row

        start = base + timedelta(days=idx)
        end = start + timedelta(days=7 if is_batch else 1)

        # Journey/Calendar 구분
        if trigger == "event" and objective in [
            "visit", "browse", "pdp", "add_to_cart",
            "checkout", "purchase", "retention",
            "nth_purchase", "churn_risk", "churned", "loyalty"
        ]:
            journey = True
        else:
            journey = False

        calendar = bool(is_batch)
        view_assignment = "Both" if (journey and calendar) else ("Journey" if journey else "Calendar")

        records.append({
            "campaign_id": cid,
            "campaign_name": name,
            "channel": channel,
            "trigger_type": trigger,
            "is_batch_campaign": is_batch,
            "primary_objective": objective,
            "journey_branch": branch,
            "campaign_type": ctype,
            "start_datetime": start,
            "end_datetime": end,
            "view_assignment": view_assignment,
        })

    return pd.DataFrame(records)


# -----------------------------
# 1. Journey 정의 (최종 합의 버전)
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

def map_row_to_journey_stage(row) -> str:
    """
    primary_objective + journey_branch 기반으로
    최종 여정 스테이지로 매핑.
    """
    obj = row["primary_objective"]
    branch = row["journey_branch"]

    if obj == "visit":
        return "onboarding"
    if obj == "browse":
        return "explore"
    if obj == "pdp":
        return "consider"

    if obj in ["add_to_cart", "checkout", "purchase"]:
        if branch == "loyalty":
            return "repeat"
        else:
            return "first_purchase"

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
# 2. Journey View (Altair, 단일 선 위 여정+캠페인)
# -----------------------------

def build_journey_chart(df: pd.DataFrame) -> alt.Chart:
    df = df.copy()
    df["journey_stage"] = df.apply(map_row_to_journey_stage, axis=1)
    df = df[df["journey_stage"].notnull()]
    if df.empty:
        return alt.Chart().mark_text(text="데이터가 없습니다.")

    stage_pos = {s: i for i, s in enumerate(JOURNEY_LINE)}
    df["stage_index"] = df["journey_stage"].map(stage_pos)

    # jitter: 같은 스테이지 내 캠페인들을 위아래로 살짝 분산
    df["y_jitter"] = 0.0
    for stage, g in df.groupby("journey_stage"):
        n = len(g)
        if n == 1:
            offsets = [0.0]
        else:
            offsets = np.linspace(-0.25, 0.25, n)
        df.loc[g.index, "y_jitter"] = offsets

    stage_counts = df.groupby("journey_stage")["campaign_id"].nunique().to_dict()
    stage_df = pd.DataFrame({
        "journey_stage": JOURNEY_LINE,
        "stage_index": [stage_pos[s] for s in JOURNEY_LINE],
        "y": 0.0,
        "label": [
            f"{pretty_stage_name(s)}\n({stage_counts.get(s, 0)} 캠페인)"
            for s in JOURNEY_LINE
        ],
    })

    line = alt.Chart(stage_df).mark_line(strokeWidth=4).encode(
        x=alt.X("stage_index:Q", axis=alt.Axis(
            title="",
            values=[stage_pos[s] for s in JOURNEY_LINE],
            labelExpr="{'%s'}[datum.value]" % "','".join([pretty_stage_name(s) for s in JOURNEY_LINE])
        )),
        y=alt.Y("y:Q", axis=None),
    )

    stage_nodes = alt.Chart(stage_df).mark_square(size=200).encode(
        x="stage_index:Q",
        y="y:Q",
        tooltip=["journey_stage", "label"],
    )

    stage_text = alt.Chart(stage_df).mark_text(dy=-25).encode(
        x="stage_index:Q",
        y="y:Q",
        text="label:N",
    )

    campaigns = alt.Chart(df).mark_circle(size=60).encode(
        x="stage_index:Q",
        y="y_jitter:Q",
        color=alt.Color("channel:N", legend=alt.Legend(title="채널")),
        tooltip=[
            "campaign_id",
            "campaign_name",
            "channel",
            "journey_stage",
            "primary_objective",
            "journey_branch",
        ],
    )

    chart = (line + stage_nodes + stage_text + campaigns).properties(
        height=500
    ).configure_view(
        strokeWidth=0
    )

    return chart


# -----------------------------
# 3. Calendar View (Altair Gantt)
# -----------------------------

def build_calendar_chart(df: pd.DataFrame) -> alt.Chart:
    batch_df = df[df["is_batch_campaign"]].copy()
    if batch_df.empty:
        return alt.Chart().mark_text(text="배치성 캠페인이 없습니다.")

    batch_df["Start"] = batch_df["start_datetime"]
    batch_df["Finish"] = batch_df["end_datetime"]
    batch_df["Campaign"] = batch_df["campaign_name"]
    batch_df["Channel"] = batch_df["channel"]

    chart = alt.Chart(batch_df).mark_bar().encode(
        x=alt.X("Start:T", title="기간 시작"),
        x2="Finish:T",
        y=alt.Y("Campaign:N", sort="-x", title="캠페인"),
        color=alt.Color("Channel:N", title="채널"),
        tooltip=[
            "campaign_id",
            "Campaign",
            "Channel",
            "primary_objective",
            "journey_branch",
            "Start",
            "Finish",
        ],
    ).properties(
        height=700
    ).configure_view(
        strokeWidth=0
    )

    return chart


# -----------------------------
# 4. Streamlit App Layout
# -----------------------------

def main():
    st.set_page_config(
        page_title="Journey & Calendar Campaign Map",
        layout="wide",
    )

    st.title("식품/유통 마케팅 캠페인 맵 (Journey + Calendar)")

    df = build_campaign_data()

    with st.expander("Raw Campaign List (47개)"):
        st.dataframe(df)

    tab1, tab2 = st.tabs(["🧭 Journey View", "📅 Calendar View"])

    # -------- Journey View Tab --------
    with tab1:
        st.subheader("고객 여정 기반 캠페인 맵")

        view_mode = st.radio(
            "캠페인 종류 선택",
            options=["여정 캠페인만", "캘린더성 캠페인만", "둘 다 보기"],
            horizontal=True,
        )

        if view_mode == "여정 캠페인만":
            base_df = df[df["view_assignment"].isin(["Journey", "Both"])].copy()
        elif view_mode == "캘린더성 캠페인만":
            base_df = df[df["view_assignment"].isin(["Calendar", "Both"])].copy()
        else:
            base_df = df.copy()

        col1, col2 = st.columns([2, 1])

        with col1:
            chart = build_journey_chart(base_df)
            st.altair_chart(chart, use_container_width=True)

        with col2:
            st.markdown("### 필터")
            channel_filter = st.multiselect(
                "채널 선택",
                options=sorted(base_df["channel"].unique()),
                default=sorted(base_df["channel"].unique()),
            )
            branch_filter = st.multiselect(
                "브랜치 선택",
                options=["common", "churn", "loyalty"],
                default=["common", "churn", "loyalty"],
                format_func=lambda x: {
                    "common": "공통",
                    "churn": "이탈 경로",
                    "loyalty": "충성 경로",
                }.get(x, x),
            )

            filtered = base_df[
                (base_df["channel"].isin(channel_filter)) &
                (base_df["journey_branch"].isin(branch_filter))
            ].copy()

            filtered["journey_stage"] = filtered.apply(map_row_to_journey_stage, axis=1)
            filtered["journey_stage_label"] = filtered["journey_stage"].apply(
                lambda x: pretty_stage_name(x) if pd.notnull(x) else ""
            )

            st.markdown("### 선택된 조건의 캠페인 목록")
            st.dataframe(
                filtered[[
                    "campaign_id",
                    "campaign_name",
                    "channel",
                    "primary_objective",
                    "journey_branch",
                    "journey_stage_label",
                    "trigger_type",
                    "is_batch_campaign",
                    "start_datetime",
                    "end_datetime",
                ]]
            )

            st.markdown(
                """
                - **굵은 선**: 가입 → 탐색 → 고려 → 첫구매 → 구매 후 경험 → 재구매 → 로열티 → 휴면/재활성화  
                - **사각형 노드**: 각 여정 스테이지 (괄호 안은 캠페인 개수)  
                - **원형 점**: 해당 여정 단계에서 실행되는 개별 캠페인 (채널별 색상)  
                """
            )

    # -------- Calendar View Tab --------
    with tab2:
        st.subheader("배치성 마케팅 캘린더")

        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown("### 필터")
            channel_filter_cal = st.multiselect(
                "채널 선택",
                options=sorted(df["channel"].unique()),
                default=sorted(df["channel"].unique()),
            )
            branch_filter_cal = st.multiselect(
                "브랜치 선택",
                options=["common", "churn", "loyalty"],
                default=["common", "churn", "loyalty"],
                format_func=lambda x: {
                    "common": "공통",
                    "churn": "이탈 경로",
                    "loyalty": "충성 경로",
                }.get(x, x),
            )

            calendar_df = df[
                (df["is_batch_campaign"]) &
                (df["channel"].isin(channel_filter_cal)) &
                (df["journey_branch"].isin(branch_filter_cal))
            ].copy()

            st.markdown("### 배치성 캠페인 테이블")
            st.dataframe(
                calendar_df[[
                    "campaign_id",
                    "campaign_name",
                    "channel",
                    "primary_objective",
                    "journey_branch",
                    "start_datetime",
                    "end_datetime",
                ]]
            )

        with col2:
            if calendar_df.empty:
                st.info("선택된 조건에 해당하는 배치성 캠페인이 없습니다.")
            else:
                cal_chart = build_calendar_chart(calendar_df)
                st.altair_chart(cal_chart, use_container_width=True)

            st.markdown(
                """
                - **가로 Bar**: 해당 기간 동안 운영되는 배치성 캠페인  
                - **색상**: 채널 구분 (Email, Kakao, Meta Ads 등)  
                - Hover 시: 캠페인 ID, 여정 목적, 브랜치 정보, 기간 확인 가능  
                """
            )

    st.markdown("---")
    st.caption(
        "※ SF API에서 가져온 캠페인 메타데이터를 기반으로, "
        "고객 여정 상 터치포인트와 배치성 마케팅 일정을 한 번에 점검하기 위한 예시 대시보드입니다."
    )


if __name__ == "__main__":
    main()
