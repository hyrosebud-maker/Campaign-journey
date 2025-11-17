import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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

        # 예시로 start/end를 생성 (배치 캠페인은 더 긴 기간)
        start = base + timedelta(days=idx)  # 단순히 index 기반으로 날짜 분산
        if is_batch:
            end = start + timedelta(days=7)
        else:
            end = start + timedelta(days=1)

        # Journey/Calendar 구분 로직
        if trigger == "event" and objective in [
            "visit", "browse", "pdp", "add_to_cart",
            "checkout", "purchase", "retention",
            "nth_purchase", "churn_risk", "churned", "loyalty"
        ]:
            journey = True
        else:
            journey = False

        if is_batch:
            calendar = True
        else:
            calendar = False

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

# 내부 키 순서 (회원가입 → 탐색 → 고려 → 첫구매 → 구매 후 경험 → 재구매 → 로열티 → 휴면/재활성화)
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
    primary_objective + journey_branch를 기반으로
    우리가 합의한 최종 저니 스테이지로 매핑.
    """
    obj = row["primary_objective"]
    branch = row["journey_branch"]

    # 1) 가입 & 온보딩
    if obj == "visit":
        return "onboarding"

    # 2) 탐색 / 고려
    if obj == "browse":
        return "explore"
    if obj == "pdp":
        return "consider"

    # 3) 첫 구매 vs 재구매 (장바구니/체크아웃/구매)
    if obj in ["add_to_cart", "checkout", "purchase"]:
        if branch == "loyalty":
            return "repeat"
        else:
            return "first_purchase"

    # 4) 구매 후 경험
    if obj == "retention":
        return "post_purchase"

    # 5) 재구매 (Nth Purchase)
    if obj == "nth_purchase":
        return "repeat"

    # 6) 로열티
    if obj == "loyalty":
        return "loyalty"

    # 7) 휴면/재활성화
    if obj in ["churn_risk", "churned"]:
        return "reactivation"

    # 8) 프로모션성 구매 의도
    if obj == "purchase_intent":
        # 첫 구매 전후 모두 붙을 수 있지만, 여기서는 '고려' 쪽에 붙임
        return "consider"

    return None  # 매핑 안 되는 경우


# -----------------------------
# 2. Journey View 시각화 (단일 선 위에 여정+캠페인)
# -----------------------------

def build_journey_figure(df: pd.DataFrame) -> go.Figure:
    """
    하나의 선 위에 여정 포인트와 캠페인이 함께 보이도록 시각화.
    - x축: 저니 스테이지 순서
    - y=0: 기준 선
    - 스테이지 노드: 큼직한 사각형 마커
    - 캠페인 노드: 원형 마커 (채널별 색상)
    """

    # 저니 스테이지 매핑
    df = df.copy()
    df["journey_stage"] = df.apply(map_row_to_journey_stage, axis=1)

    # 매핑 안 된 행은 제외
    df = df[df["journey_stage"].notnull()]
    if df.empty:
        return go.Figure()

    # x 좌표: 저니 라인 순서대로
    x_positions = {stage: i for i, stage in enumerate(JOURNEY_LINE)}
    stage_x = [x_positions[s] for s in JOURNEY_LINE]
    stage_y = [0] * len(JOURNEY_LINE)

    fig = go.Figure()

    # 1) 메인 여정 라인
    fig.add_trace(
        go.Scatter(
            x=stage_x,
            y=stage_y,
            mode="lines",
            line=dict(width=4),
            name="고객 여정 라인",
            hoverinfo="skip",
        )
    )

    # 2) 스테이지 노드 (사각형 마커 + 캠페인 수 표시)
    stage_counts = df.groupby("journey_stage")["campaign_id"].nunique().to_dict()

    fig.add_trace(
        go.Scatter(
            x=[x_positions[s] for s in JOURNEY_LINE],
            y=[0] * len(JOURNEY_LINE),
            mode="markers+text",
            marker=dict(
                size=20,
                symbol="square",
                line=dict(width=1),
            ),
            text=[
                f"{pretty_stage_name(s)}<br><sup>{stage_counts.get(s, 0)} 캠페인</sup>"
                for s in JOURNEY_LINE
            ],
            textposition="top center",
            hoverinfo="skip",
            name="여정 스테이지",
        )
    )

    # 3) 캠페인 노드 (여정 선 위에 같이 찍기, 약간의 jitter)
    node_x = []
    node_y = []
    node_text = []
    node_color = []

    for _, row in df.iterrows():
        stage = row["journey_stage"]
        x = x_positions.get(stage)
        if x is None:
            continue

        base_y = 0
        # 너무 겹치지 않게 약간 위/아래로 분산
        jitter = 0.15
        offset = ((hash(row["campaign_id"]) % 100) / 100 - 0.5) * 2 * jitter
        y = base_y + offset

        node_x.append(x)
        node_y.append(y)
        node_text.append(
            f"{row['campaign_name']}<br><sup>{row['channel']} / {row['campaign_id']}</sup>"
        )
        node_color.append(row["channel"])

    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            marker=dict(
                size=9,
            ),
            text=node_text,
            hoverinfo="text",
            name="캠페인",
        )
    )

    fig.update_layout(
        title="고객 여정 상 캠페인 맵 (단일 라인)",
        showlegend=True,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickvals=[x_positions[s] for s in JOURNEY_LINE],
            ticktext=[pretty_stage_name(s) for s in JOURNEY_LINE],
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=False,
        ),
        height=600,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


# -----------------------------
# 3. Calendar View 시각화
# -----------------------------

def build_calendar_figure(df: pd.DataFrame) -> go.Figure:
    """
    배치성 캠페인(is_batch_campaign=True)을 중심으로
    px.timeline 으로 Gantt 스타일 캘린더 뷰를 만든다.
    """

    batch_df = df[df["is_batch_campaign"]].copy()
    if batch_df.empty:
        return go.Figure()

    batch_df["Start"] = batch_df["start_datetime"]
    batch_df["Finish"] = batch_df["end_datetime"]
    batch_df["Campaign"] = batch_df["campaign_name"]
    batch_df["Channel"] = batch_df["channel"]

    fig = px.timeline(
        batch_df,
        x_start="Start",
        x_end="Finish",
        y="Campaign",
        color="Channel",
        hover_data=["campaign_id", "primary_objective", "journey_branch"],
    )

    fig.update_yaxes(autorange="reversed")  # Gantt 스타일
    fig.update_layout(
        title="배치성 마케팅 캘린더 (타임라인 뷰)",
        height=700,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


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

    # 상단: 원본 데이터 요약
    with st.expander("Raw Campaign List (47개)"):
        st.dataframe(df)

    tab1, tab2 = st.tabs(["🧭 Journey View", "📅 Calendar View"])

    # -------- Journey View Tab --------
    with tab1:
        st.subheader("고객 여정 기반 캠페인 맵")

        # 1) 제일 처음: 여정 캠페인 vs 캘린더성 캠페인 구분
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
            fig_journey = build_journey_figure(base_df)
            st.plotly_chart(fig_journey, use_container_width=True)

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

            # 여정 스테이지 표시용 컬럼 추가
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
                - **굵은 선**: 고객 여정(가입 → 탐색 → 고려 → 첫구매 → 구매 후 경험 → 재구매 → 로열티 → 휴면/재활성화)  
                - **사각형 노드**: 각 여정 스테이지 (아래에 해당 스테이지의 캠페인 수 표기)  
                - **원형 점**: 해당 여정 단계에서 고객을 터치하는 개별 캠페인들 (채널별 색상 구분)  
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
                fig_cal = build_calendar_figure(calendar_df)
                st.plotly_chart(fig_cal, use_container_width=True)

            st.markdown(
                """
                - **Timeline Bar**: 해당 기간 동안 운영되는 배치성 캠페인  
                - **색상**: 채널 구분 (Email, Kakao, Meta Ads 등)  
                - Hover 시: 캠페인 ID, 여정 목적, 브랜치 정보 확인 가능  
                """
            )

    st.markdown("---")
    st.caption(
        "※ 본 화면은 SF API에서 가져온 캠페인 메타데이터를 기반으로, "
        "고객 여정(저니) 상의 터치포인트와 배치성 마케팅 일정을 한 번에 점검하기 위한 컨설팅형 대시보드 예시입니다."
    )


if __name__ == "__main__":
    main()
