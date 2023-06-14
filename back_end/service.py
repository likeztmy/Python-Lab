from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import search
import danmaku
import user
import sql
from openpyxl import Workbook
import wordcloud
from PIL import Image
import numpy
from matplotlib import pyplot
from nltk import FreqDist
import base64

app = Flask(__name__)
cors = CORS(app)


# 弹幕解析功能接口
@app.route('/api/decipher', methods=['POST'])
def decipher_danmaku():
    req = request.json
    # print(req)
    # 获取前端的请求参数 视频名 弹幕内容
    video_name = req['video']
    danmaku_content = req['danmaku']

    # 根据视频名调用搜索方法进行爬虫
    search_info = search.get_search_info(video_name)

    # 保存搜索结果的第一个视频
    search_result = search_info[0]

    # 根据搜索结果中的视频稿件aid获取视频cid
    aid = search_result['id']
    cid = search.get_cid(aid)

    # 根据视频稿件aid和视频cid获取弹幕数据
    danmaku_list = danmaku.get_danmaku_info(aid, cid)

    # 遍历弹幕数据，查找目标弹幕内容，若找到则保存目标弹幕的midHash字段
    midHash = ''
    for danmaku_item in danmaku_list:
        if danmaku_item['content'].replace('"', '') == danmaku_content:
            midHash = danmaku_item['midHash'].replace('"', '')
            break

    # 调用decipher函数，解析midHash得到mid
    mid = user.decipher(midHash)
    # print(mid)

    # 调用get_user方法 获取用户信息
    user_info = user.get_user_wbi(mid)

    # 将用户信息返回给前端
    data = {'user': user_info}
    return jsonify(data)


# 弹幕爬取功能接口
@app.route('/api/download', methods=['POST'])
def download_danmaku():
    req = request.json

    # 获取前端的请求参数 视频名
    video_name = req['video']

    # sql.save(video=video_name)

    # 根据视频名调用搜索方法进行爬虫
    search_info = search.get_search_info(video_name)

    # 保存搜索结果的第一个视频
    search_result = search_info[0]

    # 根据搜索结果中的视频稿件aid获取视频cid
    aid = search_result['id']
    cid = search.get_cid(aid)

    # 根据视频稿件aid和视频cid爬取弹幕数据
    danmaku_list = danmaku.get_danmaku_info(aid, cid)

    # 创建excel表格的字段数组
    columns = ['id', 'progress', 'mode', 'fontsize', 'color', 'midHash', 'content', 'ctime', 'weight', 'idStr']

    # data数组用于存放弹幕数据所有字段的信息，datas数组存放所有data
    datas = []
    for danmaku_item in danmaku_list:
        data = []
        for value in danmaku_item.values():
            data.append(value)

        datas.append(data)

    # 将弹幕数据制作成excel表格
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = '弹幕'
    sheet.append(columns)
    for data in datas:
        sheet.append(data)

    workbook.save('弹幕.xlsx')

    # 以二进制流读取并返回给前端
    fileContent = open('./弹幕.xlsx', 'rb').read()
    return Response(fileContent, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    headers={"Content-Disposition": 'attachment;filename=danmaku.xlsx'})


# 词云图绘制接口
@app.route('/api/wordcloud', methods=['GET'])
def draw_wordcloud():
    # 从数据库中获取排序好的弹幕数据
    danmaku_list = sql.rank_danmaku()

    # 将弹幕数据处理为字典的形式
    # {弹幕内容：数量}
    danmakuDict = {}
    for danmaku_item in danmaku_list:
        danmakuDict[danmaku_item[0]] = danmaku_item[1]

    font = 'font.otf'

    # 获取词云图背景图片，并将图片转换为矩阵
    img = Image.open("background.png")
    mask = numpy.array(img)

    # 调用wordcloud库中的WordCloud函数和nltk库中的FreqDist函数
    # 将danmakuDict绘制成词云图
    wc = wordcloud.WordCloud(
        font_path=font,
        mask=mask,
        width=2000,
        height=1000,
        background_color='white',
    ).fit_words(FreqDist(danmakuDict))

    pyplot.imshow(wc, interpolation='bilinear')
    pyplot.axis("off")
    wc.to_file('wordcloud.png')
    pic = open("wordcloud.png", 'rb')

    # 图片采用base64编码并且转为字符串
    pic_base64 = base64.b64encode(pic.read()).decode('utf-8')
    pic.close()
    data = {
        'data': pic_base64
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
