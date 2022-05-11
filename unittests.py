import unittest
import requests
import config
import parse_sber
import parse_aliexpress


class TestBot(unittest.TestCase):
    def test_connection(self):
        self.assertEqual(
            requests.get('https://sbermegamarket.ru/').status_code, 200)
        self.assertEqual(
            requests.get('https://aliexpress.ru/').status_code, 200)

    def test_sber_parser(self):
        self.assertFalse(
            parse_sber.findProduct("телефон")["cost"] is None)
        self.assertFalse(
            parse_sber.findProduct("mac book")["cost"] is None)
        self.assertFalse(
            parse_sber.findProduct("клавиатура logitech")["cost"] is None)
        self.assertTrue(
            len(parse_sber.findProduct("телефон")) == 3)

    def test_ali_parser(self):
        self.assertFalse(
            parse_aliexpress.findProduct("телефон")["cost"] is None)
        self.assertFalse(
            parse_aliexpress.findProduct("ноутбук")["cost"] is None)
        self.assertFalse(
            parse_aliexpress.findProduct("компьютерная мышь")["cost"] is None)
        self.assertFalse(
            parse_aliexpress.findProduct("клавиатура")["cost"] is None)
        self.assertTrue(
            len(parse_aliexpress.findProduct("телефон")) == 3)


if __name__ == "__main__":
    unittest.main()
