# AI Behavior Captain🤖
* AI Behavior Captain は、AIによる行動レコメンドアプリです。  
自分の行動をAIに決めてほしいときに使ってください。


# 使い方📖
* 必要なライブラリはrequirements.txtに書いています。
```
$ pip install -r requirements.txt  
```
* ai_behavior_captain.pyを実行するとGUIアプリが起動します  
```
$ python ai_behavior_captain.py  
```
* ”人工知能おすすめボタン”を押すと過去の行動から確率的に判断しておすすめの行動が表示されます。  
* ”人工無能おすすめボタン”を押すと完全にランダムにおすすめの行動が表示されます。  
* 行動ボタンをクリックすると、行動履歴が更新され、人工知能におすすめされやすくなります。  
* ”行動を追加する”をクリックすると、テキストボックスの中身が行動リストに追加されます。  
* 行動を削除したい場合は、delete_id.pyを用いてください。削除したいIDのリストを表示入力に空白区切りで与えると該当のIDの行を削除できます。下記はIDが8, 10を削除する例。  
```
$ python delete_id.py 8 10
```

<img src=images/スクリーンショット.png width="300">

# お知らせ💡
Qiitaに記事を書きました。実際の使用例などもあるので良かったら見てください！  
[意思決定に疲れたのでAI🤖による行動レコメンドアプリを作ってみた【人工無能】](https://qiita.com/Isaka-code/items/e440161fa50032ca80d7)