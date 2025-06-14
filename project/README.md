# TDS Virtual TA

An intelligent Teaching Assistant for the Tools in Data Science course at IIT Madras that automatically answers student questions based on course content and forum discussions.

## Features

- 🔍 **Smart Search**: TF-IDF based search across course materials and forum posts
- 🤖 **AI-Powered Answers**: Uses OpenAI GPT-3.5 or Gemini for intelligent responses
- 🖼️ **Image Processing**: Can analyze uploaded images and screenshots
- 📚 **Comprehensive Knowledge Base**: Includes course content and forum discussions
- ⚡ **Fast API**: RESTful API with <30 second response times
- 🐳 **Docker Ready**: Easy deployment with Docker

## Quick Start

### 1. Setup
```bash
git clone https://github.com/yourusername/tds-virtual-ta.git
cd tds-virtual-ta
pip install -r requirements.txt
```

### 2. Scrape Data
```bash
# Scrape course content (requires Chrome with IITM login)
python scrapers/coursescraper.py

# Scrape discourse posts
python scrapers/discoursescraper.py

# Enhanced scraper with date range
python scrapers/enhanced_scraper.py --start-date 2025-01-01 --end-date 2025-04-14
```

### 3. Process Data
```bash
python data_processor.py
```

### 4. Run API
```bash
# Set API keys (optional, for better answers)
export OPENAI_API_KEY=your_key_here
export GEMINI_API_KEY=your_key_here

# Run the API
uvicorn app:app --host 0.0.0.0 --port 8000
```

### 5. Test API
```bash
curl "http://localhost:8000/api/" \
  -H "Content-Type: application/json" \
  -d '{"question": "Should I use gpt-4o-mini or gpt-3.5-turbo?"}'
```

## Deployment

### Using Docker
```bash
docker build -t tds-virtual-ta .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key tds-virtual-ta
```

### Using Railway/Render/Heroku
1. Push to GitHub
2. Connect your repository
3. Set environment variables
4. Deploy

## API Usage

### Endpoint: `POST /api/`

**Request:**
```json
{
  "question": "Your question here",
  "image": "base64_encoded_image_optional"
}
```

**Response:**
```json
{
  "answer": "AI-generated answer",
  "links": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/...",
      "text": "Relevant forum post title"
    }
  ]
}
```

## Evaluation

Run the evaluation suite:
```bash
npx -y promptfoo eval --config project-tds-virtual-ta-promptfoo.yaml
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
