import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

// Request interceptor for logging or authorization headers
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    console.error('[API Request Error]:', error);
    return Promise.reject(error);
  }
);

// Response interceptor with graceful error extraction
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const errorDetails = {
      message: error.response?.data?.detail || error.message || 'Network Error',
      status: error.response?.status,
      data: error.response?.data,
    };
    console.warn('[API Response Error]:', errorDetails);
    return Promise.reject(errorDetails);
  }
);

/**
 * Send a natural language query to the Company Brain backend
 * @param {string} prompt - The question asked by user
 * @param {boolean} demoMode - Force demo fallback mode
 * @returns {Promise<any>}
 */
export async function askQuestion(prompt, demoMode = false) {
  const response = await apiClient.post('/api/ask', {
    prompt,
    demo_mode: demoMode,
  });
  return response.data;
}

/**
 * Query the health status of the FastAPI server and FalkorDB connection
 * @returns {Promise<any>}
 */
export async function checkHealth() {
  const response = await apiClient.get('/health');
  return response.data;
}

export default apiClient;
