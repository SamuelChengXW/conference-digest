"""
Configuration for Conference Digest System
"""

# Schedule: Sunday 8:00 AM Malaysia Time (UTC+8)
# Sunday 8:00 AM MYT = Sunday 00:00 UTC
SCHEDULE_CRON = "0 0 * * 0"

# Topics to track
TOPICS = [
    # Core topics
    "Energy",
    "Renewable Energy",
    "Power Systems",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Chemical Engineering",
    "Environmental Engineering",
    "Artificial Intelligence",
    "Machine Learning",
    "Data Science",
    "Computational Intelligence",
    "Deep Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Robotics",
    "Automation",
    "Environmental Science",
    "Sustainability",
    "Climate Change",
    "Green Technology",
    "Circular Economy",
    "Carbon Management",
    "Energy Economics",
    "Development Economics",
    "Environmental Economics",
    "Industrial Economics",
    "Engineering Management",
    "Systems Engineering",
    "Industrial Engineering",
    "Petroleum Engineering",
    "Nuclear Engineering",
    "Biomedical Engineering",
    "Materials Science",
    "Nanotechnology",
    "IoT",
    "Smart Grid",
    "Energy Storage",
    "Battery Technology",
    "Hydrogen Energy",
    "Solar Energy",
    "Wind Energy",
    "Biomass",
    "Geothermal",
    "Ocean Energy",
    "Energy Efficiency",
    "Building Energy",
    "Transportation Energy",
    "Smart Cities",
    "Urban Planning",
    "Water Resources",
    "Waste Management",
    "Air Quality",
    "Pollution Control",
    "Ecology",
    "Conservation",
    "Biodiversity",
    "Ecosystem Services",
    "Environmental Policy",
    "Climate Policy",
    "Energy Policy",
    "Economic Policy",
    "Finance",
    "Investment",
    "Risk Management",
    "Supply Chain",
    "Operations Research",
    "Optimization",
    "Simulation",
    "Modeling",
    "Control Systems",
    "Signal Processing",
    "Communications",
    "Networks",
    "Cybersecurity",
    "Blockchain",
    "Cloud Computing",
    "Edge Computing",
    "High Performance Computing",
    "Quantum Computing",
    "Neural Networks",
    "Reinforcement Learning",
    "Federated Learning",
    "Explainable AI",
    "AI Ethics",
    "Responsible AI",
]

# Location scope
LOCATIONS = [
    "Malaysia",
    "Singapore",
    "Thailand",
    "Indonesia",
    "Philippines",
    "Vietnam",
    "Cambodia",
    "Laos",
    "Myanmar",
    "Brunei",
    "Asia Pacific",
    "Europe",
    "Online",
    "Virtual",
    "Hybrid",
]

# Countries to include (for filtering)
ALLOWED_COUNTRIES = [
    "malaysia", "singapore", "thailand", "indonesia", "philippines",
    "vietnam", "cambodia", "laos", "myanmar", "brunei",
    "australia", "new zealand", "japan", "south korea", "china",
    "hong kong", "taiwan", "india", "pakistan", "bangladesh",
    "sri lanka", "nepal", "bhutan", "maldives",
    "united kingdom", "germany", "france", "italy", "spain",
    "netherlands", "belgium", "switzerland", "austria", "sweden",
    "norway", "denmark", "finland", "poland", "czech republic",
    "portugal", "greece", "ireland", "online", "virtual", "hybrid"
]

# Deadline window in days
DEADLINE_WINDOW_DAYS = 120

# Minimum days until deadline to include (exclude very urgent < 3 days)
MIN_DEADLINE_DAYS = 3

# Email configuration (set via GitHub Secrets)
EMAIL_ENABLED = True
EMAIL_SMTP_SERVER = None  # Set in GitHub Secrets
EMAIL_SMTP_PORT = 587
EMAIL_USERNAME = None  # Set in GitHub Secrets
EMAIL_PASSWORD = None  # Set in GitHub Secrets
EMAIL_FROM = None  # Set in GitHub Secrets
EMAIL_TO = None  # Set in GitHub Secrets

# Telegram configuration (set via GitHub Secrets)
TELEGRAM_ENABLED = False
TELEGRAM_BOT_TOKEN = None  # Set in GitHub Secrets
TELEGRAM_CHAT_ID = None  # Set in GitHub Secrets

# Data storage
DATA_DIR = "data"
DATABASE_FILE = "conferences.json"
LOG_FILE = "digest.log"

# Website settings
WEBSITE_TITLE = "Weekly Conference Digest"
WEBSITE_DESCRIPTION = "Automated digest of academic conferences in Energy, Engineering, AI, ML, Environmental Science, and Economics"
WEBSITE_AUTHOR = "Conference Digest Bot"

# Source URLs to scrape
CONFERENCE_SOURCES = [
    # Global aggregators
    {"name": "wiki_cfp", "url": "http://www.wikicfp.com/cfp/servlet/event.search?q=energy", "type": "rss"},
    {"name": "conference_alerts", "url": "https://conferencealerts.com/", "type": "html"},
    {"name": "all_conferences", "url": "https://www.allconferences.com/", "type": "html"},
    {"name": "researchbib", "url": "https://researchbib.com/", "type": "html"},
    
    # Malaysian universities
    {"name": "um_events", "url": "https://www.um.edu.my/events", "type": "html"},
    {"name": "ukm_events", "url": "https://www.ukm.my/events", "type": "html"},
    {"name": "utm_events", "url": "https://www.utm.my/events", "type": "html"},
    {"name": "usm_events", "url": "https://www.usm.my/events", "type": "html"},
    {"name": "upm_events", "url": "https://www.upm.edu.my/events", "type": "html"},
    
    # Professional bodies
    {"name": "ieee_malaysia", "url": "https://ieee.org.my/", "type": "html"},
    {"name": "iem_events", "url": "https://www.iem.org.my/", "type": "html"},
    
    # Search-based discovery (will use search APIs)
    {"name": "google_search", "url": "search", "type": "search"},
]

# Negative keywords to exclude
NEGATIVE_KEYWORDS = [
    "medical", "clinical", "healthcare", "hospital", "patient",
    "nursing", "pharmacy", "dentistry", "veterinary",
    "fashion", "beauty", "cosmetic", "entertainment",
    "gaming", "esports", "sports", "fitness",
    "food", "culinary", "restaurant", "cooking",
    "art exhibition", "music festival", "concert",
    "trade show", "expo", "exhibition only",
    "webinar only", "podcast", "interview",
]

# Preferred publishers (for scoring)
PREFERRED_PUBLISHERS = [
    "IEEE", "ACM", "Springer", "Elsevier", "Taylor & Francis",
    "Wiley", "Nature", "Science", "MDPI", "IOP",
    "Scopus", "Web of Science", "EI Compendex"
]

# Relevance scoring weights
SCORE_WEIGHTS = {
    "topic_match": 0.4,
    "location_match": 0.2,
    "deadline_urgency": 0.15,
    "publisher_quality": 0.15,
    "source_reliability": 0.1,
}

# Minimum relevance score to include (0-1)
MIN_RELEVANCE_SCORE = 0.3
