import unittest


class TestOne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('This is setUp method.')

    @classmethod
    def tearDownClass(cls):
        print('This is tearDown method.')

    def test_3(self):
        print('test_3 method.')

    def test_1(self):
        print('test_1 method.')

    def test_2(self):
        print('test_2 method.')

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(TestOne)
    unittest.TextTestRunner(verbosity=2).run(suite)
