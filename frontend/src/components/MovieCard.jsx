import { Link } from 'react-router-dom'
import { posterUrl } from '../api'

function MovieCard({ movie, idKey = 'movie_id' }) {
  const id = movie[idKey]
  const poster = posterUrl(movie.poster_path)

  return (
    <Link to={`/movie/${id}`} className="movie-card">
      <div className="movie-card-poster">
        {poster ? (
          <img src={poster} alt={movie.title} loading="lazy" />
        ) : (
          <div className="movie-card-poster-fallback">No Image</div>
        )}
      </div>
      <div className="movie-card-title">{movie.title}</div>
    </Link>
  )
}

export default MovieCard
