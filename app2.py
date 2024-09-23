import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# データの読み込み
@st.cache_data
def load_data():
    df = pd.read_csv('business_simulation_data.csv')
    return df

df = load_data()

# アプリケーションのタイトル
st.title('事業シミュレーションデータの可視化と分析')

# 事業ごとの統計量を表示
st.header('事業ごとの統計量')

# 事業ごとに統計量を計算
business_stats = df.groupby('事業名').describe()

# 統計量を横軸に事業名、縦軸に統計量を表示
st.write(business_stats)

# 事業名ごとの売上の合計を計算
total_sales_by_business = df.groupby('事業名')['売上'].sum().reset_index()

# 売上の棒グラフを作成
st.header('事業名ごとの売上合計')
fig_sales = px.bar(total_sales_by_business, x='事業名', y='売上', title='事業名ごとの売上合計', color='売上')
st.plotly_chart(fig_sales)

# 流入経路ごとの売上の合計を計算
total_sales_by_source = df.groupby('流入経路')['売上'].sum().reset_index()

# 流入経路の棒グラフを作成
st.header('流入経路ごとの売上合計')
fig_source = px.bar(total_sales_by_source, x='流入経路', y='売上', title='流入経路ごとの売上合計', color='売上')
st.plotly_chart(fig_source)

# 地域ごとの売上の合計を計算
total_sales_by_region = df.groupby('地域')['売上'].sum().reset_index()

# 地域の棒グラフを作成
st.header('地域ごとの売上合計')
fig_region = px.bar(total_sales_by_region, x='地域', y='売上', title='地域ごとの売上合計', color='売上')
st.plotly_chart(fig_region)

# 売上と流入経路の散布図
st.header('売上 vs 流入経路')
fig_scatter = px.scatter(df, x='流入経路', y='売上', color='事業名', title='売上と流入経路の関係', 
                         hover_data=['ユーザー名', 'created_at'])
st.plotly_chart(fig_scatter)

# 売上のヒストグラム
st.header('売上の分布')
fig_histogram = px.histogram(df, x='売上', title='売上の分布', nbins=30)
st.plotly_chart(fig_histogram)

# 売上の相関行列を表示
st.header('売上の相関行列')
correlation_matrix = df.corr()
st.write(correlation_matrix)

# 相関行列のヒートマップを作成
fig_heatmap = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale='Viridis'
))
fig_heatmap.update_layout(title='相関行列のヒートマップ')
st.plotly_chart(fig_heatmap)