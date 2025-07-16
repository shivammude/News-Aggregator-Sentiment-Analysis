import React from 'react';
import { Header } from './components/Header';
import { FilterBar } from './components/FilterBar';
import { SentimentStats } from './components/SentimentStats';
import { NewsCard } from './components/NewsCard';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ErrorMessage } from './components/ErrorMessage';
import { ScrapingControls } from './components/ScrapingControls';
import { useNews } from './hooks/useNews';

function App() {
  const {
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
  } = useNews();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header searchQuery={searchQuery} onSearchChange={setSearchQuery} />
      
      <FilterBar
        selectedSentiment={selectedSentiment}
        selectedSource={selectedSource}
        selectedCategory={selectedCategory}
        onSentimentChange={setSelectedSentiment}
        onSourceChange={setSelectedSource}
        onCategoryChange={setSelectedCategory}
        sources={sources}
        categories={categories}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Scraping Controls */}
        <ScrapingControls 
          onRefresh={refreshData}
          onTriggerScraping={triggerScraping}
        />

        {error && <ErrorMessage message={error} onRetry={refreshData} />}

        {loading ? (
          <LoadingSpinner />
        ) : (
          <>
            <SentimentStats stats={sentimentStats} />
            
            {articles.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-gray-500 text-lg">
                  {error ? 'Failed to load articles.' : 'No articles found matching your criteria.'}
                </div>
                <p className="text-gray-400 mt-2">
                  {error ? 'Please check your connection and try again.' : 'Try adjusting your filters or search query.'}
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {articles.map((article) => (
                  <NewsCard key={article.id} article={article} />
                ))}
              </div>
            )}
          </>
        )}
      </main>

      {/* Floating status indicator */}
      <div className="fixed bottom-6 right-6">
        <div className="bg-white/90 backdrop-blur-md rounded-full px-4 py-2 shadow-lg border border-gray-200">
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full animate-pulse ${
              error ? 'bg-red-500' : loading ? 'bg-yellow-500' : 'bg-green-500'
            }`}></div>
            <span className="text-sm text-gray-700">
              {error ? 'Connection Error' : loading ? 'Loading...' : 'Live Updates'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;