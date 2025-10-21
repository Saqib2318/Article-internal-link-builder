Article Internal Link Builder

Overview
Article Internal Link Builder is a powerful web application designed to automate the process of generating internal links for blog articles. By leveraging AI-powered semantic analysis, the tool crawls your website (custom sites or WordPress-powered ones) to discover relevant blog URLs, extracts meta titles and descriptions, and intelligently cross-references them with your provided article content. It then suggests and inserts contextually relevant links based on specific keywords, improving SEO, user navigation, and content discoverability.
Key benefits:

SEO Optimization: Boost internal linking to enhance site authority and crawlability.
Time-Saving: Automate manual link research and insertion.
AI-Driven Relevance: Uses Google's Gemini model for accurate semantic matching.
Flexible Crawling: Supports both custom websites and WordPress sites with sitemap integration.

This full-stack project features a modern React + Vite frontend for an intuitive user interface and a robust FastAPI backend for efficient API handling and crawling logic.
Features

Website Crawling: Input a custom URL or WordPress site to fetch blog post URLs via sitemap.xml or recursive crawling.
Meta Data Extraction: Pulls title, description, and other metadata from crawled pages.
Article Analysis: Upload or paste your article content for keyword extraction and semantic processing.
Cross-Referencing: Matches article keywords with crawled content using Gemini AI for relevance scoring.
Link Suggestions: Generates a list of suggested internal links with anchor text recommendations.
One-Click Insertion: Edit and insert links directly into your article markdown or HTML.
Export Options: Download updated article with links as Markdown, HTML, or plain text.
Error Handling: Robust validation for invalid URLs, rate limiting during crawls, and AI quota management.

Tech Stack



Component
Technology
Purpose



Frontend
React 18 + Vite
Interactive UI for article input, link suggestions, and previews.


Backend
FastAPI (Python 3.11+)
RESTful APIs for crawling, AI integration, and data processing.


AI/ML
Google Gemini API
Semantic analysis for keyword matching and relevance scoring.


Crawling
Scrapy or BeautifulSoup
URL discovery and metadata extraction.


Database
SQLite (dev) / PostgreSQL (prod)
Store crawled data and session states (optional).


Other
Axios (HTTP), Tailwind CSS (styling), Pydantic (validation)
Utilities for requests, UI, and data models.


Prerequisites

Node.js (v18+) and npm/yarn for frontend.
Python 3.11+ for backend.
Google Gemini API key (sign up at Google AI Studio).
Optional: Docker for containerized deployment.

Installation
Backend Setup (FastAPI)

Clone the repository:
git clone https://github.com/Saqib2318/Article-internal-link-builder.git
cd Article-internal-link-builder/backend


Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


Set environment variables:Create a .env file in the backend root:
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///app.db  # Or your PostgreSQL URL


Run the FastAPI server:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

The API will be available at http://localhost:8000. Check docs at http://localhost:8000/docs.


Frontend Setup (React + Vite)

Navigate to the frontend directory:
cd ../frontend


Install dependencies:
npm install
# Or yarn install


Set the backend API base URL (optional, defaults to http://localhost:8000):Update src/config.js if needed:
export const API_BASE_URL = 'http://localhost:8000';


Run the development server:
npm run dev

The app will be available at http://localhost:5173.


Usage

Start the App: Ensure both frontend and backend servers are running.

Crawl Website:

Go to the "Crawler" tab.
Enter your website URL (e.g., https://example.com or WordPress site).
Select options: "WordPress Mode" for sitemap auto-detection.
Click "Start Crawl" – the backend will fetch URLs and extract metadata.


Input Article:

Paste or upload your article content in the "Editor" tab.
Optionally, specify target keywords (e.g., "SEO tips", "blogging strategies").


Generate Links:

Click "Analyze & Suggest Links".
Gemini AI will process the content, match with crawled data, and display suggestions with relevance scores.


Insert & Export:

Review suggestions, customize anchor text.
Insert selected links into the article.
Export the updated content.



Example API Endpoint (via Swagger at /docs):

POST /crawl: { "url": "https://example.com", "wordpress": true } → Returns list of URLs with metadata.
POST /analyze: { "article": "Your article text", "keywords": ["keyword1"] } → Returns link suggestions.

Project Structure
Article-internal-link-builder/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entrypoint
│   ├── requirements.txt         # Python deps
│   └── .env             # Env template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Form.jsx  # Crawling UI
│   │   │   └── LinkSuggestions.jsx # Results display
│   │   ├── services/api.js      # Axios API calls
│   │   ├── App.jsx              # Main app component
│   │   └── index.css            # Tailwind styles
│   ├── package.json             # Node deps
│   ├── vite.config.js           # Vite config
│   └── tailwind.config.js
├── docker-compose.yml           # Optional: Container setup
└── README.md                    # This file

Configuration

Gemini API: Ensure your key has access to the Gemini 1.5 Flash model for best performance.
Crawling Limits: Configurable in backend/config.py (e.g., max depth, rate limit).
Frontend Env: Use .env for VITE_API_BASE_URL.

Contributing

Fork the repo and create a feature branch (git checkout -b feature/amazing-feature).
Commit changes (git commit -m 'Add some amazing feature').
Push to the branch (git push origin feature/amazing-feature).
Open a Pull Request.

We welcome contributions for bug fixes, new features, or documentation improvements. Please adhere to PEP 8 for Python and ESLint for JS.
License
This project is licensed under the MIT License - see the LICENSE file for details.
Contact

Author: Muhammed Saqib (@Saqib2318 on GitHub)
Issues: Report bugs or request features on the Issues page.

Acknowledgments

FastAPI for blazing-fast APIs.
Vite for rapid frontend development.
Google Gemini API for advanced AI capabilities.
Open-source community for inspiration and libraries.


Built with ❤️ for content creators and SEO enthusiasts. Star the repo if it helps you!
