import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { switchMap, tap } from 'rxjs/operators';
import { ApiService } from '../../services/api.service';
import { Movie, Recommendation } from '../../models/movie.model';
import { MovieCardComponent } from '../../components/movie-card/movie-card';

@Component({
  selector: 'app-movie-detail',
  standalone: true,
  imports: [MovieCardComponent],
  templateUrl: './movie-detail.html',
  styleUrl: './movie-detail.css',
})
export class MovieDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private api = inject(ApiService);

  movie: Movie | null = null;
  recommendations: Recommendation[] = [];
  loading = true;
  notFound = false;

  ngOnInit(): void {
    this.route.params
      .pipe(
        tap(() => {
          this.loading = true;
          this.notFound = false;
          this.movie = null;
          this.recommendations = [];
        }),
        switchMap((params) => this.api.getMovie(params['id']))
      )
      .subscribe((movie) => {
        if (!movie) {
          this.notFound = true;
          this.loading = false;
          return;
        }

        this.movie = movie;
        this.loading = false;

        this.api
          .getRecommendationsByMovieId(movie.movie_id)
          .subscribe((recs) => (this.recommendations = recs));
      });
  }

  posterUrl(path: string | null | undefined): string | null {
    return this.api.posterUrl(path);
  }
}
