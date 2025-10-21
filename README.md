

# Article Internal Link Builder

A web application that automates generating contextually relevant internal links for blog articles on your site. Crawl your site (custom HTML or WordPress), extract metadata from blog URLs, cross‑reference with your article content using AI (via Google Gemini API), and insert or export internal links for improved SEO and content discoverability.

---

## 🌟 Features

* Website Crawling: Enter a custom site URL or a WordPress site; the crawler (via sitemap or recursive crawl) will discover blog URLs.
* Metadata Extraction: For each URL it finds, it pulls meta title, meta description, etc.
* Article Input & Analysis: Paste or upload your article text and optionally specify target keywords.
* AI‑Driven Cross‑Referencing: Using Gemini semantic analysis, the system matches your article content (and keywords) with the crawled URLs to find relevant linking opportunities.
* Link Suggestion & Insertion: Get a list of suggested internal links with anchor text recommendations. You can review, customize, and then insert them into your article (Markdown, HTML or plain text) or export the updated version.
* Flexible Tech Stack: Modern frontend (React + Vite) and robust backend (FastAPI).
* SEO & Content Workflow Optimization: Designed for content creators, bloggers & site owners to save time while boosting internal linking structure.

---

## 🧱 Tech Stack

| Layer       | Technology & Purpose                                                                     |
| ----------- | ---------------------------------------------------------------------------------------- |
| Frontend    | React 18 + Vite – interactive UI for article input, link suggestions & previews.         |
| Backend     | FastAPI (Python 3.11+) – REST APIs for crawling, AI integration & data processing.       |
| AI/ML       | Google Gemini API – semantic relevance matching between article content & crawled URLs.  |
| Crawling    | BeautifulSoup / Scrapy (or equivalent) – discovering blog URLs, extracting metadata.     |
| Database    | SQLite (development) / PostgreSQL (production) – storing crawled data and session state. |
| Other tools | Axios (frontend HTTP), Tailwind CSS (styling), Pydantic (data validation)                |

---

## 🧩 Prerequisites

* Node.js (v18+ recommended) and npm or yarn
* Python 3.11+
* A Google Gemini API key (obtain via Google AI Studio)
* (Optional) Docker & Docker Compose for containerised deployment

---

## 🚀 Installation & Setup

### Backend (FastAPI)

1. Clone the repository and change to the backend folder:

   ```bash
   git clone https://github.com/Saqib2318/Article-internal-link-builder.git
   cd Article-internal-link-builder/backend
   ```
2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```
3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables: create a `.env` file at the backend root with keys such as:

   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   DATABASE_URL=sqlite:///./app.db     # or your PostgreSQL connection string
   ```
5. Run the FastAPI server:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be accessible at [http://localhost:8000](http://localhost:8000) and API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

### Frontend (React + Vite)

1. Navigate to the frontend folder:

   ```bash
   cd ../frontend
   ```
2. Install Node dependencies:

   ```bash
   npm install     # or yarn install
   ```
3. Configure the backend API base URL if needed (default is `http://localhost:8000`). You can update `src/config.js` (or environment variable) like:

   ```js
   export const API_BASE_URL = 'http://localhost:8000';
   ```
4. Run the development server:

   ```bash
   npm run dev
   ```

   The frontend app will be available at [http://localhost:5173](http://localhost:5173).

---

## 🧭 Usage Guide

1. Ensure both backend and frontend servers are running.
2. In the UI, go to the “Crawler” tab (or equivalent):

   * Enter your website URL (e.g., `https://example.com`) or WordPress site.
   * Choose options (e.g., mark “WordPress mode” to detect sitemap automatically).
   * Click **Start Crawl** – the backend fetches blog URLs and extracts metadata.
3. Navigate to the “Editor” or “Article Input” section:

   * Paste or upload your article content.
   * (Optional) Provide target keywords (e.g., `"SEO tips"`, `"blogging strategies"`).
4. Hit **Analyze & Suggest Links** – the Gemini‑powered backend will process your article and match with the crawled URLs, returning link suggestions with relevance scores.
5. Review the suggestions:

   * Customize anchor texts if needed.
   * Select which links to insert into your article.
6. Insert the selected links into your article (Markdown/HTML) and/or export the updated version (Markdown, HTML, or plain text).
7. (Optional) Re‑run or re‑crawl whenever you publish new content and want to refresh your internal linking structure.

---

## 📁 Project Structure

```
Article‑Internal‑Link‑Builder/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point
│   ├── requirements.txt      # Python dependencies
│   └── .env (template)       # Environment variable template
├── frontend/
│   ├── src/
│   │   ├── assets/       # Assets of all images scripts will used
│   │   ├── components/       # UI components (e.g., info-model.jsx, navbar.jsx)
│   │   ├── pages/         # Pages Of Web APP
│   │   | ├── ArticleTable.jsx         # Response Of Web App
│   │   | ├── FormAction.jsx           #The Page Where the user put values
│   │   | ├── GetStarted.jsx           # Starting Of Web APP
│   │   | ├── SelectAction.jsx         # Selection to go through with custom or wordpress
|   |   ├── Providers/        # Providers of Web APP
|   |   | ├──selectProvider.jsx 
│   │   └── App.jsx           # Main React component
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   └── tailwind.config.js    # Tailwind CSS config
├── docker-compose.yml        # (Optional) Docker setup for full stack
└── README.md                 # This readme file
```

---

## ⚙️ Configuration & Environment Variables

* **GEMINI_API_KEY**: Your Google Gemini API key for semantic analysis.
* **DATABASE_URL**: URL for your database (e.g., `sqlite:///./app.db` for development, or PostgreSQL URI for production).
* **CRAWL_MAX_DEPTH**, **CRAWL_RATE_LIMIT** (example keys) – configurable crawler parameters (see `backend/config.py`).
* **VITE_API_BASE_URL** or similar: For the frontend to point to backend APIs in `src/config.js` or `.env`.

---

## 🤝 Contributing

We welcome contributions! Whether you’re adding a feature, fixing a bug, or improving documentation:

1. Fork the repo and create a new branch:

   ```bash
   git checkout -b feature/your‑feature
   ```
2. Make your changes (please adhere to PEP 8 for Python & ESLint for JS).
3. Commit your changes and push to your branch:

   ```bash
   git commit ‑m "Add some amazing feature"
   git push origin feature/your‑feature
   ```
4. Open a Pull Request.
5. We’ll review and merge once tests & checks are satisfied.

---

## 📄 License

This project is licensed under the **MIT License** — see the `LICENSE` file for details.

---

## 🙏 Acknowledgements

* Huge thanks to **FastAPI** for blazing‑fast, easy‑to‑use APIs.
* Appreciate **Vite** for the instant frontend dev feedback loop.
* Thanks to the **Google Gemini API** for enabling advanced semantic capabilities.
* And thank you to the open‑source community for continual inspiration and excellent libraries.

---

## 💡 Why use this tool?

* Improve your internal linking structure **automatically**, rather than doing manual link‑research one by one.
* Generate links that are **semantically relevant**—not just keyword matches, but contextually meaningful—thanks to AI assistance.
* Save time and energy: Let the crawler go fetch metadata, let the AI find relevant anchor‑texts, and you just review and export.
* Especially useful for blogs with **lots of content** (WordPress or custom) where building internal links manually becomes tedious and error‑prone.
* Helps boost **SEO**, improves user experience (via better navigation), and strengthens content discoverability.

---

## 🔮 Future Roadmap (ideas)

* Support bulk upload of multiple articles at once.
* Add user‑accounts / login to manage multiple websites.
* Dashboard with crawl analytics (link performance, internal link counts, crawl history).
* Integration with CMS platforms (WordPress plugin, Ghost, etc.).
* More AI‑powered suggestions: e.g., suggest new blog topics, identify orphan pages etc.
* Multi‑language support for international sites.

---

Again, feel free to **edit**, **trim**, or **expand** this README to match your exact implementation or feature set. If you want a simpler version (for non‑technical users) or a more detailed developer version (with API specs, architecture diagrams) I can help with those too.
