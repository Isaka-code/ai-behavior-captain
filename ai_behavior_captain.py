
import PySimpleGUI as sg
sg.theme("LightBlue")
import pandas as pd
import random


# DB
df_behaviors = pd.read_csv("behaviors.csv") # 行動のリストをメモしたcsv
df_history = pd.read_csv("history.csv") # 行動の履歴をメモしたcsv

def get_actions():
    """
    ランダムに３つの行動を選択する
    """
    l = range(len(df_behaviors))
    l = random.sample(l, 3)
    print(l) # e.g. [2, 4, 0]

    action_0 = df_behaviors.NAME[l[0]]
    action_1 = df_behaviors.NAME[l[1]]
    action_2 = df_behaviors.NAME[l[2]]
    print(action_0, action_1, action_2)
    return action_0, action_1, action_2


# GUI app

action_0, action_1, action_2 = get_actions()
layout = [
    [sg.Button('AIおすすめボタン', key="-SUBMIT-")],
    [sg.Text('行動1位:'), sg.Button(f'{action_0}', key="-BEHAVIOR1-")],
    [sg.Text('行動2位:'), sg.Button(f'{action_1}', key="-BEHAVIOR2-")],
    [sg.Text('行動3位:'), sg.Button(f'{action_2}', key="-BEHAVIOR3-")],
    [sg.Text(key="-AMOUNT-", size=(120, 10))]
]

window = sg.Window("AI Behavior Captain", layout=layout, size=(300, 150))

while True:
    event, values = window.read()
    if event == "-SUBMIT-":
        action_0, action_1, action_2 = get_actions()

        window["-BEHAVIOR1-"].update(action_0)
        window["-BEHAVIOR2-"].update(action_1)
        window["-BEHAVIOR3-"].update(action_2)

    if event == sg.WIN_CLOSED:
        break



