"""MiniMiner test suite."""
import unittest
from unittest.mock import patch
from miniminer import MiniMiner, MiniMinerAPI


class MiniMinerTest(unittest.TestCase):
    """MiniMiner test class.

    Creates a test problem based off hackattic's example. POST and GET
    functions are patched to return expected results. Expected nonce from
    test block is 45.
    """

    # TODO: Check mock value to change response accordingly

    test_problem = {'block': {'data': [], 'nonce': None}, 'difficulty': 8}
    passed = {'result': 'passed (playground mode)'}

    def setUp(self):
        """Patch requests get and post methods."""
        get_patcher = patch('miniminer.requests.get')
        self.mock_get = get_patcher.start()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.json.return_value = self.test_problem

        post_patcher = patch('miniminer.requests.post')
        self.mock_post = post_patcher.start()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json.return_value = self.passed

    def test_get(self):
        """Get test problem from stub and check it."""
        response = MiniMinerAPI('someToken').get('null')
        self.assertEqual(response, self.test_problem)

    def test_post(self):
        """Post solution to stub and check it."""
        passed = {'result': 'passed (playground mode)'}
        response = MiniMinerAPI('someToken').post(45, 'null')
        self.assertEqual(response, passed)

    def test_run(self):
        """Run MiniMiner's main method.

        Check if response is OK.
        """
        result = MiniMiner('token').run()
        self.assertEqual(result, self.passed)


if __name__ == '__main__':
    unittest.main()
