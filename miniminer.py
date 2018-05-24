"""Miniminer."""
import json
from hashlib import sha256
import requests
import math
from constants import token


class MiniMinerAPI():
    """Miniminer API.

    Defines get and post methods to get problem and send solution to endpoint.
    """

    base_url = 'https://hackattic.com/challenges/mini_miner/'
    problem_url = 'problem?access_token='
    solution_url = 'solve?access_token='

    def __init__(self, token):
        """Initialize API with provided token."""
        self.token = token

    def get(self, url):
        """Return problem from endpoint."""
        response = requests.get(url + self.token).json()
        return response

    def post(self, nonce, url):
        """Send solution to endpoint and print results."""
        payload = {'nonce': nonce}
        response = requests.post(url + self.token + '&playground=1',
                                 json=payload)
        print(response.status_code, response.json())
        return response.json()


class MiniMiner():
    """Solves hackattic's MiniMiner problem in playground mode.

    A JSON is received from the endpoint with three attributes:
    'block', 'nonce' and 'difficulty'. MiniMiner's goal is to
    find a 'nonce' that causes the SHA256 hash  of 'block' to
    start with 'difficulty' 0 bits. That is, if difficulty is
    4, the hash should start with at least 4 zero bits.
    """

    def __init__(self, token):
        """Initalize MiniMiner with token provided by user."""
        self.debug = False
        self.token = token

    def run(self, debug=False):
        """Miniminer main function. Fetch problem, solve and send."""
        self.debug = debug
        api = MiniMinerAPI(self.token)
        response = api.get(api.base_url + api.problem_url)
        nonce, digest = self._get_nonce(response['block'],
                                        response['difficulty'])
        print(nonce, digest)
        return(api.post(nonce, api.base_url + api.solution_url))

    def _get_nonce(self, block, diff):
        """Bruteforce nonce until expected minimum zero bits is found.

        Returns nonce and digest.
        """
        nonce = -1
        expected = '0' * math.ceil(diff/4)
        while 1:
            nonce += 1
            block['nonce'] = nonce
            block_json = json.dumps(block,
                                    sort_keys=True,
                                    separators=(',', ':'))
            digest = sha256(block_json.encode()).hexdigest()
            if self.debug:
                msg = 'diff: %s\tnonce: %s\tdigest: %s' % (diff, nonce, digest)
                print(msg)
            if digest.startswith(expected):
                return nonce, digest


if __name__ == '__main__':
    mm = MiniMiner(token)
    mm.run(debug=True)
