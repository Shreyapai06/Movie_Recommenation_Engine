export interface Movie {
  movie_id: number;
  title: string;
  overview: string;
  genres: string;
  cast: string;
  director: string | null;
  keywords: string;
  popularity: number;
  vote_average: number;
  vote_count: number;
  release_date: string;
  poster_path: string;
}

export interface Recommendation {
  recommended_movie_id: number;
  title: string;
  overview: string;
  genres: string;
  poster_path: string;
  similarity_score: number | null;
  rank: number;
}

export interface RecommendationResponse {
  movie_id?: number;
  title?: string;
  query?: string;
  recommendations: Recommendation[];
}
