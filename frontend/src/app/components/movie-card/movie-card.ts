import { Component, inject, Input } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Movie, Recommendation } from '../../models/movie.model';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-movie-card',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './movie-card.html',
  styleUrl: './movie-card.css',
})
export class MovieCardComponent {
  @Input() movie!: Movie | Recommendation;
  @Input() idKey: 'movie_id' | 'recommended_movie_id' = 'movie_id';

  private api = inject(ApiService);

  get movieId(): number {
    return (this.movie as unknown as Record<string, number>)[this.idKey];
  }

  get posterUrl(): string | null {
    return this.api.posterUrl(this.movie.poster_path);
  }
}
