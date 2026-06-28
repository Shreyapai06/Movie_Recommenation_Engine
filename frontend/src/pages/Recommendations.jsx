import { useState } from 'react'
import MovieCard from '../components/MovieCard'
import { getRecommendationsByQuery } from '../api'

function Recommendations() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [searched, setSearched] = useState(false)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setSearched(true)
    const data = await getRecommendationsByQuery(query.trim())
    setResults(data)
    setLoading(false)
  }

  return (
    <div className="page">
      <h1 className="page-title">Find Recommendations</h1>
      <p className="page-subtitle">
        Search by a movie title, genre, or keyword to get movie recommendations.
      </p>

      <form className="recommend-search-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="e.g. Inception, Comedy, time travel..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Recommend</button>
      </form>

      {loading && <div className="status-message">Searching...</div>}

      {!loading && searched && results.length === 0 && (
        <div className="status-message">No recommendations found for "{query}".</div>
      )}

      {!loading && results.length > 0 && (
        <div className="movie-grid">
          {results.map((rec) => (
            <MovieCard key={rec.recommended_movie_id} movie={rec} idKey="recommended_movie_id" />
          ))}
        </div>
      )}
    </div>
  )
}

export default Recommendations
