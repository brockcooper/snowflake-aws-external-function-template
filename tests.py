import unittest
import json
import lambda_function


class LambdaFunction(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        event = {"body": {
            "data": [
                [0, "Test 0"],
                [1, "Test 1"],
                [2, "Test 2"],
            ]
        }}
        self.results = lambda_function.handler(event, 'context', local=True)

    def test_body_is_json(self):
        self.assertIsInstance(self.results["body"], str)

    def test_json_is_valid(self):
        body = json.loads(self.results["body"])
        self.assertIsInstance(body, dict)

    def test_data_is_list(self):
        body = json.loads(self.results["body"])
        self.assertIsInstance(body["data"], list)

    def test_data_has_rows(self):
        body = json.loads(self.results["body"])

        n = 0
        for row in body["data"]:
            self.assertIs(row[0], n)
            n += 1


if __name__ == '__main__':
    unittest.main()
