import '@angular/compiler';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { AppComponent } from './app.component';
import { of, throwError } from 'rxjs';

describe('AppComponent', () => {
  let component: AppComponent;
  let mockGithubService: any;

  beforeEach(() => {
    mockGithubService = {
      getUser: vi.fn()
    };
    component = new AppComponent(mockGithubService);
  });

  it('should create the app', () => {
    expect(component).toBeTruthy();
  });

  it('should show error if username is empty', () => {
    component.githubUsername = '';
    component.search();
    expect(component.error).toBe("Please enter a GitHub username");
  });

  it('should strip whitespaces from username', () => {
    mockGithubService.getUser.mockReturnValue(of({}));
    component.githubUsername = '  octocat  ';
    component.search();
    expect(component.githubUsername).toBe('octocat');
    expect(mockGithubService.getUser).toHaveBeenCalledWith('octocat', false);
  });

  it('should call service with deepAnalysis flag and update data on success', () => {
    const mockData = { username: 'testuser', followers: 10, is_partial: false };
    mockGithubService.getUser.mockReturnValue(of(mockData));
    
    component.githubUsername = 'testuser';
    component.deepAnalysis = true; // Set toggle
    component.search();
    
    expect(mockGithubService.getUser).toHaveBeenCalledWith('testuser', true);
    expect(component.loading).toBe(false);
    expect(component.data).toEqual(mockData);
  });

  it('should handle is_partial results correctly', () => {
    const mockData = { username: 'testuser', followers: 10, is_partial: true };
    mockGithubService.getUser.mockReturnValue(of(mockData));
    
    component.githubUsername = 'testuser';
    component.search();
    
    expect(component.data.is_partial).toBe(true);
  });

  it('should handle 404 error correctly', () => {
    mockGithubService.getUser.mockReturnValue(throwError(() => ({ status: 404 })));
    
    component.githubUsername = 'unknown';
    component.search();
    
    expect(component.error).toContain("not found");
    expect(component.loading).toBe(false);
  });

  it('should handle zero followers state and labels', () => {
    const mockData = { username: 'lonelyuser', followers: 0, repos: [], is_partial: false };
    mockGithubService.getUser.mockReturnValue(of(mockData));
    
    component.githubUsername = 'lonelyuser';
    component.search();
    
    expect(component.data.followers).toBe(0);
    expect(component.getFollowersLabel()).toBe('No followers');
    expect(component.getReposLabel()).toBe('No repositories');
  });

  it('should handle singular labels correctly', () => {
    component.data = { followers: 1, repos: [{ name: 'one-repo' }] };
    expect(component.getFollowersLabel()).toBe('1 Follower');
    expect(component.getReposLabel()).toBe('1 Repository');
  });

  it('should handle plural labels correctly', () => {
    component.data = { followers: 2, repos: [{ name: 'r1' }, { name: 'r2' }] };
    expect(component.getFollowersLabel()).toBe('2 Followers');
    expect(component.getReposLabel()).toBe('2 Repositories');
  });
});
