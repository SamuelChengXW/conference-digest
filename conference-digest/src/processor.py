"""
Conference processor: filtering, scoring, deduplication
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict
import hashlib
from src.config import (
    DEADLINE_WINDOW_DAYS, MIN_DEADLINE_DAYS, MIN_RELEVANCE_SCORE,
    SCORE_WEIGHTS, PREFERRED_PUBLISHERS
)


class ConferenceProcessor:
    """Process, filter, score, and deduplicate conferences"""
    
    def __init__(self):
        self.today = datetime.now()
    
    def process_all(self, conferences: List[Dict], existing_conferences: List[Dict] = None) -> List[Dict]:
        """Process all conferences through the pipeline"""
        if existing_conferences is None:
            existing_conferences = []
        
        processed = []
        
        for conf in conferences:
            # Step 1: Validate and normalize
            normalized = self.normalize(conf)
            
            # Step 2: Check relevance
            if not self.is_relevant(normalized):
                continue
            
            # Step 3: Validate deadline
            if not self.validate_deadline(normalized):
                continue
            
            # Step 4: Calculate relevance score
            scored = self.calculate_score(normalized)
            
            # Step 5: Filter by minimum score
            if scored['relevance_score'] < MIN_RELEVANCE_SCORE:
                continue
            
            processed.append(scored)
        
        # Step 6: Deduplicate
        deduplicated = self.deduplicate(processed, existing_conferences)
        
        # Step 7: Sort by deadline
        sorted_confs = self.sort_by_deadline(deduplicated)
        
        return sorted_confs
    
    def normalize(self, conference: Dict) -> Dict:
        """Normalize conference data to standard format"""
        now = datetime.now()
        
        # Generate unique ID
        title_hash = hashlib.md5(conference.get('title', '').encode()).hexdigest()[:12]
        conf_id = f"conf_{now.strftime('%Y')}_{title_hash}"
        
        # Parse dates
        deadline = self.parse_date(conference.get('deadline', ''))
        conf_start = self.parse_date(conference.get('conference_date', ''))
        conf_end = conf_start  # Default same as start
        
        # Determine mode
        location = conference.get('location', '').lower()
        if 'online' in location or 'virtual' in location:
            if 'hybrid' in location:
                mode = 'Hybrid'
            else:
                mode = 'Online'
        else:
            mode = 'In-Person'
        
        # Extract country
        country = self.extract_country(conference.get('location', ''))
        
        normalized = {
            'id': conf_id,
            'title': conference.get('title', '').strip(),
            'url': conference.get('url', ''),
            'cfp_url': conference.get('cfp_url', conference.get('url', '')),
            'location': conference.get('location', ''),
            'country': country,
            'mode': mode,
            'topics': conference.get('topics', []),
            'abstract_deadline': deadline,
            'paper_deadline': deadline,  # Default same as abstract
            'notification_date': self.parse_date(conference.get('notification_date', '')),
            'conference_start_date': conf_start,
            'conference_end_date': conf_end,
            'publisher': conference.get('publisher', ''),
            'indexing': conference.get('indexing', []),
            'source': conference.get('source', 'unknown'),
            'first_seen': now.strftime('%Y-%m-%d'),
            'last_verified': now.strftime('%Y-%m-%d'),
            'relevance_score': 0.0,
            'status': 'open',
            'notes': '',
            'description': conference.get('description', '')[:500],
        }
        
        return normalized
    
    def parse_date(self, date_str: str) -> str:
        """Parse various date formats to YYYY-MM-DD"""
        if not date_str:
            return ''
        
        date_formats = [
            '%d-%m-%Y', '%d/%m/%Y', '%m-%d-%Y', '%m/%d/%Y',
            '%Y-%m-%d', '%Y/%m/%d',
            '%d %B %Y', '%d %b %Y', '%B %d, %Y', '%b %d, %Y',
            '%d %B %y', '%d %b %y',
        ]
        
        for fmt in date_formats:
            try:
                parsed = datetime.strptime(date_str.strip(), fmt)
                return parsed.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        return ''
    
    def extract_country(self, location: str) -> str:
        """Extract country from location string"""
        countries = [
            'Malaysia', 'Singapore', 'Thailand', 'Indonesia', 'Philippines',
            'Vietnam', 'Cambodia', 'Laos', 'Myanmar', 'Brunei',
            'Australia', 'New Zealand', 'Japan', 'South Korea', 'China',
            'India', 'United Kingdom', 'Germany', 'France', 'Italy',
            'Spain', 'Netherlands', 'Switzerland', 'Sweden', 'Norway',
            'Denmark', 'Finland', 'Poland', 'Portugal', 'Ireland',
        ]
        
        location_upper = location.upper()
        for country in countries:
            if country.upper() in location_upper:
                return country
        
        if 'online' in location.lower() or 'virtual' in location.lower():
            return 'Online'
        
        return ''
    
    def is_relevant(self, conference: Dict) -> bool:
        """Check if conference meets basic relevance criteria"""
        # Must have title
        if not conference.get('title'):
            return False
        
        # Must have at least one topic
        if not conference.get('topics'):
            return False
        
        # Must have URL
        if not conference.get('url'):
            return False
        
        return True
    
    def validate_deadline(self, conference: Dict) -> bool:
        """Validate that deadline is within acceptable window"""
        deadline_str = conference.get('abstract_deadline', '')
        
        if not deadline_str:
            # If no deadline specified, include but mark as unknown
            return True
        
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            
            # Check if deadline is in the future
            if deadline < self.today:
                return False
            
            # Check if deadline is within window
            max_date = self.today + timedelta(days=DEADLINE_WINDOW_DAYS)
            if deadline > max_date:
                return False
            
            # Check minimum days (exclude very urgent)
            min_date = self.today + timedelta(days=MIN_DEADLINE_DAYS)
            if deadline < min_date:
                return False
            
            return True
        except ValueError:
            # Can't parse date, include anyway
            return True
    
    def calculate_score(self, conference: Dict) -> Dict:
        """Calculate relevance score for conference"""
        score = 0.0
        
        # Topic match score (0-1)
        topic_count = len(conference.get('topics', []))
        topic_score = min(topic_count / 10.0, 1.0)  # Max score at 10 topics
        
        # Location match score
        location_score = 0.0
        country = conference.get('country', '').lower()
        if country == 'malaysia':
            location_score = 1.0
        elif country in ['singapore', 'thailand', 'indonesia']:
            location_score = 0.8
        elif country in ['australia', 'japan', 'south korea', 'china', 'india']:
            location_score = 0.6
        elif country in ['united kingdom', 'germany', 'france', 'netherlands']:
            location_score = 0.5
        elif country == 'online':
            location_score = 0.7
        
        # Deadline urgency score (closer deadlines get higher score)
        urgency_score = 0.5  # Default
        deadline_str = conference.get('abstract_deadline', '')
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
                days_until = (deadline - self.today).days
                
                if days_until <= 14:
                    urgency_score = 1.0
                elif days_until <= 30:
                    urgency_score = 0.8
                elif days_until <= 60:
                    urgency_score = 0.6
                elif days_until <= 90:
                    urgency_score = 0.4
                else:
                    urgency_score = 0.3
            except ValueError:
                pass
        
        # Publisher quality score
        publisher_score = 0.5  # Default
        publisher = conference.get('publisher', '').lower()
        if publisher:
            for pref_pub in PREFERRED_PUBLISHERS:
                if pref_pub.lower() in publisher:
                    publisher_score = 1.0
                    break
        
        # Source reliability score
        source_score = 0.5
        source = conference.get('source', '').lower()
        reliable_sources = ['ieee', 'acm', 'springer', 'elsevier', 'wiki_cfp']
        for rel_source in reliable_sources:
            if rel_source in source:
                source_score = 0.9
                break
        
        # Calculate weighted score
        score = (
            topic_score * SCORE_WEIGHTS['topic_match'] +
            location_score * SCORE_WEIGHTS['location_match'] +
            urgency_score * SCORE_WEIGHTS['deadline_urgency'] +
            publisher_score * SCORE_WEIGHTS['publisher_quality'] +
            source_score * SCORE_WEIGHTS['source_reliability']
        )
        
        conference['relevance_score'] = round(score, 3)
        
        # Add urgency level
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
                days_until = (deadline - self.today).days
                
                if days_until <= 14:
                    conference['urgency_level'] = 'High'
                elif days_until <= 30:
                    conference['urgency_level'] = 'Medium'
                else:
                    conference['urgency_level'] = 'Low'
            except ValueError:
                conference['urgency_level'] = 'Unknown'
        else:
            conference['urgency_level'] = 'Unknown'
        
        # Add action items
        conference['action_items'] = self.generate_action_items(conference)
        
        return conference
    
    def generate_action_items(self, conference: Dict) -> str:
        """Generate action items based on conference status"""
        urgency = conference.get('urgency_level', 'Unknown')
        
        if urgency == 'High':
            return "Abstract submission closes soon - prepare immediately!"
        elif urgency == 'Medium':
            return "Full paper submission open - start drafting"
        elif urgency == 'Low':
            return "Early stage - review CFP and plan submission"
        else:
            return "Review conference details and deadlines"
    
    def deduplicate(self, new_conferences: List[Dict], existing: List[Dict]) -> List[Dict]:
        """Remove duplicate conferences"""
        # Create set of existing IDs and URLs
        existing_ids = set()
        existing_urls = set()
        
        for conf in existing:
            existing_ids.add(conf.get('id', ''))
            if conf.get('url'):
                existing_urls.add(conf.get('url', ''))
        
        deduplicated = []
        seen_urls = set()
        
        for conf in new_conferences:
            url = conf.get('url', '')
            
            # Skip if already in existing database
            if conf.get('id') in existing_ids:
                continue
            
            # Skip if URL already seen in this batch
            if url and url in seen_urls:
                continue
            
            # Skip if URL exists in database
            if url and url in existing_urls:
                continue
            
            seen_urls.add(url)
            deduplicated.append(conf)
        
        return deduplicated
    
    def sort_by_deadline(self, conferences: List[Dict]) -> List[Dict]:
        """Sort conferences by deadline (most urgent first)"""
        def get_deadline(conf):
            deadline_str = conf.get('abstract_deadline', '')
            if deadline_str:
                try:
                    return datetime.strptime(deadline_str, '%Y-%m-%d')
                except ValueError:
                    return datetime.max
            return datetime.max
        
        return sorted(conferences, key=get_deadline)
    
    def merge_with_existing(self, new_conferences: List[Dict], existing: List[Dict]) -> List[Dict]:
        """Merge new conferences with existing database"""
        existing_ids = {conf.get('id'): conf for conf in existing}
        
        # Add new conferences
        for conf in new_conferences:
            conf_id = conf.get('id')
            if conf_id not in existing_ids:
                existing.append(conf)
            else:
                # Update existing record with new info
                existing_conf = existing_ids[conf_id]
                existing_conf['last_verified'] = self.today.strftime('%Y-%m-%d')
                
                # Update fields if new info is better
                if not existing_conf.get('abstract_deadline') and conf.get('abstract_deadline'):
                    existing_conf['abstract_deadline'] = conf['abstract_deadline']
                if not existing_conf.get('location') and conf.get('location'):
                    existing_conf['location'] = conf['location']
        
        return existing
