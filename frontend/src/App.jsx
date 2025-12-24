import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Entities from './pages/Entities'
import Catalogs from './pages/Catalogs'
import Attributes from './pages/Attributes'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="entities" element={<Entities />} />
        <Route path="catalogs" element={<Catalogs />} />
        <Route path="attributes" element={<Attributes />} />
      </Route>
    </Routes>
  )
}

export default App
