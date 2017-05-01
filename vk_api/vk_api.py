import requests
import json
import re
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from collections import Counter

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)


group_info = vk_api('groups.getById', group_id='vk_moscow', v='5.63')
group_id = group_info['response'][0]['id']


posts = []
item_count = 200
result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100)
posts += result["response"]["items"]
while len(posts) < item_count:
    result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100, offset=len(posts))
    posts += result['response']["items"]


def comm_get(post, n):
    #comments = []
    comm_info = []
    result = vk_api('wall.getComments', owner_id=-group_id, post_id=post, v='5.63', count=100)
    comm_info += result["response"]['items']
    #comm_info += result['response']['profiles']['bdate']
    #comm_info += result['response']['profiles']['city']
    #comments += comm_info
    if n > 100:
        while len(comm_info) < n:
            result = vk_api('wall.getComments', owner_id=-group_id, post_id=post, v='5.63', count=100, offset=len(comm_info))
            comm_info += result['response']["items"]
            #comm_info += result['response']['profiles']['bdate']
            #comm_info += result['response']['profiles']['city']
            #comments += comm_info
    return comm_info#comments


def write_file(item, item_type):
    with open('InteresnayaMoskva.txt', 'a', encoding='UTF-8') as f:
        f.write(item_type + item)#cleaned(p))
        #for c in cs:
         #   f.write('\n<comment_text>\n' + cleaned(c))


def len_count(item):
    text = item['text']
    reg = re.compile('[^а-яёА-ЯЁ0-9a-zA-Z]+', flags=re.U | re.DOTALL)
    text = re.sub(reg, ' ', text)
    words = text.split(' ')
    item_len = len(words)
    return item_len


gr1_data = {}
gr2_data = []

for post in posts:
    postlen = len_count(post)
    comm_n = post['comments']['count']
    post_id = post['id']
    comment_info = comm_get(post_id, comm_n)
    #print('yobanny rot', comment_info)
    write_file(post['text'], '\n<post_text>\n')
    if postlen not in gr1_data:
        gr1_data[postlen] = []
    for item in comment_info:  # , bdate, city in comment_info:

        #for el in item.items():
         #   print('blya', el)
        ###comment_proccess(comment)
            #if len(el) >= 4:
               # print('pizdato')
        commlen = len_count(item)

        if item['text'] != '':
            write_file(item['text'], '\n<comment_text>\n')

        gr1_data[postlen].append(commlen)
                #gr2_data += [commlen, bdate, city]
            #else:

              #  continue


