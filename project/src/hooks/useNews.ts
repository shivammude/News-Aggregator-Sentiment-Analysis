import { useState, useEffect, useMemo } from 'react';
import { NewsArticle, SentimentStats } from '../types/news';
import { apiService, ApiArticle } from '../services/api';

// Transform API article to frontend article format
const transformApiArticle = (apiArticle: ApiArticle): NewsArticle => ({
  id: apiArticle.id,
  title: apiArticle.title,
  summary: apiArticle.summary || '',
  content: apiArticle.content || '',
  url: apiArticle.url,
  source: apiArticle.source,
  author: apiArticle.author,
  publishedAt: new Date(apiArticle.published_at),
  sentiment: apiArticle.sentiment,
  sentimentScore: apiArticle.sentiment_score,
  category: apiArticle.category,
  imageUrl: apiArticle.image_url,
  readTime: apiArticle.read_time
});

export const useNews = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSentiment, setSelectedSentiment] = useState('all');
  const [selectedSource, setSelectedSource] = useState('all');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sentimentStats, setSentimentStats] = useState<SentimentStats>({
    positive: 0,
    negative: 0,
    neutral: 0,
    total: 0
  });
  const [sources, setSources] = useState<string[]>([]);
  const [categories, setCategories] = useState<string[]>([]);

  // Fetch articles from API
  const fetchArticles = async () => {
    setLoading(true);
    setError(null);

    const response = await apiService.getArticles({
      limit: 50,
      sentiment: selectedSentiment !== 'all' ? selectedSentiment : undefined,
      source: selectedSource !== 'all' ? selectedSource : undefined,
      category: selectedCategory !== 'all' ? selectedCategory : undefined,
      search: searchQuery || undefined
    });

    if (response.error) {
      setError(response.error);
      setArticles([]);
    } else if (response.data) {
      const transformedArticles = response.data.map(transformApiArticle);
      setArticles(transformedArticles);
    }

    setLoading(false);
  };

  // Fetch sentiment statistics
  const fetchSentimentStats = async () => {
    const response = await apiService.getSentimentStats();
    if (response.data) {
      setSentimentStats(response.data);
    }
  };

  // Fetch sources and categories
  const fetchMetadata = async () => {
    const [sourcesResponse, categoriesResponse] = await Promise.all([
      apiService.getSources(),
      apiService.getCategories()
    ]);

    if (sourcesResponse.data) {
      setSources(sourcesResponse.data.sources);
    }

    if (categoriesResponse.data) {
      setCategories(categoriesResponse.data.categories);
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchArticles();
    fetchSentimentStats();
    fetchMetadata();
  }, []);

  // Refetch articles when filters change
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchArticles();
      fetchSentimentStats();
    }, 500); // Debounce API calls

    return () => clearTimeout(timeoutId);
  }, [searchQuery, selectedSentiment, selectedSource, selectedCategory]);

  // Auto-refresh data every 5 minutes
  useEffect(() => {
    const interval = setInterval(() => {
      fetchArticles();
      fetchSentimentStats();
    }, 300000); // 5 minutes

    return () => clearInterval(interval);
  }, [selectedSentiment, selectedSource, selectedCategory, searchQuery]);

  // Manual refresh function
  const refreshData = async () => {
    await Promise.all([
      fetchArticles(),
      fetchSentimentStats(),
      fetchMetadata()
    ]);
  };

  // Trigger scraping
  const triggerScraping = async () => {
    const response = await apiService.triggerScraping();
    if (response.data) {
      // Refresh data after a short delay to allow scraping to complete
      setTimeout(() => {
        refreshData();
      }, 5000);
    }
    return response;
  };

  return {
    articles,
    loading,
    error,
    searchQuery,
    setSearchQuery,
    selectedSentiment,
    setSelectedSentiment,
    selectedSource,
    setSelectedSource,
    selectedCategory,
    setSelectedCategory,
    sentimentStats,
    sources,
    categories,
    refreshData,
    triggerScraping
  };
};