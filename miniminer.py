import json
from hashlib import sha256
import requests
import math
import time

class MiniMiner():
    """Solves hackattic's MiniMiner problem in playground mode!

    A JSON is received from the endpoint with three attributes:
    'block', 'nonce' and 'difficulty'. MiniMiner's goal is to
    find a 'nonce' that causes the SHA256 hash  of 'block' to
    start with 'difficulty' 0 bits. That is, if difficulty is
    4, the hash should start with at least 4 zero bits.
    """
    def __init__(self, token):
        """Initalize MiniMiner with token provided by user"""
        self.debug = False
        self.token = token
        self.get_url = 'https://hackattic.com/challenges/mini_miner/problem?access_token='
        self.post_url = 'https://hackattic.com/challenges/mini_miner/solve?access_token='

    def _get(self, url):
        """Return problem from endpoint"""
        response = requests.get(self.get_url + self.token).json()
        if self.debug:
            print(response)
            time.sleep(5)
        return response

    def _post(self, nonce, url):
        """Send solution to endpoint and print results"""
        payload = { 'nonce' : nonce }
        r = requests.post(self.post_url + self.token + '&playground=1',
                          json=payload)
        print(r.status_code, r.json())
        return r.json()

    def run(self, debug=False):
        """MiniMiner's main function. Fetch problem, solve and send."""
        self.debug = debug
        response = self._get(self.get_url)
        nonce, digest = self._get_nonce(response['block'], response['difficulty'])
        print(nonce, digest)
        return(self._post(nonce, self.post_url))


    def _get_nonce(self, block, diff):
        """Bruteforce nonce until expected minimum zero bits is found
        Returns nonce and digest
        """
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
    mm.run(debug=True)
