import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Landing from './pages/Landing'
import MovieDetail from './pages/MovieDetail'
import Recommendations from './pages/Recommendations'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/movie/:id" element={<MovieDetail />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App
