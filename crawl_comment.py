import requests
import datetime
import os
import json

# s='t3_sk6yh'
# ss = s.split('_')
# print(ss[-1])

# s = 'pet loss'
# dic = {'a':'',
#        'b':[{'source':{"url":'target'}}]}
# dic['tag'] = ['1','2']
# print(dic['tag'])
# if 'tag' in dic:
#     print('y')
# print(dic['a'])
# print(dic['b'][0]['source']['url'])


# 可以使用Python的os和json模块来实现。首先，使用os模块中的listdir函数获取文件夹下所有文件的文件名列表，
# 然后遍历列表，对于每个文件名，使用json模块中的load函数读取json文件内容。以下是示例代码：

#帖子回复总数量52565
#comment_count:40214
#reply_count:12351
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}
num_sub_per = 1000
# comment_count = 0

# def getPushshiftData(before, sub, mode, count):
#     url = 'https://api.pushshift.io/reddit/'+mode+'/search/?'+'&size='+str(num_sub_per)+'&before='+str(before)+'&subreddit='+str(sub)
#     with requests.get(url,verify=False,headers=headers) as r:
#         # try:
#         r = requests.get(url)
#         data = json.loads(r.text)
#         data = data['data']
#         comment_list = []
#         for i in data:
#
#             dic={}
#             s = i['link_id'].split('_')
#             link_id = s[-1]
#             dd = {}
#             dd[link_id] = i['author']
#             if ('is_submitter' in i and i['is_submitter']) and (dd in id_author_list):
#                 dic['type'] = 'reply'
#             elif link_id in id_list:
#                 dic['type'] = 'comment'
#             else:
#                 continue
#             dic['author'] = i['author']
#             dic['text'] = i['body']
#             dic['parent_id'] = link_id
#             dic['comment_id'] = i['id']
#             dic['created_utc'] = i['created_utc']
#             dic['score'] = i['score']
#             try:
#                 dic['no_follow'] = i['no_follow']
#             except:
#                 dic['no_follow'] = 'None'
#             comment_list.append(dic)
#
#         sub_file_name = './data/comment/' + str(count) + '_' + mode + '_' + str(before) + '.json'
#
#         with open(sub_file_name, "w") as write_file:
#             json.dump(comment_list, write_file)
#             # time.sleep(2)
#         # except:
#         #     print("An exception occurred")
#         #     pass
#         return comment_list


folder_path = "data/total_posts"
id_list = []
id_author_list = []
image_count = 0
gallery_count = 0
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r") as f:
            json_data = json.load(f)
            for item in json_data:
                if item['type'] == 'image' or item['type'] == 'gallery':
                    id_list.append(item['id'])
                    d = {}
                    d[item['id']] = item['author']
                    id_author_list.append(d)
                if item['type'] == 'image':
                    image_count+=1
                if item['type'] == 'gallery':
                    gallery_count+=len(item['image_url'])

folder_path = "data/comment"

reply_count = 0
comment_count = 0

for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        comment_list = []
        file_path = os.path.join(folder_path, filename)
        print(file_path)
        with open(file_path, "r") as f:
            json_data = json.load(f)
            for item in json_data:
                id_author = {item['parent_id']:item['author']}
                if id_author in id_author_list:
                    item['type'] = 'reply'
                    reply_count += 1
                    comment_list.append(item)
                elif item['parent_id'] in id_list:
                    item['type'] = 'comment'
                    comment_count += 1
                    comment_list.append(item)
        # f.close()
        # with open(file_path,'w') as f:
        #     json.dump(comment_list,f)
        # f.close()


# sub_reddit = 'GriefSupport'
# before = '1462075200' # 过程 2016-05-1 12:00:00 (utc)  起始2023-05-01 12:00:00am (UTC)
# after = "1447508535" # 2016-05-1 12:00:00am (UTC)
# count = 0
# data = getPushshiftData(before, sub_reddit, 'comment', count)
# print("评论数量：" + str(len(data)))
# try: #如果抓取的列表为空，最早时间减10天，减少天数视情况而定
#     earliest_time = data[-1]['created_utc']
# except:
#     earliest_time = int(before)-864000
# submission_count = comment_count + len(data)
# print('The 0 iteration of {} comments, the earliest time: {} (utc).'.format(len(data), datetime.datetime.fromtimestamp(earliest_time)))
# print('total {} comments'.format(submission_count))
#
# while True:
#     count = count + 1
#     # try:
#     data = getPushshiftData(earliest_time, sub_reddit, 'comment', count)
#     print("评论数量：" + str(len(data)))
#     try:
#         earliest_time = data[-1]['created_utc']
#     except:
#         earliest_time = earliest_time - 864000
#     if earliest_time < int(after):
#         break
#     submission_count = submission_count + len(data)
#     print('The {} iteration of {} comments, the earliest time is {} (utc).'.format(count, len(data), datetime.datetime.fromtimestamp(earliest_time)))
#     print('total {} comments'.format(submission_count))


print(id_list)
print(len(id_list))
print('image_count:'+ str(image_count))
print('gallery_count:'+ str(gallery_count))
# 对json数据进行处理，例如打印或保存到数据库等
# print(len(comment_list))
# print('comment_count:'+str(comment_count))
# print('reply_count:'+str(reply_count))
# with open('reply_comment.json','w') as f:
#     json.dump(comment_list,f)
