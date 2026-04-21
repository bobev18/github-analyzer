import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
    providedIn: 'root'
})

export class GithubService {

    private apiUrl = 'http://127.0.0.1:8000/api/user';

    constructor(private http: HttpClient) {}

    getUser(username: string, deep: boolean = false) {
        return this.http.get(`${this.apiUrl}?username=${username}&deep=${deep}`);
    }

    getConfig() {
        return this.http.get('http://127.0.0.1:8000/api/config');
    }

}