import os

import requests
from dotenv import load_dotenv


load_dotenv()


class NewsService:

    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")

        self.base_url = (
            "https://newsapi.org/v2/everything"
        )

        if not self.api_key:
            raise ValueError(
                "NEWS_API_KEY is not configured in .env"
            )

    def get_energy_risk_news(
        self,
        page_size: int = 10,
    ):
        """
        Fetch recent geopolitical, oil, maritime,
        and energy supply-chain intelligence.
        """

        # More focused search than simply searching "oil"
        query = (
            '"crude oil" OR '
            '"oil supply" OR '
            '"oil exports" OR '
            '"oil imports" OR '
            '"oil tanker" OR '
            '"energy supply" OR '
            '"energy security" OR '
            '"Strait of Hormuz" OR '
            '"Red Sea shipping" OR '
            '"shipping disruption" OR '
            '"tanker disruption" OR '
            '"port disruption" OR '
            '"energy sanctions" OR '
            '"oil sanctions" OR '
            '"refinery disruption"'
        )

        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",

            # Fetch more articles first because we
            # apply an additional relevance filter below.
            "pageSize": min(
                max(page_size * 3, 20),
                100,
            ),

            "apiKey": self.api_key,
        }

        # At least one of these terms must occur in the
        # title or description before the article reaches
        # the Live News Intelligence dashboard.
        relevant_keywords = [
            "crude",
            "oil supply",
            "oil export",
            "oil import",
            "oil price",
            "oil tanker",
            "tanker",
            "petroleum",
            "lng",
            "natural gas",
            "energy supply",
            "energy security",
            "refinery",
            "pipeline",
            "shipping",
            "maritime",
            "port",
            "hormuz",
            "red sea",
            "suez",
            "sanction",
            "opec",
            "geopolitical",
            "supply disruption",
            "supply chain",
        ]

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=15,
            )

            response.raise_for_status()

            data = response.json()

            articles = []

            for article in data.get(
                "articles",
                [],
            ):
                title = (
                    article.get("title")
                    or ""
                )

                description = (
                    article.get("description")
                    or ""
                )

                # Combine searchable article content.
                searchable_text = (
                    f"{title} {description}"
                ).lower()

                # Reject unrelated articles.
                is_relevant = any(
                    keyword in searchable_text
                    for keyword in relevant_keywords
                )

                if not is_relevant:
                    continue

                articles.append({
                    "title": title,
                    "description": description,
                    "source": (
                        article.get(
                            "source",
                            {},
                        ).get("name")
                    ),
                    "url": article.get("url"),
                    "published_at": article.get(
                        "publishedAt"
                    ),
                    "image_url": article.get(
                        "urlToImage"
                    ),
                })

                # Stop after requested number
                # of relevant articles.
                if len(articles) >= page_size:
                    break

            return {
                "status": "success",
                "total_results": len(articles),
                "articles": articles,
            }

        except requests.RequestException as e:
            return {
                "status": "error",
                "message": str(e),
                "articles": [],
            }


news_service = NewsService()