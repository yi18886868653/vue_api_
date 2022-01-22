# -*- coding: utf-8 -*-
import pandas as pd
import pymysql
from pandas import DataFrame,Series
import os
from VueApi.config import setting
from VueApi.config import getConfig
import MySQLdb
import MySQLdb.cursors

cofing = getConfig.Config()
project = cofing.get_project().project
DB = cofing.get_db()
PATH = setting.EXCEL_DIR
PATH_CSV = setting.EXCEL_DIR_CSV
case_id = cofing.get_case().case_id
run = cofing.get_db_run().run
record_id = str(cofing.get_record().record_id)
def testdb_mysql():  #读取数据库表数据写入到excel
    con = pymysql.connect(host=DB.host, user=DB.username, passwd=DB.password, database=DB.db, charset="utf8")
    cor = con.cursor(cursor=pymysql.cursors.DictCursor)
    if run == '1':
        print('调试用例')
        sql = "SELECT s.id, c.case_name,s.step_name,m.py_name,e.element,t.type_name,e.text,s.wait_time,e.array,u.user_name," \
              "s.create_time FROM step AS s,ui_case AS c,`user` AS u,type AS t,element AS e,method AS m WHERE s.case_id = " \
              "c.id AND s.user_id = u.id  AND s.element_id = e.id AND s.method_id=m.id and e.type_id= t.id and " \
              "s.case_id=" + case_id + " ORDER BY s.sort asc "
        b = pd.read_sql(sql, con)
        test_data = DataFrame.from_records(b)
        test_data.to_excel(PATH, index=False)
    elif run == '2':
        print('调试任务')
        conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                               cursorclass=MySQLdb.cursors.DictCursor)
        with conn.cursor() as cursor:
            try:
                os.remove(PATH_CSV)
            except:
                pass
            cursor.execute("select case_id from record where id='"+str(record_id)+"'")
            case = cursor.fetchall()
            cc = 1
            for id in case[0]['case_id'].split(','):
                sql = "SELECT s.id, c.case_name,s.step_name,m.py_name,e.element,t.type_name,e.text,s.wait_time,e.array,u.user_name," \
                      "s.create_time FROM step AS s,ui_case AS c,`user` AS u,type AS t,element AS e,method AS m WHERE s.case_id = " \
                      "c.id AND s.user_id = u.id  AND s.element_id = e.id AND s.method_id=m.id and e.type_id= t.id and " \
                      "s.case_id=" + id + " ORDER BY s.id asc "
                b = pd.read_sql(sql, con)
                if cc == 1:
                    test_data = DataFrame.from_records(b)
                    test_data.to_csv(PATH_CSV,encoding='utf_8_sig',mode='a')
                    cc+=1
                else:
                    test_data = DataFrame.from_records(b)
                    test_data.to_csv(PATH_CSV, encoding='utf_8_sig', mode='a', header=None)
                a = pd.read_csv(PATH_CSV,encoding='utf_8_sig')
                a.to_excel(PATH,sheet_name='Sheet1')

if __name__ == '__main__':
    pass
