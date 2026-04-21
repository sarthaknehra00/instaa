import time
import random
from typing import List, Dict
from duckduckgo_search import DDGS

class InstagramCommentScraper:
    def __init__(self, target_username: str):
        self.target_username = target_username
        self.found_comments = []

    def get_osint_queries(self) -> List[str]:
        """
        Returns the exhaustive Master OSINT Dork List.
        """
        u = self.target_username
        master_list = [
            # Direct Platform Scrape
            f'site:instagram.com "{u}" -site:instagram.com/{u}',
            f'site:instagram.com/p/ "{u}"',
            f'site:instagram.com/reel/ "{u}"',
            f'site:instagram.com/tv/ "{u}"',
            f'site:instagram.com/stories/ "{u}"',
            f'site:instagram.com "{u}" "comments"',
            f'site:instagram.com "{u}" "replied"',
            f'site:instagram.com "{u}" "commented"',
            f'site:instagram.com intext:"@{u}"',
            f'site:instagram.com "{u}" "Log in to like or comment"',
            
            # Third-Party Proxy Scrape
            f'site:picuki.com "{u}" "comments"',
            f'site:dumpor.com "{u}"',
            f'site:greatfon.com "{u}"',
            f'site:instanavigation.com "{u}"',
            f'site:iganony.com "{u}"',
            f'site:pixwox.com "{u}"',
            f'site:گرام.io "{u}"',
            f'site:saveig.app "{u}"',
            
            # Multi-Proxy Mega-Searches
            f'"{u}" (site:picuki.com OR site:dumpor.com OR site:greatfon.com)',
            f'"{u}" "comments" (site:pixwox.com OR site:instanavigation.com OR site:iganony.com)',
            f'intext:"{u}" (site:picuki.com OR site:dumpor.com)',
            
            # Cross-Platform Spillage
            f'site:tiktok.com "{u}" "instagram"',
            f'site:twitter.com "{u}" ("ig" OR "instagram")',
            f'site:x.com "{u}" ("ig" OR "instagram")',
            f'site:reddit.com "{u}" "instagram"',
            f'site:pinterest.com "{u}" "instagram"',
            f'site:twitch.tv "{u}" "instagram"',
            
            # Link Aggregators
            f'site:linktr.ee "{u}" "instagram"',
            f'site:campsite.bio "{u}" "instagram"',
            
            # Global Catch-Alls
            f'"{u}" "instagram comment"',
            f'intext:"{u}" "instagram.com/p/"',
            f'"{u}" "instagram.com/reel/"',
            f'"{u}" "photo" "instagram"',
        ]
        
        # Anti-Bot Strategy: Executing 40 complex boolean dorks in a loop will 
        # instantly trigger a 24-hour IP shadowban from DuckDuckGo resulting in [] response.
        # We take a randomized sample of 5 queries per run to stay stealthy.
        sampled_queries = random.sample(master_list, min(5, len(master_list)))
        
        # Inject an "organic" search explicitly designed to bypass DuckDuckGo's aggressive bot parser 
        # (which sometimes blindly blocks double-quotes and site: endpoints).
        organic_fallback = f'{u} instagram comment reply'
        sampled_queries.append(organic_fallback)
        
        return sampled_queries

    def parse_snippet_for_context(self, text_snippet: str, title: str, url: str) -> Dict:
        """
        Parses the raw Google / DuckDuckGo SERP text into the UI format.
        """
        # Determine Source
        source = "Instagram Direct"
        if "picuki" in url or "imginn" in url or "dumpor" in url:
            source = "Shadow Network Proxy"

        # Provide a safe post ID or shortcode
        post_id = url.split("/")[-2] if "instagram.com/p/" in url else "unknown_id"

        return {
            "id": str(time.time()),
            "post_id": post_id,
            "text": text_snippet.replace('\n', ' ').strip(),
            "timestamp": "Recently Indexed by Global Search",
            # We use a generic avatar fallback because we don't download actual images from proxies
            "post_thumbnail": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=500&auto=format&fit=crop&q=60", 
            "original_post_url": url,
            "source": source
        }

    def scan_target_posts(self, update_progress_callback=None) -> List[Dict]:
        """
        The Main Entrypoint used by main.py.
        Executes headless SERP OSINT scraping totally removing Instaloader/Playwright requirements.
        """
        try:
            if update_progress_callback:
                update_progress_callback(f"Deploying Automated OSINT Search Engine protocol for @{self.target_username}...")
            
            queries = self.get_osint_queries()
            ddgs = DDGS()
            
            for query in queries:
                if update_progress_callback:
                    update_progress_callback(f"Executing Deep Dork: {query}")
                
                try:
                    # Execute DDG search API synchronously
                    results = ddgs.text(query, max_results=8)
                    for res in results:
                        title = res.get('title', '')
                        body = res.get('body', '')
                        href = res.get('href', '')
                        
                        # Data Verification: Ensure the target is actually mentioned
                        if self.target_username.lower() in body.lower() or self.target_username.lower() in title.lower():
                            parsed_data = self.parse_snippet_for_context(body, title, href)
                            self.found_comments.append(parsed_data)
                            
                except Exception as e:
                    print(f"Error executing dork {query}: {e}")
                    
                time.sleep(2) # Protect against DuckDuckGo API Rate Limits
                
            # Aggregate and Deduplicate by Target URL
            unique_comments = {comment['original_post_url']: comment for comment in self.found_comments}.values()
            self.found_comments = list(unique_comments)

            if not self.found_comments:
                if update_progress_callback:
                    update_progress_callback(f"No indexed footprints located for @{self.target_username}.")
            else:
                 if update_progress_callback:
                    update_progress_callback(f"Extraction Complete! Intercepted {len(self.found_comments)} global results.")

            return self.found_comments

        except Exception as e:
            if update_progress_callback:
                update_progress_callback(f"OSINT Pipeline Error: {str(e)}")
            return self.found_comments
