import { useEffect, useRef, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { searchMovies } from '../api'

function Navbar() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [open, setOpen] = useState(false)
  const boxRef = useRef(null)
  const navigate = useNavigate()

  useEffect(() => {
    if (!query.trim()) {
      setResults([])
      return
    }

    const timer = setTimeout(async () => {
      const data = await searchMovies(query.trim())
      setResults(data || [])
      setOpen(true)
    }, 300)

    return () => clearTimeout(timer)
  }, [query])

  useEffect(() => {
    function handleClickOutside(event) {
      if (boxRef.current && !boxRef.current.contains(event.target)) {
        setOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  function goToMovie(movieId) {
    setOpen(false)
    setQuery('')
    navigate(`/movie/${movieId}`)
  }

  return (
    <header className="navbar">
      <Link to="/" className="navbar-brand">
        🎬 MovieRec
      </Link>

      <div className="navbar-search" ref={boxRef}>
        <input
          type="text"
          placeholder="Search movies..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => results.length > 0 && setOpen(true)}
        />
        {open && results.length > 0 && (
          <ul className="navbar-search-results">
            {results.map((movie) => (
              <li key={movie.movie_id} onClick={() => goToMovie(movie.movie_id)}>
                {movie.title}
              </li>
            ))}
          </ul>
        )}
        {open && query.trim() && results.length === 0 && (
          <ul className="navbar-search-results">
            <li className="navbar-search-empty">No movies found</li>
          </ul>
        )}
      </div>

      <Link to="/recommendations" className="navbar-recommend-btn">
        Recommendations
      </Link>
    </header>
  )
}

export default Navbar
