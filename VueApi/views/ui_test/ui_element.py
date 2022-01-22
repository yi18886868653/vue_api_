from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from VueApi.views import views
conn = views.conn
import MySQLdb
import MySQLdb.cursors
from VueApi.config import getConfig
# 实例化Config
DB = getConfig.Config().get_db()



#查询元素列表
@csrf_exempt
def get_element(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'GET':
        element_name = request.GET.get('query', '')
        pagenum = request.GET.get('pagenum','')
        pageSize = request.GET.get('pagesize','')
        min = str((int(pagenum)-1)*int(pageSize))
        try:
            if element_name:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) from  element where element_name like '%" + element_name + "%'")
                    totalRecord = cursor.fetchall()
                    totalRecord = int(totalRecord[0]['COUNT(*)'])  # 总用例数
                    # totalPageNum = (int(totalRecord) + int(pagenum) - 1) * int(pageSize) // int(pageSize)  # 总页数
                    cursor.execute(
                        "SELECT e.id,e.element,e.element_name,t.type_name,e.text,e.array,u.user_name,e.create_time from element as e, type as t,`user` as u WHERE e.type_id=t.id AND e.user_id=u.id  AND element_name like '%" + element_name + "%' GROUP BY e.id DESC" + " limit " + min + ',' + str(pageSize))
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
                with conn.cursor() as cursor:
                        cursor.execute("SELECT COUNT(*) from  element ")
                        totalRecord = cursor.fetchall()
                        totalRecord = int(totalRecord[0]['COUNT(*)']) #总用例数
                        # totalPageNum = (int(totalRecord) + int(pagenum) - 1)*int(pageSize) // int(pageSize) #总页数
                        cursor.execute("SELECT e.id,e.element,e.element_name,t.type_name,e.text,e.array,u.user_name,e.element_page,e.create_time from element as e, type as t,`user` as u WHERE e.type_id=t.id AND e.user_id=u.id GROUP BY e.id DESC  limit " + min + ',' + str(pageSize))
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
                "data": '',
                "meta": {
                    "msg": "请求方式错误",
                    "status": 400
                }
            }
        # conn.close()
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
def get_id_element(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'GET':
        id = request.GET.get('id', '')
        with conn.cursor() as cursor:
                cursor.execute("SELECT * from element where id="+id)
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
def add_element(request):
    # 新增用例
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            element = json_data['element']
            element_name = json_data['element_name']
            user_id = json_data['user_id']
            text = json_data['text']
            array = json_data['array']
            type_id = json_data['type_id']
            element_page = json_data['element_page']
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO `element`( element, element_name, user_id, text, array,type_id ,element_page, create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,now())",
                               [element, element_name, user_id, text, array,type_id,element_page])
                conn.commit()
                request_data = {
                    "meta": {
                        "msg": "元素添加成功",
                        "status": 200
                    }
                }
        except Exception as e:
            print(e)
            request_data = {
                "meta": {
                    "msg": "参数错误",
                    "status": 404
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
def edit_element(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        json_data = json.loads(request.body)
        # try:
        id = json_data['id']
        element_name = json_data['element_name']
        element = json_data['element']
        text = json_data['text']
        array = json_data['array']
        with conn.cursor() as cursor:
            cursor.execute(" UPDATE element SET element_name=%s,element=%s,text=%s,array=%s where id=%s",
                           [element_name, element, text, array, id])
            conn.commit()
            conn.commit()
            request_data = {
                "meta": {
                    "msg": "修改成功",
                    "status": 200
                }
            }
            return JsonResponse(request_data)
        # except:
        #     request_data = {
        #         "meta": {
        #             "msg": "参数不对",
        #             "status": 400
        #         }
        #     }
        # return JsonResponse(request_data)
    else:
        request_data = {
            "data": '',
            "meta": {
                "msg": "请求方式错误",
                "status": 400
            }
        }
        return JsonResponse(request_data)


# 学生信息删除处理函数
def delete(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    id = request.GET.get("id")
    ui_project = 'element'
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM " + ui_project + " WHERE id in (" + id + ")")
        cursor.execute("DELETE FROM "
                       + ui_project +
                       " WHERE id in (" + id + ")")
        conn.commit()
        request_data = {
            "meta": {
                "msg": "删除成功",
                "status": 200
            }
        }
    return JsonResponse(request_data)

if __name__ == '__main__':
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    id = '14,13,12'
    ui_project = 'element'
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM " + ui_project + " WHERE id in (" + id+")")
        cursor.execute("DELETE FROM "
                       + ui_project +
                       " WHERE id in (" + id+")")
        conn.commit()
        request_data = {
            "meta": {
                "msg": "删除成功",
                "status": 200
            }
        }