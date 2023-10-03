# -- coding: utf-8 --
import random
import urllib
import pandas as pd
import requests
import json
import csv
import time
import datetime

from requests_toolbelt import SSLAdapter


# adapter = SSLAdapter('TLSv1')
# s = requests.Session()
# s.mount('https://', adapter)

#总共带有评论的图片5340张
#单图的数量是3037
#多图的数量是673

headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
num_sub_per = 1000
submission_count = 38570
image_count = 5340
fp = open('ip.txt','r')
res = fp.read()
ip_list = res.split('\n')

def getPushshiftData(before, sub, mode, count, image_count):
    url = 'https://api.pushshift.io/reddit/'+mode+'/search/?'+'&size='+str(num_sub_per)+'&before='+str(before)+'&subreddit='+str(sub)
    with requests.get(url,verify=False,headers=headers) as r:
        # try:
        r = requests.get(url)
        data = json.loads(r.text)
        data = data['data']
        post_list = []
        for i in data:

            dic={}
            if i['num_comments'] == 0: #过滤掉没有评论的
                continue
            if i['author'] == "[deleted]": #过滤掉删除的
                continue
            if 'is_gallery' in i and i['is_gallery']: #多图的情况
                dic['type'] = 'gallery'
                gallery_url_list = []
                try:
                    for g in i['media_metadata']:
                        print(g)
                        image_url = 'https://i.redd.it/' + g + '.jpg'
                        gallery_url_list.append(image_url)
                        image_count += 1
                    dic['image_url'] = gallery_url_list
                except:
                    print("a post have been deleted")
                    continue
            elif 'post_hint' in i and (i['post_hint'] == 'image'): #单图的情况
                print("一张图片已被抓取")
                dic['type'] = 'image'
                dic['image_url'] = i['url']
                image_count += 1
            else: #剩余即是文本情况
                dic['type'] = 'text'
            dic['author'] = i['author']
            try:
                dic['author_fullname'] = i['author_fullname']
            except:
                dic['author_fullname'] = 'None'
            dic['created_utc'] = i['created_utc']
            dic['id'] = i['id']
            try:
                dic['link_flair_text'] = i['link_flair_text']
            except:
                dic['link_flair_text'] = 'no_tag'
            dic['num_comments'] = i['num_comments']
            dic['score'] = i['score']
            try:
                dic['upvote_ratio'] = i['upvote_ratio']
            except:
                dic['upvote_ratio'] = 'None'
            try:
                dic['title'] = i['title']
            except:
                dic['title'] = ''
            try:
                dic['selftext'] = i['selftext']
            except:
                dic['selftext'] = ''
            try:
                dic['send_replies'] = i['send_replies']
            except:
                dic['send_replies'] = 'None'
            post_list.append(dic)

        sub_file_name = './data/total_posts/' + str(count) + '_' + mode + '_' + str(before) + '.json'

        with open(sub_file_name, "w") as write_file:
            json.dump(post_list, write_file)
            # time.sleep(2)
        # except:
        #     print("An exception occurred")
        #     pass
        return post_list,image_count

sub_reddit = 'GriefSupport'
before = '1492622615' # 过程 2017-04-20 01:23:35 (utc)  起始2023-05-01 12:00:00am (UTC)
after = "1462075200" # 2016-05-1 12:00:00am (UTC)
count = 68
data,image_count = getPushshiftData(before, sub_reddit, 'submission', count,image_count)
print("图片数量：" + str(image_count))
print(len(data))
earliest_time = data[-1]['created_utc']
submission_count = submission_count + len(data)
print('The 68 iteration of {} submissions, the earliest time: {} (utc).'.format(len(data), datetime.datetime.fromtimestamp(earliest_time)))
print('total {} submissions'.format(submission_count))

while True:
    count = count + 1
    # try:
    data,image_count = getPushshiftData(earliest_time, sub_reddit, 'submission', count,image_count)
    print("图片数量：" + str(image_count))
    earliest_time = data[-1]['created_utc']
    if earliest_time < int(after):
        break
    submission_count = submission_count + len(data)
    print('The {} iteration of {} submissions, the earliest time is {} (utc).'.format(count, len(data), datetime.datetime.fromtimestamp(earliest_time)))
    print('total {} submissions'.format(submission_count))
    # except:
    #     print("An exception occurred")
    #     continue


# summary = {
#     'total_submission': submission_count,
#     'total_comment': comment_count,
#     'earliest_time': earliest_time,
#     'latest_time': before
# }
#
# with open('summary_anxiety.json', "w") as write_file:
#         json.dump(summary, write_file)
#
# print('Finished!')