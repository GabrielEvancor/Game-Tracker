import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; // Importante para o *ngFor
import { GameService } from '../../services/game';
import { Game } from '../../models/game';

@Component({
  selector: 'app-game-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game-list.html',
  styleUrl: './game-list.scss'
})
export class GameListComponent implements OnInit {
  
  // Local que armaneza a lista de jogos que vier do Python
  games: Game[] = [];

  // Injetamos o Service no construtor
  constructor(private gameService: GameService) {}

  // ngOnInit roda automaticamente quando o componente aparece na tela
  ngOnInit(): void {
    this.loadGames();
  }

  loadGames() {
    // Chama o garçom (Service) e se "inscreve" (subscribe) para receber a resposta
    this.gameService.getGames().subscribe({
      next: (data) => {
        this.games = data;
        console.log("Jogos carregados:", data);
      },
      error: (err) => {
        console.error("Erro ao buscar jogos:", err);
      }
    });
  }
}