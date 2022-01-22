#coding:utf-8
import xlrd
from VueApi.config import setting
from VueApi.config import getConfig
cofing = getConfig.Config()
run = cofing.get_db_run().run

excel_path = setting.EXCEL_DIR
class ExcelUtil:

    def __init__(self, excel_path):

        self.data = xlrd.open_workbook(excel_path)
        self.table = self.data.sheet_by_name('Sheet1')
        # 获取第一行数值作为key值
        self.keys = self.table.row_values(0)
        # 获取总行数值
        self.rowNum = self.table.nrows
        # 获取总列数值
        self.colNum = self.table.ncols


    def dict_data(self):
        if self.rowNum <= 1:
            print("总行数小于1")
        else:
            r = []
            j = 1
            for i in range(self.rowNum - 1):
                s = {}
                # 从第二行取对应values数值
                values = self.table.row_values(j)
                for x in range(self.colNum):
                    s[self.keys[x]] = values[x]
                r.append(s)
                j += 1
            return r
    def A(self,value):
        data = ExcelUtil(excel_path).dict_data()
        ii =[]
        for i in range(len(data)):
            a = data[i][value]
            ii.append(a)
        return ii

    def all_data(slef):
        # print(slef.keys)
        # print(slef.colNum)
        # print()
        # table1 = slef.data.sheet_by_name('Sheet1')
        # print(table1)
        if run == '1':
            print('调试用例')
            if slef.rowNum <= 1:
                print("总行数小于1")
            else:
                r = []
                j = 1
                for i in range(slef.rowNum - 1):  # 从第几行取0开始
                    # 从第一行取对应values数值
                    values = slef.table.row_values(j, 1)
                    r.append(values)
                    j += 1
                return r
        elif run == '2':
            print('调试任务')
            if slef.rowNum <= 1:
                print("总行数小于1")
            else:
                r = []
                j = 1
                for i in range(slef.rowNum - 1):  # 从第几行取0开始
                    # 从第一行取对应values数值
                    values = slef.table.row_values(j, 3) #从第几列开始取数据
                    r.append(values)
                    j += 1
                return r


if __name__ == "__main__":
    # print(excel_path)
    data = ExcelUtil(excel_path)
    a = data.dict_data()
    print(data.all_data())
    # print(data.A("操作"))
    # #读取第一行第一列数据




