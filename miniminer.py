from urllib.request import urlopen
import json
from hashlib import sha256
import requests
import math
import time

class MiniMiner():
    def __init__(self, token):
        self.debug = False
        self.token = token
        self.get_url = 'https://hackattic.com/challenges/mini_miner/problem?access_token='
        self.post_url = 'https://hackattic.com/challenges/mini_miner/solve?access_token='

    def get(self):
        url = urlopen(self.get_url + self.token)
        response = json.loads(url.read().decode())
        if self.debug:
            print(response)
            time.sleep(5)
        return response

    def post(self, nonce):
        payload = { 'nonce' : nonce }
        r = requests.post(self.post_url + self.token + '&playground=1',
                          json=payload)
        print(r.status_code, r.json())

    def run(self, debug=False):
        self.debug = debug
        response = self.get()
        nonce, digest = self.get_nonce(response['block'], response['difficulty'])
        print(nonce, digest)
        self.post(nonce)

    def get_nonce(self, block, diff):
        nonce = -1
        expected = '0' * math.ceil(diff/4)
        while 1:
            nonce += 1
            block['nonce'] = nonce
            block_json = json.dumps(block, sort_keys=True, separators=(',',':'))
            digest = sha256(block_json.encode()).hexdigest()
            if self.debug:
                print('diff: ' + str(diff) + '\tnonce: ' + str(nonce) + '\tdigest: ' + str(digest))
            if digest.startswith(expected):
                return nonce, digest

if __name__ == '__main__':
    mm = MiniMiner('87e086701c983f67')
    mm.run(debug=False)
