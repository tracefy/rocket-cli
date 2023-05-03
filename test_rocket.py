import unittest
import json
import os
from click.testing import CliRunner
from main import rocket

CONFIG_DIR = os.path.expanduser("~/.rocket")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


class TestRocketCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_install(self):
        result = self.runner.invoke(rocket, ["install"], input="testuser\n")
        self.assertEqual(result.exit_code, 0)

        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        self.assertEqual(config['default_username'], "testuser")

    def test_add(self):
        result = self.runner.invoke(rocket, ["add", "--username", "user1", "--host", "host1"])
        self.assertEqual(result.exit_code, 0)

        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        self.assertIn({"username": "user1", "host": "host1", "nickname": "host1"}, config['connections'])

    def test_add_proxy(self):
        result = self.runner.invoke(rocket, ["add-proxy", "--username", "proxyuser", "--host", "proxyhost"])
        self.assertEqual(result.exit_code, 0)

        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        self.assertEqual(config['proxy'], {"username": "proxyuser", "host": "proxyhost"})

    def test_delete(self):
        self.runner.invoke(rocket, ["delete"])

        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        self.assertEqual(config, {})


if __name__ == '__main__':
    unittest.main()
