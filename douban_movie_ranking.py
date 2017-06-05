#-*-coding:utf-8-*-
import requests
from urllib.parse import urlencode
import pymysql.cursors
from pymysql.err import IntegrityError
import time
import random

#https://movie.douban.com/j/chart/top_list_count?type=11&interval_id=100%3A90
#https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=0&limit=20

connection = pymysql.connect(host='localhost',
                             user='',
                             password='',
                             db='',
                             port=3306,
                             charset='utf8')

dict_type = {
    '纪录片':1,
    '传记':2,
    '犯罪':3,
    '历史':4,
    '动作':5,
    '情色':6,
    '歌舞':7,
    '儿童':8,
    '悬疑':10,
    '剧情':11,
    '灾难':12,
    '爱情':13,
    '音乐':14,
    '冒险':15,
    '奇幻':16,
    '科幻':17,
    '运动':18,
    '惊悚':19,
    '恐怖':20,
    '战争':22,
    '短片':23,
    '喜剧':24,
    '动画':25,
    '同性':26,
    '西部':27,
    '家庭':28,
    '武侠':29,
    '古装':30,
    '黑色电影':31
}

headers = {
    'Connection':'keep-alive',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Host':'movie.douban.com'
}


def get_list_count(type_num,interval_num):
    url_count_head = 'https://movie.douban.com/j/chart/top_list_count?'
    data = {
        'type':type_num,
        'interval_id':str(interval_num) + ':' + str(interval_num - 10)
    }
    url_list_count = url_count_head + urlencode(data)
    request = requests.get(url_list_count,headers=headers)
    list_count = request.json()['total']
    return list_count

def get_list_content(type_num,interval_num,list_count):
    url_list_head = 'https://movie.douban.com/j/chart/top_list?'
    data = {
        'type':type_num,
        'interval_id':str(interval_num) + ':' + str(interval_num - 10),
        'action':'',
        'start':0,
        'limit':list_count
    }
    url_list_content = url_list_head + urlencode(data)
    request = requests.get(url_list_content,headers=headers)
    list_content = request.json()
    return list_content

for type_name, type_num in dict_type.items():
    for interval_num in range(100,0,-10):
        list_count = get_list_count(type_num,interval_num)
        list_content = get_list_content(type_num,interval_num,list_count)
        for each in list_content:
            rank = int(each['rank'])
            _id = int(each['id'])
            title = each['title']
            score = float(each['score'])
            vote_count = int(each['vote_count'])
            types = '，'.join(each['types'])
            regions = '，'.join(each['regions'])
            release_date = each['release_date']
            cover_url = each['cover_url']
            url = each['url']
            actor_count = int(each['actor_count'])
            actors = '，'.join(each['actors'])
            try:
                with connection.cursor() as cursor:
                    sql="INSERT INTO `douban_movie_top_list` (`type_name`,`rank`,`id`,`title`,`score`,`vote_count`,`typess`,`regions`,`release_date`,`cover_url`,`url`,`actor_count`,`actors`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (type_name,rank,_id,title,score,vote_count,types,regions,release_date,cover_url,url,actor_count,actors))
                    connection.commit()
            except IntegrityError as e:
                print(e,_id)
        time.sleep(random.uniform(4,6))
    time.sleep(60)
connection.close()    




