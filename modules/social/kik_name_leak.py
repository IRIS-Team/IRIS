import requests
from iris.module import Module
from iris.util import PrintUtil


class IRISModule(Module):

    description = 'Name Leak for Kik.com and the App'
    author = 'HellSec'
    date = '09-16-2021'

    def execute(self, username: str):
        res = requests.get(f'https://ws2.kik.com/user/{username}')

        if res.status_code != 200:
            raise Exception('Profile not found')

        jsonRes = res.json()
        first = jsonRes['firstName']
        last = jsonRes['lastName']
        id = jsonRes['displayPicLastModified']
        pic = jsonRes['displayPic']

        PrintUtil.pp({
            'First Name'        : first,
            'Last Name'         : last,
            'PFP ID'            : id,
            'Profile Picture'   : pic,
        })
