# app.py

# import pandas as pd

# df = pd.read_csv("data/subway_congestion_raw.csv", encoding="cp949")

# print(df.head())
# print(df.columns)
# print(df["호선"].unique())



# import pandas as pd

# df = pd.read_csv("data/subway_congestion_raw.csv", encoding="cp949")

# print(df.head())
# print(df.columns)





# print("데이터 앞부분")
# print(df.head())

# print("\n컬럼 목록")
# print(df.columns)

# print("\n데이터 크기")
# print(df.shape)



# print("전체 호선 목록")
# print(df["호선"].unique())




# target_lines = ["2호선", "3호선"]

# df_filtered = df[df["호선"].isin(target_lines)]

# print("\n2호선, 3호선만 필터링한 데이터")
# print(df_filtered.head())

# print("\n필터링 후 호선 목록")
# print(df_filtered["호선"].unique())

# print("\n필터링 후 데이터 크기")
# print(df_filtered.shape)




import pandas as pd

df = pd.read_csv("data/subway_congestion_raw.csv", encoding="cp949")

target_lines = ["2호선", "3호선"]
df_filtered = df[df["호선"].isin(target_lines)]

print("필터링 후 호선 목록")
print(df_filtered["호선"].unique())

print("\n2호선, 3호선 역 목록")
print(df_filtered["출발역"].unique())






selected_line = "2호선"

line_data = df_filtered[df_filtered["호선"] == selected_line]

print("\n선택한 노선:", selected_line)
print(line_data.head())

print("\n선택한 노선의 역 목록")
print(line_data["출발역"].unique())







selected_station = "강남"

station_data = line_data[line_data["출발역"] == selected_station]

print("\n선택한 역:", selected_station)
print(station_data)


