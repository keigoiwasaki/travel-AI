# 必要ライブラリ
from openai import OpenAI
import json
import os
from dotenv import load_dotenv


# .env から APIキーを読み込む
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(".env に OPENAI_API_KEY が設定されていません。")


# OpenAIクライアント設定
client = OpenAI(api_key=api_key)


# 制約解析関数
def parse_user_constraints(user_input):
    """
    ユーザーの文章から観光地・飲食店の制約（時間・補足情報）だけをJSONで整理
    """
    system_prompt = """
あなたは旅行プランAIです。ユーザーの文章から、観光地または飲食店に関する制約だけをJSONで整理してください。
{
    "place_constraints": [
        {
            "place": "観光地または飲食店名",
            "type": "観光地 または 飲食店",
            "time_preference": "午前/午後/夜/指定なし",
            "notes": "ユーザーの補足情報や希望"
        }
    ]
}
注意:
- 座標は出力しない
- デフォルトの場所に関しては出力しない
- "type" は必ず "観光地" か "飲食店"
- JSON形式に厳密にしてください
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 最新かつ高速なGPT-4系モデル
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.0,
        max_tokens=400
    )

    ai_output = response.choices[0].message.content

    # JSONパース処理
    try:
        parsed_json = json.loads(ai_output)
    except json.JSONDecodeError:
        parsed_json = {"error": "JSON形式に変換できませんでした", "raw_output": ai_output}
    return parsed_json



# マージ関数
def merge_constraints(default_places, ai_constraints):
    """
    デフォルト情報とAI解析結果を統合
    - すでに存在する場所は重複せず、補足情報を更新
    """
    merged = {dp['place']: dp for dp in default_places}

    for c in ai_constraints.get("place_constraints", []):
        place = c["place"]
        if place in merged:
            # 既存のデフォルトに補足情報をマージ
            if c.get("time_preference") and c["time_preference"] != "指定なし":
                merged[place]["time_preference"] = c["time_preference"]
            if c.get("notes"):
                merged[place]["notes"] = c["notes"]
        else:
            # 新しい場所は追加
            merged[place] = c

    return {"place_constraints": list(merged.values())}



# テスト実行
if __name__ == "__main__":
    # デフォルト設定（ユーザーがUI上で選択した観光地一覧）
    default_places = [
        {"place": "新宿歌舞伎町", "type": "観光地", "time_preference": "指定なし", "notes": "デフォルト設定"},
        {"place": "渋谷スクランブル交差点", "type": "観光地", "time_preference": "指定なし", "notes": "デフォルト設定"}
    ]

    # ユーザー入力
    user_input = "新宿歌舞伎町には午前中に行きたい。スカイツリーは夜に行きたい。その周辺でディナーをしたい。"

    # AIで補足条件を解析
    ai_constraints = parse_user_constraints(user_input)

    # デフォルト情報とマージ
    final_constraints = merge_constraints(default_places, ai_constraints)

    # 結果出力
    print(json.dumps(final_constraints, ensure_ascii=False, indent=2))
