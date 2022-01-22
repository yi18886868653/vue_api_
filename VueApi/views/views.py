from django.shortcuts import render

# Create your views here.


import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from VueApi.comm import timed_task
import MySQLdb.cursors
from VueApi.config import getConfig
# 实例化Config
DB = getConfig.Config().get_db()

#自动运行
# timed_task.timed_task()




conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',cursorclass=MySQLdb.cursors.DictCursor)

@csrf_exempt
def my_api(request):
    dic = {}
    if request.method == 'GET':

        dic['message'] = 0
        return HttpResponse(json.dumps(dic))
    else:
        dic['message'] = '方法错误'
        return HttpResponse(json.dumps(dic, ensure_ascii=False))
@csrf_exempt
def test(request):
    request_data = {
        "data": {},
        "meta": {
            "msg": "启动成功",
            "status": 200
        }
    }
    return JsonResponse(request_data)

@csrf_exempt
def login(request):
    if request.method == "POST": #获取判断请求方式
            try:
                json_data = json.loads(request.body) # json.loads函数的使用，将字符串转化为字典
                username = json_data['username'] #获取接口请求发送过来的信息
                password = json_data['password']
                with conn.cursor() as cursor:
                    # '''
                    # 在这里可以写接口在发送请求后的一系列处理方法
                    # '''
                    cursor.execute("SELECT * from  user WHERE user_name='" + str(username) + "' ") #查询用户表数据
                    request_dict = cursor.fetchall()
                # conn.commit()
                try:
                    if request_dict[0]['password'] == str(password):
                        request_data = {
                            "data": {
                                "id": request_dict[0]['id'],
                                "rid": request_dict[0]['user_name'],
                                'token': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjUwMCwicmlkIjowLCJpYXQiOjE2Mzc3MzcxMTUsImV4cCI6MTYzNzgyMzUxNX0.1m4Paxnl0M8hOhZPU1hX9b7wqBp7i51EZsPlWNxTVBQ'
                            },
                            "meta": {
                                "msg": "登录成功",
                                "status": 200
                            }
                        }
                    else:
                        request_data = {
                            "data": {},
                            "meta": {
                                "msg": "密码错误",
                                "status": 400
                            }
                        }
                except  Exception as e:
                    print(e)
                    request_data = {
                            "data": {},
                            "meta": {
                                "msg": "账号错误",
                                "status": 400
                            }
                        }

            except Exception as e:
                print(e)
                request_data = {
                    "data": {},
                    "meta": {
                        "msg": "参数错误缺少username或passwrod",
                        "status": 400
                    }
                }

            return JsonResponse(request_data)
    else:
        request_data = {
            "data": {},
            "meta": {
                "msg": "请求方式错误",
                "status": 400
            }
        }
        return JsonResponse(request_data)

