FROM liruochen2008/ready_for_exp:v1.2
MAINTAINER "Dongliang Mu" <mudongliangabcd@gmail.com>
RUN apt -y update && apt -y upgrade
RUN apt -y install wget texinfo
WORKDIR /root
RUN wget https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/2.3.8/latex2rtf-2.3.8.tar.gz; \
mkdir targetsoftware; \
tar -xvf latex2rtf-2.3.8.tar.gz -C targetsoftware --strip-components 1; \
cd targetsoftware; \
(make || :) && (make install || :) && ((cp /root/targetsoftware/latex2rtf /usr/local/bin/ && (mkdir /usr/local/share/latex2rtf || :) && cp -r /root/targetsoftware/cfg/ /usr/local/share/latex2rtf/cfg/ && cp -r /root/targetsoftware/cfg/ /usr/local/lib/latex2rtf/) || :); 
RUN wget https://gitee.com/liruochen2008/LinuxFlaw/raw/master/CVE-2015-8106/exploit.tex; \
:
RUN rm -rf /var/lib/apt/lists
CMD latex2rtf exploit.tex
