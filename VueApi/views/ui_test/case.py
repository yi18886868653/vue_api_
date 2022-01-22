from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from VueApi.case.test_selenium import TestDirver
import MySQLdb
import MySQLdb.cursors
from VueApi.config import getConfig
# 实例化Config
DB = getConfig.Config().get_db()
RUN = TestDirver()
import os

#查询所有用例列表
def get_case(request):
    if request.method == 'GET':
        case_name = request.GET.get('query', '')
        pagenum = request.GET.get('pagenum','')
        pageSize = request.GET.get('pagesize','')
        min = str((int(pagenum)-1)*int(pageSize))
        try:
            if case_name:
                conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                                       cursorclass=MySQLdb.cursors.DictCursor)
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) from  ui_case where case_name like '%" + case_name + "%'")
                    totalRecord = cursor.fetchall()
                    totalRecord = int(totalRecord[0]['COUNT(*)'])  # 总用例数
                    # totalPageNum = (int(totalRecord) + int(pagenum) - 1) * int(pageSize) // int(pageSize)  # 总页数
                    cursor.execute(
                        "SELECT a.*,b.user_name FROM ui_case a,`user` b WHERE a.user_id=b.id  AND case_name like '%" + case_name + "%' GROUP BY a.id DESC" + " limit " + min + ',' + str(pageSize))
                    mysql_dict = cursor.fetchall()
                    for data in range(len(mysql_dict)):
                        mysql_dict[data]['create_time'] = mysql_dict[data]['create_time'].strftime("%Y-%m-%d %H:%M:%S")
                    request_data = {
                        "totalRecord": totalRecord,
                        "pagenum": pagenum,
                        "data": mysql_dict,
                        "meta": {
                            "msg": "获取用例列表成功",
                            "status": 200
                        }
                    }
                    return JsonResponse(request_data)
            else:
                conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                                       cursorclass=MySQLdb.cursors.DictCursor)
                with conn.cursor() as cursor:
                        cursor.execute("SELECT COUNT(*) from ui_case ")
                        totalRecord = cursor.fetchall()
                        totalRecord = int(totalRecord[0]['COUNT(*)']) #总用例数
                        # totalPageNum = (int(totalRecord) + int(pagenum) - 1)*int(pageSize) // int(pageSize) #总页数
                        cursor.execute("SELECT a.*,b.user_name FROM ui_case a,`user` b WHERE a.user_id=b.id GROUP BY a.id DESC limit " + min + ',' + str(pageSize))
                        mysql_dict = cursor.fetchall()
                        for data in range(len(mysql_dict)):
                            mysql_dict[data]['create_time'] = mysql_dict[data]['create_time'].strftime("%Y-%m-%d %H:%M:%S")
                        request_data = {
                        "totalRecord": totalRecord,
                        "pagenum": pagenum,
                        "data": mysql_dict,
                        "meta": {
                            "msg": "获取用例列表成功",
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

#查询单个用例
def get_id_case(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'GET':
        id = request.GET.get('id', '')
        with conn.cursor() as cursor:
                cursor.execute("SELECT * from  ui_case where id="+id)
                mysql_dict = cursor.fetchall()
                request_data = {
                "data": mysql_dict[0],
                "meta": {
                    "msg": "获取用例列表成功",
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
def add_case(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    # 新增用例
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            case_name = json_data['case_name']
            user_id = json_data['user_id']
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO ui_case (case_name,user_id,create_time) VALUES (%s,%s,now())",
                               [case_name,user_id])
                cursor.execute("UPDATE  ui_case set sort=id")
                conn.commit()
                request_data = {
                    "meta": {
                        "msg": "用例添加成功",
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
#修改用例
@csrf_exempt
def edit_case(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        json_data = json.loads(request.body)

        max = ''
        ui_project = 'ui_case'
        try:
            id = json_data['id']
            case_name = json_data['case_name']
            with conn.cursor() as cursor:
                cursor.execute("UPDATE " + ui_project + " SET case_name='"+case_name+"' where id='"+str(id)+"'")
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
            request_data = {
                "data": '',
                "meta": {
                    "msg": "获取用例失败",
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


# 删除处理函数
def delete(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    id = request.GET.get("id")
    ui_project = 'ui_case'
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM " + ui_project + " WHERE id=" + id)
        cursor.execute("DELETE FROM "
                       + ui_project +
                       " WHERE id =%s", [id])

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
        case_id = request.GET.get('case_id', '')
        getConfig.Config().write_driver('1')
        getConfig.Config().write_run(run)
        getConfig.Config().write_case(case_id)
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

if __name__ == '__main__':
    pass

