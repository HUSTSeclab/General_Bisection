#!/usr/bin/python
# -*- coding: utf-8 -*-
from gen_dockerfile import *
from functools import *
import subprocess
import pickle
import pprint
#生成的配置文件的文件名
target_file='config.ini'
#创建镜像和运行容器的命令
build_cmd=r'sudo docker build -t a_image_docker .'
run_cmd=r'sudo docker run a_image_docker'

#是否从文件读取软件字典，1代表是，0代表否
software_load_from_pkl=1
#是否从文件读取测试步骤，1代表是，0代表否
step_load_from_pkl=1

#测试的相关信息和步骤
id='CVE20042167'  #形如CVE20158106，必填，以便程序自动从文件中读取其余信息
#如果不从文件读取测试步骤，则需手动填写以下全局变量
software=''
start=''        #以哪个版本为起点开始二分测试
sys=''
sys_tag=''
update=''
dependencies=''
workspace=''
compilation=''
install=''
vul_binary_pos=''
link=''
deploy=''
trigger=''

#如果不从文件读取软件列表，则需手动创建
if software_load_from_pkl==0:
    version_link=dict()

#在remove列表中添加需要在测试中排除的版本号
remove=['1.8','1.9.3','1.9.4','1.9.5','1.9.6','1.9.7','1.9.8','1.9.9','1.9.10','1.9.12','1.9.17','1.9.18','1.9.19']
if software_load_from_pkl==0:
    for x in remove:
        del version_link[x]

def load_step():
    #从文件读取测试步骤
    outcome=0  #找到对应信息返回0，没找到返回1
    global id,software,start,sys,sys_tag,update,dependencies,workspace,compilation,install,vul_binary_pos,link,deploy,trigger
    pkl_file=open('step.pkl','rb')
    step=pickle.load(pkl_file)
    for x in step:
        if x['id']==id:
            #找到对应id，开始读取信息
            software=x['software']
            start=x['start']
            sys=x['sys']
            sys_tag=x['sys_tag']
            update=x['update']
            dependencies=x['dependencies']
            workspace=x['workspace']
            compilation=x['compilation']
            install=x['install']
            vul_binary_pos=x['vul_binary_pos']
            link=x['link']
            deploy=x['deploy']
            trigger=x['trigger']
            outcome=0
            break
        else:
            outcome=1
    return outcome


#environment
#参数：sys,sys_tag,update,dependencies,workspace
def gen_environment (fd):   #生成ini文件中的Environment项
    global sys,sys_tag,update,dependencies,workspace
    fd.write('[Environment]\n')
    fd.write("sys : "+sys)
    fd.write("\n")
    fd.write("sys_tag : "+sys_tag)
    fd.write("\n")
    fd.write("update : "+update)
    fd.write("\n")
    fd.write("dependencies : "+dependencies)
    fd.write("\n")
    fd.write("workspace : "+workspace)
    fd.write("\n")


#source code
#参数：compilation,install,vul_binary_pos
def gen_source_code(fd,version_link,gen_link,version_number):    #生成ini文件中的Source Code项
    global compilation,install,vul_binary_pos
    fd.write('[Source Code]\n')
    fd.write("link : "+version_link[gen_link[version_number]])
    fd.write("\n")
    fd.write("compilation : "+compilation)
    fd.write("\n")
    fd.write("install : "+install)
    fd.write("\n")
    fd.write("vul_binary_pos : "+vul_binary_pos)
    fd.write("\n")


#poc
#参数：link,deploy,trigger
#注意，若没有deploy命令，则用空指令:填充
def gen_PoC(fd):    #生成ini文件中的PoC项
    global link,deploy,trigger
    fd.write("[PoC]\n")
    fd.write("link : "+link)
    fd.write("\n")
    fd.write("deploy : "+deploy)
    fd.write("\n")
    fd.write("trigger : "+trigger)
    fd.write("\n")
   
    
#version dictionary
#将软件的版本号和对应的下载链接存入字典
def gen_version():     
    #提取存放在文件中的版本号与下载链接的字典
    #software.pkl文件中数据的格式：[[dict1,name1],[dict2,name2],[dict3,name3],...]  其中dict均为字典，name均为软件名字符串
    global software,remove
    pkl_file=open('software.pkl','rb')
    whole_list=pickle.load(pkl_file)
    #whole_list是一个列表
    for x in whole_list:
        #x也是列表
        if x[1]==software:
            #x第0项是字典，第1项是软件名
            version_link=x[0]
            break
        else:
            #没找到就返回1
            version_link=1
    #删除字典中测试需要排除的键值对        
    if version_link!=1:
        for x in remove:
            del version_link[x]
    
    return version_link


def sort_rule(str1,str2): #用于比较两个版本的前后，根据“.”分割字符串从前往后比较，数字大的版本靠后
    arr1=str1.split(".")
    arr2=str2.split(".")
    temp1=0
    temp2=0
    length=len(arr1)
    for i in range(0,length):
        temp1=int(arr1[i])
        temp2=int(arr2[i])
        if temp1 > temp2:
            return 1
        elif temp1 < temp2:
            return -1


def gen_version_list(v_list,version_link):   #将版本号升序存储在列表中，便于用下标访问
   for i in version_link.keys():
       v_list.append(i)
   v_list.sort(key=cmp_to_key(sort_rule)) #由于虚拟机里字典的keys函数取出来的键是随机的，故需要进行排序


def find_version(version_link,gen_link):     #二分查找具有漏洞的版本范围，第一个参数为版本号与链接对应的字典，第二个参数为版本号对应的列表
    global start
    left=0
    right=len(gen_link)-1
    mid=0      #作为查找左右范围的中间变量
    initial_version=gen_link.index(start) #从2.3.8版本开始二分查找漏洞
    model=initial_version   #已知版本2.3.8具有漏洞，从该版本左右各进行范围查找，并将该版本作为左右查找的一个边界
    min_version=initial_version  #具有漏洞的最小版本号,仅当检测到新的有漏洞的版本，才给min_version赋值，故赋初值为8
    max_version=initial_version  #具有漏洞的最大版本号,仅当检测到新的有漏洞的版本，才给min_version赋值，故赋初值为8
    flag=True   #判断是否有漏洞，flag=True时说明存在漏洞

    while left<=model:    #查找2.3.8版本及其左边的版本范围
        with open(target_file, "w+") as fd:   #找不到或无法创建config.ini文件退出
            if not os.path.exists(target_file):
                print("No target file!")
                return 0
            else:
                mid=(left+model)//2    #二分查找
                print(gen_link[mid]+"\n")
                gen_environment(fd)    #生成ini文件中的Environment项
                gen_source_code(fd,version_link,gen_link,mid) #生成ini文件中的Source Code项
                gen_PoC(fd)  #生成ini文件中的PoC项
                fd.seek(0)   #将文件指针置头以读取文件
                gen_file()   #产生dockerfile文件    
     
                result0=subprocess.run(build_cmd,shell=True,stdout=subprocess.PIPE)
                if result0.returncode!=0: #容器创建失败
                    flag=False
                    print("----------falied to build the docker "+gen_link[mid]+"!")
                    return 0
                else:                     #容器创建成功
                    flag=True
                    print("Sucessfully build the docker "+gen_link[mid]+"!")

                    result=subprocess.run(run_cmd,shell=True,stdout=subprocess.PIPE)
                    if result.returncode==139:   #当有漏洞时程序异常终止，returncode返回139
                        flag=True
                        print("version "+gen_link[mid]+" exsits the vulnerability !\n")  
                    else :
                        flag=False          #其他情况代表无漏洞
                        print("version "+gen_link[mid]+" doesn't exsit the vulnerability !\n")

        if flag==True:    #如果该版本有漏洞，则查找的右边界model为该版本序号，同时置最小版本为该版本序号
            model=mid
            min_version=mid
            print("\n"+gen_link[min_version]+"\n")
            fd.close()
        else :            #没有漏洞，查找的左边界为mid+1（由于mid=(left+model)//2,其中的//为向下取整，
            left=mid+1    #故当left=model-1，且flag!=True的特殊情况时，mid=left，若采用left=mid的表达式，
            fd.close()    #系统会卡在left=mid的循环中，故采用left=mid+1）
        if left==model and model==mid:
            break
            
    model=initial_version
    flag=False
    while right>=model:      #查找2.3.8版本及其右边的版本范围，右边二分查找原理与左边相同
        with open(target_file, "w+") as fd:
            if not os.path.exists(target_file):
                print("No target file!")
                return 0
            else:
                mid=(right+model)//2
                print(gen_link[mid]+"\n")
                gen_environment(fd)
                gen_source_code(fd,version_link,gen_link,mid)
                gen_PoC(fd)
                fd.seek(0)
                gen_file()
                result0=subprocess.run(build_cmd,shell=True,stdout=subprocess.PIPE)
                if result0.returncode!=0:
                    flag=False
                    print("falied to build the docker "+gen_link[mid]+"!")
                else:
                    flag=True
                    print("Sucessfully build the docker"+gen_link[mid]+"!")
                    result=subprocess.run(run_cmd,shell=True,stdout=subprocess.PIPE)
                    if result.returncode==139:
                        flag=True 
                        print("version "+gen_link[mid]+" exsits the vulnerability !\n") 
                    else :
                        flag=False
                        print("version "+gen_link[mid]+" doesn't exsit the vulnerability !\n")
        if model==right:
            break
        if  flag==False:    #表示该版本没有漏洞
            right=mid-1
            fd.close()
        else :
            model=mid+1
            max_version=mid
            print("\n"+gen_link[max_version]+"\n")
            fd.close()
        if right==model and model==mid:
            break
    print("the versions ranging from "+gen_link[min_version] +" to "+ gen_link[max_version]+" exsit the vulnerability\n")  #打印出漏洞所在版本范围


def main():
    global version_link,id
    if step_load_from_pkl==1:
        #从文件读取步骤
        print('Load steps from local file')
        if load_step()==1:
            print('case'+id+'was not included in step.pkl!')
            return
    else:
        print('Load steps manully from the code')
    if software_load_from_pkl==1:
        #从文件读取软件字典
        print('Load software dict from local file')
        version_link=gen_version()  #产生字典
        if version_link==1:
            print('software '+software+' was not included in software.pkl!\n')
            return
    else:
        print('Load software manully from the code')

    gen_link=list() #版本号列表
    gen_version_list(gen_link,version_link)
    find_version(version_link,gen_link)  #二分查找具有漏洞的版本范围


if __name__=='__main__':
    main()
