# ~*~ coding: utf-8 ~*~
#!/usr/bin/env python3

import json
import sys
import re
import os
import re
import getpass
import platform
import logging

class DirectMenu():
 
    def __init__(self):
        self.username = getpass.getuser()
        self._id = "序号"
        self._name = "名称"
        self._ip = "IP"
        self._type = "类型"
        self._account = "账号"
        self.FILE_NAME = "E:\github\Python\ssh_server\data.json"
        self.page = 1
        self.test = 1
        self.article = 10
 #       self.prompt = 'fort> '
        self.asset = u"""\033[30;42m%s%s%s%s%s\r\033[0m""" % (self._id.ljust(10),self._name.ljust(20),self._ip.center(37),self._type.ljust(10),self._account.rjust(30))

        with open(self.FILE_NAME, 'r', encoding='UTF-8') as f:
            self.data = json.load(f)

    def welcome(self):
        '''展示欢迎页面'''
        msg = u"""\n\033[1;32m  %s, 欢迎使用运维管理平台 \033[0m\r\n\r
        1) 输入 \033[32m序号\033[0m 直接登录 (未完成)\r
        2) 输入 \033[32m/\033[0m + \033[32mIP, 名称\033[0m搜索. 如: /ip(未完成)\r
        3) 输入 \033[32mP/p\033[0m 显示您有权限访问的资源.或 退出搜索\r
        4) 输入 \033[32mn\033[0m 显示下一页.\r
        5) 输入 \033[32mN\033[0m 显示上一页.\r
        6) 输入 \033[32mH/h\033[0m 帮助.\r
        0) 输入 \033[32mQ/q\033[0m 退出.\r\n""" % self.username
   
        print(msg)
    
    def dispatch(self):
        """根据用户的输入执行不同的操作
        n: 下一页
        N: 上一页
        /: 搜索资源, 支持资源名, ip
        q: 退出
        h: 打印帮助
        直接搜索登录: 直接输入会搜索, 如果唯一则直接登录资源
        """
        page_count = (len(self.data)-1)//self.article + 1
        option = self.get_input()
        if option.startswith('/'):
            option = option.lstrip('/')
            self.search_resource(option=option)        
        elif option in ['', ' ', '\r', '\n']:
            self.dispatch()
        elif option in ['n']:
            self.page += 1
            if self.page > page_count:
                self.page -= 1
                print("\033[31mIs already the last page\033[0m")
                self.dispatch()
        elif option.isdigit():
            self.login_resource(option,self.data)

        elif option in ['N']:
            self.page -=1
            if self.page < 1:
                self.page += 1
                print("\033[31mIs already the first page\033[0m")
                self.dispatch()

        elif option in ['P','p']:
            with open(self.FILE_NAME, 'r') as f:
                self.data = json.load(f)

        elif option in ['q', 'Q']:
            del self
            sys.exit()
 
        else:
            print("不支持此命令!")
            self.dispatch()

    def directmenu_display(self,data,article,page=1):
        '''   直连菜单展示
        data: 要展示的json格式数据
        page: 当前页数
        article： 每页展示条目数量
        '''
        print(self.asset)                 #打印标题
        start = (page - 1) * article
        end = page * article
        sequence = start
        for line in range(len(data[start:end])):
            fortResourceName = data[start:end][line]['fortResourceName']
            fortResourceName.encode('utf-8')
            fortResourceIp = data[start:end][line]['fortResourceIp']
            fortResourceTypeName = data[start:end][line]['fortResourceTypeName']
            fortAccounts = data[start:end][line]['fortAccounts']
            fortAccounts = re.split("\||:",fortAccounts)[1::2]
            sequence = sequence + 1
            sequence1 = str(sequence)
            asse = u"""%s %s %s %s %s""" % (self.string_ljust(sequence1,10),self.string_ljust(fortResourceName,30),fortResourceIp.center(27),self.string_ljust(fortResourceTypeName,30),fortAccounts)
            print(asse)   
    def get_input(self,prompt='fort> '):
        '''获取用户输入并返回 '''
        input_data = input(prompt)
        return input_data
 
    def login_resource(self,option,data):
        '''登陆资源'''
        option = int(option)
        fortAccounts = data[option - 1]['fortAccounts']
        fortAccounts = re.split("\||:",fortAccounts)[1::2]
        fortResourceIp = data[option - 1]['fortResourceIp']
        if (len(fortAccounts)) > 1:
            print("\033[32m有多个用户授权，请选择其中一个\033[0m")
            system_user = self.choose_system_user(fortAccounts)
            
            if system_user:              
                print(system_user,fortResourceIp)
            self.dispatch()
        else:
            print(fortAccounts)
    def choose_system_user(self,system_users):
        while True:
            for index,system_user in enumerate(system_users):
                print(index,system_user)
            option = self.get_input(prompt='System user> ')
            if option.isdigit() and int(option) < len(system_users):
                system_user = system_users[int(option)]
                return system_user
            elif option in ['q','Q']:
                return
            else:
                print('\033[31mNo system user match, please input again\033[0m')

    def search_resource(self,option):
        '''搜索资源'''
        data = self.data
        page = self.page
        article = self.article
        start = (page - 1) * article
        end = page * article
        sequence = start
        option = option.strip().lower()
        #self.prompt = 'search> '


        if option:
            #print(option)
            #print(self.asset)
            data1 = []
       # if option.isdigit() and int(option) < len(data):
            for line in range(len(data)):
                fortResourceName = data[line]['fortResourceName']
                fortResourceIp = data[line]['fortResourceIp']
                fortResourceTypeName = data[line]['fortResourceTypeName']
                fortAccounts = data[line]['fortAccounts']
                fortAccounts = re.split("\||:",fortAccounts)[1::2]
                sequence = sequence + 1
                sequence1 = str(sequence)
                id_search_result = [sequence1,fortResourceName,fortResourceIp,fortResourceTypeName]
                for item in id_search_result:
                    match = re.search(option,item)
                    if match is not None:
                        data1.append(data[line])
                        break
            #self.directmenu_display(data1,article)
            if not data1:
                print("no search")
                self.dispatch()
            else:
                self.data = data1
                
        else:
            #print("no search")
            self.directmenu_display(data,article)      
        
    def is_chinese(self,uchar):

        """判断一个unicode是否是汉字"""

        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':

            return True

        else:

            return False

 

    def align(self, text, width, just = "left" ):  
        stext = str(text)
        utext = text
        cn_count = 0

        for u in utext:

            if self.is_chinese(u):

                cn_count += 2 # 计算中文字符占用的宽度

            else:

                cn_count += 1  # 计算英文字符占用的宽度

        if just == "right":

            return " " * (width - cn_count ) + stext  

        elif just == "left":

            return stext + " " * ( width - cn_count )


    def string_ljust(self, text, width ):

        return self.align( text, width, "left" )


    def string_rjust(self, text, width ):

        return align( text, width, "right" )

    def run(self):
        while True:
            #try:
            system_version = platform.system()
            if system_version == 'Windows':
                os.system('cls')
            elif system_version == 'Linux':
                os.system('clear')
            self.welcome()
            self.directmenu_display(self.data,self.article,self.page)
            self.dispatch()
            #except:
            #    del self
            #    break


if __name__ == '__main__':
    try: 
        menu = DirectMenu()
        menu.run()
    except KeyboardInterrupt as e:
        print()
