import unittest
from unittest.mock import Mock, patch

from src.linkparser import LinkParser


class TestLinkParserUnit(unittest.TestCase):
    def test_social_replacement(self):
        url = "https://www.instagram.com/somepost"
        parser = LinkParser(url)
        result = parser.fix()
        self.assertIn("ddinstagram.com", result)

    def test_news_replacement(self):
        url = "https://www.nytimes.com/somearticle"
        parser = LinkParser(url)
        result = parser.fix()
        expected = f"https://archive.today/newest/{url}"
        self.assertEqual(result, expected)

    def test_unlocked_article_code_news(self):
        url = "https://www.nytimes.com/somearticle?unlocked_article_code=123"
        parser = LinkParser(url)
        result = parser.fix()
        self.assertIsNone(result)

    def test_invalid_domain(self):
        url = "https://www.unknownsite.com/something"
        parser = LinkParser(url)
        result = parser.fix()
        self.assertIsNone(result)

    @patch("src.linkparser.requests.get")
    def test_apple_replacement(self, mock_get):
        fake_html = """
        <html>
          <body>
            <a href="https://www.example.com/news/story">
              <span class="click-here">Click here</span>
            </a>
          </body>
        </html>
        """
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.text = fake_html
        mock_get.return_value = fake_response

        url = "https://apple.news/someapple"
        parser = LinkParser(url)
        result = parser.fix()
        expected = "https://archive.today/newest/https://www.example.com/news/story"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
