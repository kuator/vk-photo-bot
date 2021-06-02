# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
import json
import vk
import random
import requests
import os

app = Flask(__name__)

confirmation_token='c215ebfc'
access_token='92be9d44a157e45763b9e91ef024343680924dbe669fe6a2bc8cce0b9a877c97e05f7edce74d846d9fcc2'
user_token='0197551beaf8129ffda3a5ea8e2a4fca268fd70e0b7f249ec2a2799a8b1e66cdc3349a8f286ec489dba18'
user_id=343976380

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        params = (
            ('group_id', '175402552'),
            ('album_id', '258897132'),
            ('access_token', user_token),
            ('v', 5.103),
            )
        # photo_id='457240575'
        # owner_id='-175402552'
        # photo_full_id = f'photo{owner_id}_{photo_id}'

        # print(photos_list)
        # params = (
        #     ('user_id', '175402552'),
        #     ('album_id', '258897132'),
        #     ('attachments', photo_full_id),
        #     ('random_id', random.getrandbits(64)),
        #     ('message', 'sent'),
        #     ('access_token', access_token),
        #     ('reply_to', int(id)),
        #     ('v', 5.103),
        #     )
        # response = requests.get('https://api.vk.com/method/messages.send', params=params)
        response = requests.get('https://api.vk.com/method/photos.getUploadServer', params=params)
        upload_server = json.loads(response.text)['response']['upload_url']
        image_url = "https://sun9-40.userapi.com/impg/c855532/v855532066/2514a2/lL9OCsanJv0.jpg?size=1366x768&quality=96&sign=ef82a20c947a8dced9d351428d63f565&type=album"
        file_path = os.path.basename(image_url)
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)

        try:
            files = {'file1': open(file_path, 'rb')}
            response = requests.post(upload_server, files=files)
        except Exception as e:
            print(e.message)
            raise e
        os.remove(file_path)
        img_hash = json.loads(response.text)['hash']
        photos_list = json.loads(response.text)['photos_list']
        server = json.loads(response.text)['server']
        try:
            params = (
                ('group_id', '175402552'),
                ('album_id', '258897132'),
                ('hash', img_hash),
                ('photos_list', photos_list),
                ('server', server),
                ('access_token', user_token),
                ('v', 5.103),
                )
            response = requests.get('https://api.vk.com/method/photos.save', params=params)
        except Exception as e:
            print(e.message)
            raise e
        # print(type(json.loads(response.text)))
        image_data = json.loads(response.text)
        # print(data['response'][0]['owner_id'])
        photo_id=image_data['response'][0]['id']
        owner_id=image_data['response'][0]['owner_id']
        photo_full_id = f'photo{owner_id}_{photo_id}'
        print(photo_full_id)
        # print(photos_list)
        session = vk.Session()
        api = vk.API(session, v='5.110')
        # print(data)
        user_id = data['object']['user_id']
        api.messages.send(access_token=access_token, user_id=str(user_id), message='Привет!', attachment=photo_full_id, random_id=random.getrandbits(64))
        return 'ok'
    return 'ok'


