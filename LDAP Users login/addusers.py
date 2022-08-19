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

def Create_users():
    #新建一个文件；
    xls=xlwt.Workbook()
    sheet1=xls.add_sheet("Sheet1")
    #添加字段
    sheet1.write(0,0,"First name")
    sheet1.write(0, 1, "Full name")
    sheet1.write(0, 2, "Password")
    sheet1.write(0,3,"Domain name")
    #循环添加内容
    for i in range(1,60001):
        j=i+60000
        sheet1.write(i,0,"ssouser{}".format(j))
        sheet1.write(i,1,"ssouser{}".format(j))
        sheet1.write(i,2,"hyllydia@2022")
        sheet1.write(i, 3, "Siemax.com")
    #保存文件
    xls.save("D:\create_ssousers02.xls")
def xls_to_csv():
    workbook = xlrd.open_workbook('D:\create_ssousers02.xls')
    table = workbook.sheet_by_name("Sheet1")
    with codecs.open('D:\create_ssousers02.csv', 'w',encoding="utf-8") as f:
        write = csv.writer(f)
        for row_num in range(table.nrows):
            write.writerow(table.row_values(row_num))

if __name__=="__main__":
    Create_users()
    xls_to_csv()