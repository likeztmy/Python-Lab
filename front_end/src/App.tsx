import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.less'
import Layouts from './components/layouts'
import router from './router'
import { useRoutes } from 'react-router-dom'

function App() {
  return useRoutes(router)
}

export default App
