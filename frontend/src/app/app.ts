import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { GameListComponent } from './components/game-list/game-list';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [GameListComponent],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class AppComponent {
  title = 'frontend';
}