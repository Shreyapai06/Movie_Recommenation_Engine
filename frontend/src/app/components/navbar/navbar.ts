import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { DestroyRef } from '@angular/core';
import { Subject, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ApiService } from '../../services/api.service';
import { Movie } from '../../models/movie.model';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class NavbarComponent {
  private api = inject(ApiService);
  private router = inject(Router);
  private destroyRef = inject(DestroyRef);

  query = '';
  results: Movie[] = [];
  open = false;

  private search$ = new Subject<string>();

  constructor() {
    this.search$
      .pipe(
        debounceTime(300),
        distinctUntilChanged(),
        switchMap((q) => (q.trim() ? this.api.searchMovies(q.trim()) : of<Movie[]>([]))),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe((results) => {
        this.results = results;
        this.open = results.length > 0;
      });
  }

  onQueryChange(value: string): void {
    this.query = value;
    if (!value.trim()) {
      this.results = [];
      this.open = false;
      return;
    }
    this.search$.next(value);
  }

  goToMovie(movieId: number): void {
    this.open = false;
    this.query = '';
    this.results = [];
    this.router.navigate(['/movie', movieId]);
  }

  closeDropdown(): void {
    setTimeout(() => {
      this.open = false;
    }, 150);
  }
}
