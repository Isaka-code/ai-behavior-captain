# https://www.youtube.com/watch?v=pk6fgvKQ7q4  

import PySimpleGUI as sg

sg.theme("LightBlue")
# PySimpleGUIの基本① (テキスト表示)  PySimpleGUIの基本② (入力値を取得)
layout = [
    [sg.Text('名前'), sg.InputText(key="-NAME-")],
    [sg.Text('住所'), sg.InputText(key="-ADDRESS-")],
    [sg.Button('実行', key="-SUBMIT-")]
]
window = sg.Window("isax app", layout=layout, size=(300, 150))

while True:
    event, values = window.read()
    print(values)
    if event == "-SUBMIT-":
        print(values["-NAME-"])
        print(values["-ADDRESS-"])
    if event == sg.WIN_CLOSED:
        break

# PySimpleGUIの基本③ (コンボボックスと画面更新)

layout = [
    [sg.Text('牛乳（150円）:'), 
    sg.Combo(list(range(1, 11)), key="-QUANTITY-"),
    sg.Text("個")],
    [sg.Button('購入', key="-SUBMIT-")],
    [sg.Text(key="-AMOUNT-", size=(120, 10))]
]

window = sg.Window("isax app", layout=layout, size=(300, 150))

while True:
    event, values = window.read()
    print(values)
    if event == "-SUBMIT-":
        total=150 * int(values["-QUANTITY-"])
        window["-AMOUNT-"].update(value=f'金額：{total}')

    if event == sg.WIN_CLOSED:
        break

# Web APIと組み合わせる

import requests

layout = [
    [sg.Text('郵便番号:'), 
    sg.InputText(key="-NUMBER1-", size=(10, 3)),
    sg.Text("-"),
    sg.InputText(key="-NUMBER2-", size=(10, 3))],
    [sg.Text('住所:',size=(5,5)),
    sg.Text(key="-ADDRESS-", size=(20, 5))],
    [sg.Button('実行', key="-SUBMIT-")]
]

window = sg.Window("isax app", layout=layout, size=(300, 150))

while True:
    event, values = window.read()
    print(values)
    if event == "-SUBMIT-":
        num1=values["-NUMBER1-"]
        num2=values["-NUMBER2-"]
        URL="https://zipcloud.ibsnet.co.jp/api/search"
        res = requests.get(f"{URL}?zipcode={num1}{num2}")
        res_json=res.json()
        if res_json["status"]==200:
            result=res_json["results"][0]
            adr1=result["address1"]
            adr2=result["address2"]
            adr3=result["address3"]
            window["-ADDRESS-"].update(f"{adr1}{adr2}{adr3}")
        else:
            window["-ADDRESS-"].update("住所の取得に失敗")

