import React, { useState } from 'react'
import './index.less'

export default function Decipher() {
    const [user,setUser] = useState(null)
    const [video,setVideo] = useState('')
    const [danmaku,setDanmaku] = useState<any>('')

    async function search(){

        const data = {
            'video': video,
            'danmaku': danmaku
        }

        const response = await fetch('http://127.0.0.1:5000/api/decipher',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
            },
            body: JSON.stringify(data)
        }) 

        const res = response.json()
        res.then(
            data => {
                setUser(data.user)
            }
        )
    }


    return (
        <div className='decipher-wrapper'>
            <div className='title'>弹幕解析</div>
            <div className='form'>
                <div className='box'>
                    <div>视频名</div>
                    <input type="text" value={video} onChange={(e) => setVideo(e.target.value)} className='input-box' placeholder='视频名' />
                </div>
                <div className='box'>
                    <div>弹幕内容</div>
                    <input type='text' value={danmaku} onChange={(e) => setDanmaku(e.target.value)} className='input-box' placeholder='弹幕内容' />
                </div>
                <div className='btn' onClick={search}>查询用户</div>
            </div>
            {
                user &&      
                <div className='info'>
                    <div className='user-name'>
                        <div className='title'>用户名:</div>
                        <div className='name'>{user['name']}</div>
                    </div>
                    <div className='user-home'>
                        <div className='title'>空间:</div>
                        <a href={`https://space.bilibili.com/${user['mid']}`}>{`https://space.bilibili.com/${user['mid']}`}</a>
                    </div>
                </div>
            }
        </div>
    )
}
