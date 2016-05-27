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
        with open('GoodInformation.json', 'r') as f:
            self._goodInformation = json.load(f)
        self._subCategory = set()
        self._wholesale = 10
        self._discount = 0.95

    # 超市添加新的商品
    def addGood(self, good_informaion):
        pass

    # 修改批发最低数量
    def updateWholesale(self, wholesale):
        pass

    # 修改折扣额度
    def updateDiscount(self, discount):
        pass

    # 添加新的打折子类
    def addSubCategory(self, sub_category):
        self._subCategory.add(sub_category)

    # 当某些子类不打折时，进行删除操作
    def delSubCategory(self, sub_category):
        try:
            self._subCategory.remove(sub_category)
            print('add subCategory successfully!\n')
        except KeyError as e:
            print('ValueError:', e)

    # 在小票上增加物品信息, 参数为别代表商品信息字典，当前小票列表，商品数量, 当前已有商品名
    def addItem(self, goodDict, receipt, num, boughtName, subCategoryNum):
        name = goodDict['name']
        # 如果该商品与之前扫描产品相同，更改产品数量
        if name in boughtName:
            for item in receipt:
                if item['name'] == name:
                    item['num'] += num
                    if item['subCategory'] in self._subCategory:
                        subCategoryNum += num
                    break
        else:
            boughtName.add(name)
            price = goodDict['price']
            subCategory = goodDict['subCategory']
            unit = goodDict['unit']
            tmp = {'name': name, 'price': price,
                   'subCategory': subCategory, 'num': num, 'unit': unit}
            receipt.append(tmp)
            if subCategory in self._subCategory:
                subCategoryNum += num

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
                    self.addItem(good, receipt, 1, name, subCategoryNum)
                # 对于条形码中带有数量的，取其条形码后面的数字作为参数传入
                elif good['barcode'] in item:
                    self.addItem(good, receipt,
                                 int(item[len(good['barcode']) + 1]), name, subCategoryNum)
        # 打印小票
        self._printReceipt(receipt, subCategoryNum)

    # 打印小票
    def _printReceipt(self, receipt, sub_category_num):
        print('*<没钱赚商店>购物清单*')
        amount = 0
        content = ''
        discount = 0
        discountgood = '批发价出售商品：'
        for item in receipt:
            content += '名称：' + item['name'] + ',' + \
                       '数量：' + str(item['num']) + item['unit'] + ',' + \
                       '单价：' + str(item['price']) + '(元）' + ','
            if sub_category_num >= self._wholesale and item['subCategory'] in self._subCategory:
                tmp = item['price'] * item['num'] * self._discount
                content += '小计：' + str(tmp) + ',' + '(元)' + ','
                amount += tmp
                tmp = item['price'] * item['num'] * (1 - self._discount)
                discount += tmp
                content += '优惠：' + str(tmp) + '(元)'
                discountgood += '名称：' + item['name'] + ',' + \
                                '数量：' + str(item['num']) + item['unit'] + ',' + \
                                '数量：' + str(item['num']) + item['unit'] + '\n'
            else:
                tmp = item['price'] * item['num']
                amount += tmp
                content += '小计：' + str(tmp) + '（元)\n'
        if sub_category_num >= self._wholesale:
            content += discountgood
            content += '总计：' + str(amount) + '(元)' + \
                       '节省：' + str(discount) + '(元)'
        else:
            content += '总计：' + str(amount) + '(元)'
        print(content)


if __name__ == '__main__':
    t = TicketPrint()
    with open('NoDiscount.json', 'r') as f:
        jsonData = json.load(f)
        jsonData = json.dumps(jsonData)
    t.compute(jsonData)
