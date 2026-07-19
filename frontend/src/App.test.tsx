import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders the Dashboard link in sidebar', () => {
    render(<App />);
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
  });

  it('renders the sidebar navigation', () => {
    render(<App />);
    expect(screen.getByLabelText(/Sidebar Navigation/i)).toBeInTheDocument();
  });

  it('renders the main menu navigation', () => {
    render(<App />);
    expect(screen.getByLabelText(/Main Menu/i)).toBeInTheDocument();
  });

  it('renders the top navbar with search', () => {
    render(<App />);
    expect(screen.getByLabelText(/Search/i)).toBeInTheDocument();
  });

  it('renders skip-to-content target', () => {
    render(<App />);
    expect(document.getElementById('main-content')).toBeInTheDocument();
  });

  it('renders the StadiumGPT brand name', () => {
    render(<App />);
    expect(screen.getByText(/StadiumGPT/i)).toBeInTheDocument();
  });

  it('renders the main content area with correct role', () => {
    render(<App />);
    expect(screen.getByRole('main')).toBeInTheDocument();
  });

  it('renders all sidebar navigation links', () => {
    render(<App />);
    const expectedLinks = ['Dashboard', 'AI Chat', 'Navigation', 'Crowd Intel', 'Operations', 'Transport', 'Sustainability', 'Settings'];
    expectedLinks.forEach(label => {
      expect(screen.getByText(label)).toBeInTheDocument();
    });
  });

  it('renders notification and user profile buttons', () => {
    render(<App />);
    expect(screen.getByLabelText(/Notifications/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/User Profile/i)).toBeInTheDocument();
  });

  it('renders the Stadium Overview heading on dashboard', () => {
    render(<App />);
    expect(screen.getByText(/Stadium Overview/i)).toBeInTheDocument();
  });
});
