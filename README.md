# fileWeb_link
flask 文件服务器 <font color="red">不安全的</font>
使用start_hidden.vbs 调用 start_show.bat 开启 manage.py 的 flask 项目
manage.py 会生成 stop_manage.bat(可以暂停flask项目)

open_or_stop.bat 会调用 start_hidden.vbs 和 stop_manage.bat
实现服务器的开启关闭

