"""
HTML Website Generator for Conference Digest
Generates a static website that can be hosted on GitHub Pages
"""

import json
from datetime import datetime
from typing import List, Dict
import os


class WebsiteGenerator:
    """Generate static HTML website for conference digest"""
    
    def __init__(self, output_dir: str = "docs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_all(self, conferences: List[Dict], all_time_conferences: List[Dict] = None):
        """Generate all website pages"""
        
        # Generate index.html (main page)
        self.generate_index(conferences)
        
        # Generate archive.html (all conferences)
        if all_time_conferences:
            self.generate_archive(all_time_conferences)
        
        # Generate individual conference pages
        for conf in conferences:
            self.generate_conference_page(conf)
        
        # Generate RSS feed
        self.generate_rss(conferences)
        
        print(f"Website generated in {self.output_dir}/")
    
    def generate_index(self, conferences: List[Dict]):
        """Generate main index page"""
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weekly Conference Digest - Energy, Engineering, AI, ML & More</title>
    <meta name="description" content="Automated weekly digest of academic conferences in Energy, Engineering, AI, Machine Learning, Environmental Science, and Economics">
    <style>
        :root {{
            --primary: #2c3e50;
            --secondary: #3498db;
            --accent: #e74c3c;
            --warning: #f39c12;
            --success: #27ae60;
            --light: #ecf0f1;
            --dark: #2c3e50;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        h1 {{
            color: var(--primary);
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        
        .last-updated {{
            background: var(--light);
            padding: 10px 15px;
            border-radius: 5px;
            margin-top: 15px;
            display: inline-block;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: var(--secondary);
        }}
        
        .stat-label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        
        .filters {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .filter-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }}
        
        .filter-btn {{
            padding: 8px 16px;
            border: 2px solid var(--secondary);
            background: white;
            color: var(--secondary);
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .filter-btn:hover, .filter-btn.active {{
            background: var(--secondary);
            color: white;
        }}
        
        .conferences {{
            display: grid;
            gap: 20px;
        }}
        
        .conference-card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 5px solid var(--secondary);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .conference-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .conference-card.high-priority {{ border-left-color: var(--accent); }}
        .conference-card.medium-priority {{ border-left-color: var(--warning); }}
        .conference-card.low-priority {{ border-left-color: var(--success); }}
        
        .conference-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        
        .conference-title {{
            font-size: 1.4em;
            color: var(--primary);
            font-weight: bold;
        }}
        
        .conference-meta {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 15px 0;
            padding: 15px;
            background: var(--light);
            border-radius: 5px;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .meta-icon {{
            font-size: 1.2em;
        }}
        
        .topics {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 15px 0;
        }}
        
        .topic-tag {{
            background: var(--secondary);
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
        }}
        
        .urgency-badge {{
            padding: 5px 12px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.85em;
        }}
        
        .urgency-high {{ background: var(--accent); color: white; }}
        .urgency-medium {{ background: var(--warning); color: white; }}
        .urgency-low {{ background: var(--success); color: white; }}
        
        .action-box {{
            background: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            border-left: 4px solid var(--warning);
        }}
        
        .score {{
            font-size: 1.2em;
            font-weight: bold;
            color: var(--primary);
        }}
        
        .btn {{
            display: inline-block;
            padding: 10px 20px;
            background: var(--secondary);
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }}
        
        .btn:hover {{
            background: #2980b9;
        }}
        
        footer {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-top: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        @media (max-width: 768px) {{
            h1 {{ font-size: 1.8em; }}
            .conference-header {{ flex-direction: column; gap: 10px; }}
            .conference-meta {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📅 Weekly Conference Digest</h1>
            <p class="subtitle">Academic Conferences in Energy, Engineering, AI, ML, Environmental Science & Economics</p>
            <div class="last-updated">
                🔄 Last Updated: {datetime.now().strftime('%d %B %Y at %H:%M')}
            </div>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(conferences)}</div>
                <div class="stat-label">Conferences This Week</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([c for c in conferences if c.get('urgency_level') == 'High'])}</div>
                <div class="stat-label">High Priority</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([c for c in conferences if c.get('mode') == 'Online'])}</div>
                <div class="stat-label">Online/Hybrid</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(set(c.get('country', '') for c in conferences))}</div>
                <div class="stat-label">Countries</div>
            </div>
        </div>
        
        <div class="filters">
            <h3>🔍 Filter by Topic</h3>
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="filterConferences('all')">All</button>
                <button class="filter-btn" onclick="filterConferences('Energy')">Energy</button>
                <button class="filter-btn" onclick="filterConferences('Engineering')">Engineering</button>
                <button class="filter-btn" onclick="filterConferences('Artificial Intelligence')">AI</button>
                <button class="filter-btn" onclick="filterConferences('Machine Learning')">ML</button>
                <button class="filter-btn" onclick="filterConferences('Environmental')">Environmental</button>
                <button class="filter-btn" onclick="filterConferences('Economics')">Economics</button>
            </div>
        </div>
        
        <div class="conferences" id="conferencesList">
"""
        
        # Add conference cards
        for i, conf in enumerate(conferences[:50], 1):  # Limit to 50
            priority_class = f"{conf.get('urgency_level', 'Low').lower()}-priority"
            
            topics_html = ""
            for topic in conf.get('topics', [])[:8]:
                topics_html += f'<span class="topic-tag">{topic}</span>'
            
            html += f"""
            <div class="conference-card {priority_class}" data-topics="{' '.join(conf.get('topics', []))}">
                <div class="conference-header">
                    <div class="conference-title">{i}. {conf.get('title', 'Unknown')}</div>
                    <span class="urgency-badge urgency-{conf.get('urgency_level', 'Low').lower()}">{conf.get('urgency_level', 'Unknown')}</span>
                </div>
                
                <div class="conference-meta">
                    <div class="meta-item">
                        <span class="meta-icon">📍</span>
                        <span>{conf.get('location', 'Not specified')} ({conf.get('mode', 'N/A')})</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-icon">📝</span>
                        <span>Deadline: {conf.get('abstract_deadline', 'TBD')}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-icon">📅</span>
                        <span>Conference: {conf.get('conference_start_date', 'TBD')}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-icon">📊</span>
                        <span class="score">Score: {conf.get('relevance_score', 0)}</span>
                    </div>
                </div>
                
                <div class="topics">{topics_html}</div>
                
                <div class="action-box">
                    <strong>💡 Action Required:</strong> {conf.get('action_items', 'Review details')}
                </div>
                
                <a href="{conf.get('url', '#')}" target="_blank" class="btn">Visit Conference Website →</a>
            </div>
"""
        
        html += """
        </div>
        
        <footer>
            <p><strong>Note:</strong> Please verify all conference details, deadlines, and submission requirements on the official conference website before submitting.</p>
            <p>This digest is automatically generated every Sunday at 8:00 AM Malaysia Time.</p>
            <p>Generated by Conference Digest Bot | <a href="archive.html">View Archive</a></p>
        </footer>
    </div>
    
    <script>
        function filterConferences(topic) {
            const cards = document.querySelectorAll('.conference-card');
            const buttons = document.querySelectorAll('.filter-btn');
            
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            cards.forEach(card => {
                if (topic === 'all' || card.dataset.topics.includes(topic)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""
        
        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate_archive(self, conferences: List[Dict]):
        """Generate archive page with all conferences"""
        # Simplified archive generation
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Conference Archive</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #3498db; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
        a {{ color: #3498db; }}
    </style>
</head>
<body>
    <h1>📚 Conference Archive</h1>
    <p><a href="index.html">← Back to Current Digest</a></p>
    
    <table>
        <tr>
            <th>Title</th>
            <th>Location</th>
            <th>Deadline</th>
            <th>Conference Date</th>
            <th>Topics</th>
            <th>Score</th>
        </tr>
"""
        
        for conf in conferences[:200]:  # Limit archive
            html += f"""
        <tr>
            <td><a href="{conf.get('url', '#')}">{conf.get('title', 'Unknown')[:60]}</a></td>
            <td>{conf.get('location', 'N/A')}</td>
            <td>{conf.get('abstract_deadline', 'TBD')}</td>
            <td>{conf.get('conference_start_date', 'TBD')}</td>
            <td>{', '.join(conf.get('topics', [])[:3])}</td>
            <td>{conf.get('relevance_score', 0)}</td>
        </tr>
"""
        
        html += """
    </table>
</body>
</html>
"""
        
        with open(os.path.join(self.output_dir, 'archive.html'), 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate_rss(self, conferences: List[Dict]):
        """Generate RSS feed"""
        rss = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>Weekly Conference Digest</title>
    <link>https://yourusername.github.io/conference-digest/</link>
    <description>Automated digest of academic conferences in Energy, Engineering, AI, ML, Environmental Science, and Economics</description>
    <language>en-us</language>
    <lastBuildDate>""" + datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT') + """</lastBuildDate>
"""
        
        for conf in conferences[:20]:
            rss += f"""
    <item>
        <title>{conf.get('title', 'Unknown')}</title>
        <link>{conf.get('url', '')}</link>
        <description>Deadline: {conf.get('abstract_deadline', 'TBD')} | Location: {conf.get('location', 'N/A')} | Topics: {', '.join(conf.get('topics', [])[:5])}</description>
        <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
    </item>
"""
        
        rss += """
</channel>
</rss>
"""
        
        with open(os.path.join(self.output_dir, 'feed.xml'), 'w', encoding='utf-8') as f:
            f.write(rss)
    
    def generate_conference_page(self, conf: Dict):
        """Generate individual conference page (optional)"""
        pass  # Can be implemented later
