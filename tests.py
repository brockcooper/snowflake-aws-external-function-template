import unittest
import json
import translate_from_english


class TranslateFromEnglish(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        event = {"body": {
            "data": [
                [0, "Hello", ["es", "fr"]],
                [1, """All other supported data types are serialized
                    as JSON strings.""", ["es", "fr"]],
                [2, """Examples of extracting data are included in the
                    documentation for creating a remote service
                    on each platform""", ["es", "fr"]]
            ]
        }}
        self.results = translate_from_english.handler(event, 'context', local=True)

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

    def test_translation(self):
        translation = json.loads(self.results["body"])["data"][0][1]
        self.assertIsInstance(translation, list)
        self.assertEqual(translation[0]["translated_text"], 'Hola')
        self.assertEqual(translation[1]["translated_text"], 'Bonjour')
        self.assertEqual(translation[0]["status"], 'success')
        self.assertEqual(translation[1]["status"], 'success')


if __name__ == '__main__':
    unittest.main()
