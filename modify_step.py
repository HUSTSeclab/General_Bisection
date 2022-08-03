#修改pkl文件之前请先备份原文件

import pickle
import pprint

'''
pkl_file=open('step.pkl','rb')
data=pickle.load(pkl_file)
pkl_file.close()

for x in data:
    if x['id']=='CVE20158106':
        x['install']='(make install || :) && ((cp /root/targetsoftware/latex2rtf /usr/local/bin/ && (mkdir /usr/local/share/latex2rtf || :) && cp -r /root/targetsoftware/cfg/ /usr/local/share/latex2rtf/cfg/ && cp -r /root/targetsoftware/cfg/ /usr/local/lib/latex2rtf/) || :)'
        break

new_dict=dict()
new_dict['id']='CVE20042167'
new_dict['software']='latex2rtf'
new_dict['start']='1.9.15'
new_dict['sys']='liruochen2008/ready_for_exp'
new_dict['sys_tag']='v1.2'
new_dict['update']='yes'
new_dict['dependencies']='wget texinfo'
new_dict['workspace']='/root'
new_dict['compilation']='(make || :)'
new_dict['install']='(make install || :) && ((cp /root/targetsoftware/latex2rtf /usr/local/bin/ && (mkdir /usr/local/share/latex2rtf || :) && cp -r /root/targetsoftware/cfg/ /usr/local/share/latex2rtf/cfg/ && cp -r /root/targetsoftware/cfg/ /usr/local/lib/latex2rtf/) || :)'
new_dict['vul_binary_pos']=''
new_dict['link']='https://gitee.com/liruochen2008/for_download/raw/master/code/latex2rtf.c https://gitee.com/liruochen2008/for_download/raw/master/code/poc.tex'
new_dict['deploy']='gcc -o exploit latex2rtf.c'
new_dict['trigger']='(./exploit > poc.tex) && (latex2rtf poc.tex)'
data.append(new_dict)
pprint.pprint(data)

pkl_file2=open('step.pkl','wb')
pickle.dump(data,pkl_file2)
pkl_file2.close()
'''
