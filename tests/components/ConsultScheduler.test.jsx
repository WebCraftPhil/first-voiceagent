/**
 * Component tests for ConsultScheduler using React Testing Library.
 * Tests the consult scheduling form component in isolation.
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ConsultScheduler } from '../../src/components/ConsultScheduler';
import '@testing-library/jest-dom';

// Mock the API call
jest.mock('../../src/api/consults', () => ({
  createConsult: jest.fn(),
}));

import { createConsult } from '../../src/api/consults';

describe('ConsultScheduler Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders consult scheduling form', () => {
    render(<ConsultScheduler />);
    
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/phone/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /schedule/i })).toBeInTheDocument();
  });

  test('allows user to fill in form fields', () => {
    render(<ConsultScheduler />);
    
    const nameInput = screen.getByLabelText(/name/i);
    const emailInput = screen.getByLabelText(/email/i);
    const phoneInput = screen.getByLabelText(/phone/i);
    
    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });
    fireEvent.change(phoneInput, { target: { value: '+1234567890' } });
    
    expect(nameInput).toHaveValue('John Doe');
    expect(emailInput).toHaveValue('john@example.com');
    expect(phoneInput).toHaveValue('+1234567890');
  });

  test('validates required fields before submission', async () => {
    render(<ConsultScheduler />);
    
    const submitButton = screen.getByRole('button', { name: /schedule/i });
    fireEvent.click(submitButton);
    
    // Should show validation errors
    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
    });
  });

  test('validates email format', async () => {
    render(<ConsultScheduler />);
    
    const emailInput = screen.getByLabelText(/email/i);
    fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
    
    const submitButton = screen.getByRole('button', { name: /schedule/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/valid email/i)).toBeInTheDocument();
    });
  });

  test('submits form with valid data', async () => {
    const mockConsult = {
      id: '123',
      name: 'John Doe',
      email: 'john@example.com',
      phone: '+1234567890',
      date: '2024-01-15T10:00:00Z'
    };
    
    createConsult.mockResolvedValue(mockConsult);
    
    render(<ConsultScheduler />);
    
    // Fill in form
    fireEvent.change(screen.getByLabelText(/name/i), { 
      target: { value: 'John Doe' } 
    });
    fireEvent.change(screen.getByLabelText(/email/i), { 
      target: { value: 'john@example.com' } 
    });
    fireEvent.change(screen.getByLabelText(/phone/i), { 
      target: { value: '+1234567890' } 
    });
    
    // Submit
    const submitButton = screen.getByRole('button', { name: /schedule/i });
    fireEvent.click(submitButton);
    
    // Verify API was called
    await waitFor(() => {
      expect(createConsult).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'John Doe',
          email: 'john@example.com',
          phone: '+1234567890'
        })
      );
    });
    
    // Verify success message
    await waitFor(() => {
      expect(screen.getByText(/consult scheduled successfully/i)).toBeInTheDocument();
    });
  });

  test('displays error message on API failure', async () => {
    createConsult.mockRejectedValue(new Error('Network error'));
    
    render(<ConsultScheduler />);
    
    // Fill in form
    fireEvent.change(screen.getByLabelText(/name/i), { 
      target: { value: 'John Doe' } 
    });
    fireEvent.change(screen.getByLabelText(/email/i), { 
      target: { value: 'john@example.com' } 
    });
    
    // Submit
    const submitButton = screen.getByRole('button', { name: /schedule/i });
    fireEvent.click(submitButton);
    
    // Verify error message
    await waitFor(() => {
      expect(screen.getByText(/error scheduling consult/i)).toBeInTheDocument();
    });
  });

  test('shows loading state during submission', async () => {
    createConsult.mockImplementation(() => 
      new Promise(resolve => setTimeout(resolve, 1000))
    );
    
    render(<ConsultScheduler />);
    
    // Fill in form
    fireEvent.change(screen.getByLabelText(/name/i), { 
      target: { value: 'John Doe' } 
    });
    fireEvent.change(screen.getByLabelText(/email/i), { 
      target: { value: 'john@example.com' } 
    });
    
    // Submit
    const submitButton = screen.getByRole('button', { name: /schedule/i });
    fireEvent.click(submitButton);
    
    // Verify loading state
    expect(screen.getByText(/scheduling/i)).toBeInTheDocument();
    expect(submitButton).toBeDisabled();
  });
});
