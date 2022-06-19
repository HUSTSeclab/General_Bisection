#!/usr/bin/python
# -*- coding: utf-8 -*-
from gen_dockerfile import *
import subprocess
#生成的配置文件的文件名
target_file='config.ini'
#创建镜像和运行容器的命令
build_cmd=r'sudo docker build -t a_image_docker /home/seed'
run_cmd=r'sudo docker run a_image_docker'

#environment
#参数：sys,sys_tag,update,dependencies,workspace
def gen_environment (fd):   #生成ini文件中的Environment项
    sys='debian'
    sys_tag='latest'
    update='yes'
    dependencies='wget texinfo'
    workspace='/root'

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
    compilation='make'
    install='make install || (cp /root/targetsoftware/latex2rtf /usr/local/bin/ && mkdir /usr/local/share/latex2rtf && cp -r /root/targetsoftware/cfg/ /usr/local/share/latex2rtf/cfg/)'
#Bugs about installing latex2rtf:
#     "  If you nevertheless need to run install from the sources, note the following:
#     If your 'mkdir' doesn't support the '-p' option, then create the
#     necessary directories by hand and remove the option from the
#     '$MKDIR' variable.  If you have other problems, just copy
#     'latex2rtf' and 'latex2png' to a binary directory, and move the
#     contents of the 'cfg/' directory to the location specified by
#     '$CFG_INSTALL'.  "
    vul_binary_pos=''
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
    link='https://raw.githubusercontent.com/liruochen-coding/LinuxFlaw/master/CVE-2015-8106/exploit.tex'
    deploy=':'
    trigger='latex2rtf exploit.tex'

    fd.write("[PoC]\n")
    fd.write("link : "+link)
    fd.write("\n")
    fd.write("deploy : "+deploy)
    fd.write("\n")
    fd.write("trigger : "+trigger)
    fd.write("\n")
   
    
#version dictionary
#将软件的版本号和对应的下载链接存入字典
def gen_version():     #版本号与下载链接作为键值对所对应的字典，版本2.3.9不存在
    version_link=dict()
    version_link['2.0.0']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.0.0/latex2rtf-2.0.0.tar.gz'
    version_link['2.1.0']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.1.0/latex2rtf-2.1.0.tar.gz'
    version_link['2.1.1']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.1.1/latex2rtf-2.1.1beta8.tar.gz'
    version_link['2.2.0']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.2.0/latex2rtf-2.2.0.tar.gz'
    version_link['2.2.1']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.2.1/latex2rtf-2.2.1.tar.gz'
    version_link['2.3.0']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.0/latex2rtf-2.3.0.tar.gz'
    version_link['2.3.1']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.1/latex2rtf-2.3.1.tar.gz'
    version_link['2.3.2']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.2/latex2rtf-2.3.2.tar.gz'
    version_link['2.3.3']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.3/latex2rtf-2.3.3.tar.gz'
    version_link['2.3.4']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.4/latex2rtf-2.3.4.tar.gz'
    version_link['2.3.5']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.5/latex2rtf-2.3.5.tar.gz'
    version_link['2.3.6']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.6/latex2rtf-2.3.6.tar.gz'
    version_link['2.3.7']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.7/latex2rtf-2.3.7a.tar.gz'
    version_link['2.3.8']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.8/latex2rtf-2.3.8.tar.gz'
    #version_link['2.3.10']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.10/latex2rtf-2.3.10.tar.gz'
    version_link['2.3.11']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.11/latex2rtf-2.3.11a.tar.gz'
    version_link['2.3.12']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.12/latex2rtf-2.3.12.tar.gz'
    version_link['2.3.13']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.13/latex2rtf-2.3.13a.tar.gz'
    version_link['2.3.14']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.14/latex2rtf-2.3.14.tar.gz'
    version_link['2.3.15']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.15/latex2rtf-2.3.15.tar.gz'
    version_link['2.3.16']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.16/latex2rtf-2.3.16.tar.gz'
    version_link['2.3.17']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.17/latex2rtf-2.3.17.tar.gz'
    version_link['2.3.18']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.18/latex2rtf-2.3.18a.tar.gz'
    return version_link

#将版本号升序存储在列表中，便于用下标访问
def gen_version_list(v_list):
    for number in range(0,19): #按照版本序号升序创建列表，版本2.3.9不存在
        if number==9 or number==10:
            continue
        v_list.append("2.3.%s"%number)


def find_version(version_link,gen_link):     #二分查找具有漏洞的版本范围，第一个参数为版本号与链接对应的字典，第二个参数为版本号对应的列表
    left=0
    right=len(gen_link)-1
    mid=0      #作为查找左右范围的中间变量
    model=8   #已知版本2.3.8具有漏洞，从该版本左右各进行范围查找，并将该版本作为左右查找的一个边界
    min_version=8  #具有漏洞的最小版本号,仅当检测到新的有漏洞的版本，才给min_version赋值，故赋初值为8
    max_version=8  #具有漏洞的最大版本号,仅当检测到新的有漏洞的版本，才给min_version赋值，故赋初值为8
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
                    print("falied to build the docker "+gen_link[mid]+"!")
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
            
    model=8
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
    version_link=gen_version()  #产生字典

    gen_link=list() #版本号列表
    gen_version_list(gen_link)

    find_version(version_link,gen_link)  #二分查找具有漏洞的版本范围


if __name__=='__main__':
    main()
