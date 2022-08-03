# General_Bisection
General Bisection about cause and fix

step.pkl存放所有用于自动测试的软件字典，格式如下：`[dict1,dict2,dict3,...]   dict均为字典`

`dict`的结构为：

1. `dict['id']=''`
2. `dict['software']=''`
3. `dict['start']=''`
4. `dict['sys']=''`
5. `dict['sys_tag']=''`
6. `dict['update']=''`
7. `dict['dependencies']=''`
8. `dict[workspace]=''`
9. `dict['compilation']=''`
10. `dict['install']=''`
11. `dict['vul_binary_pos']=''`
12. `dict['link']=''`
13. `dict['deploy']=''`
14. `dict['trigger']=''`

software.pkl存放自动测试的步骤，格式如下：`[[dict1,name1],[dict2,name2],[dict3,name3],...]    dict均为字典，name均为软件名字符串`

`dict`的结构为：

- `dict['2.3.8']='www.baidu.com'`    键值对数量不定

Dockerfiles文件夹用于备份，存放每个漏洞的复现Dockerfile

运行`sudo python3 auto_docker_test.py`启动测试
