import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 事業名のリスト
businesses = [
    "エンベーダー",
    "rireki",
    "システム・アプリ開発",
    "RareTECH：受講料",
    "RareTECH：職業紹介",
    "RareTECH：法人"
]

# ユーザー名の生成
def generate_usernames(num_users):
    return [f"ユーザー{str(i).zfill(3)}" for i in range(1, num_users + 1)]

# データ生成関数
def generate_data(num_records):
    data = []
    usernames = generate_usernames(num_records)

    # 流入経路の選択肢と確率
    inflow_channels = ['SNS', '検索エンジン', '広告', '口コミ', 'メール'] + businesses
    probabilities = [0.2, 0.2, 0.2, 0.2, 0.1] + [0.1] * len(businesses)

    # 確率の合計を確認
    total_probability = sum(probabilities)
    if total_probability != 1.0:
        # 確率が1でない場合、正規化する
        probabilities = [p / total_probability for p in probabilities]

    for i in range(num_records):
        record = {
            '事業名': np.random.choice(businesses),
            'ユーザー名': usernames[i],
            'created_at': datetime.now() - timedelta(days=np.random.randint(0, 365)),
            '売上': np.random.randint(1000, 100000),  # 売上は1000から100000の範囲
            '流入経路': np.random.choice(inflow_channels, p=probabilities),  # 確率を指定
            '地域': np.random.choice(['東京', '大阪', '名古屋', '福岡', '札幌'])  # その他のカラム
        }
        data.append(record)

    return pd.DataFrame(data)

# データ生成
num_records = 1000  # レコード数
df = generate_data(num_records)

# CSVファイルとして保存
df.to_csv('business_simulation_data.csv', index=False, encoding='utf-8-sig')

print("business_simulation_data.csvが生成されました。")
