import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

alist=[
    "something1",
    "something12",
    "something17",
    "something2",
    "something25",
    "something29"]

alist.sort(key=natural_keys)
print(alist)


dict = {
    "type": "message_new",
    "object": {
        "id": 19634,
        "date": 1622691335,
        "out": 0,
        "user_id": 343976380,
        "read_state": 0,
        "title": "",
        "body": "",
        "attachments": [
            {
                "type": "photo",
                "photo": {
                    "album_id": -3,
                    "date": 1622691332,
                    "id": 457250516,
                    "owner_id": 343976380,
                    "has_tags": False,
                    "access_key": "d39b82feb1a1da745c",
                    "height": 673,
                    "photo_130": "https://sun9-61.userapi.com/impg/Py-KUAM6cRk2WLqumUAmm-tuGIiv-Tdjavh_PQ/0MFduOb-PNc.jpg?size=130x117&quality=96&sign=0f3fdf92504e38de220e7fa55ca6d330&c_uniq_tag=eHye8awA1SJ-EBsUuIzCd2Nuj3fimypdF7FeyE9RRnU&type=album",
                    "photo_604": "https://sun9-61.userapi.com/impg/Py-KUAM6cRk2WLqumUAmm-tuGIiv-Tdjavh_PQ/0MFduOb-PNc.jpg?size=604x542&quality=96&sign=82498a01d3ae3417333735d696be7628&c_uniq_tag=EQ9qJwHoGJ9vGmwuB3z4mxXmml8aazhOBc5v67hPux0&type=album",
                    "photo_75": "https://sun9-61.userapi.com/impg/Py-KUAM6cRk2WLqumUAmm-tuGIiv-Tdjavh_PQ/0MFduOb-PNc.jpg?size=75x67&quality=96&sign=5600a6acfdae36a485177fb283ae173e&c_uniq_tag=iX6MgP_B2auPNaWb03Q_1U5Q6dJGRsHnosGk47dMogc&type=album",
                    "photo_807": "https://sun9-61.userapi.com/impg/Py-KUAM6cRk2WLqumUAmm-tuGIiv-Tdjavh_PQ/0MFduOb-PNc.jpg?size=750x673&quality=96&sign=98d5df248f195a8fc7294639ae3aceb8&c_uniq_tag=FUwm2C1FThgtt6xx9uhuqG92rrcXBx8aq7lwrV0qTcg&type=album",
                    "text": "",
                    "width": 750,
                },
            }
        ],
        "owner_ids": [],
    },
    "group_id": 175402552,
    "event_id": "9ffd88ce96e71f71425dac1f7287344064f1e10f",
}

photo = dict['object']['attachments'][0]['photo']
keys = photo.keys()
photos = list(filter(lambda x: re.search("^photo_.*$", x), keys))
print(photos)
photos.sort(key=natural_keys)
print(photos[-1])
image_url = photo[photos[-1]]
print(image_url)


txt = "The rain in Spain"
x = re.search("Spain", txt) 
print(x)


