from django.http import JsonResponse
import json
import time
from datetime import *
from django.views.decorators.csrf import csrf_exempt
from VueApi.case.test_selenium import TestDirver
import MySQLdb
import MySQLdb.cursors
from VueApi.comm.timed_task import run_jenkins
from VueApi.config import getConfig
# 实例化Config
DB = getConfig.Config().get_db()
RUN = TestDirver()
import os

#查询所有任务列表
def get_record(request):
    if request.method == 'GET':
        record_name = request.GET.get('query', '')
        pagenum = request.GET.get('pagenum','')
        pageSize = request.GET.get('pagesize','')
        min = str((int(pagenum)-1)*int(pageSize))
        try:
            if record_name:
                conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                                       cursorclass=MySQLdb.cursors.DictCursor)
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) from  record where record_name like '%" + record_name + "%'")
                    totalRecord = cursor.fetchall()
                    totalRecord = int(totalRecord[0]['COUNT(*)'])  # 总任务数
                    # totalPageNum = (int(totalRecord) + int(pagenum) - 1) * int(pageSize) // int(pageSize)  # 总页数
                    sql = "SELECT r.*,u.user_name from  record as r,`user` as u WHERE r.user_id=u.id and r.record_name like '%" + record_name + "%' GROUP BY r.id DESC limit " + min + ',' + str(pageSize)
                    cursor.execute(sql)
                    mysql_dict = cursor.fetchall()
                    # 遍历case_id 匹配用例表的case_name
                    for r in range(len(mysql_dict)):
                        dd = ''
                        for d in mysql_dict[r]['case_id'].split(','):
                            cursor.execute(
                                "SELECT case_name from ui_case where id=" + d)
                            case_name = cursor.fetchall()
                            for r_name in range(len(case_name)):
                                dd = dd + case_name[r_name]['case_name'] + ","
                        mysql_dict[r]['case_id'] = dd.strip(',')
                    for data in range(len(mysql_dict)):
                        mysql_dict[data]['create_time'] = mysql_dict[data]['create_time'].strftime("%Y-%m-%d %H:%M:%S")
                        mysql_dict[data]['run_time'] = str(mysql_dict[data]['run_time']).strip('0').strip(':')
                    request_data = {
                        "totalRecord": totalRecord,
                        "pagenum": pagenum,
                        "data": mysql_dict,
                        "meta": {
                            "msg": "获取任务列表成功",
                            "status": 200
                        }
                    }
                    return JsonResponse(request_data)
            else:
                conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                                       cursorclass=MySQLdb.cursors.DictCursor)
                with conn.cursor() as cursor:
                        cursor.execute("SELECT COUNT(*) from  record ")
                        totalRecord = cursor.fetchall()
                        totalRecord = int(totalRecord[0]['COUNT(*)']) #总任务数
                        # totalPageNum = (int(totalRecord) + int(pagenum) - 1)*int(pageSize) // int(pageSize) #总页数
                        cursor.execute("SELECT r.*,u.user_name from  record as r,`user` as u WHERE r.user_id=u.id  GROUP BY r.id DESC limit " + min + ',' + str(pageSize))
                        mysql_dict = cursor.fetchall()
                        # 遍历case_id 匹配用例表的case_name

                        for r in range(len(mysql_dict)):
                            dd = ''
                            for d in mysql_dict[r]['case_id'].split(','):
                                cursor.execute(
                                    "SELECT case_name from ui_case where id=" + d)
                                case_name = cursor.fetchall()
                                for r_name in range(len(case_name)):
                                    dd = dd + case_name[r_name]['case_name'] + ","
                            mysql_dict[r]['case_id'] = dd.strip(',')
                        for data in range(len(mysql_dict)):
                            mysql_dict[data]['create_time'] = mysql_dict[data]['create_time'].strftime("%Y-%m-%d %H:%M:%S")
                            mysql_dict[data]['run_time'] = str(mysql_dict[data]['run_time']).strip('0').strip(':')
                        request_data = {
                        "totalRecord": totalRecord,
                        "pagenum": pagenum,
                        "data": mysql_dict,
                        "meta": {
                            "msg": "获取任务列表成功",
                            "status": 200
                        }
                    }
                return JsonResponse(request_data)
        except Exception as e:
            print(e)  # 打印所有异常到屏幕
            request_data = {
                "data":'',
                "meta": {
                    "msg": "请求方式错误",
                    "status": 400
                }
            }
        return JsonResponse(request_data)
    else:
        request_data = {
            "data": '',
            "meta": {
                "msg": "请求方式错误",
                "status": 400
            }
        }
    return JsonResponse(request_data)

#查询单个任务
def get_id_record(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'GET':
        id = request.GET.get('id', '')
        with conn.cursor() as cursor:
                cursor.execute("SELECT * from  record where id="+id)
                mysql_dict = cursor.fetchall()
                for r in range(len(mysql_dict)):
                    dd = []
                    for d in mysql_dict[r]['case_id'].split(','):
                        dd.append(int(d))
                    mysql_dict[r]['case_id'] = dd
                for data in range(len(mysql_dict)):
                    mysql_dict[data]['create_time'] = mysql_dict[data]['create_time'].strftime("%Y-%m-%d %H:%M:%S")
                    mysql_dict[data]['run_time'] = str(mysql_dict[data]['run_time']).strip('0').strip(':')
                request_data = {
                "data": mysql_dict[0],
                "meta": {
                    "msg": "获取任务列表成功",
                    "status": 200
                }
            }
        return JsonResponse(request_data)
    else:
        request_data = {
            "data": '',
            "meta": {
                "msg": "请求方式错误",
                "status": 400
            }
        }
    return JsonResponse(request_data)

@csrf_exempt
def add_record(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    # 新增任务
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            record_name = json_data['record_name']
            case_id_data = json_data['case_id']
            run_time = json_data['run_time']
            print(run_time)
            case_id =''
            for case in case_id_data:
                case_id=case_id+str(case)+','
            case_id=case_id.strip(',')
            user_id = json_data['user_id']
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO record (record_name,user_id,case_id,run_time,create_time) VALUES (%s,%s,%s,%s,now())",
                               [record_name,user_id,case_id,run_time])
                conn.commit()
                request_data = {
                    "meta": {
                        "msg": "任务添加成功",
                        "status": 200
                    }
                }
        except Exception as e:
            print(e)  # 打印所有异常到屏幕
            request_data = {
                "data": '',
                "meta": {
                    "msg": "请求方式错误",
                    "status": 400
                }
            }
        return JsonResponse(request_data)
    else:
        request_data = {
            "data": '',
            "meta": {
                "msg": "请求方式错误",
                "status": 400
            }
        }
    return JsonResponse(request_data)
#修改任务
@csrf_exempt
def edit_record(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        json_data = json.loads(request.body)

        max = ''
        ui_project = 'record'
        try:
            id = json_data['id']
            record_name = json_data['record_name']
            case_id_data = json_data['case_id']
            run_time = json_data['run_time']
            case_id =''
            for case in case_id_data:
                case_id=case_id+str(case)+','
            case_id=case_id.strip(',')
            with conn.cursor() as cursor:
                cursor.execute("UPDATE " + ui_project + " SET record_name='"+record_name+"',case_id='"+case_id+"',run_time='"+run_time+"' where id='"+str(id)+"'")
                conn.commit()
                request_data = {
                    "meta": {
                        "msg": "修改成功",
                        "status": 200
                    }
                }
            return JsonResponse(request_data)
        except Exception as e:
            print(e)
            sort = json_data['sort']
            sort1 = json_data['sort1']
            with conn.cursor() as cursor:
                while int(sort) > int(sort1):
                    max = sort
                    sort, sort1 = sort1, sort
                else:
                    # sort排序方法
                    if str(int(sort) + 1) == sort1:
                        print("交换")
                        with conn.cursor() as cursor:
                            cursor.execute("UPDATE " + ui_project + " SET sort=" + sort + ",id=99999  WHERE id=" + sort1)
                            cursor.execute(
                                "UPDATE " + ui_project + " SET sort=" + sort1 + ",id=99998  WHERE id=" + str(sort))
                            cursor.execute(
                                "UPDATE " + ui_project + "  SET id=sort WHERE sort in(" + sort + "," + sort1 + ")")
                            conn.commit()
                    else:
                        print("插入")
                        base = str(sort1)
                        base1 = str(sort)
                        sort = str(int(sort) - 1)
                        sort1 = str(int(sort1) + 1)
                        with conn.cursor() as cursor:
                            if max == '':
                                cursor.execute(
                                    "UPDATE " + ui_project + " SET  sort=id+10000 where id >" + sort + " and id<" + sort1)
                                cursor.execute(
                                    "UPDATE " + ui_project + " SET sort=sort+(SELECT count(a.id) FROM (SELECT * FROM " + ui_project + ") a WHERE a.sort>" + sort + "+10000 ) WHERE id=" + base1)
                                cursor.execute("UPDATE " + ui_project + " SET id=sort;")
                                cursor.execute(
                                    "UPDATE " + ui_project + " SET id=id-10001 where id >" + sort + "+10001 and id<" + sort1 + "+10001")
                                cursor.execute(
                                    "UPDATE " + ui_project + " SET sort=id  where sort >" + sort + "+10001 and sort<" + sort1 + "+10001")
                                conn.commit()
                            else:
                                cursor.execute(
                                    "UPDATE " + ui_project + " SET  sort=id+10000 where id >" + sort + " and id<" + sort1)
                                cursor.execute(
                                    "UPDATE " + ui_project + " SET sort=sort-(SELECT count(a.id) FROM (SELECT * FROM " + ui_project + ") a WHERE a.sort>" + sort + "+10000 ) WHERE id=" + base)
                                cursor.execute("UPDATE " + ui_project + " SET id=sort;")
                                cursor.execute(
                                    "UPDATE " + ui_project + " SET id=id-9999 where id >" + sort + "+9999 and id<" + sort1 + "+9999")
                                cursor.execute(
                                    "UPDATE " + ui_project + " SET sort=id  where sort >" + sort + "+9999 and sort<" + sort1 + "+9999")
                                conn.commit()
                    request_data = {
                        "meta": {
                            "msg": "成功",
                            "status": 200
                        }
                    }
                return JsonResponse(request_data)
    else:
        request_data = {
            "data": '',
            "meta": {
                "msg": "请求方式错误",
                "status": 400
            }
        }
        return JsonResponse(request_data)


# 删除处理函数
def delete(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    id = request.GET.get("id")
    ui_project = 'record'
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM " + ui_project + " WHERE id=" + id)
        cursor.execute("DELETE FROM "
                       + ui_project +
                       " WHERE id =%s", [id])
        cursor.execute("SET @i=0;")
        cursor.execute("UPDATE "
                       + ui_project +
                       " SET `id`=(@i:=@i+1);")
        cursor.execute("ALTER TABLE "
                       + ui_project +
                       " AUTO_INCREMENT=0;")
        conn.commit()
        request_data = {
            "meta": {
                "msg": "成功",
                "status": 200
            }
        }
    return JsonResponse(request_data)

def case(request):
    if request.method == 'GET':
        run = request.GET.get('run', '')
        record = request.GET.get('record_id', '')
        getConfig.Config().write_run(run)
        getConfig.Config().write_record(record)
        getConfig.Config().write_driver('1')
        os.system("python d:/vue_api/VueApi/case/test_selenium.py")
        request_data = {
            "data": '',
            "meta": {
                "msg": "调试成功",
                "status": 200
            }
        }
        return JsonResponse(request_data)
    else:
        request_data = {
            "data": '',
            "meta": {
                "msg": "请求方式错误",
                "status": 400
            }
        }
    return JsonResponse(request_data)

def jenkins(request):
    if request.method == 'GET':
        run = request.GET.get('run', '')
        record = request.GET.get('record_id', '')
        driver = 2
        getConfig.Config().write_run(str(run))
        getConfig.Config().write_record(str(record))
        getConfig.Config().write_driver(str(driver))
        run_jenkins()
        request_data = {
            "data": '',
            "meta": {
                "msg": "调试成功",
                "status": 200
            }
        }
        return JsonResponse(request_data)
    else:
        request_data = {
            "data": '',
            "meta": {
                "msg": "请求方式错误",
                "status": 400
            }
        }
    return JsonResponse(request_data)

if __name__ == '__main__':
    pass