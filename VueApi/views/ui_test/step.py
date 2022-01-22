from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from VueApi.views import views
conn = views.conn
from time import sleep

import MySQLdb
import MySQLdb.cursors
from VueApi.config import getConfig
# 实例化Config
DB = getConfig.Config().get_db()


#查询步骤列表
def get_step(request):
    if request.method == 'GET':
        conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                               cursorclass=MySQLdb.cursors.DictCursor)
        step_name = request.GET.get('query', '')
        pagenum = request.GET.get('pagenum','')
        pageSize = request.GET.get('pagesize','')
        case_id = request.GET.get('case_id', '')
        min = str((int(pagenum)-1)*int(pageSize))
        try:
            if step_name:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) from  step where step_name like '%" + step_name + "%'")
                    totalRecord = cursor.fetchall()
                    totalRecord = int(totalRecord[0]['COUNT(*)'])  # 总步骤数
                    # totalPageNum = (int(totalRecord) + int(pagenum) - 1) * int(pageSize) // int(pageSize)  # 总页数
                    sql = "	SELECT s.id, s.step_name,e.element_name,m.method_name,s.wait_time,c.case_name,u.user_name,s.sort,s.create_time FROM" \
                          " step AS s,ui_case AS c,`user` AS u,type AS t,element AS e,method AS m WHERE s.element_id = e.id 	AND s.method_id = m.id 	AND s.user_id = u.id 	AND s.case_id = c.id 	AND  s.step_name like'%" + step_name + "%' AND s.case_id="+case_id+ \
                          " GROUP BY s.id  DESC LIMIT " + min + ',' + str(pageSize)
                    cursor.execute(sql)
                    mysql_dict = cursor.fetchall()
                    sleep(0.1)
                    for data in range(len(mysql_dict)):
                        mysql_dict[data]['create_time'] = mysql_dict[data]['create_time'].strftime("%Y-%m-%d %H:%M:%S")
                    request_data = {
                        "totalRecord": totalRecord,
                        "pagenum": pagenum,
                        "data": mysql_dict,
                        "meta": {
                            "msg": "获取步骤列表成功",
                            "status": 200
                        }
                    }
                    return JsonResponse(request_data)
            else:
                with conn.cursor() as cursor:
                        cursor.execute("SELECT COUNT(*) from  step ")
                        totalRecord = cursor.fetchall()
                        totalRecord = int(totalRecord[0]['COUNT(*)']) #总步骤数
                        # totalPageNum = (int(totalRecord) + int(pagenum) - 1)*int(pageSize) // int(pageSize) #总页数
                        sql = "	SELECT s.id, s.step_name,e.element_name,m.method_name,s.wait_time,c.case_name,u.user_name,s.sort,s.create_time FROM" \
                              " step AS s,ui_case AS c,`user` AS u,type AS t,element AS e,method AS m WHERE  s.element_id = e.id 	AND s.method_id = m.id 	AND s.user_id = u.id 	AND s.case_id = c.id 	AND s.case_id="+case_id+" GROUP BY s.id DESC LIMIT " + min + ',' + str(pageSize)
                        cursor.execute(sql)
                        mysql_dict = cursor.fetchall()
                        sleep(0.1)
                        for data in range(len(mysql_dict)):
                            mysql_dict[data]['create_time'] = mysql_dict[data]['create_time'].strftime("%Y-%m-%d %H:%M:%S")
                        request_data = {
                        "totalRecord": totalRecord,
                        "pagenum": pagenum,
                        "data": mysql_dict,
                        "meta": {
                            "msg": "获取步骤列表成功",
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

#查询单个步骤
def get_id_step(request):
    if request.method == 'GET':
        id = request.GET.get('id', '')
        with conn.cursor() as cursor:
            sql = "	SELECT * from step WHERE  id="+id
            cursor.execute(sql)
            mysql_dict = cursor.fetchall()
            request_data = {
            "data": mysql_dict[0],
            "meta": {
                "msg": "获取步骤列表成功",
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
def add_step(request):
    # 新增步骤
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            step_name = json_data['step_name']
            case_id = json_data['case_id']
            element_id = json_data['element_id']
            user_id = json_data['user_id']
            method_id = json_data['method_id']
            wait_time = json_data['wait_time']
            with conn.cursor() as cursor:
                cursor.execute("	INSERT INTO step ( step_name, case_id, user_id, element_id, method_id, wait_time, create_time)  VALUES (%s,%s,%s,%s,%s,%s,now())",
                               [step_name,case_id,user_id,element_id,method_id,wait_time])
                cursor.execute("UPDATE  step set sort=id")
                conn.commit()
                request_data = {
                    "meta": {
                        "msg": "步骤添加成功",
                        "status": 200
                    }
                }
        except Exception as e:
            print(e)
            request_data = {
                "meta": {
                    "msg": "添加失败",
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
    #修改步骤
@csrf_exempt
def edit_step(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        max = ''
        ui_project = 'step'
        try:
            id = json_data['id']
            step_name = json_data['step_name']
            element_id = json_data['element_id']
            method_id = json_data['method_id']
            wait_time = json_data['wait_time']
            with conn.cursor() as cursor:
                cursor.execute("UPDATE " + ui_project + " SET step_name=%s, element_id=%s, method_id=%s, wait_time=%s where id=%s",[step_name,element_id,method_id,wait_time,id])
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
            try:
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
            except Exception as e:
                print(e)
                request_data = {
                    "meta": {
                        "msg": "排序失败",
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


# 学生信息删除处理函数
def delete(request):
    id = request.GET.get("id")
    ui_project = 'step'
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
        cursor.execute("UPDATE "
                       + ui_project +
                       " SET sort=id;")
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