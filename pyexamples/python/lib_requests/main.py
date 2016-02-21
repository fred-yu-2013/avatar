# -*- coding: utf-8 -*-
from datetime import datetime
import requests


def to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)


def to_utf8(src):
    return src.encode('utf-8')


def example():
    """
    演示POST请求
    """
    headers = {
        'channelId': '9',
        'token': '',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'androidcgi.wepiao.com',
        'Connection': 'Keep-Alive',
        'User-Agent': '',
    }
    data = r'sign=C5B1FB98BBC44EA4D4BA964150300A93&v=2015110401&t=1450848769&cityId=82&imei=&appkey=9&from=0123456789&appver=5.3.0&deviceid=ffffffff-fdbe-bb2d-678d-815f0033c587'
    response = requests.post('http://androidcgi.wepiao.com/cinema/list', data=data, headers=headers)
    result = response.json()
    if result['ret'] != 0:
        print '获取影院列表失败'
        return
    cinemas = result['data']
    print '共获取影院{}家'.format(len(cinemas))
    for c in cinemas:
        print '{}: id/{}, tel/{}'.format(to_utf8(c['name']), c['id'], c['tele'])

    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

def example2():
    # cid = cinemas[0]['id']
    cid = '1001865'
    headers = {
        'channelId': '9',
        'token': '',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'androidcgi.wepiao.com',
        'Connection': 'Keep-Alive',
        'User-Agent': '',
    }
    # data = r'sign=1719416DD6ADB3A35FF385DF448C9088&v=2015110401&t=1450850711&cinemaId=#CINEMA_ID#&cityId=82&imei=&appkey=9&from=0123456789&appver=5.3.0&deviceid=ffffffff-fdbe-bb2d-678d-815f0033c587'
    # data = r'sign=BC77988B906547959A69FEB84C394690&v=2015110401&t=1450850711&cinemaId=#CINEMA_ID#&cityId=82&imei=&appkey=9&from=0123456789&appver=5.3.0&deviceid=ffffffff-fdbe-bb2d-678d-815f0033c587'
    # data = data.replace(r'#CINEMA_ID#', cid)
    data = r'sign=A10D35AEDE645E56AC05A40EF7BA78B8&v=2015110401&t=1450854941&cinemaId=1012109&cityId=82&imei=&appkey=9&from=0123456789&appver=5.3.0&deviceid=ffffffff-fdbe-bb2d-678d-815f0033c587'
    response = requests.post('http://androidcgi.wepiao.com/sche/cinema', data=data, headers=headers)
    result = response.json()
    if result['ret'] != 0:
        print '获取电影列表失败'
        return
    movies = result['data']
    print '共获取电影{}部'.format(len(movies))
    for m in movies:
        print '{}: id/{}'.format(to_utf8(m['name']), m['id'])

    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

    days = movies[0]['sche']
    for d in days:
        print '日期：{}'.format(d['date'])
        sessions = d['info'][0]['seat_info']
        for s in sessions:
            print '场次：{}-{}/{}/{}/{}'.format(to_datetime(s['start_unixtime']),
                                             to_datetime(s['end_unixtime']),
                                             to_utf8(s['roomname']),
                                             to_utf8(s['lagu']) + to_utf8(s['type']),
                                             float(s['price']))

if __name__ == '__main__':
    # example()
    example2()
