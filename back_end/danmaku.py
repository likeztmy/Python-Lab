import time
import requests
import google.protobuf.text_format as text_format
import my_pb2 as Danmaku


# 根据aid和cid爬取弹幕数据
# aid：视频稿件id ---> pid
# cid: 视频id ---> oid
def get_danmaku_info(aid, cid):
    url = "https://api.bilibili.com/x/v2/dm/web/seg.so"
    headers = {
        'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                      '113.0.0.0Safari / 537.36Edg / 113.0.1774.42 '
    }
    params = {
        'type': '1',  # 弹幕类型
        'oid': cid,   # 视频id
        'pid': aid,   # 视频稿件id
        'segment_index': '1',   # 弹幕数据分包
    }
    res = requests.get(url=url, params=params, headers=headers)
    content = res.content

    # 此处调用了rpc通信协议里的接口来反序列化处理弹幕数据
    danmaku_seg = Danmaku.DmSegMobileReply()
    danmaku_seg.ParseFromString(content)

    dataList = []

    for i in range(len(danmaku_seg.elems)):
        text = text_format.MessageToString(danmaku_seg.elems[i], as_utf8=True)
        text_arr = text.split('\n')
        data = {}
        for words in text_arr:
            if words == '':
                continue
            words_arr = words.split(': ')
            words_key = words_arr[0]
            words_value = words_arr[1]
            data[words_key] = words_value

        dataList.append(data)

    # for data in dataList:
    #     ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data['ctime'])))

    return dataList


# 将弹幕的字段设置成和数据库中的字段一致
def refactor_danmaku(aid, cid):
    danmaku_list = get_danmaku_info(aid, cid)
    new_danmaku_list = []
    for danmaku_item in danmaku_list:
        ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(danmaku_item['ctime'])))
        item = {
            'id': danmaku_item['id'],
            'content': danmaku_item['content'],
            'date': ctime
        }
        new_danmaku_list.append(item)

    return new_danmaku_list


# 设置id列表 用以写入数据库
def make_id_list(upMid, aid, cid):
    danmaku_list = get_danmaku_info(aid, cid)
    id_list = []
    for danmaku_item in danmaku_list:
        item = {
            'aid': aid,
            'cid': cid,
            'upMid': upMid,
            'userMid': danmaku_item['midHash'],
            'danmakuId': danmaku_item['id']
        }
        id_list.append(item)
    return id_list
