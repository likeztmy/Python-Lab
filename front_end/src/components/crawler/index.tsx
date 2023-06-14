import React, { useState } from 'react'
import './index.less'
import { message } from 'antd'

export default function Crawler() {
    
    const [video,setVideo] = useState('')

    async function search(){

        const data = {
            'video': video,
        }

        const response = await fetch('http://127.0.0.1:5000/api/download',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
            },
            body: JSON.stringify(data)
        }) 
        const res = response.blob()
        res.then(
            data => {
                message.success('爬取成功')
                const downloadURL = window.URL.createObjectURL(data)
                console.log(downloadURL)
                const a = document.createElement('a')
                a.style.display =  'none';
                a.href = downloadURL
                a.download = video+'弹幕'
                document.body.appendChild(a)
                a.click()
            }
        )
    }


    return (
        <div className='crawler-wrapper'>
            <div className='title'>弹幕爬取</div>
            <div className='form'>
                <div className='box'>
                    <div>视频名</div>
                    <input type="text" value={video} onChange={(e) => setVideo(e.target.value)} className='input-box' placeholder='视频名' />
                </div>
                <div className='btn' onClick={search}>爬取弹幕</div>
            </div>
        </div>
    )
}
