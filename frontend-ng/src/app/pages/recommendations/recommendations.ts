import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DestroyRef } from '@angular/core';
import { Subject } from 'rxjs';
import { switchMap, tap } from 'rxjs/operators';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ApiService } from '../../services/api.service';
import { Recommendation } from '../../models/movie.model';
import { MovieCardComponent } from '../../components/movie-card/movie-card';

@Component({
  selector: 'app-recommendations',
  standalone: true,
  imports: [FormsModule, MovieCardComponent],
  templateUrl: './recommendations.html',
  styleUrl: './recommendations.css',
})
export class RecommendationsComponent {
  private api = inject(ApiService);
  private destroyRef = inject(DestroyRef);

  query = '';
  results: Recommendation[] = [];
  loading = false;
  searched = false;

  private search$ = new Subject<string>();

  constructor() {
    this.search$
      .pipe(
        tap(() => {
          this.loading = true;
          this.searched = true;
          this.results = [];
        }),
        switchMap((q) => this.api.getRecommendationsByQuery(q)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe((results) => {
        this.results = results;
        this.loading = false;
      });
  }

  submit(): void {
    if (!this.query.trim()) return;
    this.search$.next(this.query.trim());
  }
}
