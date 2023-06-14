from sqlalchemy import Column, String, Integer, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

import danmaku
import search

login = 'root'
password = 'ccnuccnu'
host = '127.0.0.1'
port = '3306'

Base = declarative_base()


# 弹幕表
class Danmaku(Base):
    __tablename__ = 'danmaku'
    id = Column(String(20), primary_key=True, unique=True, comment='弹幕id')
    content = Column(String(200), comment='弹幕内容')
    date = Column(DateTime, comment='弹幕发布时间')

    def __repr__(self):
        return f"Danmaku(id={self.id}, content={self.content}, date={self.date})"


# 视频表
class Video(Base):
    __tablename__ = 'video'
    mid = Column(Integer, comment='视频创作者id')
    aid = Column(Integer, primary_key=True, unique=True, comment='稿件id')
    cid = Column(Integer, primary_key=True, unique=True, comment='视频id')
    season_id = Column(Integer, primary_key=True, unique=True, comment='剧集id')
    tname = Column(String(20), comment='视频类型')
    title = Column(String(40), comment='视频标题')
    desc = Column(String(400), comment='简介')
    duration = Column(Integer, comment='视频时长')
    view = Column(Integer, comment='观看数量')
    danmaku = Column(Integer, comment='弹幕数量')
    reply = Column(Integer, comment='评论数量')
    favorite = Column(Integer, comment='收藏数量')
    coin = Column(Integer, comment='投币数量')
    share = Column(Integer, comment='转发数量')
    like = Column(Integer, comment='点赞数量')
    achievement = Column(String(100), comment='视频亮点')

    def __repr__(self):
        return f"Video(mid={self.mid},aid={self.aid},cid={self.cid}, season_id={self.season_id}, tname={self.tname}, " \
               f"title={self.title}, desc={self.desc}, duration={self.duration}, view={self.view}, danmaku={self.danmaku}, " \
               f"reply={self.reply}, favorite={self.favorite}, coin={self.coin}, share={self.share}, like={self.like})"


# 索引表
class Reference(Base):
    __tablename__ = 'reference'
    aid = Column(Integer, comment='稿件id')
    cid = Column(Integer, comment='视频id')
    upMid = Column(Integer, comment='视频创作者id')
    userMid = Column(String(20), comment='弹幕发布者id(加密后)')
    danmakuId = Column(String(20), primary_key=True, unique=True, comment='弹幕id')

    def __repr__(self):
        return f"Reference(aid={self.aid}, cid={self.cid}, upMid={self.upMid}, userMid={self.userMid}, danmakuId={self.danmakuId})"


# 创建表
def create_table():
    engine = create_engine(f'mysql+mysqlconnector://{login}:{password}@{host}:{port}/bilibili?auth_plugin'
                           f'=mysql_native_password', echo=True)
    Base.metadata.create_all(engine)


# 查看数据库中是否已有弹幕数据
def is_save(aid):
    engine = create_engine(f'mysql+mysqlconnector://{login}:{password}@{host}:{port}/bilibili?auth_plugin'
                           f'=mysql_native_password&charset=utf8mb4', echo=True)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    result = session.query(Reference).filter_by(aid=aid).first()
    if result:
        return True
    else:
        return False


# 保存数据到索引表中
def save_reference_info(referenceList):
    engine = create_engine(f'mysql+mysqlconnector://{login}:{password}@{host}:{port}/bilibili?auth_plugin'
                           f'=mysql_native_password&charset=utf8mb4', echo=True)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for reference in referenceList:
        reference_info = Reference(
            aid=reference['aid'],
            cid=reference['cid'],
            upMid=reference['upMid'],
            userMid=reference['userMid'],
            danmakuId=reference['danmakuId']
        )
        session.add(reference_info)
        session.commit()


# 保存数据到弹幕表中
def save_danmaku_info(danmaku):
    engine = create_engine(f'mysql+mysqlconnector://{login}:{password}@{host}:{port}/bilibili?auth_plugin'
                           f'=mysql_native_password', echo=True)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    danmaku_info = Danmaku(id=danmaku['id'], content=danmaku['content'], date=danmaku['date'])
    session.add(danmaku_info)
    session.commit()


# 保存数据到视频表中
def save_video_info(videoList):
    engine = create_engine(f'mysql+mysqlconnector://{login}:{password}@{host}:{port}/bilibili?auth_plugin'
                           f'=mysql_native_password&charset=utf8mb4', echo=True)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for video in videoList:
        video_info = Video(
            mid=video['mid'],
            aid=video['aid'],
            cid=video['cid'],
            tname=video['tname'],
            title=video['title'],
            desc=video['desc'],
            duration=video['duration'],
            view=video['view'],
            danmaku=video['danmaku'],
            reply=video['reply'],
            favorite=video['favorite'],
            coin=video['coin'],
            share=video['share'],
            like=video['like'],
            achievement=video['achievement']
        )
        session.add(video_info)
        session.commit()


# 排序弹幕数据并返回
def rank_danmaku():
    engine = create_engine(f'mysql+mysqlconnector://{login}:{password}@{host}:{port}/bilibili?auth_plugin'
                           f'=mysql_native_password&charset=utf8mb4', echo=True)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    danmakuList = session.query(Danmaku.content, func.count(Danmaku.content)). \
        group_by(Danmaku.content). \
        order_by(func.count(Danmaku.content).desc()). \
        limit(100). \
        all()
    session.commit()
    return danmakuList


# 每次使用弹幕爬取功能时都会保存弹幕数据到数据库中
def save(video):

    # 根据视频名调用搜索方法进行爬虫
    search_info = search.get_search_info(video)

    # 保存搜索结果的第一个视频
    search_result = search_info[0]

    # 根据搜索结果中的视频稿件aid获取视频cid
    aid = search_result['id']
    cid = search.get_cid(aid)
    if is_save(aid):

        # 将弹幕数据的字段处理为与数据库中弹幕数据的字段一致
        new_danmaku_list = danmaku.refactor_danmaku(aid, cid)

        # 制作索引表数据，之后用于存入数据库
        id_list = danmaku.make_id_list(search_info[0]['mid'], aid, cid)

        # 制作视频信息数据，之后用于存入数据库
        video_info = video.get_video_info(aid)
        video_list = [{
            'mid': video_info['owner']['mid'],
            'aid': video_info['aid'],
            'cid': video_info['cid'],
            'tname': video_info['tname'],
            'title': video_info['title'],
            'desc': video_info['desc'],
            'duration': video_info['duration'],
            'view': video_info['stat']['view'],
            'danmaku': video_info['stat']['danmaku'],
            'reply': video_info['stat']['reply'],
            'favorite': video_info['stat']['favorite'],
            'coin': video_info['stat']['coin'],
            'share': video_info['stat']['share'],
            'like': video_info['stat']['like'],
            'achievement': '无'
        }]

        save_video_info(video_list)
        save_danmaku_info(new_danmaku_list)
        save_reference_info(id_list)

