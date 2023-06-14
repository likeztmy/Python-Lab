import { FormOutlined, MenuOutlined } from '@ant-design/icons';
import { Layout, Menu, theme } from 'antd';
import './index.less'
import fileCheck from '../../assets/fileCheck.png'
import { Outlet, useNavigate } from 'react-router-dom';
import React from 'react';

const { Header, Sider } = Layout;


const Layouts: React.FC = (props:any) => {
    const {
        token: { colorBgContainer },
    } = theme.useToken();

    
    const navigate = useNavigate()

    const column = [
        {
            icon: FormOutlined,
            name: "弹幕解析",
            onclick: () => navigate('/home/decipher')
        },
        {
            icon: MenuOutlined,
            name: "弹幕爬取",
            onclick: () => navigate('/home/crawler')
        },
        {
            icon: MenuOutlined,
            name: "词云图绘制",
            onclick: () => navigate('/home/wordcloud')
        },
    ]

    return (
        <Layout className='wrapper'>
            <Header className='header' style={{color: colorBgContainer, fontSize: 24}}>
                <div className='fileCheck'><img src={fileCheck} alt="#"></img></div>    
                <div>弹幕爬取工具</div>
                {/* <div className='exit'><UserOutlined /></div> */}
            </Header>
            <Layout className='sider-layout'>
                <Sider
                    breakpoint="lg"
                    collapsedWidth="0"
                    className='sider'
                >
                    <Menu
                        className='menu'
                        theme="dark"
                        mode="inline"
                        defaultSelectedKeys={['1']}
                        items={column.map(
                            (item, index) => ({
                                key: String(index + 1),
                                icon: React.createElement(item.icon),
                                label: item.name,
                                onClick: item.onclick
                            }),
                        )}
                    />
                </Sider>
                <Layout className='content-layout'>
                    <Outlet/>
                </Layout>
            </Layout>
        </Layout>
    );
};

export default Layouts;