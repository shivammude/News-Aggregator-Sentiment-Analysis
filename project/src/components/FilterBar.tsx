import React from 'react';
import { Filter, Calendar, Globe } from 'lucide-react';

interface FilterBarProps {
  selectedSentiment: string;
  selectedSource: string;
  selectedCategory: string;
  onSentimentChange: (sentiment: string) => void;
  onSourceChange: (source: string) => void;
  onCategoryChange: (category: string) => void;
  sources: string[];
  categories: string[];
}

export const FilterBar: React.FC<FilterBarProps> = ({
  selectedSentiment,
  selectedSource,
  selectedCategory,
  onSentimentChange,
  onSourceChange,
  onCategoryChange,
  sources,
  categories
}) => {
  const sentiments = [
    { value: 'all', label: 'All Sentiments', color: 'bg-gray-100 text-gray-700' },
    { value: 'positive', label: 'Positive', color: 'bg-green-100 text-green-700' },
    { value: 'negative', label: 'Negative', color: 'bg-red-100 text-red-700' },
    { value: 'neutral', label: 'Neutral', color: 'bg-blue-100 text-blue-700' }
  ];

  return (
    <div className="bg-white/80 backdrop-blur-md border-b border-gray-200 px-4 py-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-gray-500" />
            <span className="text-sm font-medium text-gray-700">Filters:</span>
          </div>

          {/* Sentiment Filter */}
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-600">Sentiment:</span>
            <div className="flex space-x-1">
              {sentiments.map((sentiment) => (
                <button
                  key={sentiment.value}
                  onClick={() => onSentimentChange(sentiment.value)}
                  className={`px-3 py-1 text-xs font-medium rounded-full transition-all duration-200 ${
                    selectedSentiment === sentiment.value
                      ? sentiment.color
                      : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  {sentiment.label}
                </button>
              ))}
            </div>
          </div>

          {/* Source Filter */}
          <div className="flex items-center space-x-2">
            <Globe className="w-4 h-4 text-gray-500" />
            <select
              value={selectedSource}
              onChange={(e) => onSourceChange(e.target.value)}
              className="text-sm border border-gray-200 rounded-lg px-3 py-1 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Sources</option>
              {sources.map((source) => (
                <option key={source} value={source}>
                  {source}
                </option>
              ))}
            </select>
          </div>

          {/* Category Filter */}
          <div className="flex items-center space-x-2">
            <Calendar className="w-4 h-4 text-gray-500" />
            <select
              value={selectedCategory}
              onChange={(e) => onCategoryChange(e.target.value)}
              className="text-sm border border-gray-200 rounded-lg px-3 py-1 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Categories</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};