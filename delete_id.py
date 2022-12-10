import pandas as pd
import sys

def delete_id():
    """
    Usage:
        $ python delete_id.py 8 10
    """
    # データ読み込み
    df_behaviors = pd.read_csv("data/behaviors.csv") # 行動テーブルをメモしたCSV
    df_history = pd.read_csv("data/history.csv") # 行動の履歴をメモしたCSV

    # コマンドライン引数のidリストの行動データを行動テーブルと、行動履歴から削除する
    for id in sys.argv[1:]:
        print(f"ID = {id}のデータを削除します")
        df_behaviors = df_behaviors.loc[df_behaviors.ID != int(id), :]
        df_history = df_history.loc[df_history.ITEM_ID != int(id), :]

    # 結果を表示
    print(df_behaviors)
    print(df_history)

    # CSVに書き込む
    df_behaviors.to_csv("data/behaviors.csv", index=False)
    df_history.to_csv("data/history.csv", index=False)


if __name__ == "__main__":
    delete_id()
