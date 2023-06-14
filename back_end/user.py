import time

import requests
from functools import reduce
from hashlib import md5
import urllib.parse

CRCPOLYNOMIAL = 0xEDB88320
crctable = [0 for x in range(256)]


def create_table():
    for i in range(256):
        crcreg = i
        for _ in range(8):
            if (crcreg & 1) != 0:
                crcreg = CRCPOLYNOMIAL ^ (crcreg >> 1)
            else:
                crcreg = crcreg >> 1
        crctable[i] = crcreg


def crc32(string):
    crcstart = 0xFFFFFFFF
    for i in range(len(str(string))):
        index = (crcstart ^ ord(str(string)[i])) & 255
        crcstart = (crcstart >> 8) ^ crctable[index]
    return crcstart


def crc32_last_index(string):
    crcstart = 0xFFFFFFFF
    for i in range(len(str(string))):
        index = (crcstart ^ ord(str(string)[i])) & 255
        crcstart = (crcstart >> 8) ^ crctable[index]
    return index


def get_crc_index(t):
    for i in range(256):
        if crctable[i] >> 24 == t:
            return i
    return -1


def deep_check(i, index):
    string = ""
    tc = 0x00
    hashcode = crc32(i)
    tc = hashcode & 0xff ^ index[2]
    if not (57 >= tc >= 48):
        return [0]
    string += str(tc - 48)
    hashcode = crctable[index[2]] ^ (hashcode >> 8)
    tc = hashcode & 0xff ^ index[1]
    if not (57 >= tc >= 48):
        return [0]
    string += str(tc - 48)
    hashcode = crctable[index[1]] ^ (hashcode >> 8)
    tc = hashcode & 0xff ^ index[0]
    if not (57 >= tc >= 48):
        return [0]
    string += str(tc - 48)
    return [1, string]


def decipher(mid_hash):
    create_table()
    index = [0 for x in range(4)]
    i = 0
    # print(f"0x{mid_hash}")
    ht = int(f"0x{mid_hash}", 16) ^ 0xffffffff
    for i in range(3, -1, -1):
        index[3 - i] = get_crc_index(ht >> (i * 8))
        snum = crctable[index[3 - i]]
        ht ^= snum >> ((3 - i) * 8)
    for i in range(100000000):
        lastindex = crc32_last_index(i)
        if lastindex == index[3]:
            deepCheckData = deep_check(i, index)
            if deepCheckData[0]:
                break
    if i == 100000000:
        return -1
    return f"{i}{deepCheckData[1]}"


# 旧的用户信息接口，鉴权方式为Cookie，缺点是需要经常手动更新Cookie
def get_user(mid: int):
    print(mid)
    url = 'https://api.bilibili.com/x/space/acc/info'
    header = {
        "authority": "api.bilibili.com",
        'Cookie': "buvid3=A95424E4-A244-60D5-0F09-5BCC7A9790D107525infoc; b_nut=1686101107; b_lsid=5CF2A16F_18893752311; _uuid=8F76F254-74B5-794E-6C7F-7FCE2F2A10ACE07486infoc",
        'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                      '110.0.0.0Safari / 537.36Edg / 110.0.1587.57 '
    }
    params = {
                 'mid': mid,
             },
    res = requests.get(url, params=params, headers=header)
    content = res.json()
    print(content)
    return content['data']


# 此处为破解wbi鉴权的方法，该demo来源于 https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/sign/wbi.md
mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]


def getMixinKey(orig: str):
    '对 imgKey 和 subKey 进行字符顺序打乱编码'
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]


def encWbi(params: dict, img_key: str, sub_key: str):
    '为请求参数进行 wbi 签名'
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time  # 添加 wts 字段
    params = dict(sorted(params.items()))  # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v
        in params.items()
    }
    query = urllib.parse.urlencode(params)  # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
    params['w_rid'] = wbi_sign
    return params


def getWbiKeys() -> tuple[str, str]:
    '获取最新的 img_key 和 sub_key'
    resp = requests.get('https://api.bilibili.com/x/web-interface/nav')
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content['data']['wbi_img']['img_url']
    sub_url: str = json_content['data']['wbi_img']['sub_url']
    img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    return img_key, sub_key


# 目前b站使用的用户信息接口
def get_user_wbi(mid: int):
    img_key, sub_key = getWbiKeys()

    signed_params = encWbi(
        params={
            'mid': mid,
            'token': '',
            'platform': 'web',
            'web_location': '1550101',
        },
        img_key=img_key,
        sub_key=sub_key
    )

    query = urllib.parse.urlencode(signed_params)
    # print(signed_params)
    # print('https://api.bilibili.com/x/space/wbi/acc/info?' + query)

    url = 'https://api.bilibili.com/x/space/wbi/acc/info?' + query
    header = {
        "authority": "api.bilibili.com",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 '
                      'Safari/537.36 Edg/113.0.1774.50',
    }

    res = requests.get(url, headers=header)
    content = res.json()
    return {
        'mid': content['data']['mid'],
        'name': content['data']['name'],
        'sex': content['data']['sex'],
        'level': content['data']['level'],
        'sign': content['data']['sign'],
    }


def make_user_list(id_list):
    user_list = []
    for userId in id_list:
        user_info = get_user(userId)
        item = {
            'mid': user_info['data']['mid'],
            'name': user_info['data']['name'],
            'sex': user_info['data']['sex'],
            'level': user_info['data']['level'],
            'sign': user_info['data']['sign'],
        }
        user_list.append(item)

    return user_list
