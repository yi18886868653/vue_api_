from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from VueApi.views import views
import json
conn = views.conn
import MySQLdb
import MySQLdb.cursors
from VueApi.config import getConfig
# 实例化Config
DB = getConfig.Config().get_db()

#查询元素列表
@csrf_exempt
def get_method(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'GET':
        method_name = request.GET.get('query', '')
        pagenum = request.GET.get('pagenum','')
        pageSize = request.GET.get('pagesize','')
        min = str((int(pagenum)-1)*int(pageSize))
        try:
            if method_name:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) from  method where method_name like '%" + method_name + "%'")
                    totalRecord = cursor.fetchall()
                    totalRecord = int(totalRecord[0]['COUNT(*)'])  # 总用例数
                    # totalPageNum = (int(totalRecord) + int(pagenum) - 1) * int(pageSize) // int(pageSize)  # 总页数
                    cursor.execute(
                        "SELECT a.*,b.user_name FROM method a,`user` b WHERE a.user_id=b.id  AND method_name like '%" + method_name + "%'" + " limit " + min + ',' + str(pageSize))
                    mysql_dict = cursor.fetchall()
                    request_data = {
                        "totalRecord": totalRecord,
                        "pagenum": pagenum,
                        "data": mysql_dict,
                        "meta": {
                            "msg": "获取元素列表成功",
                            "status": 200
                        }
                    }
                    return JsonResponse(request_data)
            else:
                with conn.cursor() as cursor:
                        cursor.execute("SELECT COUNT(*) from  method ")
                        totalRecord = cursor.fetchall()
                        totalRecord = int(totalRecord[0]['COUNT(*)']) #总用例数
                        # totalPageNum = (int(totalRecord) + int(pagenum) - 1)*int(pageSize) // int(pageSize) #总页数
                        cursor.execute("SELECT a.*,b.user_name FROM method a,`user` b WHERE a.user_id=b.id  limit " + min + ',' + str(pageSize))
                        mysql_dict = cursor.fetchall()
                        request_data = {
                        "totalRecord": totalRecord,
                        "pagenum": pagenum,
                        "data": mysql_dict,
                        "meta": {
                            "msg": "获取元素列表成功",
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

#查询单个元素
@csrf_exempt
def get_id_method(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'GET':
        id = request.GET.get('id', '')
        with conn.cursor() as cursor:
                cursor.execute("SELECT * from  method where id="+str(id))
                mysql_dict = cursor.fetchall()
                request_data = {
                "data": mysql_dict[0],
                "meta": {
                    "msg": "获取元素成功",
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
def add_method(request):
    # 新增元素
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        # try:
            json_data = json.loads(request.body)
            print(json_data)
            method_name = json_data['method_name']
            py_name = json_data['py_name']
            user_id = json_data['user_id']
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO method (method_name,py_name,user_id) VALUES (%s,%s,%s)",
                               [method_name,py_name,user_id])
                conn.commit()
                request_data = {
                    "meta": {
                        "msg": "用例添加成功",
                        "status": 200
                    }
                }
        # except:
        #     request_data = {
        #         "meta": {
        #             "msg": "参数错误 method_name,py_name,user_id为必填项",
        #             "status": 404
        #         }
        #     }
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
def edit_methode(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            ui_project = 'method'
            id = json_data['id']
            method_name = json_data['method_name']
            py_name = json_data['py_name']
            with conn.cursor() as cursor:
                cursor.execute("UPDATE " + ui_project + " SET method_name='"+method_name+"',py_name='"+py_name+"' where id='"+str(id)+"'")
                conn.commit()
                request_data = {
                    "meta": {
                        "msg": "修改成功",
                        "status": 200
                    }
                }
            return JsonResponse(request_data)
        except:
            request_data = {
                "meta": {
                    "msg": "缺少参数",
                    "status": 400
                }
            }
            return JsonResponse(request_data)


@csrf_exempt
def delete(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    id = request.GET.get("id")
    ui_project = 'method'
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
if __name__ == '__main__':
    pass