import React, { useState } from 'react'
import './index.less'

export default function WordCloud() {

    const [pic,setPic] = useState('')
    async function search(){

        const response = await fetch('http://127.0.0.1:5000/api/wordcloud',{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
            },
        }) 
        
        const res = response.json()
        res.then(
            data => {
                setPic('data:image/png;base64,'+data.data)
            }
        )
    }

    return (
        <>
            <div className='wordcloud-wrapper'>
                <div className='title'>词云图</div>
                <div className='btn' onClick={search}>获取词云图</div>
            </div>
            <a href={pic} download='wordcloud.png' className='img-box'>
                <img src={pic} alt="" />
            </a>
        </>
    )
}
