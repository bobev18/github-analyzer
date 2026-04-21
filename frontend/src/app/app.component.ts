import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GithubService } from './github.service';


@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './app.component.html'
})

export class AppComponent {

    githubUsername = '';
    data: any = null;
    error: string | null = null;
    loading = false;

    constructor(private githubService: GithubService) {}

    search() {
        if (!this.githubUsername.trim()) {
            this.error = "Please enter a GitHub username";
            return;
        }

        this.loading = true;
        this.error = null;
        this.data = null;

        this.githubService.getUser(this.githubUsername).subscribe({
            next: (response) => {
                this.data = response;
                this.loading = false;
            },
            error: (err) => {
                this.loading = false;
                if (err.status === 404) {
                    this.error = `User '${this.githubUsername}' not found.`;
                } else if (err.status === 403) {
                    this.error = "GitHub API rate limit exceeded. Please try again later.";
                } else {
                    this.error = "An error occurred while fetching user data.";
                }
            }
        });
    }

}