import MySQLdb.cursors
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from VueApi.views import views
conn = views.conn
from VueApi.config import getConfig
# 实例化Config
DB = getConfig.Config().get_db()
@csrf_exempt
def users(request):
    if request.method == "GET":  # 获取判断请求方式
        pagenum = request.GET.get('pagenum','')
        pageSize = request.GET.get('pagesize','')
        with conn.cursor() as cursor:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) from  user ")
                totalRecord = cursor.fetchall()
                totalRecord = int(totalRecord[0]['COUNT(*)']) #总用例数
                totalPageNum = (int(totalRecord) + int(pageSize) - 1) // int(pageSize) #总页数
                cursor.execute("SELECT * from  user limit " + str((int(pagenum) - 1) * int(pageSize)) + ',' + str(pageSize))
                data = cursor.fetchall()
                request_data = {
                    "data": {
                        "totalpage": totalPageNum,
                        "pagenum": int(pagenum),
                        "users": data
                    }
                }
                return JsonResponse(request_data)
    else:
        request_data = {
            "data": '',
            "meta": {
                "msg": "请求方式不对",
                "status": 404
            }
        }
        return JsonResponse(request_data)


def recursion(id):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    with conn.cursor() as cursor:
        cursor.execute("SELECT * from menus WHERE id='"+str(id)+"'")  # 查询用户表数据
        mysql_dict = cursor.fetchall()
        if mysql_dict:
            data = {}
            data['id'] = mysql_dict[0]['id']
            data['authName'] = mysql_dict[0]['authName']
            data['path'] = mysql_dict[0]['path']
            data['children'] = ''
            ##通过父级查询子集
            cursor.execute("SELECT t3.* FROM (SELECT t1.*,t2.*,IF(FIND_IN_SET(fid, @pids) "
                           "> 0, @pids := CONCAT(@pids, ',', id), '0') AS isChild FROM (SELECT * FROM menus  "
                           "ORDER BY fid,id) AS t1,( SELECT @pids := " + str(
                id) + " ) AS t2 ) t3 WHERE t3.isChild != '0' "
                      "ORDER BY id DESC  LIMIT 1;")
            data1 = cursor.fetchall()
            if data1:
                dd = []
                try:
                    for b in data1[0]['isChild'].split(','):
                        if str(id) == str(b):
                            pass  #如果ID等于本身不执行
                        else:
                            a = recursion(b) #重复执行查询所有子集
                            if a: #a有值追加到列表
                                dd.append(a)
                            else:
                                pass
                        data['children'] = dd #讲子集信息追加到children
                except Exception as e:
                    print(e)  # 打印所有异常到屏幕

            return data

        else:

            pass

@csrf_exempt
def menus(request):
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    if request.method == "GET":  # 获取判断请求方式
        # request_dict = request.GET.get('Authorization',request.headers['Authorization'])  # 获取接口请求发送过来的信息
        #
        # print(request_dict) #token
        '''
        在这里可以写接口在发送请求后的一系列处理方法
        '''
        with conn.cursor() as cursor:
            cursor.execute("SELECT * from menus WHERE level=0")  # 查询用户表数据
            request_dict = cursor.fetchall()
            data = []
            for dict in range(len(request_dict)):
                try:
                    d = recursion(request_dict[dict]['id']) #调用递归方法，通过父级拿到所有子集并归类
                    data.append(d)
                except Exception as e:
                    print(e)
            request_data = {
                    "data":
                         data
                         ,
                    "meta": {
                        "msg": "获取菜单列表成功",
                        "status": 200
                    }
             }

        return JsonResponse(request_data)

    else:
        request_data = {
            "data":'',
            "meta": {
                "msg": "请求方式错误",
                "status": 400
            }
        }
        return JsonResponse(request_data)



if __name__ == '__main__':
    a = recursion(1)
    print(a)