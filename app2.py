import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("서울 지하철 혼잡도 분석 대시보드")

# CSV 불러오기
df = pd.read_csv("data/subway_congestion_raw.csv", encoding="cp949")

# 컬럼명 앞뒤 공백 제거
df.columns = df.columns.str.strip()

# 노선 선택
line_list = sorted(df["호선"].dropna().unique())
selected_line = st.selectbox("노선을 선택하세요", line_list)

# 선택한 노선에 해당하는 데이터만 필터링
line_df = df[df["호선"] == selected_line]

# 역 선택
station_list = sorted(line_df["출발역"].dropna().unique())
selected_station = st.selectbox("역을 선택하세요", station_list)

# 선택한 노선 + 역에 해당하는 데이터 필터링
station_df = line_df[line_df["출발역"] == selected_station]

# 요일 선택
day_list = sorted(station_df["요일구분"].dropna().unique())
selected_day = st.selectbox("요일을 선택하세요", day_list)

# 선택한 노선 + 역 + 요일에 해당하는 데이터 필터링
day_df = station_df[station_df["요일구분"] == selected_day]

# 상하구분 선택
direction_list = sorted(day_df["상하구분"].dropna().unique())
selected_direction = st.selectbox("상하구분을 선택하세요", direction_list)

# 선택한 노선 + 역 + 요일 + 상하구분에 해당하는 데이터 필터링
direction_df = day_df[day_df["상하구분"] == selected_direction]

# 선택한 조건 표시
st.subheader("선택한 조건")
st.write(f"선택한 노선: {selected_line}")
st.write(f"선택한 역: {selected_station}")
st.write(f"선택한 요일: {selected_day}")
st.write(f"선택한 상하구분: {selected_direction}")
st.subheader("선택한 조건의 원본 데이터")
st.dataframe(direction_df)

# 혼잡도 그래프 시각화
info_columns = ["요일구분", "호선", "역번호", "출발역", "상하구분"]
time_columns = [col for col in df.columns if col not in info_columns]
y_values = direction_df[time_columns].values[0]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=time_columns,
    y=y_values,
    mode="lines+markers",
    marker=dict(size=6),
    line=dict(width=2),
))
fig.update_layout(
    title=f"{selected_line} {selected_station} {selected_day} {selected_direction} 혼잡도",
    xaxis_title="시간대",
    yaxis_title="혼잡도 (%)",
    xaxis=dict(tickangle=45),
    font=dict(family="Malgun Gothic", size=13),
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)