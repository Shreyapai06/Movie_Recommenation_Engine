import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import MovieCard from '../components/MovieCard'
import { getMovie, getRecommendationsByMovieId, posterUrl } from '../api'

function MovieDetail() {
  const { id } = useParams()
  const [movie, setMovie] = useState(null)
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)
  const [notFound, setNotFound] = useState(false)

  useEffect(() => {
    setLoading(true)
    setNotFound(false)

    getMovie(id).then((data) => {
      if (!data) {
        setNotFound(true)
        setLoading(false)
        return
      }

      setMovie(data)
      setLoading(false)

      getRecommendationsByMovieId(id).then(setRecommendations)
    })
  }, [id])

  if (loading) return <div className="status-message">Loading movie...</div>
  if (notFound) return <div className="status-message error">Movie not found.</div>

  const poster = posterUrl(movie.poster_path)

  return (
    <div className="page">
      <div className="movie-detail">
        <div className="movie-detail-poster">
          {poster ? (
            <img src={poster} alt={movie.title} />
          ) : (
            <div className="movie-card-poster-fallback">No Image</div>
          )}
        </div>

        <div className="movie-detail-info">
          <h1>{movie.title}</h1>
          <p className="movie-detail-overview">{movie.overview}</p>

          <dl className="movie-detail-meta">
            <dt>Genres</dt>
            <dd>{movie.genres || '—'}</dd>

            <dt>Director</dt>
            <dd>{movie.director || '—'}</dd>

            <dt>Cast</dt>
            <dd>{movie.cast || '—'}</dd>

            <dt>Release Date</dt>
            <dd>{movie.release_date || '—'}</dd>

            <dt>Rating</dt>
            <dd>{movie.vote_average} ({movie.vote_count} votes)</dd>

            <dt>Popularity</dt>
            <dd>{movie.popularity}</dd>

            {movie.keywords && (
              <>
                <dt>Keywords</dt>
                <dd>{movie.keywords}</dd>
              </>
            )}
          </dl>
        </div>
      </div>

      {recommendations.length > 0 && (
        <section className="recommendations-section">
          <h2>You might also like</h2>
          <div className="movie-grid">
            {recommendations.map((rec) => (
              <MovieCard key={rec.recommended_movie_id} movie={rec} idKey="recommended_movie_id" />
            ))}
          </div>
        </section>
      )}
    </div>
  )
}

export default MovieDetail
