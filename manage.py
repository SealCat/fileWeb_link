# -*- coding: utf-8 -*-
from ftpServer import app
import os
def produce_stop_bat(pid, tmpfile="stop_xxx.bat"):
    # 待写入内容
    stop_cmd = 'taskkill /pid ' + str(pid) + ' /f'  # 关闭指定进程
    del_self_cmd = "del %0"  # 删除自身文件
    # 文件路径和名称
    tmp_all = "stop_" + tmpfile + ".bat"
    # 写入文件
    with open(file=tmp_all, mode="w") as f:
        f.write(stop_cmd + "\n" + del_self_cmd)
 
# 进程号
pid = os.getpid()
# 本文件名（不含后缀.py）
myfilename = os.path.split(__file__)[-1].split(".")[0]
# 生成关闭进程的脚本文件
produce_stop_bat(pid, myfilename)

if __name__ == '__main__':
    app.run(host='127.0.0.1')
