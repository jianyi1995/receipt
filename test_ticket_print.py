__author__ = 'Administrator'

import unittest
import json
from ticket_print import TicketPrint

'''
时间：2016.5.28
描述：对TicktPrint类进行测试
思路：利用等价类划分的方式来设计单元测试用例，
     总共分为有批发价商品和无批发价商品，
     因为所有信息来自机器扫描之后传递的条形码，所以不考虑不合理输入
     其中有批发价商品测试分为只有一类批发类和有多类批发类
     无批发价商品分为没有批发类产品或有但数量不足最低标准
'''


class TestTicketPrint(unittest.TestCase):
    _expected_no_discount_out = \
        '*<没钱赚商店>购物清单*\n' + \
        '名称：可口可乐,数量：3瓶,单价：3.00(元）,小计：9.00（元)\n' + \
        '名称：雪碧,数量：2瓶,单价：3.00(元）,小计：6.00（元)\n' + \
        '名称：苹果,数量：7.0斤,单价：5.50(元）,小计：38.50（元)\n' + \
        '-' * 60 + '\n' + \
        '总计：53.50(元)\n' + \
        '-' * 60
    _expected_discount_out = \
        '*<没钱赚商店>购物清单*\n' + \
        '名称：可口可乐,数量：8瓶,单价：3.00(元）,小计：22.80,(元),优惠：1.20(元)\n' + \
        '名称：雪碧,数量：3瓶,单价：3.00(元）,小计：8.55,(元),优惠：0.45(元)\n' + \
        '名称：苹果,数量：2.0斤,单价：5.50(元）,小计：11.00（元)\n' + \
        '-' * 60 + '\n' + \
        '批发价出售商品：\n' + \
        '名称：可口可乐,数量：8瓶\n' + \
        '名称：雪碧,数量：3瓶\n' + \
        '-' * 60 + '\n' + \
        '总计：42.35(元)节省：1.65(元)\n' + \
        '-' * 60
    _expected_2_discount_out = \
        '*<没钱赚商店>购物清单*\n' + \
        '名称：可口可乐,数量：3瓶,单价：3.00(元）,小计：8.55,(元),优惠：0.45(元)\n' + \
        '名称：雪碧,数量：2瓶,单价：3.00(元）,小计：5.70,(元),优惠：0.30(元)\n' + \
        '名称：苹果,数量：7.0斤,单价：5.50(元）,小计：36.57,(元),优惠：1.93(元)\n' + \
        '-' * 60 + '\n' + \
        '批发价出售商品：\n' + \
        '名称：可口可乐,数量：3瓶\n' + \
        '名称：雪碧,数量：2瓶\n' + \
        '名称：苹果,数量：7.0斤\n' + \
        '-' * 60 + '\n' + \
        '总计：50.82(元)节省：2.68(元)\n' + \
        '-' * 60

    # 测试没有需要批发价出售，但有产品在批发类中时输出是否正确
    def test_no_discount_with_subCategory(self):
        t = TicketPrint()
        t.addSubCategory("碳酸饮料")
        with open('no_discount.json', 'r') as f:
            json_data = json.load(f)
            json_data = json.dumps(json_data)
        result = t.compute(json_data)
        expected_out = self._expected_no_discount_out
        self.assertEqual(result, expected_out)

    # 测试没有需要批发价出售，且无产品在批发类中时输出是否正确
    def test_no_discount_no_subCategory(self):
        t = TicketPrint()
        with open('no_discount.json', 'r') as f:
            json_data = json.load(f)
            json_data = json.dumps(json_data)
        result = t.compute(json_data)
        expected_out = self._expected_no_discount_out
        self.assertEqual(result, expected_out)

    # 测试有需要批发价出售，且是只有一类满足批发类的产品
    def test_discount_one_subCategory(self):
        t = TicketPrint()
        with open('discount.json', 'r') as f:
            json_data = json.load(f)
            json_data = json.dumps(json_data)
        t.addSubCategory('碳酸饮料')
        result = t.compute(json_data)
        expected_out = self._expected_discount_out
        self.assertEqual(result, expected_out)

    # 测试有需要批发价出售，且是多类满足批发类的产品
    def test_discount_with_right_subCategory(self):
        t = TicketPrint()
        t.addSubCategory('碳酸饮料')
        t.addSubCategory('水果')
        with open('no_discount.json', 'r') as f:
            json_data = json.load(f)
            json_data = json.dumps(json_data)
        result = t.compute(json_data)
        excepted_out = self._expected_2_discount_out
        self.assertEqual(result, excepted_out)


if __name__ == '__main__':
    unittest.main()
