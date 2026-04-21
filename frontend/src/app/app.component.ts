import { Component, AfterViewInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GithubService } from './github.service';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './app.component.html'
})

export class AppComponent {
    @ViewChild('techChart') techChartRef!: ElementRef;
    
    githubUsername = '';
    data: any = null;
    error: string | null = null;
    loading = false;
    chart: any = null;

    constructor(private githubService: GithubService) {}

    search() {
        if (!this.githubUsername.trim()) {
            this.error = "Please enter a GitHub username";
            return;
        }

        this.loading = true;
        this.error = null;
        this.data = null;
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }

        this.githubService.getUser(this.githubUsername).subscribe({
            next: (response) => {
                this.data = response;
                this.loading = false;
                setTimeout(() => this.initChart(), 0);
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

    initChart() {
        if (!this.techChartRef || !this.data || !this.data.repos) return;

        const languages = this.data.repos
            .map((r: any) => r.language)
            .filter((l: any) => l !== null);
        
        const counts: any = {};
        languages.forEach((l: string) => counts[l] = (counts[l] || 0) + 1);

        const labels = Object.keys(counts);
        const values = Object.values(counts);

        const ctx = this.techChartRef.nativeElement.getContext('2d');
        this.chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        '#7d5fff', '#00d2ff', '#3ae374', '#ff9f1a', '#ff4dff', '#ff3838'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#8b949e',
                            font: { size: 12, family: 'Outfit' }
                        }
                    }
                }
            }
        });
    }
}