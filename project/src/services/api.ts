const API_BASE_URL = 'http://localhost:8000/api';

export interface ApiArticle {
  id: string;
  title: string;
  summary?: string;
  content?: string;
  url: string;
  source: string;
  author?: string;
  published_at: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  sentiment_score: number;
  category: string;
  image_url?: string;
  read_time: number;
  scraped_at: string;
}

export interface ApiSentimentStats {
  positive: number;
  negative: number;
  neutral: number;
  total: number;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiService {
  private async fetchWithErrorHandling<T>(url: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('API Error:', error);
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  async getArticles(params: {
    limit?: number;
    sentiment?: string;
    source?: string;
    category?: string;
    search?: string;
  } = {}): Promise<ApiResponse<ApiArticle[]>> {
    const searchParams = new URLSearchParams();
    
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        searchParams.append(key, value.toString());
      }
    });

    const url = `${API_BASE_URL}/articles?${searchParams.toString()}`;
    return this.fetchWithErrorHandling<ApiArticle[]>(url);
  }

  async getSentimentStats(): Promise<ApiResponse<ApiSentimentStats>> {
    return this.fetchWithErrorHandling<ApiSentimentStats>(`${API_BASE_URL}/sentiment-stats`);
  }

  async getSources(): Promise<ApiResponse<{ sources: string[] }>> {
    return this.fetchWithErrorHandling<{ sources: string[] }>(`${API_BASE_URL}/sources`);
  }

  async getCategories(): Promise<ApiResponse<{ categories: string[] }>> {
    return this.fetchWithErrorHandling<{ categories: string[] }>(`${API_BASE_URL}/categories`);
  }

  async triggerScraping(): Promise<ApiResponse<{ message: string }>> {
    try {
      const response = await fetch(`${API_BASE_URL}/scrape`, {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('API Error:', error);
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  async getScrapingStatus(): Promise<ApiResponse<{
    last_scrape?: string;
    articles_scraped: number;
    sources_active: number;
    status: string;
    next_scrape?: string;
  }>> {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/scraping-status`);
  }
}

export const apiService = new ApiService();