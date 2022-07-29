# General_Bisection
General Bisection about cause and fix

software.pkl存放所有用于自动测试的软件字典，格式如下：`[dict1,dict2,dict3,...]   dict均为字典`

step.pkl存放自动测试的步骤，格式如下：`[[dict1,name1],[dict2,name2],[dict3,name3],...]    dict均为字典，name均为软件名字符串`

Dockerfiles文件夹用于备份，存放每个漏洞的复现Dockerfile

运行`sudo python3 auto_docker_test.py`启动测试
