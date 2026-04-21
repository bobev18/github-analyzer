import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
    providedIn: 'root'
})

export class GithubService {

    private getBaseUrl(): string {
        const hostname = window.location.hostname;
        const isLocal = hostname === 'localhost' || hostname === '127.0.0.1';
        
        if (isLocal) {
            return 'http://127.0.0.1:8000';
        }
        
        // Fallback to the production backend URL on Render
        return (window as any).API_URL || 'https://github-analyzer-api.onrender.com';
    }

    constructor(private http: HttpClient) {}

    getUser(username: string, deep: boolean = false) {
        const apiUrl = `${this.getBaseUrl()}/api/user`;
        return this.http.get(`${apiUrl}?username=${username}&deep=${deep}`);
    }

    getConfig() {
        return this.http.get(`${this.getBaseUrl()}/api/config`);
    }

}