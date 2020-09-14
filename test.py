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
        # self.assertTrue(m.attack() >= 100 and m.attack() <= 200)  # 测试两次
    # def test_init(self):
    #     a = Item('雪糕', amount=100, outDateTime=5)
    #     self.assertEqual(a.outDateTime, 5)
    #
    # def test_ValueError(self):
    #     a = Item('雪糕', amount=100, outDateTime=-1)
    #     with self.assertRaises(ValueError):
    #         a.outDateTime = -1
    #     with self.assertRaises(ValueError):
    #         a.amount = 'a'
    #
    # def test_AttributeError(self):
    #     a = Item('雪糕', amount=100, outDateTime=-1)
    #     with self.assertRaises(AttributeError):
    #         a.inTime = 123


# if __name__ == '__main__':
#     unittest.main()
