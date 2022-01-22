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

#查询所有元素页面列表
def get_element_page(request):
    if request.method == 'GET':
        element_page_id = request.GET.get('query', 'elementpageid')
        element_page_name = request.GET.get('query', '')
        pagenum = request.GET.get('pagenum','')
        pageSize = request.GET.get('pagesize','')
        min = str((int(pagenum)-1)*int(pageSize))
        try:
            if element_page_name:
                conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                                       cursorclass=MySQLdb.cursors.DictCursor)
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) from  ui_element_page where element_page_name like '%" + element_page_name + "%'")
                    totalRecord = cursor.fetchall()
                    totalRecord = int(totalRecord[0]['COUNT(*)'])  # 总元素页面数
                    # totalPageNum = (int(totalRecord) + int(pagenum) - 1) * int(pageSize) // int(pageSize)  # 总页数
                    cursor.execute(
                        "SELECT *,b.user_name FROM ui_element_page a,`user` b WHERE a.user_id=b.id  AND element_page_name like '%" + element_page_name + "%' GROUP BY a.id DESC" + " limit " + min + ',' + str(pageSize))
                    mysql_dict = cursor.fetchall()
                    for data in range(len(mysql_dict)):
                        mysql_dict[data]['create_time'] = mysql_dict[data]['create_time'].strftime("%Y-%m-%d %H:%M:%S")
                    request_data = {
                        "totalRecord": totalRecord,
                        "pagenum": pagenum,
                        "data": mysql_dict,
                        "meta": {
                            "msg": "获取元素页面列表成功",
                            "status": 200
                        }
                    }
                    return JsonResponse(request_data)
            else:
                conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                                       cursorclass=MySQLdb.cursors.DictCursor)
                with conn.cursor() as cursor:
                        cursor.execute("SELECT COUNT(*) from ui_element_page ")
                        totalRecord = cursor.fetchall()
                        totalRecord = int(totalRecord[0]['COUNT(*)']) #总元素页面数
                        # totalPageNum = (int(totalRecord) + int(pagenum) - 1)*int(pageSize) // int(pageSize) #总页数
                        cursor.execute("SELECT a.*,b.user_name FROM ui_element_page a,`user` b WHERE a.user_id=b.id GROUP BY a.id DESC limit " + min + ',' + str(pageSize))
                        mysql_dict = cursor.fetchall()
                        for data in range(len(mysql_dict)):
                            mysql_dict[data]['create_time'] = mysql_dict[data]['create_time'].strftime("%Y-%m-%d %H:%M:%S")
                        request_data = {
                        "totalRecord": totalRecord,
                        "pagenum": pagenum,
                        "data": mysql_dict,
                        "meta": {
                            "msg": "获取元素页面列表成功",
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

#查询单个元素页面
def get_id_element_page(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'GET':
        id = request.GET.get('id', '')
        with conn.cursor() as cursor:
                cursor.execute("SELECT * from  ui_element_page where id="+id)
                mysql_dict = cursor.fetchall()
                request_data = {
                "data": mysql_dict[0],
                "meta": {
                    "msg": "获取元素页面列表成功",
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
def add_element_page(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    # 新增元素页面
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            element_page_name = json_data['element_page_name']
            user_id = json_data['user_id']
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO ui_element_page (element_page_name,user_id,create_time) VALUES (%s,%s,now())",
                               [element_page_name,user_id])
                conn.commit()
                request_data = {
                    "meta": {
                        "msg": "元素页面添加成功",
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
#修改元素页面
@csrf_exempt
def edit_element_page(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        json_data = json.loads(request.body)

        max = ''
        ui_project = 'ui_element_page'
        try:
            id = json_data['id']
            element_page_name = json_data['element_page_name']
            with conn.cursor() as cursor:
                cursor.execute("UPDATE " + ui_project + " SET element_page_name='"+element_page_name+"' where id='"+str(id)+"'")
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
                    "msg": "获取元素页面失败",
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
    ui_project = 'ui_element_page'
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

def element_page(request):
    if request.method == 'GET':
        run = request.GET.get('run', '')
        element_page_id = request.GET.get('element_page_id', '')
        getConfig.Config().write_driver('1')
        getConfig.Config().write_run(run)
        getConfig.Config().write_element_page(element_page_id)
        os.system("python d:/vue_api/VueApi/element_page/test_selenium.py")
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

