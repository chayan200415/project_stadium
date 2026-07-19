/**
 * API configuration for StadiumGPT frontend.
 *
 * Centralizes the API base URL so it's not hardcoded across
 * individual page components. Change this value for different
 * environments (development, staging, production).
 */

/** Base URL for the StadiumGPT backend API. */
export const API_BASE_URL = "https://project-stadium.onrender.com";

/**
 * Constructs a full API endpoint URL.
 *
 * @param path - The API path (e.g., '/api/chat/')
 * @returns The full URL string
 */
export function apiUrl(path: string): string {
  return `${API_BASE_URL}${path}`;
}
