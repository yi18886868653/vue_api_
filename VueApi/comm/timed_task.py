import MySQLdb
import MySQLdb.cursors
import datetime
import threading
import os
from time import sleep
import jenkins

from VueApi.config import getConfig
# 实例化Config
DB = getConfig.Config().get_db()
def func():
    conn = MySQLdb.connect(host=DB.host, user=DB.username, passwd=DB.password, db=DB.db, charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    with conn.cursor() as cursor:
        cursor.execute("SELECT id,run_time from record ")
        data = cursor.fetchall()
        dd = []
        for id in data:
          print(id['run_time'])
          now_time = str(datetime.datetime.now().strftime('%H:%M'))
          data_time = str(id['run_time']).strip('0').strip(':')
          print(now_time+"=="+data_time)

          if now_time == data_time:
              dd.append(id['id'])
        print(dd)
        for d in dd:
          print(d)
          print('执行')
          run = 2
          record = d
          driver = 2
          getConfig.Config().write_run(str(run))
          getConfig.Config().write_record(str(record))
          getConfig.Config().write_driver(str(driver))
          run_jenkins()
          timed_task()
    #如果需要循环调用，就要添加以下方法
    timer = threading.Timer(1800, func)
    timer.start()


def timed_task():
  # 获取现在时间
  now_time = datetime.datetime.now()
  now_hour = now_time.hour
  now_minute = now_time.minute
  now_year = now_time.date().year
  now_month = now_time.date().month
  now_day = now_time.date().day


  #判断当前时间是否半小时
  if now_minute == 0 or now_minute == 30:
    next_time = now_time
  elif now_minute > 30 :
    now_hour+=1
    print(now_hour)
    next_time = datetime.datetime.strptime(
      str(now_year)+"-"+str(now_month)+"-"+str(now_day)+" "+str(now_hour)+":00:00", "%Y-%m-%d %H:%M:%S")
  elif now_minute <30:
    next_time = datetime.datetime.strptime(
      str(now_year) + "-" + str(now_month) + "-" + str(now_day) + " " + str(now_hour) + ":30:00", "%Y-%m-%d %H:%M:%S")


  #距离下次任务间隔多少秒
  timer_start_time = (next_time - now_time).total_seconds()
  print("距离自动执行任务还有:"+str(timer_start_time)+"秒")
  # 54186.75975
  #定时器,参数为(多少时间后执行，单位为秒，执行的方法)
  timer = threading.Timer(timer_start_time, func)
  timer.start()

jenkins_host = 'http://jenkins-case.com:8080'
jenkins_user = 'admin'
jenkins_password = 'admin'
job_name = 'regression testing'
def run_jenkins():
    server = jenkins.Jenkins(jenkins_host, username=jenkins_user, password=jenkins_password)
    server.build_job(job_name, {'project': 'aiad'}) #参数
    # 获取job名为job_name的job的相关信息
    # server.get_job_info(job_name)
    # 获取job名为job_name的job的最后次构建号
    sleep(10)
    status= status_jenkins()
    if status == False:
        print('jenkin构建结束')


def status_jenkins():
    server = jenkins.Jenkins(jenkins_host, username=jenkins_user, password=jenkins_password)
    build_number = server.get_job_info(job_name)['lastBuild']['number']
    print(build_number)
    # 获取job名为job_name的job的某次构建的执行结果状态
    server.get_build_info(job_name, build_number)['result']
    # 判断job名为job_name的job的某次构建是否还在构建中
    status = server.get_build_info(job_name, build_number)['building']
    if status == False:
        print('返回')
        return status
    else:
        print('构建中')
        sleep(15)
        status = status_jenkins()
        return status


if __name__ == '__main__':
    func()