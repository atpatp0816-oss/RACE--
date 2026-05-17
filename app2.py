import streamlit as st
import pandas as pd

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


#상하구분 선택

direction_list = sorted(day_df["상하구분"].dropna().unique())
selected_direction = st.selectbox("상하구분을 선택하세요", direction_list)

# 선택한 노선 + 역 + 상하구분에 해당하는 데이터 필터링
direction_df = day_df[day_df["상하구분"] == selected_direction]


st.subheader("선택한 조건")
st.write(f"선택한 노선: {selected_line}")
st.write(f"선택한 역: {selected_station}")
st.write(f"선택한 요일: {selected_day}")
st.write(f"선택한 상하구분: {selected_direction}")
st.subheader("선택한 조건의 원본 데이터")
st.dataframe(direction_df)



#혼잡도 그래프 시각화
import matplotlib.pyplot as plt


#한글 폰트 설정(Windows의 경우 "Malgun Gothic" 사용)(글자가 안깨지게 설정)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False



x_values=[]
y_values=[]
info_columns = ["요일구분", "호선", "역번호", "출발역", "상하구분"]
for column in df.columns:
    if column not in info_columns:
        y_values.append(direction_df[column].values[0])
        x_values.append(column)
plt.figure(figsize=(10, 5))
plt.plot(x_values, y_values, marker="o")
plt.title(f"{selected_line} {selected_station} {selected_day} {selected_direction} 혼잡도")
plt.xlabel("시간대")
plt.ylabel("혼잡도")
plt.xticks(rotation=45) #x축 레이블을 45도 회전하여 겹치지 않도록 설정
st.pyplot(plt)



# 혼잡도 등급 분류 함수
def classify_congestion(value):
    if value <= 25:
        return "여유"
    elif value <= 50:
        return "보통"
    elif value <= 75:
        return "주의"
    else:
        return "혼잡"


# 등급별 색상 지정 함수
def color_congestion_level(level):
    if level == "여유":
        return "background-color: #d9fdd3"
    elif level == "보통":
        return "background-color: #d6eaff"
    elif level == "주의":
        return "background-color: #fff3cd"
    elif level == "혼잡":
        return "background-color: #f8d7da"
    else:
        return ""

# x_values, y_values를 이용해서 새 표 생성
congestion_table = pd.DataFrame({
    "시간대": x_values,
    "혼잡도": y_values
})

# 여기서 classify_congestion 함수가 호출됨
congestion_table["등급"] = congestion_table["혼잡도"].apply(classify_congestion)

# 여기서 color_congestion_level 함수가 호출됨
styled_table = congestion_table.style.map(
    color_congestion_level,
    subset=["등급"]
)

st.subheader("시간대별 혼잡도 등급표")
st.dataframe(styled_table)

#streamlit 실행법: python -m streamlit run app2.py :)
