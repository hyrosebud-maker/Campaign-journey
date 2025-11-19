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
    width = 1400          # 이전: 2500
    margin_left = 40      # 이전: 120
    margin_right = 40     # 이전: 120
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
    # 🔧 컨테이너 폭에 맞게, 왼쪽 정렬
    svg.append(
        f'<svg width="100%" height="{height}" '
        f'viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    )

    # 1) 채널 Legend (가로)
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

    # 3) 스테이지 라벨 (겹침 방지 로직 포함)
    stage_char_width = 9
    stage_gap = 20
    outer_margin = 10

    centers = []
    widths = []
    labels = []

    for stage in JOURNEY_LINE:
        label = pretty_stage_name(stage)
        labels.append(label)
        centers.append(stage_x[stage])
        widths.append(len(label) * stage_char_width)

    # 왼쪽 -> 오른쪽
    min_center = x_min + widths[0] / 2 + outer_margin
    centers[0] = max(centers[0], min_center)
    for i in range(1, len(JOURNEY_LINE)):
        min_center = centers[i-1] + (widths[i-1] + widths[i]) / 2 + stage_gap
        if centers[i] < min_center:
            centers[i] = min_center

    # 오른쪽 -> 왼쪽
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
        svg.append(
            f'<text x="{sx}" y="{sy-22}" text-anchor="middle" '
            f'font-size="13" fill="#111">{label}</text>'
        )

    # 4) 전 여정 영향 화살표 (기존 그대로)
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
