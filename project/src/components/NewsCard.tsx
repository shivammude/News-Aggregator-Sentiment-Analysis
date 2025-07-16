import React from 'react';
import { ExternalLink, Clock, User, Eye } from 'lucide-react';
import { NewsArticle } from '../types/news';

interface NewsCardProps {
  article: NewsArticle;
}

export const NewsCard: React.FC<NewsCardProps> = ({ article }) => {
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'negative':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'neutral':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getSentimentScore = (score: number) => {
    return score > 0 ? `+${score.toFixed(2)}` : score.toFixed(2);
  };

  const formatTime = (date: Date) => {
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 60) {
      return `${diffInMinutes}m ago`;
    } else if (diffInMinutes < 1440) {
      return `${Math.floor(diffInMinutes / 60)}h ago`;
    } else {
      return `${Math.floor(diffInMinutes / 1440)}d ago`;
    }
  };

  return (
    <article className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-all duration-300 group">
      {/* Image */}
      {article.imageUrl && (
        <div className="relative h-48 overflow-hidden">
          <img
            src={article.imageUrl}
            alt={article.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <div className="absolute top-3 right-3">
            <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getSentimentColor(article.sentiment)}`}>
              {article.sentiment.charAt(0).toUpperCase() + article.sentiment.slice(1)}
            </span>
          </div>
        </div>
      )}

      {/* Content */}
      <div className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <span className="font-medium text-gray-700">{article.source}</span>
            <span>•</span>
            <span>{article.category}</span>
          </div>
          <div className="flex items-center space-x-1 text-xs text-gray-500">
            <Clock className="w-3 h-3" />
            <span>{formatTime(article.publishedAt)}</span>
          </div>
        </div>

        {/* Title */}
        <h2 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors duration-200">
          {article.title}
        </h2>

        {/* Summary */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-3">
          {article.summary}
        </p>

        {/* Sentiment Score */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <span className="text-xs text-gray-500">Sentiment Score:</span>
            <span className={`text-sm font-medium ${
              article.sentimentScore > 0 ? 'text-green-600' : 
              article.sentimentScore < 0 ? 'text-red-600' : 'text-blue-600'
            }`}>
              {getSentimentScore(article.sentimentScore)}
            </span>
          </div>
          <div className="flex items-center space-x-4 text-xs text-gray-500">
            <div className="flex items-center space-x-1">
              <Clock className="w-3 h-3" />
              <span>{article.readTime} min read</span>
            </div>
            {article.author && (
              <div className="flex items-center space-x-1">
                <User className="w-3 h-3" />
                <span>{article.author}</span>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between pt-3 border-t border-gray-100">
          <button className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-700 transition-colors duration-200">
            <Eye className="w-4 h-4" />
            <span>Read More</span>
          </button>
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 text-sm text-gray-500 hover:text-gray-700 transition-colors duration-200"
          >
            <ExternalLink className="w-4 h-4" />
            <span>Source</span>
          </a>
        </div>
      </div>
    </article>
  );
};