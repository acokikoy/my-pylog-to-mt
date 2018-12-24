# my_pylog.py
# Pythonの勉強履歴。ログデータはDataAPI経由でMTに保存する。

from datetime import datetime
import re

import mt


def show_log(log:dict):
    '''取得したログを整形して表示'''
    log_date = log['log_id']
    body = log['body']
    progress = log['progress']

    if progress:
        progress = '[[' + progress + ']], '

    print(f'{log_date} -- {progress}{body}')


# DataAPIの準備
api = mt.DataAPI()

api.base_url = 'http://YourDomain/MT_Path/mt-data-api.cgi/v4'
api.site_id = 1 #対象サイトのID
api.contenttype_id = 2 #対象コンテンツタイプのID
api.username = 'MTユーザ名'
api.password = 'Webサービスパスワード'
api.client_id = 'my_pylog' #なんでもいい

# DataAPI: 直前のログ1件を取得
r_status_code, r_json = api.list_contents(limit=1)

if r_status_code == 200:
    # 取得した直前のログを、整形して表示
    content = mt.fitems(r_json)[2][0]    
    print('last log:')
    show_log(content)

else:
    print('NG:', r_status_code)


# 新しいログを入力
# 書式: [[progress]], body  ※[[progress]], は省略可能
i = input("input new log:\n  ")

i.strip()
m = re.match('(\[\[(.+?)\]\],\s*)*(.+)$', i)

body = m.group(3)
progress = m.group(2)
if progress == None:
    progress = ''

#現在日時を取得してstr_nowにセット
dt = datetime.now()
str_now = datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')

# DataAPI: 投稿
content_data = {
    'data': [
        {'data': str_now, 'id': '7', 'label': 'log_id'}, 
        {'data': progress, 'id': '8', 'label': 'progress'}, 
        {'data': body, 'id': '9', 'label': 'body'}], 
    'label': str_now,
    'status': 'Publish'
}

# 認証が通ると api.access_token にアクセストークンがセットされる。
api.authenticate()

# 一件投稿
r_status_code, r_json = api.create_content(content_data)

# 結果表示: レスポンスを整形して表示する
if r_status_code == 200:
    print('logged:')
    show_log(mt.fitem(r_json))
    
else:
    print('NG:', r_status_code)


# 'done'と表示しておしまい
print('done')
