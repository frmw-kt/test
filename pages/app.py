import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# カスタムCSSの定義
st.markdown("""
<style>
.big-font {
    font-size:50px !important;
    font-weight: bold;
    color: #000000;  # ドジャーブルー
    padding: 20px 0px;
    border-radius: 10px;
    background: linear-gradient(to right, #FFFFFF, #FFFFFF);
    text-align: left;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)


# データの読み込み
@st.cache_data
def load_data():
    df = pd.read_csv('campaign.csv')
    return df
df = load_data()

# 空白行を追加する関数
def add_space(num_lines=1):
    for _ in range(num_lines):
        st.markdown("&nbsp;")


# アプリケーションのタイトル
st.markdown('<p class="big-font">　Dashboard</p>', unsafe_allow_html=True)


# サイドバーでキャンペーンを選択
selected_campaigns = st.sidebar.multiselect(
    'キャンペーンを選択',
    options=df['キャンペーン'].unique(),
    default=df['キャンペーン'].unique()
)
# 選択されたキャンペーンでデータをフィルタリング
filtered_df = df[df['キャンペーン'].isin(selected_campaigns)]



# 概要統計
add_space(2)
st.header('概要統計', divider="gray")
total_clicks = filtered_df['クリック数'].sum()
total_impressions = filtered_df['表示回数'].sum()
total_conversions = filtered_df['コンバージョン'].sum()
total_cost = filtered_df['費用'].sum()

# 1行目：クリック数と表示回数
row1_col1, row1_col2 = st.columns(2)
row1_col1.metric("総クリック数", f"{total_clicks:,}")
row1_col2.metric("総表示回数", f"{total_impressions:,}")

# 2行目：コンバージョン数と費用
row2_col1, row2_col2 = st.columns(2)
row2_col1.metric("総コンバージョン数", f"{total_conversions:,}")
row2_col2.metric("総費用", f"{filtered_df['通貨コード'].iloc[0]} {total_cost:,.0f}")

# キャンペーンパフォーマンス比較
add_space(2)
st.header('キャンペーンパフォーマンス比較', divider="gray")
fig = go.Figure(data=[
    go.Bar(name='クリック数', x=filtered_df['キャンペーン'], y=filtered_df['クリック数']),
    go.Bar(name='コンバージョン', x=filtered_df['キャンペーン'], y=filtered_df['コンバージョン'])
])
fig.update_layout(barmode='group', title='キャンペーン別クリック数とコンバージョン')
st.plotly_chart(fig)

# パフォーマンス指標テーブル
st.dataframe(filtered_df.style.format({
    '表示回数': '{:,.0f}',
    'クリック率': '{:.2%}',
    'クリック数': '{:,.0f}',
    'コンバージョン率': '{:.2%}',
    'コンバージョン': '{:.0f}',
    '平均クリック単価': '{:.2f}',
    'コンバージョン単価': '{:.2f}',
    '費用': '{:.0f}',
}))


# キャンペーンタイプ別の分析
add_space(2)
st.header('キャンペーンタイプ別分析', divider="gray")
campaign_type_data = filtered_df.groupby('キャンペーン タイプ').agg({
    'クリック数': 'sum',
    '表示回数': 'sum',
    'コンバージョン': 'sum',
    '費用': 'sum'
}).reset_index()

campaign_type_data['CTR'] = campaign_type_data['クリック数'] / campaign_type_data['表示回数']
campaign_type_data['CVR'] = campaign_type_data['コンバージョン'] / campaign_type_data['クリック数']
campaign_type_data['CPC'] = campaign_type_data['費用'] / campaign_type_data['クリック数']

fig = px.bar(campaign_type_data, x='キャンペーン タイプ', y=['クリック数', 'コンバージョン'], 
             title='キャンペーンタイプ別のパフォーマンス')
st.plotly_chart(fig)

st.dataframe(campaign_type_data.style.format({
    'クリック数': '{:,.0f}',
    '表示回数': '{:,.0f}',
    'コンバージョン': '{:.0f}',
    '費用': '{:.0f}',
    'CTR': '{:.2%}',
    'CVR': '{:.2%}',
    'CPC': '{:.2f}'
}))




# 散布図：クリック数 vs コンバージョン
add_space(2)
st.header('クリック率 - コンバージョン率', divider="gray")
fig = px.scatter(filtered_df, x='クリック率', y='コンバージョン率', color='キャンペーン', 
                 size='費用', hover_data=['キャンペーン タイプ'], title='クリック率 - コンバージョン率')
st.plotly_chart(fig)

