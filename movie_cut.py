#截取视频，去掉头尾
# -*- coding: UTF-8 -*-

import os
import math
import re
import sys

#请根据您的情况自行修改todo位置的代码

def cut_movie(src_path,des_path):
    #todo 片头长度
    header_time_str='00:02:27'
    #header_time_str = '00:00:00'
    header_time=header_time_str.split(":")
    header_time=int(header_time[0])*3600+int(header_time[1])*60+int(header_time[2])
    print ("header_time",header_time)
    #todo 片尾长度
    #footer_time_str='00:01:58'
    footer_time_str = '00:00:00'
    footer_time=footer_time_str.split(":")
    footer_time=int(footer_time[0])*3600+int(footer_time[1])*60+int(footer_time[2])
    print ("footer_time",footer_time)

    #tmp = os.popen('''ffprobe "/Volumes/TOSHIBA/\[纪晓岚1\]\[40集\]\[2001\]/01.mkv"  2>&1''')
    tmp = os.popen('''ffprobe "{}"  2>&1'''.format(src_path))
    tmp=tmp.read()
    #print ("------",tmp)
    matchObj=re.search(r"Duration: (.*?),",tmp,re.M|re.I)
    if not matchObj:
        return
    time_l=matchObj.group(1)
    print("time_l",time_l)

    #movie_len_str='00:46:51.05'
    movie_len_str=time_l
    movie_len_str=movie_len_str[:-3]

    print (movie_len_str)
    movie_len = movie_len_str.split(":")

    if int(movie_len[1])<39:
        #小于44分钟，可能没有片尾片头信息
        print (int(movie_len[1]))
        return

    movie_len=int(movie_len[0])*3600+int(movie_len[1])*60+int(movie_len[2])
    print ("movie_len",movie_len)

    #包含头的时间
    #now_time_len=movie_len-header_time-footer_time
    now_time_len = movie_len - footer_time
    print ("now_time_len",now_time_len)

    h=math.floor( now_time_len/3600)
    print ("h",h)
    m=math.floor((now_time_len-(3600*h))/60)
    print (m)
    s=now_time_len-(3600*h)-(60*m)
    print (s)

    if h<10:
        h="0{}".format(h)
    if m<10 :
        m = "0{}".format(m)
    if s<10:
        s = "0{}".format(s)

    end_time_len="{}:{}:{}".format(h,m,s)
    print(end_time_len)

    cmd="""ffmpeg -i "{}" -vcodec copy -acodec copy -ss {} -to {} "{}"  -y """.format(src_path,header_time_str,end_time_len,des_path)

    os.system(cmd)

    print(cmd)

if __name__ == '__main__':
    #todo 要裁剪的目录
    for root,paths,fnames in os.walk("/Volumes/TOSHIBA/[纪晓-岚4][42集][2009]"):
        #包含"head"的目录会被裁剪
        if re.search(r"head",root,re.I|re.M):
            #print (root,paths,fnames)
            root_str=os.path.split(root)
            #print(len(fnames))
            #exit(0)
            print (root_str)
            for p in fnames:
                s_path=os.path.join(root,p)
                print (s_path)
                e_path=os.path.join(root_str[1],p)
                print (e_path)
                if not os.path.exists(root_str[1]):
                    os.makedirs(root_str[1])
                #todo 保存文件在命令行所在目录，注意不要和视屏源在同一目录下避免被覆盖
                cut_movie(s_path,e_path)
                #exit(0)
