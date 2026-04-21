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

  it('should call service and update data on success', () => {
    const mockData = { username: 'testuser', followers: 10 };
    mockGithubService.getUser.mockReturnValue(of(mockData));
    
    component.githubUsername = 'testuser';
    component.search();
    
    expect(component.loading).toBe(false);
    expect(component.data).toEqual(mockData);
  });

  it('should handle 404 error correctly', () => {
    mockGithubService.getUser.mockReturnValue(throwError(() => ({ status: 404 })));
    
    component.githubUsername = 'unknown';
    component.search();
    
    expect(component.error).toContain("not found");
    expect(component.loading).toBe(false);
  });
});
