import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# データ生成関数
def generate_campaign_data(start_date, end_date, num_campaigns=5):
    date_range = pd.date_range(start=start_date, end=end_date)
    campaigns = [f'キャンペーン{i+1}' for i in range(num_campaigns)]
    
    data = []
    for date in date_range:
        for campaign in campaigns:
            row = {
                'キャンペーン': campaign,
                'キャンペーンの状態': np.random.choice(['有効', '一時停止', '削除'], p=[0.8, 0.15, 0.05]),
                'キャンペーン タイプ': np.random.choice(['検索', 'ディスプレイ', 'ショッピング', 'P-MAX'], p=[0.4, 0.3, 0.2, 0.1]),
                'クリック数': np.random.randint(10, 1000),
                '表示回数': np.random.randint(1000, 100000),
                'クリック率': np.random.uniform(0.01, 0.1),
                '通貨コード': 'JPY',
                '平均クリック単価': np.random.randint(50, 500),
                '費用': np.random.randint(1000, 100000),
                'コンバージョン': np.random.randint(0, 50),
                'ビュースルー コンバージョン': np.random.randint(0, 20),
                'コンバージョン単価': np.random.randint(1000, 10000),
                'コンバージョン率': np.random.uniform(0.01, 0.1)
            }
            data.append(row)
    
    df = pd.DataFrame(data)
    df['クリック率'] = df['クリック数'] / df['表示回数']
    df['コンバージョン率'] = df['コンバージョン'] / df['クリック数']
    df['コンバージョン単価'] = df['費用'] / df['コンバージョン'].where(df['コンバージョン'] > 0, 1)
    
    return df

# データ生成
start_date = '2024-09-20'
end_date = '2024-10-20'
df = generate_campaign_data(start_date, end_date)

# CSVファイルとして保存
df.to_csv('campaign.csv', index=False, encoding='utf-8-sig')

print("campaign.csvが生成されました。")