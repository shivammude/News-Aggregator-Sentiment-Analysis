import React from 'react';
import { TrendingUp, TrendingDown, Minus, BarChart3 } from 'lucide-react';
import { SentimentStats as SentimentStatsType } from '../types/news';

interface SentimentStatsProps {
  stats: SentimentStatsType;
}

export const SentimentStats: React.FC<SentimentStatsProps> = ({ stats }) => {
  const positivePercentage = Math.round((stats.positive / stats.total) * 100);
  const negativePercentage = Math.round((stats.negative / stats.total) * 100);
  const neutralPercentage = Math.round((stats.neutral / stats.total) * 100);

  const statCards = [
    {
      label: 'Positive',
      value: stats.positive,
      percentage: positivePercentage,
      icon: TrendingUp,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200'
    },
    {
      label: 'Negative',
      value: stats.negative,
      percentage: negativePercentage,
      icon: TrendingDown,
      color: 'text-red-600',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-200'
    },
    {
      label: 'Neutral',
      value: stats.neutral,
      percentage: neutralPercentage,
      icon: Minus,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200'
    },
    {
      label: 'Total Articles',
      value: stats.total,
      percentage: 100,
      icon: BarChart3,
      color: 'text-gray-600',
      bgColor: 'bg-gray-50',
      borderColor: 'border-gray-200'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {statCards.map((stat, index) => {
        const Icon = stat.icon;
        return (
          <div
            key={index}
            className={`${stat.bgColor} ${stat.borderColor} border rounded-xl p-4 transition-all duration-200 hover:shadow-md`}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
                <p className="text-xs text-gray-500">{stat.percentage}% of total</p>
              </div>
              <div className={`${stat.color} opacity-60`}>
                <Icon className="w-8 h-8" />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};