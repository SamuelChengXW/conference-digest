"""
Sample data generator for testing and demonstration
Creates realistic conference entries to populate the database
"""

import json
from datetime import datetime, timedelta
import random


def generate_sample_conferences():
    """Generate sample conferences for demonstration"""
    
    now = datetime.now()
    
    samples = [
        {
            "title": "International Conference on Sustainable Energy Systems 2026",
            "url": "https://icse2026.example.com",
            "location": "Kuala Lumpur, Malaysia",
            "country": "Malaysia",
            "mode": "Hybrid",
            "topics": ["Energy", "Renewable Energy", "Sustainability", "Power Systems"],
            "abstract_deadline": (now + timedelta(days=15)).strftime('%Y-%m-%d'),
            "conference_start_date": (now + timedelta(days=90)).strftime('%Y-%m-%d'),
            "publisher": "IEEE",
            "indexing": ["Scopus", "IEEE Xplore"],
            "source": "ieee_malaysia",
            "relevance_score": 0.92,
            "urgency_level": "High",
            "action_items": "Abstract submission closes soon - prepare immediately!"
        },
        {
            "title": "Asia Pacific AI and Machine Learning Summit 2026",
            "url": "https://apaiml2026.example.com",
            "location": "Singapore",
            "country": "Singapore",
            "mode": "In-Person",
            "topics": ["Artificial Intelligence", "Machine Learning", "Deep Learning", "Data Science"],
            "abstract_deadline": (now + timedelta(days=25)).strftime('%Y-%m-%d'),
            "conference_start_date": (now + timedelta(days=100)).strftime('%Y-%m-%d'),
            "publisher": "Springer",
            "indexing": ["Scopus", "EI Compendex"],
            "source": "conference_alerts",
            "relevance_score": 0.88,
            "urgency_level": "Medium",
            "action_items": "Full paper submission open - start drafting"
        },
        {
            "title": "International Conference on Environmental Engineering and Climate Change",
            "url": "https://iceecc2026.example.com",
            "location": "Bangkok, Thailand",
            "country": "Thailand",
            "mode": "Hybrid",
            "topics": ["Environmental Engineering", "Climate Change", "Sustainability", "Environmental Science"],
            "abstract_deadline": (now + timedelta(days=35)).strftime('%Y-%m-%d'),
            "conference_start_date": (now + timedelta(days=110)).strftime('%Y-%m-%d'),
            "publisher": "Elsevier",
            "indexing": ["Scopus"],
            "source": "conference_alerts",
            "relevance_score": 0.85,
            "urgency_level": "Medium",
            "action_items": "Full paper submission open - start drafting"
        },
        {
            "title": "European Conference on Energy Economics and Policy",
            "url": "https://eceep2026.example.com",
            "location": "Berlin, Germany",
            "country": "Germany",
            "mode": "Online",
            "topics": ["Energy Economics", "Environmental Economics", "Economic Policy", "Energy Policy"],
            "abstract_deadline": (now + timedelta(days=45)).strftime('%Y-%m-%d'),
            "conference_start_date": (now + timedelta(days=120)).strftime('%Y-%m-%d'),
            "publisher": "Taylor & Francis",
            "indexing": ["Web of Science", "Scopus"],
            "source": "wiki_cfp",
            "relevance_score": 0.78,
            "urgency_level": "Low",
            "action_items": "Early stage - review CFP and plan submission"
        },
        {
            "title": "Malaysia Green Technology and Sustainability Conference",
            "url": "https://mgts2026.example.com",
            "location": "Cyberjaya, Malaysia",
            "country": "Malaysia",
            "mode": "In-Person",
            "topics": ["Green Technology", "Sustainability", "Environmental Science", "Circular Economy"],
            "abstract_deadline": (now + timedelta(days=20)).strftime('%Y-%m-%d'),
            "conference_start_date": (now + timedelta(days=85)).strftime('%Y-%m-%d'),
            "publisher": "MDPI",
            "indexing": ["Scopus"],
            "source": "um_events",
            "relevance_score": 0.90,
            "urgency_level": "High",
            "action_items": "Abstract submission closes soon - prepare immediately!"
        },
        {
            "title": "International Conference on Smart Grid and Renewable Energy",
            "url": "https://icsgre2026.example.com",
            "location": "Online/Hybrid",
            "country": "Online",
            "mode": "Hybrid",
            "topics": ["Smart Grid", "Renewable Energy", "Power Systems", "Energy Storage"],
            "abstract_deadline": (now + timedelta(days=30)).strftime('%Y-%m-%d'),
            "conference_start_date": (now + timedelta(days=95)).strftime('%Y-%m-%d'),
            "publisher": "IEEE",
            "indexing": ["IEEE Xplore", "Scopus"],
            "source": "ieee_malaysia",
            "relevance_score": 0.87,
            "urgency_level": "Medium",
            "action_items": "Full paper submission open - start drafting"
        },
        {
            "title": "Asia-Pacific Workshop on Industrial Engineering and Operations Research",
            "url": "https://apwieor2026.example.com",
            "location": "Tokyo, Japan",
            "country": "Japan",
            "mode": "In-Person",
            "topics": ["Industrial Engineering", "Operations Research", "Optimization", "Systems Engineering"],
            "abstract_deadline": (now + timedelta(days=50)).strftime('%Y-%m-%d'),
            "conference_start_date": (now + timedelta(days=115)).strftime('%Y-%m-%d'),
            "publisher": "Springer",
            "indexing": ["Scopus", "EI Compendex"],
            "source": "conference_alerts",
            "relevance_score": 0.72,
            "urgency_level": "Low",
            "action_items": "Early stage - review CFP and plan submission"
        },
        {
            "title": "International Conference on Data Science and Artificial Intelligence Applications",
            "url": "https://icdsaia2026.example.com",
            "location": "Sydney, Australia",
            "country": "Australia",
            "mode": "Hybrid",
            "topics": ["Data Science", "Artificial Intelligence", "Machine Learning", "Computer Vision"],
            "abstract_deadline": (now + timedelta(days=40)).strftime('%Y-%m-%d'),
            "conference_start_date": (now + timedelta(days=105)).strftime('%Y-%m-%d'),
            "publisher": "ACM",
            "indexing": ["Scopus", "ACM Digital Library"],
            "source": "wiki_cfp",
            "relevance_score": 0.82,
            "urgency_level": "Medium",
            "action_items": "Full paper submission open - start drafting"
        },
        {
            "title": "Conference on Advances in Mechanical Engineering and Manufacturing",
            "url": "https://camem2026.example.com",
            "location": "Penang, Malaysia",
            "country": "Malaysia",
            "mode": "In-Person",
            "topics": ["Mechanical Engineering", "Manufacturing", "Automation", "Robotics"],
            "abstract_deadline": (now + timedelta(days=60)).strftime('%Y-%m-%d'),
            "conference_start_date": (now + timedelta(days=130)).strftime('%Y-%m-%d'),
            "publisher": "IOP",
            "indexing": ["Scopus", "EI Compendex"],
            "source": "utm_events",
            "relevance_score": 0.75,
            "urgency_level": "Low",
            "action_items": "Early stage - review CFP and plan submission"
        },
        {
            "title": "International Symposium on Environmental Policy and Governance",
            "url": "https://isepg2026.example.com",
            "location": "Amsterdam, Netherlands",
            "country": "Netherlands",
            "mode": "Online",
            "topics": ["Environmental Policy", "Climate Policy", "Sustainability", "Environmental Economics"],
            "abstract_deadline": (now + timedelta(days=55)).strftime('%Y-%m-%d'),
            "conference_start_date": (now + timedelta(days=125)).strftime('%Y-%m-%d'),
            "publisher": "Elsevier",
            "indexing": ["Scopus", "Web of Science"],
            "source": "conference_alerts",
            "relevance_score": 0.70,
            "urgency_level": "Low",
            "action_items": "Early stage - review CFP and plan submission"
        }
    ]
    
    # Add IDs and timestamps
    for i, conf in enumerate(samples):
        conf['id'] = f"conf_{now.year}_{i+1:03d}"
        conf['first_seen'] = now.strftime('%Y-%m-%d')
        conf['last_verified'] = now.strftime('%Y-%m-%d')
        conf['status'] = 'open'
        conf['description'] = f"Leading conference on {', '.join(conf['topics'][:2])} in {conf['country']}"
    
    return samples


if __name__ == "__main__":
    samples = generate_sample_conferences()
    
    # Save to data directory
    with open('data/conferences.json', 'w', encoding='utf-8') as f:
        json.dump(samples, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(samples)} sample conferences")
    print("Saved to data/conferences.json")
    
    # Generate website
    from src.website_generator import WebsiteGenerator
    
    gen = WebsiteGenerator(output_dir="docs")
    gen.generate_all(samples, samples)
    
    print("Website generated in docs/")
