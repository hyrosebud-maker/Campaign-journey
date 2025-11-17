# app.py

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

        # view_assignment 로직 (R1~R4와 비슷하게)
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
            # 청크 중 일부는 Journey-only
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
# 1. Journey View 시각화
# -----------------------------

JOURNEY_STAGES = [
    "visit",
    "browse",
    "pdp",
    "add_to_cart",
    "checkout",
    "purchase",
    "retention",
]

CHURN_BRANCH = ["churn_risk", "churned"]
LOYALTY_BRANCH = ["nth_purchase", "loyalty"]


def pretty_stage_name(stage_key: str) -> str:
    mapping = {
        "visit": "유입/온보딩",
        "browse": "상품 탐색",
        "pdp": "상품 관심(PDP)",
        "add_to_cart": "구매 의도(장바구니)",
        "checkout": "구매 시도(Checkout)",
        "purchase": "구매 완료",
        "retention": "리텐션",
        "churn_risk": "이탈 임박",
        "churned": "이탈",
        "nth_purchase": "N차 구매",
        "loyalty": "충성 고객",
        "purchase_intent": "구매 의도(프로모션)",
    }
    return mapping.get(stage_key, stage_key)


def build_journey_figure(df: pd.DataFrame) -> go.Figure:
    """
    저니 박스 + 캠페인 점 + 브랜치(이탈/충성) 라인 시각화.
    컨설팅 장표 느낌의 단순한 네트워크 레이아웃.
    """

    # x 좌표: 메인 스테이지 0~6
    x_positions = {stage: i for i, stage in enumerate(JOURNEY_STAGES)}
    # y 좌표: common=0, churn=-1, loyalty=1
    y_base = {"common": 0, "churn": -1, "loyalty": 1}

    fig = go.Figure()

    # 1) 메인 스테이지 박스(검정 배경 느낌)
    for stage in JOURNEY_STAGES:
        x = x_positions[stage]
        fig.add_shape(
            type="rect",
            x0=x - 0.4,
            y0=-0.3,
            x1=x + 0.4,
            y1=0.3,
            line=dict(width=1),
            fillcolor="black",
            opacity=0.15,
        )
        # 스테이지 이름 + 캠페인 수 표시
        count_stage = df[df["primary_objective"] == stage]["campaign_id"].nunique()
        fig.add_annotation(
            x=x,
            y=0,
            text=f"{pretty_stage_name(stage)}<br><sup>{count_stage} 캠페인</sup>",
            showarrow=False,
            font=dict(size=12),
        )

    # 2) 브랜치 스테이지 박스 (이탈/충성)
    # Churn Branch (아래)
    for i, stage in enumerate(CHURN_BRANCH):
        x = x_positions["retention"] + i + 1  # 리텐션 이후 오른쪽으로 전개
        fig.add_shape(
            type="rect",
            x0=x - 0.4,
            y0=-1.3,
            x1=x + 0.4,
            y1=-0.7,
            line=dict(width=1),
            fillcolor="black",
            opacity=0.15,
        )
        count_stage = df[df["primary_objective"] == stage]["campaign_id"].nunique()
        fig.add_annotation(
            x=x,
            y=-1.0,
            text=f"{pretty_stage_name(stage)}<br><sup>{count_stage} 캠페인</sup>",
            showarrow=False,
            font=dict(size=12),
        )

    # Loyalty Branch (위)
    for i, stage in enumerate(LOYALTY_BRANCH):
        x = x_positions["retention"] + i + 1
        fig.add_shape(
            type="rect",
            x0=x - 0.4,
            y0=0.7,
            x1=x + 0.4,
            y1=1.3,
            line=dict(width=1),
            fillcolor="black",
            opacity=0.15,
        )
        count_stage = df[df["primary_objective"] == stage]["campaign_id"].nunique()
        fig.add_annotation(
            x=x,
            y=1.0,
            text=f"{pretty_stage_name(stage)}<br><sup>{count_stage} 캠페인</sup>",
            showarrow=False,
            font=dict(size=12),
        )

    # 3) 메인 플로우 라인 (공통 경로)
    xs = [x_positions[s] for s in JOURNEY_STAGES]
    ys = [0] * len(xs)
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            line=dict(width=3),
            name="공통 여정",
            hoverinfo="skip",
        )
    )

    # 4) 브랜치 라인 (이탈/충성)
    # Retention에서 갈라지는 효과
    ret_x = x_positions["retention"]

    # 이탈 브랜치 (점선)
    churn_xs = [ret_x, ret_x + 1, ret_x + 2]
    churn_ys = [0, -1, -1]
    fig.add_trace(
        go.Scatter(
            x=churn_xs,
            y=churn_ys,
            mode="lines",
            line=dict(width=2, dash="dash"),
            name="이탈 경로",
            hoverinfo="skip",
        )
    )

    # 충성 브랜치 (실선)
    loyalty_xs = [ret_x, ret_x + 1, ret_x + 2]
    loyalty_ys = [0, 1, 1]
    fig.add_trace(
        go.Scatter(
            x=loyalty_xs,
            y=loyalty_ys,
            mode="lines",
            line=dict(width=2),
            name="충성 경로",
            hoverinfo="skip",
        )
    )

    # 5) 캠페인 노드들 (검정 박스 안에 배치되는 느낌)
    # y축 jitter를 약간 줘서 박스 안에 퍼지게
    node_x = []
    node_y = []
    node_text = []
    node_color = []

    for _, row in df.iterrows():
        obj = row["primary_objective"]
        branch = row["journey_branch"]

        # 어떤 x/y 좌표에 찍을지 결정
        if obj in JOURNEY_STAGES:
            x = x_positions[obj]
            base_y = 0
        elif obj in CHURN_BRANCH:
            idx = CHURN_BRANCH.index(obj)
            x = x_positions["retention"] + idx + 1
            base_y = -1
        elif obj in LOYALTY_BRANCH or obj in ["purchase_intent"]:
            if obj == "purchase_intent":
                # 구매 의도형 프로모션은 구매 직전/리텐션 사이 어딘가로
                x = (x_positions["checkout"] + x_positions["purchase"]) / 2
                base_y = 0
            else:
                idx = LOYALTY_BRANCH.index(obj)
                x = x_positions["retention"] + idx + 1
                base_y = 1
        else:
            # Unknown 스테이지는 스킵
            continue

        # jitter
        jitter = 0.12
        y = base_y + (0.5 - 1.0 * (hash(row["campaign_id"]) % 100) / 100) * jitter

        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{row['campaign_name']}<br><sup>{row['channel']} / {row['campaign_id']}</sup>")
        # 채널 기반 색상 그룹핑 느낌 (실제 색은 브라우저 디폴트)
        node_color.append(row["channel"])

    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            marker=dict(size=10),
            text=node_text,
            hoverinfo="text",
            name="캠페인",
        )
    )

    fig.update_layout(
        title="고객 여정 상 캠페인 맵 (공통 + 이탈/충성 브랜치)",
        showlegend=True,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickvals=list(x_positions.values()) + [x_positions["retention"] + 1, x_positions["retention"] + 2],
            ticktext=[pretty_stage_name(s) for s in JOURNEY_STAGES] + ["", ""],
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
# 2. Calendar View 시각화
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
# 3. Streamlit App Layout
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

        col1, col2 = st.columns([2, 1])

        with col1:
            fig_journey = build_journey_figure(df)
            st.plotly_chart(fig_journey, use_container_width=True)

        with col2:
            st.markdown("### 필터")
            channel_filter = st.multiselect(
                "채널 선택",
                options=sorted(df["channel"].unique()),
                default=sorted(df["channel"].unique()),
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

            stage_filter = st.multiselect(
                "여정 단계 선택",
                options=[*JOURNEY_STAGES, *CHURN_BRANCH, *LOYALTY_BRANCH],
                default=[*JOURNEY_STAGES, *CHURN_BRANCH, *LOYALTY_BRANCH],
                format_func=pretty_stage_name,
            )

            filtered = df[
                (df["channel"].isin(channel_filter)) &
                (df["journey_branch"].isin(branch_filter)) &
                (df["primary_objective"].isin(stage_filter))
            ]

            st.markdown("### 선택된 조건의 캠페인 목록")
            st.dataframe(
                filtered[[
                    "campaign_id",
                    "campaign_name",
                    "channel",
                    "primary_objective",
                    "journey_branch",
                    "trigger_type",
                    "is_batch_campaign",
                    "start_datetime",
                    "end_datetime",
                ]]
            )

            st.markdown(
                """
                - **검정 박스**: 각 Journey Stage  
                - **점선/실선 라인**: 이탈/충성 브랜치 흐름  
                - **점**: 해당 스테이지에서 고객을 터치하는 개별 캠페인들  
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
        "고객 여정(저니) 상의 허점과 배치성 마케팅 일정을 한 번에 점검하기 위한 컨설팅형 대시보드 예시입니다."
    )


if __name__ == "__main__":
    main()
