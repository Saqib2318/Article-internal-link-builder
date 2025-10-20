import { Route,Routes } from 'react-router'
import GetStarted from './pages/GetStarted'
import SelectAction from './pages/selectAction'
import AutoInternalToolForm from './pages/FormAction'
import ArticleTableForm from './pages/ArticleTableForm'

function App() {

  return (
    <>
      <Routes>
        <Route element={<GetStarted/>} path='/' index/>
        <Route element={<SelectAction/>} path='/select-action' />
        <Route element={<AutoInternalToolForm/>} path='/Form-Action'/>
        <Route element={<ArticleTableForm/>} path='/result-article' />
      </Routes>
    </>
  )
}

export default App
