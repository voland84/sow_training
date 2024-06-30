import unittest
from streamlit.testing.v1 import AppTest

class TestChatbotApp(unittest.TestCase):
    def test_smoke(self):
        """Test if the app runs without throwing an exception."""
        at = AppTest.from_file("../sow_generator.py", default_timeout=10).run()
        assert not at.exception


    def test_sidebar(self):
        """Test if a single text input exists in the sidebar."""
        at = AppTest.from_file("../sow_generator.py").run()
        assert len(at.text_input) == 2
