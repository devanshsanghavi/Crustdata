__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
from dotenv import load_dotenv
load_dotenv()

# Defining the LLM we will using. I'm using a Llama-3.3 inference from Groq. Using Groq makes our application run much faster.
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=1,
    groq_api_key=os.getenv("API_KEY"),
    max_tokens=32768
)

# This is some text I scrapped from the documentation using ChatGPT. I tried many different techniques to scrape text (they are all given at the end), but came across various issues. So for now, I have used this. If all the API documentation is stored in a different format that could be easy to scrape, I would love to use that.
scrappedText = """
**Company Endpoint**

**1. Enrichment: Company Data API**
- **Overview**: Retrieve detailed data about one or multiple companies using domain, name, LinkedIn URL, or company ID.
- **Required**: Authentication token (`auth_token`).
- **Request Parameters**:
  - `company_domain`: Comma-separated list of domains (e.g., `hubspot.com`).
  - `company_name`: Comma-separated list of names (e.g., `"Google, Inc."`).
  - `company_linkedin_url`: Comma-separated list of LinkedIn URLs.
  - `company_id`: List of IDs for pre-ingested companies.
  - `fields`: Specify desired fields for response (e.g., `company_name,headcount`).
  - `enrich_realtime`: Boolean, triggers real-time enrichment (default: `False`).

**Response Structure**:
- `company_id`: integer
- `company_name`: string
- `linkedin_profile_url`: string
- `hq_country`: string
- `year_founded`: string
- `headcount`: integer
- `revenue_range`: string

**Key Points**:
- Use `fields` to reduce payload size.
- Real-time enrichment takes approximately 10 minutes.

**Examples**:
- By Domain:
  ```bash
  curl 'https://api.crustdata.com/screener/company?company_domain=hubspot.com' \
  --header 'Authorization: Token $token'
  ```

---
**Company Endpoint**

**2. Company Discovery: Screening API**
- **Overview**: Screen/filter companies using firmographic and growth metrics.
- **Required**: Authentication token (`auth_token`).
- **Request Parameters**:
  - `metrics`: Specify columns for response (e.g., `linkedin_headcount`).
  - `filters`: Filter conditions (e.g., `revenue > $1M`).
  - `offset`: Starting result point (default: 0).
  - `count`: Number of results (default: 100).

**Response Structure**:
- `fields`: Array of requested columns.
- `rows`: Data rows corresponding to `fields`.

**Examples**:
- Screen companies with headcount > 50 in the US:
  ```json
  {
    "metrics": [{"metric_name": "linkedin_headcount"}],
    "filters": {
      "op": "and",
      "conditions": [
        {"column": "linkedin_headcount", "type": ">", "value": 50},
        {"column": "largest_headcount_country", "type": "=", "value": "USA"}
      ]
    },
    "count": 100
  }
  ```

---
**Company Endpoint**

**3. Company Identification API**
- **Overview**: Identify a company using name, website, or LinkedIn profile URL.
- **Required**: Authentication token (`auth_token`).
- **Request Parameters**:
  - `query_company_name`: Name of the company.
  - `query_company_website`: Website URL.
  - `query_company_linkedin_url`: LinkedIn profile URL.
  - `count`: Max number of results (default: 10).

**Response Structure**:
- `company_id`: integer
- `company_name`: string
- `company_website`: string
- `linkedin_profile_url`: string
- `headcount`: integer
- `score`: float

**Examples**:
- Identify 'Serve Robotics':
  ```bash
  curl 'https://api.crustdata.com/screener/identify/' \
  --data '{"query_company_name": "Serve Robotics"}' \
  --header 'Authorization: Token $token'
  ```

---
**Company Endpoint**

**4. Company Dataset API**
- **Overview**: Retrieve specific datasets related to companies, such as job listings, decision-makers, news articles, and G2 reviews.
- **Required**: Authentication token (`auth_token`).
- **Request Parameters**:
  - `filters`: Conditions for data (e.g., job openings > 10).
  - `count`: Number of records to retrieve (default: 100).

**Response Structure**:
- `fields`: Attributes of the dataset.
- `rows`: Data rows corresponding to `fields`.

**Examples**:
- Retrieve job listings:
  ```bash
  curl 'https://api.crustdata.com/data_lab/job_listings/Table/' \
  --data '{"filters": {"op": "and", "conditions": [{"column": "job_openings_count", "type": ">", "value": 10}]}, "count": 100}' \
  --header 'Authorization: Token $token'
  ```

---
**Company Endpoint**

**5. Search: LinkedIn Company Search API (real-time)**
- **Overview**: Search for company profiles using LinkedIn Sales Navigator search URLs or custom filters.
- **Required**: Authentication token (`auth_token`).
- **Request Parameters**:
  - `linkedin_sales_navigator_search_url`: URL from Sales Navigator.
  - `filters`: Custom search criteria as JSON.

**Response Structure**:
- List of company profiles matching the criteria.

**Examples**:
- Search using Sales Navigator URL:
  ```bash
  curl 'https://api.crustdata.com/screener/company/search/' \
  --data '{"linkedin_sales_navigator_search_url": "<Sales Navigator URL>"}' \
  --header 'Authorization: Token $token'
  ```

---
**Company Endpoint**

**6. LinkedIn Posts by Company API (real-time)**
- **Overview**: Retrieve real-time LinkedIn posts made by companies.
- **Required**: Authentication token (`auth_token`).
- **Request Parameters**:
  - `company_id`: List of company IDs.
  - `fields`: Specify desired fields for posts (e.g., `post_content,likes_count`).

**Response Structure**:
- Array of LinkedIn posts with specified attributes.

**Examples**:
- Retrieve posts by company ID:
  ```bash
  curl 'https://api.crustdata.com/screener/posts/company/' \
  --data '{"company_id": [12345], "fields": ["post_content", "likes_count"]}' \
  --header 'Authorization: Token $token'
  ```

---
**Company Endpoint**

**7. LinkedIn Posts Keyword Search (real-time)**
- **Overview**: Search LinkedIn posts in real-time using specific keywords.
- **Required**: Authentication token (`auth_token`).
- **Request Parameters**:
  - `keywords`: List of keywords to search for.
  - `fields`: Specify desired fields for posts.

**Response Structure**:
- Array of LinkedIn posts containing the keywords.

**Examples**:
- Search posts with keywords:
  ```bash
  curl 'https://api.crustdata.com/screener/posts/keywords/' \
  --data '{"keywords": ["AI", "Machine Learning"], "fields": ["post_content", "author"]}' \
  --header 'Authorization: Token $token'
  ```

---

**People Endpoint**

**1. Enrichment: People Profile(s) API**
- **Overview**: Retrieve enriched profile data for individuals using LinkedIn URLs.
- **Required**: Authentication token (`auth_token`).
- **Request Parameters**:
  - `linkedin_url`: LinkedIn profile URL(s).
  - `fields`: Comma-separated list of fields to include in the response (e.g., `name,position`).

**Response Structure**:
- `name`: string
- `linkedin_profile_url`: string
- `position`: string
- `company`: string

**Examples**:
- By LinkedIn URL:
  ```bash
  curl 'https://api.crustdata.com/screener/people?linkedin_url=https://linkedin.com/in/example' \
  --header 'Authorization: Token $token'
  ```

---
**People Endpoint**

**2. Search: LinkedIn People Search API (real-time)**
- **Overview**: Search for LinkedIn profiles using custom filters.
- **Required**: Authentication token (`auth_token`).
- **Request Parameters**:
  - `filters`: Custom search criteria as JSON.

**Response Structure**:
- List of LinkedIn profiles matching the criteria.

**Examples**:
- Search by filters:
  ```bash
  curl 'https://api.crustdata.com/screener/people/search/' \
  --data '{"filters": {"current_title": "CEO", "region": "USA"}}' \
  --header 'Authorization: Token $token'
  ```

---
**People Endpoint**

**3. LinkedIn Posts by Person API (real-time)**
- **Overview**: Retrieve LinkedIn posts made by specific individuals in real-time.
- **Required**: Authentication token (`auth_token`).
- **Request Parameters**:
  - `person_id`: List of person IDs.
  - `fields`: Specify desired fields for posts (e.g., `post_content,likes_count`).

**Response Structure**:
- Array of LinkedIn posts with specified attributes.

**Examples**:
- Retrieve posts by person ID:
  ```bash
  curl 'https://api.crustdata.com/screener/posts/person/' \
  --data '{"person_id": [12345], "fields": ["post_content", "likes_count"]}' \
  --header 'Authorization: Token $token'
  ```

---

**API Usage Endpoint**

**1. Get Remaining Credits**
- **Overview**: Retrieve the remaining credit balance for API usage.
- **Required**: Authentication token (`auth_token`).
- **Request Parameters**: None.

**Response Structure**:
- `remaining_credits`: integer

**Examples**:
- Check remaining credits:
  ```bash
  curl 'https://api.crustdata.com/usage/credits/' \
  --header 'Authorization: Token $token'
  ```

"""

# This just splits the text into chunks.
arr = scrappedText.split("---")

# Storing these chunks in a vector database. This helps because we easily retrieve chunks that our relevant to the user's question and then use them to answer the question.
import chromadb
client = chromadb.PersistentClient("vectorstore")
collection = client.get_or_create_collection(name="Crustdata")
for index, data in enumerate(arr):
  collection.add(
    documents=[data],
    ids=[str(index)]
  )

# Defining the final function that we will use to retrieve the relevant data and then answer the question.
from langchain_core.prompts import PromptTemplate
def answer(question):
  prompt = PromptTemplate.from_template(
      """
      ### These are some text chunks scrapped from Crustdata's API documentation website which are relevant to the question:
      {text}

      ### Some more context:
      The Crustdata API gives you programmatic access to firmographic and growth metrics data for companies across the world from more than 16 datasets (Linkedin headcount, Glassdoor, Instagram, G2, Web Traffic, Apple App Store reviews, Google Play Store, News among others). This documentation describes various available API calls and schema of the response. If you have any questions, please reach out to [abhilash@crustdata.com].

      ### Your task:
      Use these chunks to answer the following question: {question}
      """
  )
  chain = prompt | llm
  queryResult = collection.query(query_texts=[question], n_results=3)["documents"] # This query will get the 3 most relevant chunks
  res = chain.invoke(input={"question": question, "text": queryResult}) # We finally call the LLM here
  return res.content

# answer("How do I search for people given their current title, current company and location?")

import streamlit as st
st.title("Crustdata Customer Support Agent")
userInput = st.text_input("Enter your question...")
submitButton = st.button("Submit")
if submitButton:
  st.text(answer(userInput))