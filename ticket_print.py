__author__ = 'Administrator'
import json

'''编写日期：2016.5.27
类名：TicketPrint
功能描述：根据扫到的条码的json数据，存储的商品信息和商店目前的打折商品种类
打印出结算清单
'''


class TicketPrint(object):
    # 初始化打折子类信息和加载商品信息
    def __init__(self):
        # 从GoodInformation.json文件中读取商品信息
        with open('good_information.json', 'r') as f:
            self._goodInformation = json.load(f)
        self._sub_category = set()
        self._wholesale = 10
        self._discount = 0.95

    # 超市添加新的商品
    def add_good(self, good_informaion):
        pass

    # 修改批发最低数量
    def update_wholesale(self, wholesale):
        self._wholesale = wholesale

    # 修改折扣额度
    def update_discount(self, discount):
        self._discount = discount

    # 添加新的打折子类
    def addSubCategory(self, sub_category):
        self._sub_category.add(sub_category)

    # 当某些子类不打折时，进行删除操作
    def del_sub_category(self, sub_category):
        try:
            self._sub_category.remove(sub_category)
            print('add subCategory successfully!\n')
        except KeyError as e:
            print('ValueError:', e)

    # 在小票上增加物品信息, 参数为别代表商品信息字典，当前小票列表，商品数量, 当前已有商品名
    def add_item(self, good_dict, receipt, num, bought_name):
        name = good_dict['name']
        sub_category_num = 0
        # 如果该商品与之前扫描产品相同，更改产品数量
        if name in bought_name:
            for item in receipt:
                if item['name'] == name:
                    item['num'] += num
                    if item['subCategory'] in self._sub_category:
                        sub_category_num = num
                    break
        else:
            bought_name.add(name)
            price = good_dict['price']
            sub_category = good_dict['subCategory']
            unit = good_dict['unit']
            tmp = {'name': name, 'price': price,
                   'subCategory': sub_category, 'num': num, 'unit': unit}
            receipt.append(tmp)
            if sub_category in self._sub_category:
                sub_category_num = num
        return sub_category_num

    # 根据条形码将商品信息加入到小票中
    def compute(self, json_data):
        data = json.loads(json_data)
        subCategoryNum = 0
        name = set()
        receipt = []
        # 遍历所有购买商品的条码
        for item in data:
            # 从商品信息中查找该条码对应的商品信息
            for good in self._goodInformation:
                # 条码分为两类，1类是不带-，1类是带-，后面接数量的
                # 对于前一类，直接记录商品参数即可
                if item == good['barcode']:
                    subCategoryNum += self.add_item(good, receipt, 1, name)
                # 对于条形码中带有数量的，取其条形码后面的数字作为参数传入
                elif good['barcode'] in item:
                    subCategoryNum += \
                        self.add_item(good, receipt,
                                     float(item[len(good['barcode']) + 1]), name)
        # 打印小票
        return self._print_receipt(receipt, subCategoryNum)

    # 打印小票
    def _print_receipt(self, receipt, sub_category_num):
        content = '*<没钱赚商店>购物清单*\n'
        amount = 0
        discount = 0
        discountgood = '批发价出售商品：\n'
        for item in receipt:
            content += '名称：' + item['name'] + ',' + \
                       '数量：' + str(item['num']) + item['unit'] + ',' + \
                       '单价：' + '%.2f' % item['price'] + '(元）' + ','
            if sub_category_num >= self._wholesale and item['subCategory'] in self._sub_category:
                tmp = round(item['price'] * item['num'] * self._discount, 2)
                content += '小计：' + '%.2f' % tmp + ',' + '(元)' + ','
                amount += tmp
                tmp = round(item['price'] * item['num'] * (1 - self._discount), 2)
                discount += tmp
                content += '优惠：' + '%.2f' % tmp + '(元)\n'
                discountgood += '名称：' + item['name'] + ',' + \
                                '数量：' + str(item['num']) + item['unit'] + '\n'
            else:
                tmp = round(item['price'] * item['num'], 2)
                amount += tmp
                content += '小计：' + '%.2f' % tmp + '（元)\n'
        content += '-' * 60 + '\n'
        if sub_category_num >= self._wholesale:
            content += discountgood
            content += '-' * 60 + '\n'
            content += '总计：' + str(amount) + '(元)' + \
                       '节省：' + '%.2f' % discount + '(元)'
        else:
            content += '总计：' + '%.2f' % amount + '(元)'
        content += '\n' + '-' * 60
        print(content)
        return content


if __name__ == '__main__':
    t = TicketPrint()
    with open('no_discount.json', 'r') as f:
        jsonData = json.load(f)
        jsonData = json.dumps(jsonData)
    t.addSubCategory('水果')
    t.addSubCategory('碳酸饮料')
    t.compute(jsonData)
