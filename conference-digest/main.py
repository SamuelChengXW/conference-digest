"""
Main entry point for Conference Digest System
"""

import json
import os
from datetime import datetime
from src.scraper import ConferenceScraper
from src.processor import ConferenceProcessor
from src.email_sender import EmailSender
from src.website_generator import WebsiteGenerator
from src.config import DATA_DIR, DATABASE_FILE, LOG_FILE


def load_existing_conferences() -> list:
    """Load existing conferences from database"""
    db_path = os.path.join(DATA_DIR, DATABASE_FILE)
    
    if os.path.exists(db_path):
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading database: {e}")
    
    return []


def save_conferences(conferences: list):
    """Save conferences to database"""
    db_path = os.path.join(DATA_DIR, DATABASE_FILE)
    
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(conferences, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(conferences)} conferences to database")


def main():
    """Main execution function"""
    print("=" * 60)
    print("CONFERENCE DIGEST SYSTEM")
    print(f"Running at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Step 1: Load existing conferences
        print("\n[1/6] Loading existing conference database...")
        existing_conferences = load_existing_conferences()
        print(f"Loaded {len(existing_conferences)} existing conferences")
        
        # Step 2: Scrape new conferences
        print("\n[2/6] Fetching conferences from sources...")
        scraper = ConferenceScraper()
        raw_conferences = scraper.fetch_all_sources()
        print(f"Fetched {len(raw_conferences)} raw conferences")
        
        # Step 3: Process and filter
        print("\n[3/6] Processing and filtering conferences...")
        processor = ConferenceProcessor()
        new_conferences = processor.process_all(raw_conferences, existing_conferences)
        print(f"Found {len(new_conferences)} relevant new conferences")
        
        # Step 4: Merge with existing
        print("\n[4/6] Merging with existing database...")
        all_conferences = processor.merge_with_existing(new_conferences, existing_conferences)
        
        # Remove expired conferences
        active_conferences = []
        for conf in all_conferences:
            deadline = conf.get('abstract_deadline', '')
            if deadline:
                try:
                    deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
                    if deadline_date >= datetime.now():
                        active_conferences.append(conf)
                except:
                    active_conferences.append(conf)
            else:
                active_conferences.append(conf)
        
        print(f"Total active conferences: {len(active_conferences)}")
        
        # Step 5: Save to database
        print("\n[5/6] Saving to database...")
        save_conferences(active_conferences)
        
        # Step 6: Generate website
        print("\n[6/6] Generating website...")
        website_gen = WebsiteGenerator(output_dir="docs")
        website_gen.generate_all(new_conferences, active_conferences)
        
        # Step 7: Send email
        print("\n[7/7] Sending email digest...")
        email_sender = EmailSender()
        email_sent = email_sender.send_digest(new_conferences)
        
        if email_sent:
            print("✓ Email sent successfully")
        else:
            print("⚠ Email not sent (configuration may be incomplete)")
        
        # Summary
        print("\n" + "=" * 60)
        print("EXECUTION SUMMARY")
        print("=" * 60)
        print(f"New conferences found: {len(new_conferences)}")
        print(f"Total active conferences: {len(active_conferences)}")
        print(f"Website generated: docs/index.html")
        print(f"Email sent: {email_sent}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
