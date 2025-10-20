# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, HttpUrl
# from typing import Optional, List
# import re
# import spacy
# import requests
# import time
# from urllib.robotparser import RobotFileParser
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse
# from sentence_transformers import SentenceTransformer, util
# from transformers import pipeline
# from bs4 import XMLParsedAsHTMLWarning
# import warnings
# import nltk

# warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
# nltk.download('stopwords')

# app = FastAPI(title="Internal Link Builder API", description="API for building internal links in content")
# app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["http://localhost:5173"],
#         allow_credentials=True,  # Allow cookies and authentication headers
#         allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
#         allow_headers=["*"],     # Allow all headers
# )
# # Load NLP models
# nlp = spacy.load("en_core_web_lg")
# sentence_model = SentenceTransformer('all-distilroberta-v1')
# paraphraser = pipeline("text2text-generation", model="google/flan-t5-base")

# class LinkBuildRequest(BaseModel):
#     content: str
#     main_url: HttpUrl
#     num_links: int = 3
#     plateform: str = "custom"
#     wp_base_url: Optional[HttpUrl] = None
#     wp_post_id: Optional[int] = None

# class LinkBuildResponse(BaseModel):
#     modified_content: str
#     inserted_links: List[dict]
#     html_format_content: str
    
# def extract_keywords(content: str, top_n: int = 10) -> List[str]:
#     """Extract semantically relevant keywords using SpaCy and BERT embeddings."""
#     doc = nlp(content)
#     keywords = []
#     for ent in doc.ents:
#         if ent.label_ in ["PERSON", "ORG", "PRODUCT", "GPE", "NORP"]:
#             keywords.append(ent.text.lower())
#     for chunk in doc.noun_chunks:
#         if len(chunk.text.split()) <= 3:
#             keywords.append(chunk.text.lower())
#     keywords = list(set(keywords))[:top_n * 2]
#     if not keywords:
#         return []
#     embeddings = sentence_model.encode(keywords + [content], convert_to_tensor=True)
#     content_embedding = embeddings[-1]
#     similarities = util.cos_sim(embeddings[:-1], content_embedding)
#     ranked_keywords = sorted(zip(keywords, similarities), key=lambda x: x[1], reverse=True)[:top_n]
#     return [kw[0] for kw in ranked_keywords]

# def is_crawling_allowed(main_url: str, user_agent: str = "InternalLinkTool/1.0") -> tuple[bool, List[str]]:
#     """Check if crawling is allowed by robots.txt and extract sitemap URLs."""
#     parsed_url = urlparse(main_url)
#     robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
#     rp = RobotFileParser()
#     sitemap_urls = []
#     try:
#         response = requests.get(robots_url, headers={"User-Agent": user_agent}, timeout=10)
#         response.raise_for_status()
#         rp.parse(response.text.splitlines())
#         for line in response.text.splitlines():
#             if line.lower().startswith("sitemap:"):
#                 sitemap_url = line.split(":", 1)[1].strip()
#                 if sitemap_url:
#                     sitemap_urls.append(sitemap_url)
#     except requests.RequestException:
#         return True, []
#     return rp.can_fetch(user_agent, main_url), sitemap_urls
# def get_sitemap_urls(main_url: str, sitemap_urls: Optional[List[str]] = None) -> List[str]:
#     """Fetch URLs from sitemap(s), prioritizing post/blog/article/news sitemaps if available."""
#     parsed_url = urlparse(main_url)
#     headers = {"User-Agent": "InternalLinkTool/1.0"}
#     if not sitemap_urls:
#         sitemap_urls = [f"{parsed_url.scheme}://{parsed_url.netloc}/sitemap.xml"]
    
#     collected_urls = []
#     for sitemap_url in sitemap_urls:
#         try:
#             response = requests.get(sitemap_url, headers=headers, timeout=10)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, "xml")
            
#             if soup.find("sitemapindex"):
#                 sub_sitemaps = [loc.text for loc in soup.find_all("loc")]
#                 priority_sitemap = next(
#                     (
#                         url
#                         for url in sub_sitemaps
#                         if any(kw in url.lower() for kw in ["post-sitemap", "post", "blog", "article", "news",'content',"sitemap-content"])
#                     ),
#                     None,
#                 )
#                 if priority_sitemap:
#                     sub_sitemaps = [priority_sitemap]
#                 for sub_url in sub_sitemaps:
#                     try:
#                         sub_resp = requests.get(sub_url, headers=headers, timeout=10)
#                         sub_resp.raise_for_status()
#                         sub_soup = BeautifulSoup(sub_resp.text, "xml")
#                         urls = [loc.text for loc in sub_soup.find_all("loc")]
#                         collected_urls.extend(urls)
#                     except requests.RequestException:
#                         continue
#             else:
#                 urls = [loc.text for loc in soup.find_all("loc")]
#                 collected_urls.extend(urls)
#             time.sleep(1)
#         except requests.RequestException as e:
#             print(f"Error fetching sitemap {sitemap_url}: {e}")
    
#     return list(set(collected_urls))
# def get_wordpress_urls(wp_base_url: str, *_args, **_kwargs) -> List[str]:
#     """
#     Fetch WordPress blog post URLs using the RSS feed. 
#     No authentication required. Works for most public blogs.
#     """
#     rss_url = f"{wp_base_url.rstrip('/')}/feed/"
#     headers = {"User-Agent": "InternalLinkTool/1.0"}

#     try:
#         response = requests.get(rss_url, headers=headers, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, "xml")
#         urls= []
#         # Extract all <link> elements inside <item>
#         urls = [item.find("link").text.strip() for item in soup.find_all("item") if item.find("link")]
#         urls.extend([item.find("a[href=]").text.strip() for item in soup.find_all("item") if item.find("a[href=]")])

#         return list(set(urls))  # remove duplicates
#     except requests.RequestException as e:
#         print(f"Error fetching RSS feed from {rss_url}: {e}")
#         return []


# def crawl_urls(main_url: str, max_urls: int = 50) -> List[str]:
#     def filter_post_urls(urls: List[str]) -> List[str]:
#         EXCLUDE_KEYWORDS = ["privacy", "terms", "contact", "login", "signup", "category", "author",'wp-json','wp-content','wp-admin','wp-includes']

#         return [
#             url for url in urls
#             if not any(ex in url.lower() for ex in EXCLUDE_KEYWORDS)
#         ]

#     can_crawl, sitemap_urls = is_crawling_allowed(main_url)
#     if not can_crawl:
#         return []

#     urls = get_sitemap_urls(main_url, sitemap_urls)
#     if not urls:
#         try:
#             response = requests.get(main_url, headers={"User-Agent": "InternalLinkTool/1.0"}, timeout=10)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, "html.parser")
#             parsed_url = urlparse(main_url)
#             links = soup.find_all("a", href=True)
#             urls = [
#                 urljoin(main_url, link["href"])
#                 for link in links
#                 if urlparse(urljoin(main_url, link["href"])).netloc == parsed_url.netloc
#             ]
#         except requests.RequestException:
#             return []

#     return filter_post_urls(urls)[:max_urls]


# def match_urls_to_keywords(urls: List[str], keywords: List[str], main_url: str) -> List[tuple]:
#     """Match URLs to keywords using semantic similarity."""
#     matched_urls = []
#     keyword_embeddings = sentence_model.encode(keywords, convert_to_tensor=True)
#     for url in urls:
#         try:
#             response = requests.get(url, headers={"User-Agent": "InternalLinkTool/1.0"}, timeout=10)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, "html.parser")
#             title = soup.title.text if soup.title else ""
#             meta_desc = soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={"name": "description"}) else ""
#             page_text = title + " " + meta_desc + " " + soup.get_text(separator=" ", strip=True)
#             page_embedding = sentence_model.encode(page_text, convert_to_tensor=True)
#             similarities = util.cos_sim(keyword_embeddings, page_embedding)
#             max_similarity = similarities.max().item()
#             best_keyword = keywords[similarities.argmax().item()]
#             if max_similarity > 0.4:
#                 matched_urls.append((max_similarity, url, best_keyword))
#             time.sleep(1)
#         except requests.RequestException:
#             continue
#     return sorted(matched_urls, key=lambda x: x[0], reverse=True)

# def generate_anchor_text(keyword: str) -> str:
#     """Generate varied anchor text using T5 paraphrasing."""
#     try:
#         prompt = f"Paraphrase the phrase: {keyword}"
#         result = paraphraser(prompt, max_length=50, num_return_sequences=1)
#         return result[0]["generated_text"].strip()
#     except:
#         return keyword

# def insert_links_advanced(content: str, matched_urls: List[tuple], num_links: int) -> tuple[str, List[dict]]:
#     """Insert links at contextually appropriate positions using LLM-based sentence scoring."""
#     doc = nlp(content)
#     sentences = list(doc.sents)
#     if not sentences:
#         return content, []

#     sentence_texts = [sent.text for sent in sentences]
#     sentence_embeddings = sentence_model.encode(sentence_texts, convert_to_tensor=True)
#     content_embedding = sentence_model.encode(content, convert_to_tensor=True)
#     sentence_scores = util.cos_sim(sentence_embeddings, content_embedding).flatten()
    
#     sentence_data = sorted(
#         [(i, sent, score.item()) for i, (sent, score) in enumerate(zip(sentences, sentence_scores))],
#         key=lambda x: x[2],
#         reverse=True
#     )

#     modified_content = content
#     inserted = 0
#     used_urls = set()
#     used_keywords = set()
#     inserted_links = []
#     num_sentences = len(sentences)
#     target_positions = [
#         i for i in range(num_sentences)
#         if i in [0, num_sentences//2, num_sentences-1] or i % (num_sentences//max(1, num_links)) == 0
#     ]

#     for score, url, keyword in matched_urls:
#         if inserted >= num_links:
#             break
#         if url in used_urls or keyword in used_keywords:
#             continue
#         anchor_text = generate_anchor_text(keyword) if inserted % 2 == 0 else keyword
#         for pos, sent, _ in sentence_data:
#             if pos not in target_positions:
#                 continue
#             if keyword.lower() in sent.text.lower() and inserted < num_links:
#                 for token in sent:
#                     if token.text.lower() == keyword.lower() and token.dep_ in ["nsubj", "dobj", "pobj"]:
#                         pattern = rf'(?<!<[^>]*)\b({re.escape(keyword)})\b(?!([^<]*>))'
#                         link = f'<a href="{url}">{anchor_text}</a>'
#                         modified_content, count = re.subn(pattern, link, modified_content, 1, flags=re.IGNORECASE)
#                         if count > 0:
#                             inserted += 1
#                             used_urls.add(url)
#                             used_keywords.add(keyword)
#                             inserted_links.append({"url": url, "keyword": keyword, "anchor_text": anchor_text, "similarity": float(score)})
#                             target_positions = [p for p in target_positions if p != pos]
#                             break
#                 if inserted >= num_links:
#                     break

#     return modified_content, inserted_links

# def format_framework_link(url: str, anchor_text: str) -> str:
#     """Format links for specific frameworks."""
#     relative_url = urlparse(url).path
#     return f'<a href="{relative_url}">{anchor_text}</a>'


# def prompt_for_html_conversion(article: str) -> str:
#     return f"""
#         Convert the following article into clean HTML format using semantic tags like <article>, <h1>, <h2>, <p>, <a>, <ul>, <li> where appropriate.
#         Preserve all inserted hyperlinks as proper HTML <a> tags.

#         --- ARTICLE START ---

#         {article}

#         --- ARTICLE END ---
# """

# @app.post("/build-links", response_model=LinkBuildResponse)
# async def build_internal_links(request: LinkBuildRequest):
#     """Build internal links with advanced NLP and API integration."""
#     can_crawl, sitemap_urls = is_crawling_allowed(str(request.main_url))
#     if not can_crawl:
#         raise HTTPException(status_code=403, detail="Crawling not allowed by robots.txt")

#     keywords = extract_keywords(request.content)
#     if not keywords:
#         raise HTTPException(status_code=400, detail="No keywords extracted from content")

#     if request.plateform == "wordpress" and request.wp_base_url:
#         urls = get_wordpress_urls(str(request.wp_base_url), request.wp_username, request.wp_password)
#     else:
#         urls = crawl_urls(str(request.main_url))
    
#     print(urls)
#     print(keywords)
#     if not urls:
#         raise HTTPException(status_code=404, detail="No URLs found to link")

#     matched_urls = match_urls_to_keywords(urls, keywords, str(request.main_url))
#     print(matched_urls)
#     if not matched_urls:
#         raise HTTPException(status_code=404, detail="No relevant URLs found for keywords")

#     if request.plateform == "custom":
#         modified_content = request.content
#         inserted = 0
#         used_urls = set()
#         used_keywords = set()
#         inserted_links = []
#         doc = nlp(request.content)
#         sentences = list(doc.sents)
#         sentence_texts = [sent.text for sent in sentences]
#         sentence_embeddings = sentence_model.encode(sentence_texts, convert_to_tensor=True)
#         content_embedding = sentence_model.encode(request.content, convert_to_tensor=True)
#         sentence_scores = util.cos_sim(sentence_embeddings, content_embedding).flatten()
#         sentence_data = sorted(
#             [(i, sent, score.item()) for i, (sent, score) in enumerate(zip(sentences, sentence_scores))],
#             key=lambda x: x[2],
#             reverse=True
#         )
#         htmlGenerated = prompt_for_html_conversion(modified_content)
#         html_format_content = paraphraser(htmlGenerated, max_length=5000, num_return_sequences=1)[0]['generated_text']
#         num_sentences = len(sentences)
#         target_positions = [
#             i for i in range(num_sentences)
#             if i in [0, num_sentences//2, num_sentences-1] or i % (num_sentences//max(1, request.num_links)) == 0
#         ]
#         for score, url, keyword in matched_urls:
#             if inserted >= request.num_links:
#                 break
#             if url in used_urls or keyword in used_keywords:
#                 continue
#             anchor_text = generate_anchor_text(keyword) if inserted % 2 == 0 else keyword
#             for pos, sent, _ in sentence_data:
#                 if pos not in target_positions:
#                     continue
#                 if keyword.lower() in sent.text.lower() and inserted < request.num_links:
#                     for token in sent:
#                         if token.text.lower() == keyword.lower() and token.dep_ in ["nsubj", "dobj", "pobj"]:
#                             pattern = rf'(?<!<[^>]*)\b({re.escape(keyword)})\b(?!([^<]*>))'
#                             link = format_framework_link(url, anchor_text, request.plateform)
#                             modified_content, count = re.subn(pattern, link, modified_content, 1, flags=re.IGNORECASE)
#                             if count > 0:
#                                 inserted += 1
#                                 used_urls.add(url)
#                                 used_keywords.add(keyword)
#                                 inserted_links.append({"url": url, "keyword": keyword, "anchor_text": anchor_text, "similarity": float(score)})
#                                 target_positions = [p for p in target_positions if p != pos]
#                                 break
#                     if inserted >= request.num_links:
#                         break
#     else:
#         modified_content, inserted_links = insert_links_advanced(request.content, matched_urls, request.num_links)
#         htmlGenerated = prompt_for_html_conversion(modified_content)
#         html_format_content = paraphraser(htmlGenerated, max_length=5000,max_new_tokens=256, num_return_sequences=1)[0]['generated_text']

#     return LinkBuildResponse(
#         modified_content=modified_content,
#         inserted_links=inserted_links,
#         html_format_content=html_format_content
#     )

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)




import os
import re
import json
import time
import requests
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from typing import Optional, List

import google.generativeai as genai
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

# --- Configuration and Model Loading ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCqa3b6xCOfMnCTHjN_0KJwSKN5uxro0QM")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please create one.")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  # Corrected to valid model

# --- FastAPI App Setup ---
app = FastAPI(
    title="Internal Link Builder API (Gemini Powered)",
    description="API for building internal links in content using Google Gemini."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class LinkBuildRequest(BaseModel):
    content: str
    main_url: HttpUrl
    num_links: int = 3
    plateform: str = "custom"  # 'custom', 'wordpress', 'nextjs', 'nuxtjs', 'vue'
    wp_base_url: Optional[HttpUrl] = None
    wp_post_id: Optional[int] = None

class LinkBuildResponse(BaseModel):
    modified_content: str
    inserted_links: List[dict]
    html_format_content: str

# --- Helper Functions for Web Crawling ---
def is_crawling_allowed(main_url: str, user_agent: str = "InternalLinkTool/1.0") -> tuple[bool, List[str]]:
    """Check if crawling is allowed by robots.txt and extract sitemap URLs."""
    parsed_url = urlparse(main_url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    rp = RobotFileParser()
    sitemap_urls = []
    try:
        response = requests.get(robots_url, headers={"User-Agent": user_agent}, timeout=10)
        response.raise_for_status()
        rp.parse(response.text.splitlines())
        for line in response.text.splitlines():
            if line.lower().startswith("sitemap:"):
                sitemap_url = line.split(":", 1)[1].strip()
                if sitemap_url:
                    sitemap_urls.append(sitemap_url)
    except requests.RequestException:
        return True, []
    return rp.can_fetch(user_agent, main_url), sitemap_urls


def get_sitemap_urls(main_url: str, sitemap_urls: Optional[List[str]] = None) -> List[str]:
    """Fetch URLs from sitemap(s), prioritizing content-related pages."""
    parsed_url = urlparse(main_url)
    headers = {"User-Agent": "InternalLinkTool/1.0"}
    if not sitemap_urls:
        sitemap_urls = [f"{parsed_url.scheme}://{parsed_url.netloc}/sitemap.xml"]

    collected_urls = []
    for sitemap_url in sitemap_urls:
        try:
            print(f"Fetching sitemap: {sitemap_url}")
            response = requests.get(sitemap_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "xml")
            if soup.find("sitemapindex"):
                sub_sitemaps = [loc.text for loc in soup.find_all("loc")]
                # Prioritize sitemaps with keywords like post, blog, article, news, content, including numbered variants
                priority_sitemaps = [
                    url for url in sub_sitemaps
                    if re.search(r'(post|blog|article|news|content)-?sitemap\d*\.xml', url.lower())
                ]
                sub_sitemaps_to_crawl = priority_sitemaps if priority_sitemaps else sub_sitemaps
                for sub_url in sub_sitemaps_to_crawl:
                    try:
                        sub_resp = requests.get(sub_url, headers=headers, timeout=50)
                        sub_resp.raise_for_status()
                        sub_soup = BeautifulSoup(sub_resp.text, "xml")
                        urls = [loc.text for loc in sub_soup.find_all("loc")]
                        collected_urls.extend(urls)
                        print(f"Collected {len(urls)} URLs from sub-sitemap: {sub_url}")
                    except requests.RequestException as e:
                        print(f"Error fetching sub-sitemap {sub_url}: {e}")
                        continue
            else:
                urls = [loc.text for loc in soup.find_all("loc")]
                collected_urls.extend(urls)
            time.sleep(1)
        except requests.RequestException as e:
            print(f"Error fetching sitemap {sitemap_url}: {e}")
    print(collected_urls)
    return list(set(collected_urls))

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List

def get_wordpress_urls(wp_base_url: str, per_page: int = 100, pages: int = 1) -> List[str]:
    headers = {"User-Agent": "InternalLinkTool/1.0"}
    urls = []
    for page in range(1, pages + 1):
        api_url = f"{wp_base_url.rstrip('/')}/wp-json/wp/v2/posts?per_page={per_page}&page={page}"
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            urls.extend([post['link'] for post in data if 'link' in post])
            if len(data) < per_page:
                break  # No more pages
        except requests.RequestException as e:
            print(f"[API ERROR] Page {page} failed: {e}")
            break
    return list(set(urls))

def crawl_urls(main_url: str) -> List[str]:
    """Crawl the website to find internal URLs, prioritizing content-related pages."""
    def filter_post_urls(urls: List[str]) -> List[str]:
        # POST_KEYWORDS = ["blog", "post", "article", "news", "story", "read", "202"]
        EXCLUDE_KEYWORDS = ["privacy", "terms", "contact", "login", "signup", "category", "author", "wp-json", "wp-content", "wp-admin", "wp-includes", "feed"]
        return [
            url for url in urls
            if not any(ex in url.lower() for ex in EXCLUDE_KEYWORDS)
        ]

    can_crawl, sitemap_urls = is_crawling_allowed(main_url)
    if not can_crawl:
        print(f"Crawling not allowed for {main_url} by robots.txt.")
        return []

    urls = get_sitemap_urls(main_url, sitemap_urls)
    if not urls:
        print(f"No sitemap URLs found for {main_url}, attempting basic crawl.")
        try:
            response = requests.get(main_url, headers={"User-Agent": "InternalLinkTool/1.0"}, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            parsed_main_url = urlparse(main_url)
            links = soup.find_all("a", href=True)
            urls = [
                urljoin(main_url, link["href"])
                for link in links
                if urlparse(urljoin(main_url, link["href"])).netloc == parsed_main_url.netloc
            ]
        except requests.RequestException as e:
            print(f"Error crawling main URL {main_url}: {e}")
            return []

    return filter_post_urls(urls)

# --- Input Sanitization ---
def sanitize_content(content: str) -> str:
    """Sanitize content to avoid triggering Gemini safety filters."""
    sensitive_keywords = [
        r'\b(violence|explicit|adult|offensive)\b',
        r'\b(hate|discrimination|abuse)\b',
    ]
    sanitized = content
    for pattern in sensitive_keywords:
        sanitized = re.sub(pattern, '[REDACTED]', sanitized, flags=re.IGNORECASE)
    return sanitized

# --- Gemini Powered NLP Functions ---
async def call_gemini(prompt: str, max_output_tokens: int = 2048, temperature: float = 0.7) -> str:
    """Helper to call Gemini API with a prompt."""
    try:
        print(f"Sending prompt to Gemini (first 500 chars): {prompt[:500]}...")
        safety_settings = {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE"
        }
        response = await model.generate_content_async(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature
            ),
            safety_settings=safety_settings
        )
        if response.candidates and response.candidates[0].finish_reason == 2:
            print(f"Safety violation detected. Full response: {response}")
            raise HTTPException(
                status_code=400,
                detail="Gemini API blocked response due to safety concerns (finish_reason=2). Please review the input content or URLs for sensitive material."
            )
        if response.text:
            print(f"Received response (first 500 chars): {response.text[:500]}...")
            return response.text.strip()
        print("No text in response, returning empty string.")
        return ""
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        print(f"Failed prompt (first 500 chars): {prompt[:500]}...")
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

async def extract_keywords_gemini(content: str, top_n: int = 10) -> List[str]:
    """Extract semantically relevant keywords using Gemini."""
    prompt = f"""Given the following article content, identify the top {top_n} most important keywords and concepts that would be suitable for internal linking to other related articles. Focus on nouns and noun phrases that represent key topics. Provide them as a comma-separated list, e.g., "keyword1, keyword2, keyword3".

    Content:
    {content}
    """
    response_text = await call_gemini(prompt, max_output_tokens=200, temperature=0.3)
    if not response_text:
        print("No keywords extracted by Gemini.")
        return []
    keywords = [kw.strip().lower() for kw in response_text.split(',') if kw.strip()]
    return list(set(keywords))

async def match_urls_to_keywords_gemini(urls: List[str], keywords: List[str], main_article_content: str, num_links: int) -> List[dict]:
    """Match URLs to keywords and suggest anchor text using Gemini."""
    if not urls or not keywords:
        return []

    url_data = []
    for url in urls:
        try:
            response = requests.get(url, headers={"User-Agent": "InternalLinkTool/1.0"}, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.text if soup.title else ""
            meta_desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", property="og:description")
            description = meta_desc_tag["content"] if meta_desc_tag and "content" in meta_desc_tag.attrs else ""
            url_data.append({"url": url, "title": title, "description": description})
            time.sleep(0.1)
        except requests.RequestException as e:
            print(f"Could not fetch {url} for Gemini context: {e}")
            continue

    if not url_data:
        print("No valid URL data fetched for matching.")
        return []

    url_list_str = "\n".join([f"- URL: {d['url']}\n  Title: {d['title']}\n  Description: {d['description']}" for d in url_data])
    keyword_list_str = ", ".join(keywords)

    prompt = f"""
    You are an expert SEO and content strategist. Your task is to identify the best internal links from a list of URLs to be inserted into a given main article.

    Main Article Content (for context, do not modify or include in output):
    {main_article_content[:1000]}

    Keywords/Concepts from Main Article to Link:
    {keyword_list_str}

    Potential Internal Link URLs (with their titles and descriptions):
    {url_list_str}

    For each of the most relevant potential internal link URLs (up to {num_links} links), provide the following information in a JSON format.
    Focus on finding URLs that are highly semantically related to the main article's keywords/concepts.
    For the 'anchor_text', pick a natural-sounding phrase *from the main article's content* that best represents the link's topic. This anchor text MUST exist as a phrase within the main article, or be a very slight, grammatical modification of existing text.

    Output format (JSON array of objects):
    ```json
    [
      {{
        "url": "chosen_url",
        "keyword": "matched_keyword_or_concept",
        "anchor_text": "suggested_anchor_text_from_article_context",
        "reason": "brief_explanation_of_why_this_link_is_relevant_and_good_anchor_text_choice"
      }}
    ]
    ```
    Do not suggest more than {num_links} links. Ensure the JSON is valid and contains only the array.
    """

    try:
        response_text = await call_gemini(prompt, max_output_tokens=2048, temperature=0.5)
        if response_text.startswith("```json"):
            response_text = response_text[len("```json"):].strip()
            if response_text.endswith("```"):
                response_text = response_text[:-len("```")].strip()
        if not response_text:
            print("Gemini returned empty response for URL matching.")
            return []
        matched_links = json.loads(response_text)
        return matched_links[:num_links]
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from Gemini: {e}")
        print(f"Gemini response was:\n---\n{response_text}\n---")
        return []
    except HTTPException as e:
        print(f"Gemini API error in match_urls_to_keywords: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred in match_urls_to_keywords_gemini: {e}")
        return []

async def insert_links_gemini(content: str, inserted_links_data: List[dict], plateform: str, main_url_domain: str) -> str:
    """Inserts links into the content using Gemini, ensuring natural placement."""
    if not inserted_links_data:
        return content

    links_to_insert_str = ""
    for link_data in inserted_links_data:
        full_url = link_data["url"]
        # parsed_full_url = urlparse(full_url)

        links_to_insert_str += (
            f"- Anchor Text: '{link_data['anchor_text']}'\n"
            f"  Target URL: {link_data['url']}\n"
        )

 
    prompt_template = """You are an expert SEO Content Editor. Your sole task is to strategically insert a list of internal links into the provided article content.

The anchor texts provided in the list are guaranteed to exist within the article.

Follow these rules precisely:
1.  **Find and Convert:** Find the first occurrence of each exact anchor text within the article and convert that phrase into an HTML hyperlink.
2.  **Exact Anchor Text:** You MUST use the exact anchor text provided for each link. Do not modify it.
3.  **One-Time Use:** Each target URL from the list must be used only ONCE.
4.  **Preserve Content:** Do not add, remove, or change any of the original article content besides inserting the required links.
5.  **Link Format:** Use the standard HTML anchor tag format: `<a href="TARGET_URL">Anchor Text</a>`.

---

**## Article Content ##**

{article_content}

---

**## Links to Insert ##**

{links_to_insert}
"""
    final_prompt = prompt_template.format(
    article_content=content, 
    links_to_insert=links_to_insert_str
    )
    modified_content = await call_gemini(final_prompt, max_output_tokens=4000, temperature=0.1)
    return modified_content if modified_content else content

async def prompt_for_html_conversion_gemini(article: str) -> str:
    """Convert an article into clean HTML format using Gemini."""
    prompt = f"""
    Convert the following article into clean HTML format using semantic tags like <article>, <header>, <h1>, <h2>, <p>, <a>, <ul>, <ol>, <li> where appropriate.
    Ensure all existing hyperlinks (specifically `<a>` tags or framework-specific link components) are preserved exactly as they are.
    Do not invent new content, new links, or modify the text content of existing links. Focus solely on structural HTML conversion.

    --- ARTICLE START ---

    {article}

    --- ARTICLE END ---
    """

    html_format_content = await call_gemini(prompt, max_output_tokens=5000)
    return html_format_content if html_format_content else article

# --- FastAPI Endpoint ---
@app.post("/build-links", response_model=LinkBuildResponse)
async def build_internal_links(request: LinkBuildRequest):
    """Main endpoint to build internal links in content using Google Gemini."""
    sanitized_content = sanitize_content(request.content)

    can_crawl, sitemap_urls = is_crawling_allowed(str(request.main_url))
    if not can_crawl:
        raise HTTPException(status_code=403, detail="Crawling not allowed by robots.txt for the main URL.")

    # 1. Extract Keywords using Gemini
    keywords = await extract_keywords_gemini(sanitized_content, top_n=10)
    if not keywords:
        print("No keywords extracted, returning original content.")
        html_format_content = await prompt_for_html_conversion_gemini(sanitized_content)
        return LinkBuildResponse(
            modified_content=sanitized_content,
            inserted_links=[],
            html_format_content=html_format_content
        )

    # 2. Get Target URLs
    if request.plateform == "wordpress" and request.wp_base_url:
        urls = get_wordpress_urls(str(request.wp_base_url))
        print(urls)
    else:
        urls = crawl_urls(str(request.main_url))

    if not urls:
        print("No URLs found, returning original content.")
        html_format_content = await prompt_for_html_conversion_gemini(sanitized_content)
        return LinkBuildResponse(
            modified_content=sanitized_content,
            inserted_links=[],
            html_format_content=html_format_content
        )

    # 3. Match URLs to Keywords
    matched_urls_data = await match_urls_to_keywords_gemini(urls, keywords, sanitized_content, request.num_links)
    inserted_links_info = [
        {
            "url": item["url"],
            "keyword": item.get("keyword", ""),
            "anchor_text": item["anchor_text"],
            "reason": item.get("reason", "No reason provided."),
            "similarity": 1.0
        }
        for item in matched_urls_data
    ]

    # 4. Insert Links into Content
    parsed_main_url = urlparse(str(request.main_url))
    main_url_domain = f"{parsed_main_url.scheme}://{parsed_main_url.netloc}"
    modified_content = await insert_links_gemini(sanitized_content, inserted_links_info, request.plateform, main_url_domain)

    # 5. Convert to HTML Format
    html_format_content = await prompt_for_html_conversion_gemini(modified_content)

    return LinkBuildResponse(
        modified_content=modified_content,
        inserted_links=inserted_links_info, 
        html_format_content=html_format_content
    )

# --- Run the Application ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)