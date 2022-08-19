#coding:utf-8
"""
Author:Hou Yuling
Time:8/18/2022 2:04 PM
"""
import socket

#创建TCP Socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("socket created")