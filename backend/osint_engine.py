from typing import List, Dict, Optional
import json

class OSINTMatrixGenerator:
    def __init__(self, target_username: str):
        self.target_username = target_username

    def generate_dork_matrix(self) -> Dict[str, List[str]]:
        """
        Generates the exhaustive 20+ OSINT Google Dork query matrix based on the strategy plan.
        """
        u = self.target_username
        
        matrix = {
            "Phase 1: Direct Platform": [
                f'site:instagram.com/p/ "{u}"',
                f'site:instagram.com/reel/ "{u}"',
                f'site:instagram.com "{u}" -site:instagram.com/{u}',
                f'site:instagram.com "{u}" AND ("commented" OR "replied")',
                f'site:instagram.com "{u}" "liked this"',
                f'site:instagram.com inurl:comments "{u}"'
            ],
            "Phase 2: Shadow Network": [
                f'site:picuki.com "{u}" "comments"',
                f'site:picuki.com intext:"{u}"',
                f'site:imginn.com "{u}"',
                f'site:imginn.com intext:"{u}"',
                f'site:dumpor.com "{u}"',
                f'site:dumpor.com "comment" "{u}"',
                f'site:greatfon.com "{u}"',
                f'site:instanavigation.com "{u}"'
            ],
            "Phase 3: Cross-Platform & Brand Footprint": [
                f'"{u}" "instagram"',
                f'"{u}" "ig"',
                f'site:tiktok.com "{u}" "instagram"',
                f'site:tiktok.com intext:"{u}" "ig"',
                f'site:twitter.com "{u}" "instagram"',
                f'site:x.com "{u}" "ig"',
                f'site:reddit.com "{u}" "instagram"',
                f'site:facebook.com "{u}" "instagram"'
            ]
        }
        
        return matrix

    def fetch_high_probability_dorks(self) -> List[str]:
        """
        Returns the top 3 highest probability queries for immediate extraction.
        """
        u = self.target_username
        return [
            f'site:instagram.com/p/ "{u}"',
            f'site:picuki.com "{u}" "comments"',
            f'site:instagram.com "{u}" -site:instagram.com/{u}'
        ]

class OSINTDataParser:
    @staticmethod
    def parse_raw_search_result(snippet: str, url: str, target_username: str) -> Optional[Dict]:
        """
        Decodes a raw text search snippet and infers the comment context.
        """
        snippet_lower = snippet.lower()
        if target_username.lower() not in snippet_lower:
            return None
            
        return {
            "target_username": target_username,
            "url": url,
            "inferred_context": snippet,
            "platform_source": "Instagram" if "instagram.com" in url else "Shadow Network",
            "is_direct_comment_match": "commented" in snippet_lower or "replied" in snippet_lower
        }
