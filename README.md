# travel-AI

最適化とAIを活用した旅行プラン作成アプリ

## 概要

本アプリは、ユーザーが入力した条件や希望に基づき、AIと最適化アルゴリズムを組み合わせて旅行スケジュールを提案するアプリです。

- 観光地・飲食店の提案をAIが補助  
- 移動時間や時間帯制約を考慮したスケジュール作成  
- ホテルやレストランの情報をAPI経由で取得可能  
- ユーザー入力とデフォルト地点を組み合わせて柔軟にプランを生成  

## 特徴

1. **AIによる補助**  
   - ユーザーの自然言語入力を解析  
   - 観光地や飲食店、時間帯制約などをJSON形式で整理  

2. **最適化アルゴリズム**  
   - 移動時間や時間帯制約を考慮した旅行順序の最適化  
   - OR-Tools等を利用可能  

3. **API連携**  
   - ホテル情報やレストラン情報を取得可能  
   - 移動時間の計算に交通API利用可能  

4. **柔軟なカスタマイズ**  
   - デフォルトで設定した観光地やスポットを保持  
   - ユーザー入力による補足条件を統合  

```bash
travel-AI/
│
├── .env                          # APIキーなどの環境変数
├── requirements.txt              # 依存パッケージ
├── README.md                     # プロジェクト説明
│
├── src/
│   ├── main.py                   # メイン実行スクリプト
│   │
│   ├── language/                 
│   │   └── language_parser.py    # 言語解析（OpenAI利用）
│   │
│   ├── hotel/                    
│   │   └── hotel_search.py       # ホテル検索
│   │
│   ├── route/                    
│   │   └── route_planner.py      # 経路最適化
│   │
│   ├── restaurant/               
│   │   └── restaurant_search.py  # レストラン検索
│   │
│   └── utils/
│       └── config_loader.py      # .env読込用ユーティリティ
│
└── notebooks/
    └── development.ipynb         # 開発・検証用ノートブック
```

## ⚙️ 主な機能

| 機能カテゴリ | 説明 |
|---------------|------|
| 🗣 **言語解析 (language)** | ユーザーの自然言語入力を解析し、観光地・飲食店・時間制約などをJSON形式で整理 |
| 🏨 **ホテル検索 (hotel)** | 観光地やチェックイン時間に基づき、最適なホテルエリアを検索 |
| 🚗 **経路最適化 (route)** | 観光地の順序や制約条件をもとに最適経路を計算 |
| 🍽 **レストラン検索 (restaurant)** | 食事時間やエリアに応じて候補の飲食店を提案 |

## .envファイル設定
`.env` ファイルにAPIキーを保存します。  
例：
- GOOGLE_API_KEY=your_google_api_key_here
- HOTEL_API_KEY=your_hotel_api_key_here
- RESTAURANT_API_KEY=your_restaurant_api_key_here

## 実行確認（Python 3.11以上推奨）
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt

### ユーザー入力の解析を確認
python src/language_parser.py

