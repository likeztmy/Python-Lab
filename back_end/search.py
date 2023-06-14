import requests


# 获取视频cid
def get_cid(aid):
    url = f'https://api.bilibili.com/x/player/pagelist?aid={aid}'
    headers = {
        'Cookie': "buvid3=F9B2E6C3-B5C3-6626-34F3-566131DB71F480758infoc; i-wanna-go-back=-1; _uuid=D108F4535-105B6-5CE7-2CC9-C8279F13248179715infoc; header_theme_version=CLOSE; buvid_fp_plain=undefined; rpdid=|(JY~|lk~~)m0J'uY)J~|kR)~; nostalgia_conf=-1; CURRENT_BLACKGAP=0; CURRENT_PID=efad4e40-f2dd-11ed-8e03-b7945e8c6a89; ogvEpOrder=2; selectedMode=false; bp_video_offset_499737426=798884550339985400; DedeUserID=3494349608323701; DedeUserID__ckMd5=c9b1de12b87b94e6; b_ut=5; FEED_LIVE_VERSION=V_LIVE_2; bp_t_offset_3494349608323701=9223372036854775807; fingerprint=c3fd402c79993327a442c0c29f53bea5; buvid_fp=c3fd402c79993327a442c0c29f53bea5; SESSDATA=56cc125a%2C1701585459%2C51e5f%2A61; bili_jct=608a0bfcdcd44e06613be3b9af535bae; sid=6n5vd9m3; PVID=2; innersign=0; b_lsid=AD68CAA10_188900A27B5; b_nut=1686043766; home_feed_column=4; browser_resolution=427-754; CURRENT_FNVAL=16; buvid4=CF800290-6B98-377E-6725-05C7915B51A885562-023050521-sc6TKcUNTk5LUiIz3D1bkw%3D%3D",
        'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                      '110.0.0.0Safari / 537.36Edg / 110.0.1587.57 '
    }
    res = requests.get(url=url, headers=headers)
    content = res.json()
    return content['data'][0]['cid']


# 调用搜索接口，获取视频信息
def get_search_info(keyword):
    url = 'https://api.bilibili.com/x/web-interface/wbi/search/all/v2'
    params = {
        'keyword': keyword,
    }
    headers = {
        'Cookie': "buvid3=F9B2E6C3-B5C3-6626-34F3-566131DB71F480758infoc; i-wanna-go-back=-1; _uuid=D108F4535-105B6-5CE7-2CC9-C8279F13248179715infoc; header_theme_version=CLOSE; buvid_fp_plain=undefined; rpdid=|(JY~|lk~~)m0J'uY)J~|kR)~; nostalgia_conf=-1; CURRENT_BLACKGAP=0; CURRENT_PID=efad4e40-f2dd-11ed-8e03-b7945e8c6a89; ogvEpOrder=2; selectedMode=false; bp_video_offset_499737426=798884550339985400; DedeUserID=3494349608323701; DedeUserID__ckMd5=c9b1de12b87b94e6; b_ut=5; FEED_LIVE_VERSION=V_LIVE_2; bp_t_offset_3494349608323701=9223372036854775807; fingerprint=c3fd402c79993327a442c0c29f53bea5; buvid_fp=c3fd402c79993327a442c0c29f53bea5; SESSDATA=56cc125a%2C1701585459%2C51e5f%2A61; bili_jct=608a0bfcdcd44e06613be3b9af535bae; sid=6n5vd9m3; PVID=2; innersign=0; b_lsid=AD68CAA10_188900A27B5; b_nut=1686043766; home_feed_column=4; browser_resolution=427-754; CURRENT_FNVAL=16; buvid4=CF800290-6B98-377E-6725-05C7915B51A885562-023050521-sc6TKcUNTk5LUiIz3D1bkw%3D%3D",
        'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                      '110.0.0.0Safari / 537.36Edg / 110.0.1587.57 '
    }
    res = requests.get(url=url, params=params, headers=headers)
    content = res.json()
    return content['data']['result'][11]['data']
