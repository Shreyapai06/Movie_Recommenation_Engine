import { Routes } from '@angular/router';
import { LandingComponent } from './pages/landing/landing';
import { MovieDetailComponent } from './pages/movie-detail/movie-detail';
import { RecommendationsComponent } from './pages/recommendations/recommendations';

export const routes: Routes = [
  { path: '', component: LandingComponent },
  { path: 'movie/:id', component: MovieDetailComponent },
  { path: 'recommendations', component: RecommendationsComponent },
  { path: '**', redirectTo: '' },
];
