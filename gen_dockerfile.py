#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
from configparser import SafeConfigParser
import os

config_file = "config.ini"

dockerfile = "Dockerfile"

def add_maintainer(fd):
    fd.write("MAINTAINER \"Dongliang Mu\" <mudongliangabcd@gmail.com>")
    fd.write("\n")
    
def add_system(fd, os, os_tag):
    if not os_tag:
        fd.write("FROM " + os)
    else:
        fd.write("FROM " + os + ":" + os_tag)
    fd.write("\n")

def add_update_by_sys(fd, linux):
    if (linux.lower() == "debian" or linux.lower() == "ubuntu" or 
        linux.lower() == "kali" or 1==1):
        #暂时去除对系统的判断
        fd.write("RUN apt -y update && apt -y upgrade")
        fd.write("\n")
    else:
        print(linux + "is not supported for now")
        # yum -y update

def install_dep_by_sys(fd, linux, package):
    if (linux.lower() == "debian" or linux.lower() == "ubuntu" or 
        linux.lower() == "kali" or 1==1):
        #暂时去除对系统的判断
        #不再默认安装build-essential软件包
        fd.write("RUN apt -y install " + package)
        fd.write("\n")
    else:
        print(linux + "is not supported for now")
        # yum install package

def switch_workspace(fd, workspace):
    fd.write("WORKDIR " + workspace)
    fd.write("\n")

def install_program(fd, prog_link, compile_method, prog_install):
    fd.write("RUN wget " + prog_link + "; \\")
    fd.write("\n")
    #将压缩包解压到以下目录
    fd.write("mkdir targetsoftware; \\")
    fd.write("\n")

    prog_name = os.path.basename(prog_link)

    if prog_name.endswith("tar.gz"):
        prog_dir=prog_name.split('.tar.gz')[0]
        fd.write("tar -xvf " + prog_name + " -C targetsoftware --strip-components 1; \\")
        #-C指定解压目录 --strip-components去除原有目录结构
        fd.write("\n")
    elif prog_name.endswith("zip"):
        prog_dir=prog_name.split('.zip')[0]
        fd.write("unzip -j " + prog_name + " -d targetsoftware; \\")
        #-j去除目录结构 -d指定解压目录
        fd.write("\n")
    else :
        print(prog_name, "has unsupported compression format")
    fd.write("cd targetsoftware; \\" )
    fd.write("\n")

    fd.write(compile_method)
    fd.write(" && ")
    fd.write(prog_install)
    fd.write("; \n")
    
def deploy_poc(fd, poc_link, deploy):
    fd.write("RUN wget " + poc_link + "; \\")
    fd.write("\n")
    fd.write(deploy)
    fd.write("\n")

def add_trigger_method(fd, trigger):
    fd.write("CMD " + trigger)
    fd.write("\n")

def clean_cache_by_sys(fd, linux):
    if (linux.lower() == "debian" or linux.lower() == "ubuntu" or 
        linux.lower() == "kali" or 1==1):
        #暂时去除对系统的判断
        fd.write("RUN rm -rf /var/lib/apt/lists")
        fd.write("\n")
    else:
        print(linux + "is not supported for now")
        # yum clean all


def gen_file():
    print("Read config file and generate one Dockerfile")

    clean_cache = False

    with open(dockerfile, "w") as fd:
        if not os.path.exists(config_file):
            print("No configuration file")
                 
        config = SafeConfigParser()
        config.read(config_file)

        sys_linux = config.get("Environment", "sys") 
        sys_tag = config.get("Environment", "sys_tag") 
        update = config.getboolean("Environment", "update") 
        dep = config.get("Environment", "dependencies") 
        workspace = config.get("Environment", "workspace")

        add_system(fd, sys_linux, sys_tag)
        add_maintainer(fd)

        if update:
            add_update_by_sys(fd, sys_linux)
            clean_cache = True

        if dep:
            install_dep_by_sys(fd, sys_linux, dep)

        switch_workspace(fd, workspace)

        prog_link = config.get("Source Code", "link")
        compile_method = config.get("Source Code", "compilation")
        prog_install = config.get("Source Code", "install")
        binary_pos = config.get("Source Code", "vul_binary_pos")

        install_program(fd, prog_link, compile_method, prog_install)

        poc_link = config.get("PoC", "link")
        deploy = config.get("PoC", "deploy")
        trigger = config.get("PoC", "trigger")
         
        deploy_poc(fd, poc_link, deploy)

        if clean_cache:
            clean_cache_by_sys(fd, sys_linux)
    
        add_trigger_method(fd, trigger)

    print("Finish Dockerfile generation")
