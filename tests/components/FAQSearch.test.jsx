/**
 * Component tests for FAQSearch component.
 * Tests FAQ search and display functionality.
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { FAQSearch } from '../../src/components/FAQSearch';
import '@testing-library/jest-dom';

// Mock the API
jest.mock('../../src/api/faq', () => ({
  searchFAQs: jest.fn(),
  getAllFAQs: jest.fn(),
}));

import { searchFAQs, getAllFAQs } from '../../src/api/faq';

describe('FAQSearch Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders search input and button', () => {
    render(<FAQSearch />);
    
    expect(screen.getByPlaceholderText(/search faqs/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument();
  });

  test('displays FAQs on initial load', async () => {
    const mockFAQs = [
      { id: '1', question: 'What are your hours?', answer: '9-5 EST' },
      { id: '2', question: 'How do I schedule?', answer: 'Use the form' }
    ];
    
    getAllFAQs.mockResolvedValue(mockFAQs);
    
    render(<FAQSearch />);
    
    await waitFor(() => {
      expect(screen.getByText('What are your hours?')).toBeInTheDocument();
      expect(screen.getByText('How do I schedule?')).toBeInTheDocument();
    });
  });

  test('searches FAQs when user types and submits', async () => {
    const mockResults = [
      { id: '1', question: 'What are your hours?', answer: '9-5 EST' }
    ];
    
    searchFAQs.mockResolvedValue(mockResults);
    
    render(<FAQSearch />);
    
    const searchInput = screen.getByPlaceholderText(/search faqs/i);
    fireEvent.change(searchInput, { target: { value: 'hours' } });
    fireEvent.click(screen.getByRole('button', { name: /search/i }));
    
    await waitFor(() => {
      expect(searchFAQs).toHaveBeenCalledWith('hours');
      expect(screen.getByText('What are your hours?')).toBeInTheDocument();
    });
  });

  test('searches FAQs when user presses Enter', async () => {
    const mockResults = [
      { id: '1', question: 'What are your hours?', answer: '9-5 EST' }
    ];
    
    searchFAQs.mockResolvedValue(mockResults);
    
    render(<FAQSearch />);
    
    const searchInput = screen.getByPlaceholderText(/search faqs/i);
    fireEvent.change(searchInput, { target: { value: 'hours' } });
    fireEvent.keyPress(searchInput, { key: 'Enter', code: 'Enter' });
    
    await waitFor(() => {
      expect(searchFAQs).toHaveBeenCalledWith('hours');
    });
  });

  test('displays "no results" message when search returns empty', async () => {
    searchFAQs.mockResolvedValue([]);
    
    render(<FAQSearch />);
    
    const searchInput = screen.getByPlaceholderText(/search faqs/i);
    fireEvent.change(searchInput, { target: { value: 'nonexistent' } });
    fireEvent.click(screen.getByRole('button', { name: /search/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/no results found/i)).toBeInTheDocument();
    });
  });

  test('expands FAQ item to show answer when clicked', async () => {
    const mockFAQs = [
      { id: '1', question: 'What are your hours?', answer: 'We are open Monday-Friday, 9 AM to 5 PM EST.' }
    ];
    
    getAllFAQs.mockResolvedValue(mockFAQs);
    
    render(<FAQSearch />);
    
    await waitFor(() => {
      expect(screen.getByText('What are your hours?')).toBeInTheDocument();
    });
    
    // Initially answer should not be visible
    expect(screen.queryByText(/we are open monday-friday/i)).not.toBeInTheDocument();
    
    // Click to expand
    fireEvent.click(screen.getByText('What are your hours?'));
    
    // Answer should now be visible
    await waitFor(() => {
      expect(screen.getByText(/we are open monday-friday/i)).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    searchFAQs.mockRejectedValue(new Error('Network error'));
    
    render(<FAQSearch />);
    
    const searchInput = screen.getByPlaceholderText(/search faqs/i);
    fireEvent.change(searchInput, { target: { value: 'test' } });
    fireEvent.click(screen.getByRole('button', { name: /search/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/error loading faqs/i)).toBeInTheDocument();
    });
  });
});
