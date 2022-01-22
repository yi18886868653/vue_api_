import sys
sys.path.extend(['D:\\vue_api'])
import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from VueApi.comm import getExcel
from VueApi.config import setting
from selenium.webdriver.support.ui import WebDriverWait
import pytest
from VueApi.comm.mylog import Logger
from time import sleep
import pywinauto
from pywinauto.keyboard import send_keys


logger = Logger(logger='TestMylog').getlog()  # 实例化日志类
excel_path = setting.EXCEL_DIR
data = getExcel.ExcelUtil(excel_path)
@allure.feature("朝霞智投")
class TestDirver(object):
    def get_element(self, method, value, browser,i=0):
        try:
            if method == 'xpath':
                element = browser.find_element_by_xpath(value)
            elif method == 'id':
                element = browser.find_element_by_id(value)
            elif method == 'name':
                element = browser.find_element_by_class_name(value)
            elif method == 'text':
                element = browser.find_element_by_link_text(value)
            elif method == 'class':
                element = browser.find_elements_by_class_name(value)[i]
            elif method == 'css':
                element = browser.find_elements_by_css_selector(value)[i]
            else:
                print('请输入类型method（id,name,text,xpath,class,css')
            return element
        except TimeoutException:
            return print('查找元素超时')

    def element_wait(self, by, value, browser, secs=10):
        """
         等待元素显示
         """
        try:
            if by == "id":
                el = WebDriverWait(browser, secs, 1).until(EC.presence_of_element_located((By.ID, value)))
            elif by == "name":
                el = WebDriverWait(browser, secs, 1).until(EC.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                el = WebDriverWait(browser, secs, 1).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "text":
                el = WebDriverWait(browser, secs, 1).until(EC.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "xpath":
                el = WebDriverWait(browser, secs, 1).until(EC.presence_of_element_located((By.XPATH, value)))

            elif by == "css":
                el = WebDriverWait(browser, secs, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            else:
                raise NoSuchElementException(
                    "找不到元素，请检查语法或元素")
            return el
        except TimeoutException:
            print("查找元素超时请检查元素")
            return "查找元素超时请检查元素"



    @pytest.mark.parametrize('case,use_case_step,action,location,type,text,time,i,username,t',data.all_data() ) #pytest装饰器参数化，遍历excel文档
    @allure.story("用例")
    def test_Cz(self,browser,case,use_case_step,action,location,type,time,text,i,username,t):
        #print(ca,ca1)
        # try:
           with allure.step(case):
            if action == '首页':
                browser.get(text)
                browser.maximize_window()
                
            if action == "点击":
                if type == "xpath" :
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.click()
                elif type == "id":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.click()
                elif type == "text":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.click()
                elif type == "class":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.click()
                elif type == "css":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.click()
                sleep(time)

            if action == "输入":
                if type == "xpath":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.send_keys(text)
                elif type == "id":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.send_keys(text)
                elif type == "text":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.send_keys(text)
                elif type =="class":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.send_keys(text)
                elif type == "css":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.send_keys(text)
                sleep(time)
            if action == "清除":
                '''清除输入框的内容'''
                if type == "xpath":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.clear()
                elif type == "id":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.clear()
                elif type == "text":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.clear()
                elif type == "class":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.clear()
                elif type == "css":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    el.clear()
                sleep(time)
            if action == "右键":
                """
                右键单击元素.
                """

                if type == "xpath":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).context_click(el).perform()
                elif type == "id":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).context_click(el).perform()
                elif type == "text":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).context_click(el).perform()
                elif type == "class":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).context_click(el).perform()
                elif type == "css":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).context_click(el).perform()
                sleep(time)
            if action == "悬停":


                """
                  鼠标移到元素（悬停）.
                  """

                if type == "xpath":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).move_to_element(el).perform()
                elif type == "id":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).move_to_element(el).perform()
                elif type == "text":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).move_to_element(el).perform()
                elif type == "class":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).move_to_element(el).perform()
                elif type == "css":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).move_to_element(el).perform()
               
                sleep(time)
            if action == "双击":
                """
                双击元素.
                """
                if type == "xpath":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).double_click(el).perform()
                elif type == "id":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).double_click(el).perform()
                elif type == "text":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).double_click(el).perform()
                elif type == "class":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).double_click(el).perform()
                elif type == "css":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    ActionChains(browser).double_click(el).perform()
                sleep(time)

            if action == "滚动":
                """滚动到元素的位置"""
                if type == "xpath":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    browser.execute_script("arguments[0].scrollIntoView();", el)
                elif type == "id":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    browser.execute_script("arguments[0].scrollIntoView();", el)
                elif type == "text":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    browser.execute_script("arguments[0].scrollIntoView();", el)
                elif type == "class":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    browser.execute_script("arguments[0].scrollIntoView();", el)
                elif type == "css":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    browser.execute_script("arguments[0].scrollIntoView();", el)
                sleep(time)

            if action == "移动":
                """
                把一个元素拖到一定的距离，然后把它放下.
                """
                if type == "xpath":
                    self.element_wait(type, location, browser)
                    el  = self.get_element(type, location, browser, i)
                sleep(time)

            if action == "元素文本":
                """
                获取元素属性的值.
                """
                if type == "xpath":
                    self.element_wait(type, location, browser)
                    el  = self.get_element(type, location, browser, i)
                    return el.get_attribute('textContent')
                elif type == "id":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    return el.get_attribute('textContent')
                elif type == "text":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    return el.get_attribute('textContent')
                elif type == "class":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    return el.get_attribute('textContent')
                elif type == "css":
                    self.element_wait(type, location, browser)
                    el = self.get_element(type, location, browser, i)
                    return el.get_attribute('textContent')
                sleep(time)

            if action == "键盘输入":
                """
               直接控制键盘输入
                """
                ActionChains(browser).send_keys(text).perform()
                sleep(time)

            if action == "关闭当前页面":
                """
                模拟用户在弹出框的标题栏中点击“关闭”按钮窗口或选项卡.
                """
                browser.close()
                sleep(time)
            if action == "结束":
                """
                 结束.
                """
                # browser.close()
                browser.quit()
                sleep(time)

            if action == "刷新":
                """
                 刷新当前页面.
                """
                browser.refresh()
                sleep(time)
            if action == "窗口标题":
                """
                得到窗口标题.
                用法:
                driver.get_title()
                """
                return browser.title
                sleep(time)
            if action == "断言":
                """
                断言内容
                """
                sleep(2)
                if type == "xpath":
                    self.element_wait(type, location, browser)
                    el  = self.get_element(type, location, browser, i)
                    assert el.text == text
                elif type == "id":
                    self.element_wait(type, location, browser)
                    el  = self.get_element(type, location, browser, i)
                    assert el.text == text
                elif type == "text":
                    self.element_wait(type, location, browser)
                    el  = self.get_element(type, location, browser, i)
                    assert el.text == text
                elif type == "class":
                    self.element_wait(type, location, browser)
                    el  = self.get_element(type, location, browser, i)
                    assert el.text == text
                elif type == "css":
                    self.element_wait(type, location, browser)
                    el  = self.get_element(type, location, browser, i)
                    assert el.text == text
                print("断言成功")
                sleep(time)
            if action == '切换页面':
                handles = browser.window_handles
                print(handles)
                print(text)
                browser.switch_to.window(handles[int(text)])
                sleep(time)

            if action == '上传文件':
                # 使用pywinauto来选择文件
                app = pywinauto.Desktop()
                # 选择文件上传的窗口
                dlg = app["打开"]
                # 选择文件地址输入框，点击激活
                dlg["Toolbar3"].click()
                # 键盘输入上传文件的路径
                send_keys("桌面")
                # 键盘输入回车，打开该路径
                send_keys("{VK_RETURN}")
                # 选中文件名输入框，输入文件名
                dlg["文件名(&N):Edit"].type_keys("1.jpg")
                # 点击打开
                dlg["打开(&O)"].click()
    # except:
        #     logger.info(case+":"+use_case_step+",""执行失败")

    def run_case(self):
        pytest.main(["/vue_api/VueApi/case/test_mysql.py"])
        pytest.main(["/vue_api/VueApi/case","-s","-v"])

if __name__ == '__main__':
   # data = getExcel.ExcelUtil(excel_path)
   # test = TestDirver()
   # test.test_Cz()
   # #test.Cz(action=data.A("操作"), value=data.A("定位"), type=data.A("类型"), value1=data.A("值"))
   a = TestDirver()
   a.run_case() #运行pytest
