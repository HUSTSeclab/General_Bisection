#修改pkl文件之前请先备份原文件

import pickle
import pprint

'''
pkl_file=open('software.pkl','rb')
data=pickle.load(pkl_file)

for x in data:
    if x[1]=='latex2rtf':
        (x[0])['1.9.11']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/1.9k/latex2rtf-1.9k.tar.gz'
        (x[0])['1.9.10']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/1.9j/latex2rtf-1.9j.tar.gz'
        (x[0])['1.9.9']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/1.9i/latex2rtf-1.9i.tar.gz'
        (x[0])['1.9.8']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/1.9h/latex2rtf-1.9h.tar.gz'
        (x[0])['1.9.7']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/1.9g/latex2rtf-1.9g.tar.gz'
        (x[0])['1.9.6']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/1.9f/latex2rtf-1.9f.tar.gz'
        (x[0])['1.9.5']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/1.9e/latex2rtf-1.9e.tar.gz'
        (x[0])['1.9.4']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/1.9d/latex2rtf-1.9d.tar.gz'
        (x[0])['1.9.3']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/1.9c/latex2rtf-1.9c.tar.gz'
        (x[0])['1.8']='https://sourceforge.net/projects/latex2rtf/files/latex2rtf-unix/1.8aa/latex2rtf_1.8aa.tar.gz'
        break

pprint.pprint(data)
pkl_file.close()

pkl_file2=open('software.pkl','wb')
pickle.dump(data,pkl_file2)
pkl_file2.close()
'''