import unittest

from src.driver import AmazonAwsCloudProviderShell2GDriver


class TestAwsCloudProviderShell2GDriver(unittest.TestCase):
    def setUp(self):
        AmazonAwsCloudProviderShell2GDriver()

    def tearDown(self):
        pass

    def test_000_something(self):
        pass


if __name__ == "__main__":
    import sys

    sys.exit(unittest.main())
