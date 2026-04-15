const API_BASE_URL = process.env.REACT_APP_API_URL || '';

export const api = {
  analyzeAd: async (formData: FormData) => {
    const response = await fetch(`${API_BASE_URL}/analyze-ad`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      throw new Error('Failed to analyze ad');
    }
    return response.json();
  },

  scrapePage: async (url: string) => {
    const response = await fetch(`${API_BASE_URL}/scrape-landing-page`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ page_url: url }),
    });
    if (!response.ok) {
      throw new Error('Failed to scrape page');
    }
    return response.json();
  },

  generatePersonalizedPage: async (data: any) => {
    const response = await fetch(`${API_BASE_URL}/generate-personalized-page`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Failed to generate personalized page');
    }
    return response.json();
  },

  getPageGeneration: async (id: string) => {
    const response = await fetch(`${API_BASE_URL}/pages/${id}`);
    if (!response.ok) {
      throw new Error('Failed to get page generation');
    }
    return response.json();
  },

  healthCheck: async () => {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  },
};
