import { RouteObject,Navigate } from "react-router-dom";

import WordCloud from "../components/wordcloud";
import Decipher from "../components/decipher";
import Crawler from "../components/crawler";
import Layouts from "../components/layouts";

const router: RouteObject[] = [
    {
        path: '/',
        element: <Navigate to='/home' />
    },
    {
        path:'/home',
        element: <Decipher />
    },
    {
        path: '/home',
        element: <Layouts/>,
        children: [
            {path:"",element: <Navigate to="decipher" />},
            {path:"decipher",element: <Decipher />},
            {path:"crawler",element: <Crawler />},
            {path:'wordcloud',element: <WordCloud />}
        ]
    }
]

export default router