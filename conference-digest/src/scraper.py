"""
Main scraper module for fetching conference data from various sources
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import feedparser
import json
from src.config import CONFERENCE_SOURCES, ALLOWED_COUNTRIES, NEGATIVE_KEYWORDS


class ConferenceScraper:
    """Scrape conference data from multiple sources"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch_all_sources(self) -> List[Dict]:
        """Fetch conferences from all configured sources"""
        all_conferences = []
        
        for source in CONFERENCE_SOURCES:
            try:
                if source['type'] == 'rss':
                    conferences = self.fetch_rss(source)
                elif source['type'] == 'html':
                    conferences = self.fetch_html(source)
                elif source['type'] == 'search':
                    conferences = self.fetch_search_based(source)
                else:
                    conferences = []
                
                all_conferences.extend(conferences)
                print(f"Fetched {len(conferences)} conferences from {source['name']}")
            except Exception as e:
                print(f"Error fetching {source['name']}: {str(e)}")
        
        return all_conferences
    
    def fetch_rss(self, source: Dict) -> List[Dict]:
        """Fetch from RSS feeds"""
        conferences = []
        
        try:
            feed = feedparser.parse(source['url'])
            
            for entry in feed.entries:
                conference = {
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'description': entry.get('description', entry.get('summary', '')),
                    'date': entry.get('published', ''),
                    'source': source['name'],
                    'location': '',
                    'deadline': '',
                    'conference_date': '',
                    'topics': [],
                    'publisher': '',
                    'indexing': [],
                }
                
                # Try to extract location from description
                conf = self.parse_description(conference)
                conferences.append(conf)
        except Exception as e:
            print(f"RSS fetch error for {source['name']}: {str(e)}")
        
        return conferences
    
    def fetch_html(self, source: Dict) -> List[Dict]:
        """Fetch from HTML pages"""
        conferences = []
        
        try:
            response = self.session.get(source['url'], timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Generic extraction - will need site-specific parsers
            conference_links = []
            
            # Look for common conference link patterns
            for link in soup.find_all('a', href=True):
                href = link['href'].lower()
                text = link.get_text().lower()
                
                if any(keyword in text or keyword in href for keyword in 
                      ['conference', 'symposium', 'workshop', 'call for paper', 'cfp']):
                    conference_links.append({
                        'text': link.get_text().strip(),
                        'url': link['href'] if link['href'].startswith('http') else source['url'] + link['href']
                    })
            
            # Limit to first 20 to avoid overwhelming
            for link_info in conference_links[:20]:
                conference = {
                    'title': link_info['text'],
                    'url': link_info['url'],
                    'description': '',
                    'date': '',
                    'source': source['name'],
                    'location': '',
                    'deadline': '',
                    'conference_date': '',
                    'topics': [],
                    'publisher': '',
                    'indexing': [],
                }
                
                # Try to fetch detail page
                conf = self.fetch_detail_page(conference)
                conferences.append(conf)
                
        except Exception as e:
            print(f"HTML fetch error for {source['name']}: {str(e)}")
        
        return conferences
    
    def fetch_detail_page(self, conference: Dict) -> Dict:
        """Fetch detailed information from conference page"""
        try:
            response = self.session.get(conference['url'], timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get full page text
            page_text = soup.get_text().lower()
            conference['description'] = page_text[:2000]  # First 2000 chars
            
            # Parse dates and locations
            conference = self.parse_description(conference)
            
        except Exception as e:
            print(f"Detail page fetch error: {str(e)}")
        
        return conference
    
    def fetch_search_based(self, source: Dict) -> List[Dict]:
        """Search-based discovery using Google/Bing search queries"""
        conferences = []
        
        search_queries = [
            "call for papers Malaysia energy conference 2025 2026",
            "call for papers artificial intelligence conference Asia Pacific 2025 2026",
            "call for papers machine learning conference Europe 2025 2026",
            "call for papers environmental science conference Malaysia 2025 2026",
            "call for papers economics conference Asia 2025 2026",
            "call for papers engineering conference Malaysia 2025 2026",
            "call for abstracts sustainability conference 2025 2026",
            "CFP renewable energy conference 2025 2026",
            "paper submission deadline AI ML conference 2025 2026",
            "academic conference call for papers Europe 2025 2026",
        ]
        
        # Note: In production, use Google Custom Search API or Serper API
        # For now, we'll generate mock results based on queries
        for query in search_queries:
            # This would normally call a search API
            # For MVP, we create placeholder entries
            conference = {
                'title': f"Conference related to: {query[:50]}...",
                'url': '',
                'description': query,
                'date': '',
                'source': 'search_discovery',
                'location': '',
                'deadline': '',
                'conference_date': '',
                'topics': [],
                'publisher': '',
                'indexing': [],
            }
            conferences.append(conference)
        
        return conferences
    
    def parse_description(self, conference: Dict) -> Dict:
        """Extract structured data from conference description"""
        text = conference.get('description', '') + ' ' + conference.get('title', '')
        text_lower = text.lower()
        
        # Extract location
        location = self.extract_location(text)
        conference['location'] = location
        
        # Extract dates
        dates = self.extract_dates(text)
        conference['deadline'] = dates.get('deadline', '')
        conference['conference_date'] = dates.get('conference_date', '')
        conference['notification_date'] = dates.get('notification_date', '')
        
        # Extract topics
        topics = self.extract_topics(text)
        conference['topics'] = topics
        
        # Extract publisher
        publisher = self.extract_publisher(text)
        conference['publisher'] = publisher
        
        return conference
    
    def extract_location(self, text: str) -> str:
        """Extract location from text"""
        location_patterns = [
            r'(?:location|place|venue|held in|held at|city)[:\s]+([^\n,]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+),?\s+(?:Malaysia|Singapore|Thailand|Indonesia|Europe|Asia)',
            r'(?:Malaysia|Singapore|Thailand|Indonesia|Philippines|Vietnam|Europe|Asia Pacific)',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).strip()
        
        # Check for online/hybrid
        if any(word in text.lower() for word in ['online', 'virtual', 'hybrid', 'remote']):
            return 'Online/Hybrid'
        
        return ''
    
    def extract_dates(self, text: str) -> Dict:
        """Extract various dates from text"""
        dates = {
            'deadline': '',
            'conference_date': '',
            'notification_date': ''
        }
        
        # Date patterns
        date_pattern = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})'
        
        # Submission deadline
        deadline_match = re.search(r'(?:submission deadline|abstract deadline|paper deadline|deadline)[:\s]+' + date_pattern, text, re.IGNORECASE)
        if deadline_match:
            dates['deadline'] = deadline_match.group(1)
        
        # Conference date
        conf_match = re.search(r'(?:conference date|event date|held on|dates)[:\s]+' + date_pattern, text, re.IGNORECASE)
        if conf_match:
            dates['conference_date'] = conf_match.group(1)
        
        # Notification date
        notif_match = re.search(r'(?:notification|acceptance notice|result)[:\s]+' + date_pattern, text, re.IGNORECASE)
        if notif_match:
            dates['notification_date'] = notif_match.group(1)
        
        return dates
    
    def extract_topics(self, text: str) -> List[str]:
        """Extract topics from text"""
        from src.config import TOPICS
        
        found_topics = []
        text_lower = text.lower()
        
        for topic in TOPICS:
            if topic.lower() in text_lower:
                found_topics.append(topic)
        
        return found_topics[:10]  # Limit to top 10
    
    def extract_publisher(self, text: str) -> str:
        """Extract publisher information"""
        from src.config import PREFERRED_PUBLISHERS
        
        for publisher in PREFERRED_PUBLISHERS:
            if publisher.lower() in text.lower():
                return publisher
        
        return ''
    
    def is_relevant(self, conference: Dict) -> bool:
        """Check if conference is relevant based on filters"""
        title = conference.get('title', '').lower()
        description = conference.get('description', '').lower()
        location = conference.get('location', '').lower()
        
        # Check negative keywords
        for keyword in NEGATIVE_KEYWORDS:
            if keyword.lower() in title or keyword.lower() in description:
                return False
        
        # Check location filter
        if location:
            is_allowed = any(country in location for country in ALLOWED_COUNTRIES)
            if not is_allowed and 'online' not in location and 'virtual' not in location and 'hybrid' not in location:
                return False
        
        # Check if has topics
        if not conference.get('topics'):
            return False
        
        return True
