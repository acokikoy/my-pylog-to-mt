# mt.py

import json
import requests

class DataAPI:
    def __init__(self):
        self.base_url = ''
        self.site_id = 1
        self.contenttype_id = 1

        self.username = ''
        self.password = '' 
        self.client_id = ''
        self.access_token = ''


    # コンテンツデータの一覧を取得(GET)
    # GET /v4/sites/:site_id/contentTypes/:content_type_id/data?limit=N
    def list_contents(self, limit=1):
        # url_list_contents = 'http://YourDomain/MT_Path/mt-data-api.cgi/v4/sites/1/contentTypes/2/data?limit=1'
        url_list_contents = self.base_url + '/sites/' + str(self.site_id) + '/contentTypes/' + str(self.contenttype_id) + '/data?limit=' + str(limit)

        # レスポンス取得
        r = requests.get(url_list_contents)
        return r.status_code, r.json()


    # コンテンツデータ1件取得(GET)
    # GET /v4/sites/:site_id/contentTypes/:content_type_id/data/:content_id 
    def get_content(self, contentdata_id):
        # url_get_content = 'http://YourDomain/MT_Path/mt-data-api.cgi/v4/sites/1/contentTypes/2/data/XX'
        url_get_content = self.base_url + '/sites/' + str(self.site_id) + '/contentTypes/' + str(self.contenttype_id) + '/data/' + str(contentdata_id)

        headers = {}
        if self.access_token:
            auth = 'MTAuth accessToken=' + self.access_token
            headers = {'X-MT-Authorization': auth }
            
        # レスポンス取得
        r = requests.get(url_get_content, headers=headers)
        return r.status_code, r.json()

    # 認証(POST)
    # POST /v4/authentication
    def authenticate(self):
        # url_authentication = 'http://YourDomain/MT_Path/mt-data-api.cgi/v4/authentication'
        url_authentication = self.base_url + '/authentication'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {
            'username': self.username,
            'password': self.password, 
            'remenber': 1,
            'clientId': self.client_id
        }

        # レスポンス取得
        r = requests.post(url_authentication, params, headers=headers)
        self.access_token = r.json()['accessToken']
        return r.status_code, r.json()

    # コンテンツデータ投稿(POST)
    # POST /v4/sites/:site_id/contentTypes/:content_type_id/data
    def create_content(self, content_data):        
        '''
        # url_create_content = 'http://YourDomain/MT_Path/mt-data-api.cgi/v4/sites/1/contentTypes/2/data'
        Args:
            content_data(dict): {
                'data': [
                    {'data': '2018-12-17 23:00:00', 'id': '7', 'label': 'log_id'}, 
                    {'data': '383問中、333問修了', 'id': '8', 'label': 'progress'}, 
                    {'data': 'テスト投稿', 'id': '9', 'label': 'body'}], 
                'label': '2018-12-17 23:00:00', 
                'status': 'Publish'
            }
        '''
        url_create_content = self.base_url + '/sites/' + str(self.site_id) + '/contentTypes/' + str(self.contenttype_id) + '/data'

        auth = 'MTAuth accessToken=' + self.access_token
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-MT-Authorization': auth }

        r = requests.post(url_create_content, headers=headers, data='content_data='+json.dumps(content_data))
        return r.status_code, r.json()


# データ整形 - コンテンツデータ1個分
def fitem(item):
    '''
    コンテンツデータ1件分から使うデータだけ取り出し、
    扱い易い形に整形して返す
    '''

    content = {}

    content['id'] = item['id']
    content['author_name'] = item['author']['displayName']
    content['basename'] = item['basename']
    content['blog_id'] = item['blog']['id']
    content['createdDate'] = item['createdDate']
    content['modifiedDate'] = item['modifiedDate']
    content['date'] = item['date']
    content['label'] = item['label']
    content['status'] = item['status']
    content['updatable'] = item['updatable']

    # contentdata
    for cd in item['data']:
        label = cd['label']
        content[label] = cd['data']

    return content

# データ整形 - コンテンツ一覧
def fitems(r_json):
    '''
    get_contentsのレスポンス(json)を、各コンテンツデータが扱い易い形に整形して返す
    Args:
        r_json (dict): list_contents取得値
    Returns:
        total_items (int): 総データ数
        cnt_items: 今回取得したデータ数
        contents[id] (list): コンテンツデータ詳細
    '''
    # # レスポンスの結果を解析する
    total_items = r_json['totalResults'] # 全コンテンツ数
    items = r_json['items'] #コンテンツデータ詳細
    cnt_items = len(items) # 今回取得したコンテンツ数

    # コンテンツデータ値を扱いやすい形に再編
    contents = []
    for item in items:
        contents.append(fitem(item))

    return (total_items, cnt_items, contents)


if __name__ == '__main__':

    api = mt.DataAPI(base_url, site_id, contenttype_id)

    api.base_url = 'http://YourDomain/MT_Path/mt-data-api.cgi/v4'
    api.site_id = 1
    api.contenttype_id = 2
   
    api.username = 'MTユーザ名'
    api.password = 'Webサービスパスワード'
    api.client_id = 'my_pylog' #なんでもいい


    # r_status_code, r_json = api.list_contents()
    # r_status_code, r_json = api.get_content(2)
    # r_status_code, r_json = api.authenticate()
    api.authenticate()
    r_status_code, r_json = api.create_content()

    
    if r_status_code == 200:
        print('OK:', r_status_code)
    else:
        print('NG:', r_status_code)

    print(api.access_token)
    print(r_json)
