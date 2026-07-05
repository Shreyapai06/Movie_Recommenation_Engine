import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { Movie, Recommendation, RecommendationResponse } from '../models/movie.model';
import { environment } from '../../environments/environment';

export const TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private base = environment.apiBase;

  posterUrl(posterPath: string | null | undefined): string | null {
    return posterPath ? `${TMDB_IMAGE_BASE}${posterPath}` : null;
  }

  getAllMovies(): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.base}/movies/`).pipe(
      catchError(() => of([]))
    );
  }

  getMovie(movieId: number | string): Observable<Movie | null> {
    return this.http.get<Movie>(`${this.base}/movies/${movieId}`).pipe(
      catchError(() => of(null))
    );
  }

  searchMovies(query: string): Observable<Movie[]> {
    return this.http
      .get<Movie[]>(`${this.base}/movies/search?query=${encodeURIComponent(query)}`)
      .pipe(catchError(() => of([])));
  }

  getRecommendationsByMovieId(movieId: number | string): Observable<Recommendation[]> {
    return this.http
      .get<RecommendationResponse>(`${this.base}/recommend/${movieId}`)
      .pipe(
        map((r) => r.recommendations),
        catchError(() => of([]))
      );
  }

  getRecommendationsByQuery(query: string): Observable<Recommendation[]> {
    return this.http
      .get<RecommendationResponse>(`${this.base}/recommend/search?q=${encodeURIComponent(query)}`)
      .pipe(
        map((r) => r.recommendations),
        catchError(() => of([]))
      );
  }
}
