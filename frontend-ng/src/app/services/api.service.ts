import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { Movie, Recommendation, RecommendationResponse } from '../models/movie.model';

export const TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);

  posterUrl(posterPath: string | null | undefined): string | null {
    return posterPath ? `${TMDB_IMAGE_BASE}${posterPath}` : null;
  }

  getAllMovies(): Observable<Movie[]> {
    return this.http.get<Movie[]>('/movies/').pipe(
      catchError(() => of([]))
    );
  }

  getMovie(movieId: number | string): Observable<Movie | null> {
    return this.http.get<Movie>(`/movies/${movieId}`).pipe(
      catchError(() => of(null))
    );
  }

  searchMovies(query: string): Observable<Movie[]> {
    return this.http
      .get<Movie[]>(`/movies/search?query=${encodeURIComponent(query)}`)
      .pipe(catchError(() => of([])));
  }

  getRecommendationsByMovieId(movieId: number | string): Observable<Recommendation[]> {
    return this.http
      .get<RecommendationResponse>(`/recommend/${movieId}`)
      .pipe(
        map((r) => r.recommendations),
        catchError(() => of([]))
      );
  }

  getRecommendationsByQuery(query: string): Observable<Recommendation[]> {
    return this.http
      .get<RecommendationResponse>(`/recommend/search?q=${encodeURIComponent(query)}`)
      .pipe(
        map((r) => r.recommendations),
        catchError(() => of([]))
      );
  }
}
