export interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  content: string;
  url: string;
  source: string;
  author?: string;
  publishedAt: Date;
  sentiment: 'positive' | 'negative' | 'neutral';
  sentimentScore: number;
  category: string;
  imageUrl?: string;
  readTime: number;
}

export interface SentimentStats {
  positive: number;
  negative: number;
  neutral: number;
  total: number;
}

export interface NewsSource {
  id: string;
  name: string;
  domain: string;
  credibility: number;
  logo: string;
}