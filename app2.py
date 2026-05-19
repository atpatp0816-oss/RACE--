import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz
import time

st.title("서울 지하철 혼잡도 분석 대시보드")

# 서울 현재시간
seoul_tz = pytz.timezone("Asia/Seoul")
now = datetime.now(seoul_tz)

# 오늘 요일 → 요일구분 매핑
weekday = now.weekday()  # 0=월 ~ 6=일
if weekday == 5:
    today_day = "토요일"
elif weekday == 6:
    today_day = "일요일"
else:
    today_day = "평일"

# CSV 불러오기
df = pd.read_csv("data/subway_congestion_raw.csv", encoding="cp949")
df.columns = df.columns.str.strip()

# 시간대 컬럼 파싱 → 현재시간과 가장 가까운 컬럼 찾기
info_columns = ["요일구분", "호선", "역번호", "출발역", "상하구분"]
time_columns = [col for col in df.columns if col not in info_columns]

def col_to_minutes(col):
    """'8시30분' → 510 (분 단위)"""
    h, rest = col.replace("분", "").split("시")
    return int(h) * 60 + (int(rest) if rest else 0)

now_minutes = now.hour * 60 + now.minute
time_minutes = [col_to_minutes(col) for col in time_columns]
closest_idx = min(range(len(time_minutes)), key=lambda i: abs(time_minutes[i] - now_minutes))
closest_col = time_columns[closest_idx]

# 노선 선택 (디폴트: 2호선)
line_list = sorted(df["호선"].dropna().unique())
default_line_idx = line_list.index("2호선") if "2호선" in line_list else 0
selected_line = st.selectbox("노선을 선택하세요", line_list, index=default_line_idx)
line_df = df[df["호선"] == selected_line]

# 역 선택 (디폴트: 한양대)
station_list = sorted(line_df["출발역"].dropna().unique())
default_station_idx = station_list.index("한양대") if "한양대" in station_list else 0
selected_station = st.selectbox("역을 선택하세요", station_list, index=default_station_idx)
station_df = line_df[line_df["출발역"] == selected_station]

# 요일 선택 (오늘 날짜 디폴트)
day_list = sorted(station_df["요일구분"].dropna().unique())
default_day_idx = day_list.index(today_day) if today_day in day_list else 0
selected_day = st.selectbox("요일을 선택하세요", day_list, index=default_day_idx)
day_df = station_df[station_df["요일구분"] == selected_day]

# 상하구분 선택
direction_list = sorted(day_df["상하구분"].dropna().unique())
selected_direction = st.selectbox("상하구분을 선택하세요", direction_list)
direction_df = day_df[day_df["상하구분"] == selected_direction]

# 선택한 조건 표시
st.subheader("선택한 조건")
st.write(f"선택한 노선: {selected_line}")
st.write(f"선택한 역: {selected_station}")
st.write(f"선택한 요일: {selected_day}")
st.write(f"선택한 상하구분: {selected_direction}")

# 원본 데이터 — 현재시간 열을 복사해 ⏰ 컬럼으로 앞에 추가
now_col_name = f"⏰ {closest_col}"
display_df = direction_df.copy()
display_df.insert(len(info_columns), now_col_name, display_df[closest_col])
ordered_cols = info_columns + [now_col_name] + time_columns

st.subheader("선택한 조건의 원본 데이터")
st.caption(f"현재시간({now.strftime('%H:%M')})과 가장 가까운 열: {closest_col}")
st.dataframe(
    display_df,
    use_container_width=True,
    column_order=ordered_cols,
)

# 혼잡도 그래프 시각화
y_values = direction_df[time_columns].values[0]

fig = go.Figure()

# 혼잡도 꺾은선
fig.add_trace(go.Scatter(
    x=time_columns,
    y=y_values,
    mode="lines+markers",
    name="혼잡도",
    marker=dict(size=6),
    line=dict(width=2),
))

# 현재시간 회색 수직선 (x축이 문자열이므로 add_shape 사용)
fig.add_shape(
    type="line",
    x0=closest_col, x1=closest_col,
    y0=0, y1=1,
    xref="x", yref="paper",
    line=dict(color="gray", width=2, dash="dash"),
)
fig.add_annotation(
    x=closest_col,
    y=1,
    xref="x", yref="paper",
    text=f"현재 {now.strftime('%H:%M')}",
    showarrow=False,
    yanchor="bottom",
    font=dict(color="gray", size=12),
)

fig.update_layout(
    title=f"{selected_line} {selected_station} {selected_day} {selected_direction} 혼잡도",
    xaxis_title="시간대",
    yaxis_title="혼잡도 (%)",
    xaxis=dict(tickangle=45),
    font=dict(family="Malgun Gothic", size=13),
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)

# 10초마다 자동 새로고침
time.sleep(10)
st.rerun()