"""
Email sender module for conference digest
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import os
from datetime import datetime


class EmailSender:
    """Send conference digest via email"""
    
    def __init__(self):
        self.smtp_server = os.getenv('EMAIL_SMTP_SERVER')
        self.smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))
        self.username = os.getenv('EMAIL_USERNAME')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.from_email = os.getenv('EMAIL_FROM')
        self.to_email = os.getenv('EMAIL_TO')
    
    def send_digest(self, conferences: List[Dict], format_type: str = 'html') -> bool:
        """Send weekly digest email"""
        
        if not all([self.smtp_server, self.username, self.password, self.from_email, self.to_email]):
            print("Email configuration incomplete. Skipping email send.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Weekly Conference Digest - {datetime.now().strftime('%d %B %Y')}"
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            
            # Generate content
            text_content = self.generate_text_digest(conferences)
            html_content = self.generate_html_digest(conferences)
            
            # Attach both versions
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            
            print(f"Email sent successfully to {self.to_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def generate_text_digest(self, conferences: List[Dict]) -> str:
        """Generate plain text digest"""
        lines = []
        lines.append("=" * 60)
        lines.append("WEEKLY CONFERENCE DIGEST")
        lines.append(f"Week of: {datetime.now().strftime('%d %B %Y')}")
        lines.append("=" * 60)
        lines.append("")
        
        if not conferences:
            lines.append("No new conferences found this week.")
            return "\n".join(lines)
        
        lines.append(f"Total Conferences Found: {len(conferences)}")
        lines.append("")
        lines.append("-" * 60)
        
        for i, conf in enumerate(conferences[:20], 1):  # Limit to 20
            lines.append("")
            lines.append(f"{i}. {conf.get('title', 'Unknown')}")
            lines.append(f"   Location: {conf.get('location', 'Not specified')}")
            lines.append(f"   Mode: {conf.get('mode', 'Not specified')}")
            
            deadline = conf.get('abstract_deadline', '')
            if deadline:
                lines.append(f"   Submission Deadline: {deadline}")
            
            conf_date = conf.get('conference_start_date', '')
            if conf_date:
                lines.append(f"   Conference Date: {conf_date}")
            
            topics = conf.get('topics', [])
            if topics:
                lines.append(f"   Topics: {', '.join(topics[:5])}")
            
            lines.append(f"   Urgency: {conf.get('urgency_level', 'Unknown')}")
            lines.append(f"   Action: {conf.get('action_items', '')}")
            lines.append(f"   Website: {conf.get('url', 'Not available')}")
            lines.append(f"   Relevance Score: {conf.get('relevance_score', 0)}")
        
        lines.append("")
        lines.append("-" * 60)
        lines.append("")
        lines.append("Note: Please verify all details on the official conference website before submitting.")
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def generate_html_digest(self, conferences: List[Dict]) -> str:
        """Generate HTML digest"""
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
                h2 { color: #34495e; margin-top: 30px; }
                .conference { background: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin: 20px 0; border-radius: 4px; }
                .conference h3 { margin: 0 0 10px 0; color: #2c3e50; }
                .high-priority { border-left-color: #e74c3c; }
                .medium-priority { border-left-color: #f39c12; }
                .low-priority { border-left-color: #27ae60; }
                .meta { color: #7f8c8d; font-size: 0.9em; }
                .topics { background: #ecf0f1; padding: 5px 10px; border-radius: 3px; display: inline-block; margin: 5px 0; }
                .action { background: #fff3cd; padding: 10px; border-radius: 3px; margin: 10px 0; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #3498db; color: white; }
                tr:hover { background-color: #f5f5f5; }
                .score { font-weight: bold; color: #2c3e50; }
                .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; font-size: 0.9em; }
                a { color: #3498db; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>📅 Weekly Conference Digest</h1>
            <p class="meta"><strong>Week of:</strong> """ + datetime.now().strftime('%d %B %Y') + """</p>
        """
        
        if not conferences:
            html += "<p>No new conferences found this week.</p>"
        else:
            html += f"<p><strong>Total Conferences Found:</strong> {len(conferences)}</p>"
            
            # Summary table
            html += """
            <h2>Quick Overview</h2>
            <table>
                <tr>
                    <th>Deadline</th>
                    <th>Conference</th>
                    <th>Location</th>
                    <th>Topics</th>
                    <th>Urgency</th>
                </tr>
            """
            
            for conf in conferences[:15]:
                deadline = conf.get('abstract_deadline', 'TBD')
                title = conf.get('title', 'Unknown')
                location = conf.get('location', 'Not specified')
                topics = ', '.join(conf.get('topics', [])[:3])
                urgency = conf.get('urgency_level', 'Unknown')
                
                urgency_class = ''
                if urgency == 'High':
                    urgency_class = 'style="color: #e74c3c; font-weight: bold;"'
                elif urgency == 'Medium':
                    urgency_class = 'style="color: #f39c12;"'
                
                html += f"""
                <tr>
                    <td>{deadline}</td>
                    <td><a href="{conf.get('url', '#')}">{title[:50]}{'...' if len(title) > 50 else ''}</a></td>
                    <td>{location}</td>
                    <td>{topics}</td>
                    <td {urgency_class}>{urgency}</td>
                </tr>
                """
            
            html += "</table>"
            
            # Detailed list
            html += "<h2>Detailed Listings</h2>"
            
            for i, conf in enumerate(conferences[:20], 1):
                priority_class = ''
                urgency = conf.get('urgency_level', '')
                if urgency == 'High':
                    priority_class = 'high-priority'
                elif urgency == 'Medium':
                    priority_class = 'medium-priority'
                else:
                    priority_class = 'low-priority'
                
                html += f"""
                <div class="conference {priority_class}">
                    <h3>{i}. {conf.get('title', 'Unknown')}</h3>
                    <p><strong>📍 Location:</strong> {conf.get('location', 'Not specified')} ({conf.get('mode', 'Not specified')})</p>
                """
                
                deadline = conf.get('abstract_deadline', '')
                if deadline:
                    html += f'<p><strong>📝 Submission Deadline:</strong> <span style="color: #e74c3c;">{deadline}</span></p>'
                
                conf_date = conf.get('conference_start_date', '')
                if conf_date:
                    html += f'<p><strong>📅 Conference Date:</strong> {conf_date}</p>'
                
                notification = conf.get('notification_date', '')
                if notification:
                    html += f'<p><strong>🔔 Notification Date:</strong> {notification}</p>'
                
                topics = conf.get('topics', [])
                if topics:
                    html += f'<p><strong>🏷️ Topics:</strong> <span class="topics">{", ".join(topics[:8])}</span></p>'
                
                publisher = conf.get('publisher', '')
                if publisher:
                    html += f'<p><strong>📚 Publisher:</strong> {publisher}</p>'
                
                indexing = conf.get('indexing', [])
                if indexing:
                    html += f'<p><strong>📖 Indexing:</strong> {", ".join(indexing)}</p>'
                
                html += f"""
                    <p><strong>⚡ Urgency:</strong> {conf.get('urgency_level', 'Unknown')}</p>
                    <p><strong>📊 Relevance Score:</strong> <span class="score">{conf.get('relevance_score', 0)}</span></p>
                    <div class="action"><strong>💡 Action Required:</strong> {conf.get('action_items', 'Review details')}</div>
                    <p><strong>🔗 Website:</strong> <a href="{conf.get('url', '#')}" target="_blank">{conf.get('url', 'Not available')}</a></p>
                </div>
                """
        
        html += """
            <div class="footer">
                <p><strong>Note:</strong> Please verify all conference details, deadlines, and submission requirements on the official conference website before submitting. This digest is automatically generated and may contain outdated or incorrect information.</p>
                <p>Generated automatically by Conference Digest Bot</p>
            </div>
        </body>
        </html>
        """
        
        return html
