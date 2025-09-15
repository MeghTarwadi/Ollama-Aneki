from ddgs import DDGS
from bs4 import BeautifulSoup
import ollama
from ollama import chat
from rich import print as rprint

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


class Search:
    def getData(prompt, keyword):

        if keyword not in prompt:
            return prompt

        original_prompt = prompt

        def build_query(current):
            return f'Generate a list of search queries. Input Query: "{current}" \nprevious conversation : [] \n\nOutput:'

        # Ask LLM to generate queries
        query_prompt = build_query(prompt.replace(keyword, ""))

        # Ensure the fine-tuned model is available
        available_models = [model.model for model in ollama.list().models]
        model_name = "hf.co/MEGHT/qwen3-finetuned-search"

        if not any(model_name in m for m in available_models):
            rprint("{blue} Downloading model for search...")
            ollama.pull(model_name)

        # Query the model for search suggestions
        response = chat(
            model=model_name,
            messages=[{"role": "user", "content": query_prompt}],
        )

        search_queries = response["message"]["content"].split("\n")
        # print(search_queries)
        search_queries = search_queries[4:-2]  # Only take top 3 queries
        rprint(f"[bold yellow]Generated Queries:[/bold yellow] {search_queries}")

        # Function to scrape visible text from a webpage
        def extract_text_from_url(url):
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                resp = requests.get(url, headers=headers, timeout=10)
                resp.raise_for_status()
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                return ""

            soup = BeautifulSoup(resp.text, "html.parser")

            # Remove unnecessary tags
            for tag in soup(["script", "style", "noscript"]):
                tag.extract()

            return " ".join(soup.stripped_strings)

        # Collect and process top 2 links per query using DuckDuckGo
        extracted_information = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = []

            with DDGS() as ddgs:
                for query in search_queries:
                    urls = [r["href"] for r in ddgs.text(query, max_results=2)]
                    print(f"Query: {query}, URLs: {urls}")

                    for url in urls:
                        future = executor.submit(extract_text_from_url, url)
                        future_to_url.append(future)

            for future in as_completed(future_to_url):
                text = future.result()
                if text:
                    extracted_information.append(text)

        # Final output
        result = (
            f"Original Prompt: {original_prompt}\n"
            f"Extracted Information: {extracted_information}"
        )
        return result
