import unittest
from monster import Monster

class TestItem(unittest.TestCase):
    def test_attack(self):
        m = Monster(100, {'撞击': [300, 400], '泰山压顶': [450, 600]})
        attres = m.normalattack()
        print(attres)
        if attres[0] == '撞击':
            self.assertTrue(attres[1] >= 300 and attres[1] <= 400)
        elif attres[0] == '泰山压顶':
            self.assertTrue(attres[1] >= 450 and attres[1] <= 600)
        else:
            self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
