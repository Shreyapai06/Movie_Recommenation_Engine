import { Component, inject, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { Movie } from '../../models/movie.model';
import { MovieCardComponent } from '../../components/movie-card/movie-card';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [MovieCardComponent],
  templateUrl: './landing.html',
  styleUrl: './landing.css',
})
export class LandingComponent implements OnInit {
  private api = inject(ApiService);

  movies: Movie[] = [];
  loading = true;
  error: string | null = null;

  ngOnInit(): void {
    this.api.getAllMovies().subscribe({
      next: (movies) => {
        this.movies = movies;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message;
        this.loading = false;
      },
    });
  }
}
