import random
import datetime
import pandas as pd
import numpy as np
from scipy.special import softmax
import pyautogui
import PySimpleGUI as sg
sg.theme("LightBlue")

class AiBehaviorCaptain:
    def __init__(self, recomend_num, is_save, is_screenshot=False, show_num=4):
        # データ読み込み
        self.df_behaviors = pd.read_csv("data/behaviors.csv") # 行動テーブルをメモしたCSV
        self.df_history = pd.read_csv("data/history.csv") # 行動の履歴をメモしたCSV

        # ハイパーパラメータ
        self.recomend_num = recomend_num # レコメンド数
        self.is_save = is_save # CSVに保存する場合はTrue
        self.is_screenshot = is_screenshot # 画面のスクリーンショットを保存する場合はTrue　※Qiitaに記事を投稿するために使用
        self.show_num = show_num # データ更新時にターミナルに表示する行数

    def get_behaviors(self, algo_name):
        """
        アルゴリズム名を入力とし、選択された行動リストを返す
        """
        # 行動数が少ない場合はあるものだけを返す
        if len(self.df_behaviors) < self.recomend_num:
            return self.df_behaviors.NAME.unique().tolist() + [""] * (self.recomend_num - len(self.df_behaviors.NAME.unique()))
        # アルゴリズムがランダムの場合
        elif algo_name == "random":
            return self.random_get_behaviors()
        # アルゴリズムがソフトマックスの場合
        elif algo_name == "softmax":
            return self.softmax_get_behaviors()

    def random_get_behaviors(self):
        """
        アルゴリズムA : ランダムに行動を選択する
        """
        # ランダムに行動テーブルのインデックスを選ぶ
        l = range(len(self.df_behaviors))
        l = random.sample(l, self.recomend_num)

        # 選択された行動をリストにappendする
        behavior_list = []
        for i in range(self.recomend_num):
            behavior = self.df_behaviors.NAME[l[i]]
            behavior_list.append(behavior)
        return behavior_list
    
    def softmax_get_behaviors(self):
        """
        アルゴリズムB : softmax関数の値に基づき、確率的に行動を選択する
        """
        # 行動の選択された回数を数える
        behaviors_count = self.df_history.groupby("ITEM_ID").count()["DATE"]
        behaviors_num = len(behaviors_count)
        # softmax関数の値を計算する
        m = softmax(behaviors_count).tolist()
        # softmax関数の値に基づき、確率的に行動を選択する
        l = np.random.choice(behaviors_num, self.recomend_num, p=m, replace=False)

        # 選択された行動をリストにappendする
        behavior_list = []
        for i in range(self.recomend_num):
            behavior = self.df_behaviors.NAME[l[i]]
            behavior_list.append(behavior)
        return behavior_list

    def write_behavior(self, behavior_name):
        # 行動テーブルに書き込む
        last_ID = max(self.df_behaviors.ID.unique()) # 行動テーブルの最後のID
        self.df_behaviors.loc[last_ID + 1] = [last_ID + 1, behavior_name]
        
        if self.is_save:
            self.df_behaviors.to_csv("data/behaviors.csv", index=False) # CSVに書き込む
        print(f"{behavior_name}が行動テーブルに追加されました")   
        print(self.df_behaviors.iloc[-self.show_num:])

    def add_history(self, behavior_name):
        # 行動の履歴に追加する
        dt_now = datetime.datetime.now()
        behavior_ID = self.df_behaviors[self.df_behaviors.NAME == behavior_name].ID.unique()[0]
        df_new = pd.DataFrame({"DATE":[dt_now], "ITEM_ID":[behavior_ID]})
        self.df_history = pd.concat([self.df_history, df_new], axis=0, ignore_index=True)
        if self.is_save:
            self.df_history.to_csv("data/history.csv", index=False) # CSVに書き込む
        print(f"{behavior_name}が行動履歴に追加されました")
        print(self.df_history.iloc[-self.show_num:])

    def app(self):
        """
        GUI アプリ関連
        """
        # 初期値の行動を取得
        behavior_list = self.get_behaviors("softmax")
        # GUIアプリのレイアウト
        behavior_layouts = [[sg.Text(f'行動{i+1}位:'), sg.Button(f'{behavior_list[i]}', key=f"-BEHAVIOR{i+1}-")] for i in range(self.recomend_num)]
        layout = [
            [sg.Button('人工知能おすすめボタン', key="-SUBMIT1-")],
            [sg.Button('人工無能おすすめボタン', key="-SUBMIT2-")],
            [sg.Text(key="-AMOUNT-", size=(10, 1))],
            behavior_layouts,
            [sg.Text(key="-ANNOUNCEMENT1-", size=(100, 1))],
            [sg.Button('行動を追加する', key="-ADD-"), sg.InputText(key="-NEW_behavior-", size=(120, 1))],
            [sg.Text(key="-ANNOUNCEMENT2-", size=(100, 1))],
            [sg.Text(key="-AMOUNT-", size=(10, 1))],
        ]
        # GUIアプリのウインドウ
        window = sg.Window("AI Behavior Captain", layout=layout, size=(400, 450))

        # アプリの起動
        while True:
            event, values = window.read()
            # Qiita投稿用に画面のスクリーンショットを撮る場合
            if self.is_screenshot:
                screenshot = pyautogui.screenshot(region = (755, 300, 430, 530))
                dt_now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                screenshot.save(f'images/{dt_now}.png')
            # 人工知能ボタンがクリックされた場合（確率的にレコメンド）
            if event == "-SUBMIT1-":
                behavior_list = self.get_behaviors("softmax")
                for i, behavior in enumerate(behavior_list):
                    window[f"-BEHAVIOR{i+1}-"].update(behavior)
            # 人工無能ボタンがクリックされた場合（ランダムにレコメンド）
            if event == "-SUBMIT2-":
                behavior_list = self.get_behaviors("random")
                for i, behavior in enumerate(behavior_list):
                    window[f"-BEHAVIOR{i+1}-"].update(behavior)
            # レコメンドされた行動ボタンがクリックされた場合
            for i in range(self.recomend_num):
                if event == f"-BEHAVIOR{i+1}-":
                    self.add_history(behavior_list[i]) # 行動履歴に追加する
                    window[f"-BEHAVIOR{i+1}-"].update(f"★{behavior_list[i]}★")
                    window["-ANNOUNCEMENT1-"].update(f"Let's {behavior_list[i]} !")
            # 行動を追加するボタンがクリックされた場合
            if event == "-ADD-":
                behavior_name = values["-NEW_behavior-"]
                # すでに行動テーブルに無いかチェック
                if behavior_name in self.df_behaviors.NAME.unique():
                    print(f"{behavior_name}はすでに存在します")
                    window["-ANNOUNCEMENT2-"].update(f"{behavior_name} exist !")
                else:
                    print(f"{behavior_name}は新規の行動です")
                    self.write_behavior(behavior_name) # 行動テーブルに追加する
                    self.add_history(behavior_name) # 行動履歴に追加する
                    window["-ANNOUNCEMENT2-"].update(f"{behavior_name} added !")

            # アプリの画面を閉じると終了
            if event == sg.WIN_CLOSED:
                break
            
            


if __name__ == "__main__":
    # ハイパーパラメータ
    recomend_num = 5 # レコメンド数
    is_save = True # CSVに保存する場合はTrue

    # インスタンスの生成
    abc = AiBehaviorCaptain(recomend_num, is_save)
    # GUIアプリたち
    abc.app()
