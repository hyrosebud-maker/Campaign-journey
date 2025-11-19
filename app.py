# --- 2-5. 47개 캠페인 점 + 아래 라벨 (겹치지 않게 행 배정) ---

label_base_y = baseline_y + 30

# 1) 먼저 라벨용 아이템 리스트 만들기
label_items = []
for _, r in df.iterrows():
    label_items.append({
        "x": float(r["x"]),
        "text": str(r["campaign_name"]),
        "row": r,  # 원본 row 전체를 같이 들고 있게
    })

# 2) 행 배정
placements, max_row = assign_label_rows(
    label_items,
    char_width=6,        # 글자당 대략 폭 (px)
    row_gap=16,          # 행 사이 간격
    base_y=label_base_y,
)

# 필요하면 SVG 높이를 행 수에 맞게 키우고 싶으면 여기서 max_row를 이용해서 height 조정 가능

for item, row_idx, label_y in placements:
    r = item["row"]
    x = item["x"]
    color = channel_colors.get(r["channel"], "#666666")

    line_y2 = label_y - 6  # 텍스트 바로 위까지 세로선

    # 세로선
    svg.append(
        f'<line x1="{x}" y1="{baseline_y+8}" x2="{x}" y2="{line_y2}" '
        'stroke="#bbbbbb" stroke-width="1" />'
    )
    # 타임라인 위의 점
    svg.append(
        f'<circle cx="{x}" cy="{baseline_y}" r="4" fill="{color}" />'
    )
    # 한글 캠페인명
    svg.append(
        f'<text x="{x}" y="{label_y}" text-anchor="middle" '
        'font-size="10" fill="#222">'
        f'{r["campaign_name"]}</text>'
    )
