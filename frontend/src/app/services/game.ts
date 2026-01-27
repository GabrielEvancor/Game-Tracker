import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Game } from '../models/game';

@Injectable({
  providedIn: 'root'
})
export class GameService {
  // A URL da API
  private apiUrl = 'http://localhost:8000/games';

  // Injetando o HttpClient
  constructor(private http: HttpClient) { }

  // Método para buscar jogos (Read)
  getGames(
    skip: number = 0, // parametro obrigatorio
    limit: number = 20, // parametro obrigatorio
    search?: string, 
    genre?: string,
    maxPrice?: number
  ): Observable<Game[]> {
    
    let params = new HttpParams()
      .set('skip', skip)
      .set('limit', limit);

    if (search) params = params.set('search', search);
    if (genre) params = params.set('genre', genre);
    if (maxPrice) params = params.set('max_price', maxPrice);

    // Faz o GET http://localhost:8000/games?...
    return this.http.get<Game[]>(this.apiUrl, { params });
  }
}