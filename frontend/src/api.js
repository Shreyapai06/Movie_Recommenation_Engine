export const TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500'

export function posterUrl(posterPath) {
  return posterPath ? `${TMDB_IMAGE_BASE}${posterPath}` : null
}

async function getJson(url) {
  const res = await fetch(url)

  if (!res.ok) {
    if (res.status === 404) return null
    throw new Error(`Request to ${url} failed with ${res.status}`)
  }

  return res.json()
}

export function getAllMovies() {
  return getJson('/movies/')
}

export function getMovie(movieId) {
  return getJson(`/movies/${movieId}`)
}

export function searchMovies(query) {
  return getJson(`/movies/search?query=${encodeURIComponent(query)}`)
}

export async function getRecommendationsByMovieId(movieId) {
  const data = await getJson(`/recommend/${movieId}`)
  return data ? data.recommendations : []
}

export async function getRecommendationsByQuery(query) {
  const data = await getJson(`/recommend/search?q=${encodeURIComponent(query)}`)
  return data ? data.recommendations : []
}
