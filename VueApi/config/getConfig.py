#coding:utf-8
import os
import configparser
from VueApi.config import setting
class Dictionary(dict):

    '''
    把config.ini中的参数添加值dict
    '''
    def __getattr__(self, keyname):
        #如果key值不存在则返回默认值"not find requirements keyname"
        return self.get(keyname, "requirements.ini中没有找到对应的keyname")

class Config(object):
    '''
    ConfigParser二次封装，在字典中获取value
    '''
    def __init__(self):
        #——————————————————————————————————————————
        # 设置conf.ini路径
        #current_dir = os.path.dirname(__file__)
        #top_one_dir = os.path.dirname(current_dir)
        #file_name = top_one_dir + "\\**.ini"  当前项目路径+文件路径
        #--------------------------------------—————
        # 引用setting ini文件路径
        file_name = setting.CONFIG_DIR
        # 实例化ConfigParser对象
        self.config = configparser.ConfigParser()
        self.config.read(file_name)
        #根据section把key、value写入字典
        for section in self.config.sections():
            setattr(self, section, Dictionary())
            for keyname, value in self.config.items(section):
                setattr(getattr(self, section), keyname, value)

    def getconf(self, section):
        '''
        用法：
        conf = Config()
        info = conf.getconf("main").url
         '''
        if section in self.config.sections():
            pass
        else:
            print("requirements.ini 找不到该 section")
        return getattr(self, section)
     #获取ini数据
    def get_db(self):
        value = self.getconf("DATABASE")
        return value

    def get_http(self):
        value = self.getconf("HTTP")
        return value

    def get_drive(self):
        value = self.getconf("DRIVE")
        return value

    def get_db_run(self):
        value = self.getconf("DATABASE_RUN")
        return value

    def get_project(self):
        value = self.getconf("PROJECT")
        return value

    def get_case(self):
        value = self.getconf("CASE")
        return value

    def get_record(self):
        value = self.getconf("RECORD")
        return value

    def write_driver(self,int):
        file_name = setting.CONFIG_DIR
        self.config.read(file_name)
        # a = self.config.add_section("DRIVER")
        self.config.set("DRIVER", "driver", int)
        self.config.write(open(file_name, "r+"))  # 可以把r+改成其他方式，看看结果:)

    def write_run(self,int):
        file_name = setting.CONFIG_DIR
        self.config.read(file_name)
        # a = self.config.add_section("DRIVER")
        self.config.set("DATABASE_RUN", "run", int)
        self.config.write(open(file_name, "r+"))  # 可以把r+改成其他方式，看看结果:)

    def write_record(self,int):
        file_name = setting.CONFIG_DIR
        self.config.read(file_name)
        # a = self.config.add_section("DRIVER")
        self.config.set("RECORD", "record_id", int)
        self.config.write(open(file_name, "r+"))  # 可以把r+改成其他方式，看看结果:)

    def write_case(self, int):
        file_name = setting.CONFIG_DIR
        self.config.read(file_name)
        # a = self.config.add_section("DRIVER")
        self.config.set("CASE", "case_id", int)
        self.config.write(open(file_name, "r+"))  # 可以把r+改成其他方式，看看结果:)

if __name__ == "__main__":
    conf = Config()
    info = conf.getconf("DATABASE")
    print(conf.get_db().host)
    conf.cs()
    #使用方法  导入类 from comm.getConfig import Config
    #实例化对象   data = Data()
    #调用方法get_http方法获取url的值 data.get_http().url