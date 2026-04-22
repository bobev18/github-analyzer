import '@angular/compiler';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { AppComponent } from './app.component';
import { of } from 'rxjs';
import { ElementRef } from '@angular/core';

describe('AppComponent Chart Initialization Fixed', () => {
  let component: AppComponent;
  let mockGithubService: any;

  beforeEach(() => {
    mockGithubService = {
      getUser: vi.fn(),
      getConfig: vi.fn().mockReturnValue(of({ github_auth_enabled: true, include_topics: false }))
    };
    component = new AppComponent(mockGithubService);
    
    // Mock Chart constructor globally or on the component
    // We'll just mock the initChart to see if it's called
  });

  it('should initialize chart when techChart setter is called with an element', () => {
    const mockData = { 
      username: 'test', 
      repos: [{ name: 'repo1', language: 'TypeScript' }] 
    };
    component.data = mockData;
    
    const spy = vi.spyOn(component, 'initChart');
    
    // Simulate Angular calling the setter when the element is rendered
    const mockElement = {
      nativeElement: {
        getContext: () => ({
          // Mock canvas context
        })
      }
    } as ElementRef;
    
    component.techChart = mockElement;
    
    expect(spy).toHaveBeenCalled();
  });
});
