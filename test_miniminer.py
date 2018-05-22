import unittest
import json
from unittest.mock import patch, Mock
from miniminer import MiniMiner

class MiniMinerTest(unittest.TestCase):
    """MiniMiner test suite.
    Creates a test problem based off hackattic's example. POST and GET
    functions are patched to return expected results. Expected nonce from
    test block is 45.
    """

    test_problem = json.dumps({'block':{'data':[],'nonce':None}, 'difficulty':8})
    passed = json.dumps({'result': 'passed (playground mode)'})


    def setUp(self):
        get_patcher = patch('miniminer.requests.get')
        self.mock_get = get_patcher.start()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json.return_value = json.loads(self.test_problem)

        post_patcher = patch('miniminer.requests.post')
        self.mock_post = post_patcher.start()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json.return_value = json.loads(self.passed)

    def test_get(self):
        test_problem_json = json.dumps(self.test_problem)
        response = MiniMiner('someToken')._get('null')
        response = json.dumps(response)
        self.assertEqual(response, self.test_problem)

    def test_post(self):
        passed = {'result': 'passed (playground mode)'}
        response = MiniMiner('someToken')._post(45, 'null')
        self.assertEqual(response, passed)

    def test_get_nonce(self):
        test_problem = json.loads(self.test_problem)
        block = test_problem['block']
        diff = test_problem['difficulty']
        nonce = MiniMiner('token')._get_nonce(block, diff)
        self.assertEqual(nonce[0], 45)

    def test_run(self):
        result = MiniMiner('token').run()
        result = json.dumps(result)
        self.assertEqual(result, self.passed)

if __name__ == '__main__':
    unittest.main()

