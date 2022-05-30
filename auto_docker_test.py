from __future__ import print_function
import os

target_file='config.ini'


#environment
def gen_environment (fd):   #生成ini文件中的Environment项
    sys='debian'
    sys_tag='latest'
    update='yes'
    dependencies='wget texinfo'
    workspace='/root'

    fd.write('[Environment]\n')
    fd.write(f"sys : {sys}\n")
    fd.write(f"sys_tag : {sys_tag}\n")
    fd.write(f"update : {update}\n")
    fd.write(f"dependencies : {dependencies}\n")
    fd.write(f"workspace : {workspace}\n")
    fd.write("\n")


#source code
def gen_source_code(fd,version_link,gen_link,version_number):    #生成ini文件中的Source Code项
    compilation='make'
    install='make install || : && make check || : && make install || :'
    vul_binary_pos=''
    fd.write('[Source_Code]\n')
    fd.write(f"link : {version_link[gen_link[version_number]]}\n")
    fd.write(f"compilation : {compilation}\n")
    fd.write(f"install : {install}\n")
    fd.write(f"vul_binary_pos : {vul_binary_pos}\n")
    fd.write("\n")


#poc
def gen_PoC(fd):    #生成ini文件中的PoC项
    link='https://raw.githubusercontent.com/liruochen-coding/LinuxFlaw/master/CVE-2015-8106/exploit.tex'
    deploy=':'
    trigger='latex2rtf exploit.tex'

    fd.write("[PoC]\n")
    fd.write(f"link : {link}\n")
    fd.write(f"deploy : {deploy}\n")
    fd.write(f"trigger : {trigger}\n")
   
    
#version dictionary
def gen_version():     #版本号与下载链接作为键值对所对应的字典，版本2.3.9不存在
    version_link=dict()
    version_link['2.3.0']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.0/latex2rtf-2.3.0.tar.gz'
    version_link['2.3.1']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.1/latex2rtf-2.3.1.tar.gz'
    version_link['2.3.2']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.2/latex2rtf-2.3.2.tar.gz'
    version_link['2.3.3']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.3/latex2rtf-2.3.3.tar.gz'
    version_link['2.3.4']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.4/latex2rtf-2.3.4.tar.gz'
    version_link['2.3.5']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.5/latex2rtf-2.3.5.tar.gz'
    version_link['2.3.6']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.6/latex2rtf-2.3.6.tar.gz'
    version_link['2.3.7']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.7/latex2rtf-2.3.7a.tar.gz'
    version_link['2.3.8']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.8/latex2rtf-2.3.8.tar.gz'
    version_link['2.3.10']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.10/latex2rtf-2.3.10.tar.gz'
    version_link['2.3.11']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.11/latex2rtf-2.3.11a.tar.gz'
    version_link['2.3.12']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.12/latex2rtf-2.3.12.tar.gz'
    version_link['2.3.13']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.13/latex2rtf-2.3.13a.tar.gz'
    version_link['2.3.14']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.14/latex2rtf-2.3.14.tar.gz'
    version_link['2.3.15']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.15/latex2rtf-2.3.15.tar.gz'
    version_link['2.3.16']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.16/latex2rtf-2.3.16.tar.gz'
    version_link['2.3.17']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.17/latex2rtf-2.3.17.tar.gz'
    version_link['2.3.18']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.18/latex2rtf-2.3.18a.tar.gz'
    return version_link


def find_version(version_link,gen_link):     #二分查找具有漏洞的版本范围，第一个参数为版本号与链接对应的字典，第二个参数为版本号对应的列表
    left=0
    right=len(gen_link)-1
    mid=0      #作为查找左右范围的中间变量
    model=8   #已知版本2.3.8具有漏洞，从该版本左右各进行范围查找，并将该版本作为左右查找的一个边界
    min_version=0  #具有漏洞的最小版本号
    max_version=len(gen_link)-1  #具有漏洞的最大版本号
    flag=True   #判断是否有漏洞，此处待修改为gen_dockerfile文件、docker容器等的使用结果

    while left<model:    #查找2.3.8版本及其左边的版本范围
        with open(target_file, "w+") as fd:   #找不到或无法创建config.ini文件退出
            if not os.path.exists(target_file):
                print("No target file!")
                return 0
            else:
                mid=(left+model)//2    #二分查找
                gen_environment(fd)    #生成ini文件中的Environment项
                gen_source_code(fd,version_link,gen_link,mid) #生成ini文件中的Source Code项
                gen_PoC(fd)  #生成ini文件中的PoC项
                fd.close()
        if flag==True:    #如果该版本有漏洞，则查找的右边界model为该版本序号，同时置最小版本为该值
            model=mid
            min_version=mid
        else :            #没有漏洞，查找的左边界为mid+1（由于mid=(left+model)//2,其中的//为向下取整，
            left=mid+1    #故当left=model-1，且flag!=True的特殊情况时，mid=left，若采用left=mid的表达式，
                          #系统会卡在left=mid的循环中，故采用left=mid+1）
            
    model=8
    flag=False
    while right>model:      #查找2.3.8版本及其右边的版本范围，右边二分查找原理与左边相同
        with open(target_file, "w+") as fd:
            if not os.path.exists(target_file):
                print("No target file!")
                return 0
            else:
                mid=(right+model)//2
                gen_environment(fd)
                gen_source_code(fd,version_link,gen_link,mid)
                gen_PoC(fd)
                fd.close()
        if  flag==False:    #表示该版本没有漏洞
            right=mid-1
        else :
            model=mid
            max_version=mid

    print(f"version from {gen_link[min_version]} to {gen_link[max_version]}\n")  #打印出漏洞所在版本范围


def main():
    version_link=gen_version()  #产生字典
    gen_link=list(version_link.keys())  #将版本号存储在列表中，便于用下标访问
    find_version(version_link,gen_link)  #二分查找具有漏洞的版本范围


if __name__=='__main__':
    main()

#用上述信息批量生成config.ini文件，自动替换软件version和对应的link
#使用config.ini生成dockerfile
#随后向linux终端输入使用dockerfile创建镜像的命令，并读取终端的返回信息（可以使用subprocess.check_output()）