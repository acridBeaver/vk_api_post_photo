import json
import shutil
import sys
from pathlib import Path

import requests


class VKApi:
    def __init__(self, app_id=None, access_token=None):
        self.app_id = app_id
        self.access_token = access_token

        self.session = requests.Session()

    @staticmethod
    def get_target_id():
        while True:
            print("Input id of the post")
            target_id = str(input())
            for i in target_id:
                if i not in [str(x) for x in range(10)]:
                    continue
            return target_id

    def get_post_photo(self):
        post = self.get_target_id()
        url = 'https://api.vk.com/method/wall.getById?posts={post}&extended=0&access_token={token}&v=5.130' \
            .format(post=post, token=self.access_token)
        answer = json.loads(requests.get(url).text)
        answer = answer['response'][0]
        if 'attachments' in answer:
            attachments = answer['attachments']
        else:
            print('this post has no photo')
            sys.exit(0)
        photos = []
        for attachment in attachments:
            if attachment['type'] == 'photo':
                photo = attachment['photo']['sizes'][-1]['url']
                photos.append(photo)
            else:
                continue
        print(photos)
        self.save_photo('directory', photos)

    @staticmethod
    def save_photo(dir_name, photos):
        path = Path.cwd() / dir_name
        if not path.is_dir():
            path.mkdir()
        i = 0
        for photo in photos:
            response = requests.get(photo, stream=True)
            file_name = str(i) + '.jpg'
            i += 1
            file_path = path / file_name
            print('saving' + file_name)
            with open(file_path, "wb") as out:
                shutil.copyfileobj(response.raw, out)


if __name__ == "__main__":
    print('give me access_token')
    access_token = str(input())
    print('give me app ID')
    app_id = str(input())
    api = VKApi(access_token=access_token,
                app_id=app_id)
    api.get_post_photo()
