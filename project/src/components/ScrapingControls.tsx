import React, { useState } from 'react';
import { RefreshCw, Download, Play, CheckCircle } from 'lucide-react';

interface ScrapingControlsProps {
  onRefresh: () => Promise<void>;
  onTriggerScraping: () => Promise<any>;
}

export const ScrapingControls: React.FC<ScrapingControlsProps> = ({
  onRefresh,
  onTriggerScraping
}) => {
  const [refreshing, setRefreshing] = useState(false);
  const [scraping, setScraping] = useState(false);
  const [scrapingSuccess, setScrapingSuccess] = useState(false);

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      await onRefresh();
    } finally {
      setRefreshing(false);
    }
  };

  const handleTriggerScraping = async () => {
    setScraping(true);
    setScrapingSuccess(false);
    
    try {
      const response = await onTriggerScraping();
      if (response.data) {
        setScrapingSuccess(true);
        setTimeout(() => setScrapingSuccess(false), 3000);
      }
    } finally {
      setScraping(false);
    }
  };

  return (
    <div className="bg-white/80 backdrop-blur-md rounded-xl border border-gray-200 p-4 mb-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Data Controls</h3>
          <p className="text-sm text-gray-600">Manage news data scraping and updates</p>
        </div>
        
        <div className="flex items-center space-x-3">
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
            <span>{refreshing ? 'Refreshing...' : 'Refresh Data'}</span>
          </button>
          
          <button
            onClick={handleTriggerScraping}
            disabled={scraping}
            className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            {scrapingSuccess ? (
              <>
                <CheckCircle className="w-4 h-4" />
                <span>Scraping Started!</span>
              </>
            ) : (
              <>
                <Play className={`w-4 h-4 ${scraping ? 'animate-pulse' : ''}`} />
                <span>{scraping ? 'Starting...' : 'Scrape News'}</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};