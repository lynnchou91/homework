'''
作业：建git共享文件，并用pymysql建立数据库
author：周小灵
date：2019.11.06
'''
import pymysql
from hashlib import sha1


conn = pymysql.Connect(host='127.0.0.1',user='root',password='123',port=3306,charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)

# 1.建库
try:
    sql = "create database bbs default charset = 'utf8'"
    result=cursor.execute(sql)
    if result >0:
        print("创建成功")
        cursor.execute("use bbs")
    else:
        print("创建失败")
except Exception as e:
    print(e)
    exit()

# 2.建表
try:
    sql1 = "create table if not exists user(" \
           "uid int primary key auto_increment," \
           "username varchar(10) unique, " \
           "usertype enum('0','1') default '0'," \
           "password varchar(100), " \
           "regtime datetime default current_timestamp, " \
           "email varchar(50))"
    result = cursor.execute(sql1)
    # if result > 0:
    #     print("创建成功")
    # else:
    #     print("创建失败")
except Exception as e:
    print(e)

# cursor.execute("use bbs")

# 3.输入信息并验证，验证通过则写入user表
username0=input("请输入注册用户名：")
password0=input("请输入注册密码：")
password0=sha1(password0.encode('utf8')).hexdigest()
email0=input("请输入注册邮箱：")

sql2 = "select username from user"
sql3 = "insert into user(username,password,email) values('{}','{}','{}')"
cursor.execute(sql2)
res = cursor.fetchall()
print(res)
tmp=[]
for i in range(len(res)):
    tmp += [res[i]['username']]
print(tmp)
try:
    if username0 in tmp:
        print('用户已经存在，请重新输入')
    elif len(username0) <=2:
        print('⽤户名⻓度必须⼤于2')
    elif str.isspace(username0):
        print('⽤户名不能为纯空格')
    else:
        sql3 = sql3.format(username0,password0,email0)
        cursor.execute(sql3)
        conn.commit()
except Exception as e:
    print(e)


# 4.用户登录
username1=input("请输入用户名：")
password1=input("请输入密码：")
password1 = sha1(password1.encode('utf8')).hexdigest()
sql4 = "select username,password from user where username='{}' and password='{}'".format(username1,password1)
if cursor.execute(sql4):
    print('登录成功')
else:
    print('用户名或密码错误，请重新输入')

# 5.显示信息
sql5 = "select username '用户名',usertype '用户类型', password '密码', regtime '注册时间', email from user"
cursor.execute(sql5)
print(cursor.fetchall())

cursor.close()
conn.close()
