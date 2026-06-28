import { useEffect, useState } from 'react'
import MovieCard from '../components/MovieCard'
import { getAllMovies } from '../api'

function Landing() {
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getAllMovies()
      .then((data) => setMovies(data || []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="status-message">Loading movies...</div>
  if (error) return <div className="status-message error">Failed to load movies: {error}</div>

  return (
    <div className="page">
      <h1 className="page-title">Popular Movies</h1>
      <div className="movie-grid">
        {movies.map((movie) => (
          <MovieCard key={movie.movie_id} movie={movie} />
        ))}
      </div>
    </div>
  )
}

export default Landing
