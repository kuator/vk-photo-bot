# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
import json
import random
import requests
import os
from config import confirmation_token, community_token, user_token

app = Flask(__name__)

group_id='175402552'
album_id='258897132'

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        if 'attachments' not in data['object']:
            return 'ok'
        if len(data['object']['attachments'])==0:
            return 'ok'
        if data['object']['attachments'][0]['type'] != 'photo':
            return 'ok'
        owner_id = data['object']['attachments'][0]['photo']['owner_id']
        photo_id = data['object']['attachments'][0]['photo']['id']
        photo_full_id = f'{owner_id}_{photo_id}'
        if 'access_key' in data['object']['attachments'][0]['photo']:
            if len(data['object']['attachments'][0]['photo']['access_key'])>0:
                access_key = data['object']['attachments'][0]['photo']['access_key']
                photo_full_id = f'{photo_full_id}_{access_key}'

        user_id = data['object']['user_id']
        params = (
            ('peer_id', user_id),
            ('access_token', community_token),
            ('media_type', 'photo'),
            ('count', 20),
            ('v', 5.131),
            )
        response = requests.get('https://api.vk.com/method/messages.getHistoryAttachments', params=params)
        text = json.loads(response.text)
        image_url = text['response']['items'][0]['attachment']['photo']['sizes'][-1]['url']
        print(text['response']['items'])
        
        params = (
            ('group_id', group_id),
            ('album_id', album_id),
            ('access_token', user_token),
            ('v', 5.103),
            )
        response = requests.get('https://api.vk.com/method/photos.getUploadServer', params=params)
        text = json.loads(response.text)
        upload_server = json.loads(response.text)['response']['upload_url']
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
                ('group_id', group_id),
                ('album_id', album_id),
                ('hash', img_hash),
                ('photos_list', photos_list),
                ('server', server),
                ('access_token', user_token),
                ('v', 5.131),
                )
            response = requests.get('https://api.vk.com/method/photos.save', params=params)
        except Exception as e:
            print(e.message)
            raise e
        image_data = json.loads(response.text)
        photo_id=image_data['response'][0]['id']
        owner_id=image_data['response'][0]['owner_id']
        photo_full_id = f'photo{owner_id}_{photo_id}'
        user_id = data['object']['user_id']
        params = (
            ('user_id', user_id),
            ('attachment', photo_full_id),
            ('random_id', random.getrandbits(64)),
            ('message', 'привет, привет'),
            ('access_token', community_token),
            ('v', 5.131),
            )
        response = requests.get('https://api.vk.com/method/messages.send', params=params)
    return 'ok'


