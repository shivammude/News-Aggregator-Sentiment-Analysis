# News Aggregator Sentiment Analysis Dashboard - NewsScope

A comprehensive news aggregation and sentiment analysis system built with React frontend and Python FastAPI backend.

![Dashboard](https://github.com/shivammude/News-Aggregator-Sentiment-Analysis/blob/master/project/Dashboard.png)

![Articles_SentimentScore](https://github.com/shivammude/News-Aggregator-Sentiment-Analysis/blob/master/project/Articles_SentimentScore.png)

## Features

### Frontend (React + TypeScript)
- **Modern Dashboard**: Beautiful, responsive UI with Tailwind CSS
- **Real-time Updates**: Live sentiment analysis and article updates
- **Advanced Filtering**: Filter by sentiment, source, category, and search
- **Sentiment Visualization**: Interactive statistics and charts
- **Responsive Design**: Works perfectly on desktop and mobile

### Backend (Python + FastAPI)
- **Web Scraping**: Automated scraping from multiple news sources
- **Sentiment Analysis**: VADER + TextBlob for accurate sentiment detection
- **RESTful API**: Clean, documented API endpoints
- **Database Storage**: MongoDB for scalable data storage
- **Background Tasks**: Automated periodic scraping
- **Error Handling**: Robust error handling and logging

## Tech Stack

### Frontend
- React 18 with TypeScript
- Tailwind CSS for styling
- Lucide React for icons
- Vite for development and building

### Backend
- FastAPI (Python web framework)
- BeautifulSoup4 + Selenium for web scraping
- VADER Sentiment + TextBlob for sentiment analysis
- MongoDB with Motor (async driver)
- Uvicorn ASGI server

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- MongoDB (local or cloud)

### Installation

1. **Clone and install frontend dependencies:**
```bash
npm install
```

2. **Set up Python backend:**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp backend/.env.example backend/.env
# Edit .env with your MongoDB URL and other settings
```

4. **Start the application:**

Option 1 - Start both frontend and backend together:
```bash
npm run dev-full
```

Option 2 - Start separately:
```bash
# Terminal 1: Start backend
npm run backend

# Terminal 2: Start frontend
npm run dev
```

5. **Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Endpoints

### Articles
- `GET /api/articles` - Get filtered articles
- `POST /api/scrape` - Trigger manual scraping

### Statistics
- `GET /api/sentiment-stats` - Get sentiment statistics
- `GET /api/sources` - Get available news sources
- `GET /api/categories` - Get available categories

### System
- `GET /api/scraping-status` - Get scraping status
- `DELETE /api/articles` - Clear all articles (dev only)

## News Sources

Currently configured sources:
- Times of India
- NDTV
- CNN
- NY Times

## Sentiment Analysis

The system uses a hybrid approach:
- **VADER Sentiment** (70% weight) - Optimized for social media/news
- **TextBlob** (30% weight) - General purpose sentiment analysis



Sentiment categories:
- **Positive**: Score ≥ 0.05
- **Negative**: Score ≤ -0.05
- **Neutral**: -0.05 < Score < 0.05

## Configuration

### Backend Configuration (`backend/.env`)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=news_aggregator
SCRAPING_INTERVAL_MINUTES=30
MAX_ARTICLES_PER_SOURCE=20
SELENIUM_TIMEOUT=10
HEADLESS_BROWSER=true
```

### Adding New News Sources
Edit `backend/config.py` to add new sources with CSS selectors:

```python
{
    "name": "Source Name",
    "url": "https://example.com",
    "selectors": {
        "articles": "div.article",
        "title": "h2.title",
        "link": "a",
        "summary": "p.summary"
    },
    "category": "General"
}
```

## Development

### Frontend Development
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
```

### Backend Development
```bash
cd backend
python -m uvicorn main:app --reload  # Start with auto-reload
```

### Database Management
The system automatically creates indexes and handles database operations. For development, you can clear all articles using the API endpoint.

## Production Deployment

### Frontend
```bash
npm run build
# Deploy dist/ folder to your hosting service
```

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Environment Variables
Set these in production:
- `MONGODB_URL` - Your MongoDB connection string
- `DATABASE_NAME` - Database name
- Configure CORS origins in `main.py`

## Monitoring and Logging

The system includes comprehensive logging:
- Scraping activities and errors
- API request/response logging
- Database operation logs
- Sentiment analysis performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs for error details
3. Ensure all dependencies are installed correctly
4. Verify MongoDB connection and permissions
