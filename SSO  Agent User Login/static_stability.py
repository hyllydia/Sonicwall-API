#coding:utf-8
"""
Author:Hou Yuling
Time:10/19/2021 4:04 PM
"""
#--coding:utf-8--
#思路：
#1、创建一个新的xlsx文件；
#2、workbook的名字
#3、A列,B列是用户名，test1, test2 ...依次加1
#4、C列是密码，D列域名，E列OU=Users, 这一列可以不写
#5、在盒子上测试，发现用户的CN="test1",CN="Users",DC="Siemax",DC="com"

import xlwt
import xlrd
import csv
import codecs


def dealwith_ab(b,a):
    if a > 255:
        a = 0
        b += 1
    return b,a

def Create_users():
    #新建一个文件；
    xls=xlwt.Workbook()
    sheet1=xls.add_sheet("static")
    #添加字段
    # sheet1.write(0,0,"First name")
    # sheet1.write(0, 1, "Full name")
    # sheet1.write(0, 2, "Password")
    # sheet1.write(0,3,"Domain name")
    #循环添加内容
    #4700
    b, a = 100, 1
    for i in range(1, 3001):
        b, a = dealwith_ab(b, a)
        sheet1.write(i, 0, "20.101.{}.{}".format(b, a))
        sheet1.write(i, 1, "domain\\user{}".format(i))
        a += 1
    #5700
    m, n = 100, 1
    for i in range(3001, 6001):
        m, n = dealwith_ab(m, n)
        sheet1.write(i, 0, "30.101.{}.{}".format(m, n))
        sheet1.write(i, 1, "domain\\user{}".format(i))
        n += 1
    #6700
    b1, a1 = 100, 1
    for i in range(6001, 9001):
        b1, a1 = dealwith_ab(b1, a1)
        sheet1.write(i, 0, "40.101.{}.{}".format(b1, a1))
        sheet1.write(i, 1, "domain\\user{}".format(i))
        a1 += 1
    #10700
    b2, a2 = 100, 1
    for i in range(9001, 12001):
        b2, a2 = dealwith_ab(b2, a2)
        sheet1.write(i, 0, "50.101.{}.{}".format(b2, a2))
        sheet1.write(i, 1, "domain\\user{}".format(i))
        a2 += 1
    #11700
    b4, a4 = 100, 1
    for i in range(15001, 18001):
        b4, a4 = dealwith_ab(b4, a4)
        sheet1.write(i, 0, "60.101.{}.{}".format(b4, a4))
        sheet1.write(i, 1, "domain\\user{}".format(i))
        a4 += 1
        #保存文件
    xls.save("D:\static.xls")
def xls_to_csv():
    workbook = xlrd.open_workbook('D:\static.xls')
    table = workbook.sheet_by_name("static")
    with codecs.open('D:\static.csv', 'w',encoding="utf-8") as f:
        write = csv.writer(f)
        for row_num in range(table.nrows):
            write.writerow(table.row_values(row_num))

if __name__=="__main__":
    Create_users()
    xls_to_csv()