# Conference Digest System

Automated weekly digest of academic conferences in **Energy, Engineering, AI, Machine Learning, Environmental Science, and Economics**.

## Features

- 📅 **Weekly Automation**: Runs every Sunday at 8:00 AM Malaysia Time
- 🌐 **Website**: Beautiful static website hosted on GitHub Pages
- 📧 **Email Delivery**: HTML email digest sent automatically
- 🔍 **Smart Filtering**: Filters by topics, location, and deadline window
- ⭐ **Relevance Scoring**: Ranks conferences by relevance to your interests
- 📊 **Database**: Maintains history and prevents duplicates

## Coverage

### Topics
- Energy (Renewable, Power Systems, Solar, Wind, etc.)
- Engineering (All disciplines)
- Artificial Intelligence & Machine Learning
- Environmental Science & Sustainability
- Economics (Energy, Environmental, Industrial)

### Locations
- Malaysia (primary focus)
- Asia Pacific region
- Europe
- Online/Hybrid conferences

### Deadline Window
- Next 120 days from current date

## Quick Start

### 1. Create Repository
```bash
# Create a new GitHub repository named "conference-digest"
# Clone it locally or use GitHub Codespaces
```

### 2. Copy Files
Copy all files from this directory to your repository.

### 3. Configure GitHub Secrets
Go to your repository → Settings → Secrets and variables → Actions → New repository secret

Add these secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `EMAIL_SMTP_SERVER` | SMTP server address | `smtp.gmail.com` |
| `EMAIL_SMTP_PORT` | SMTP port | `587` |
| `EMAIL_USERNAME` | Your email address | `yourname@gmail.com` |
| `EMAIL_PASSWORD` | App password (not regular password) | `xxxx xxxx xxxx xxxx` |
| `EMAIL_FROM` | From email address | `yourname@gmail.com` |
| `EMAIL_TO` | Recipient email | `yourname@gmail.com` |

**For Gmail:**
1. Enable 2FA on your Google account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Use the app password as `EMAIL_PASSWORD`

### 4. Enable GitHub Pages
1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` (will be created automatically)
4. Folder: `/ (root)`
5. Save

### 5. Enable GitHub Actions
1. Go to Actions tab
2. Click "I understand my workflows, go ahead and enable them"
3. Manually trigger first run: Click "Run workflow" → "Run workflow"

### 6. View Your Website
After first successful run:
```
https://YOUR_USERNAME.github.io/conference-digest/
```

## Project Structure

```
conference-digest/
├── .github/workflows/
│   └── digest.yml          # GitHub Actions workflow
├── src/
│   ├── config.py           # Configuration settings
│   ├── scraper.py          # Conference data scraper
│   ├── processor.py        # Filtering and scoring
│   ├── email_sender.py     # Email delivery
│   └── website_generator.py # Static site generator
├── data/
│   └── conferences.json    # Conference database (auto-generated)
├── docs/                   # Generated website (auto-generated)
│   ├── index.html
│   ├── archive.html
│   └── feed.xml
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Manual Execution

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional for email)
export EMAIL_SMTP_SERVER=smtp.gmail.com
export EMAIL_USERNAME=yourname@gmail.com
export EMAIL_PASSWORD="your-app-password"
export EMAIL_FROM=yourname@gmail.com
export EMAIL_TO=yourname@gmail.com

# Run the digest
python main.py
```

## Customization

### Change Schedule
Edit `.github/workflows/digest.yml`:
```yaml
schedule:
  - cron: '0 0 * * 0'  # Sunday 00:00 UTC = Sunday 8:00 AM MYT
```

Cron format: `minute hour day month weekday`

### Modify Topics
Edit `src/config.py` - `TOPICS` list.

### Change Deadline Window
Edit `src/config.py`:
```python
DEADLINE_WINDOW_DAYS = 120  # Change to desired days
```

### Add More Sources
Edit `src/config.py` - `CONFERENCE_SOURCES` list.

## Troubleshooting

### No Conferences Found
- Check if sources are accessible
- Verify topic filters aren't too restrictive
- Check logs in Actions tab

### Email Not Sent
- Verify all email secrets are set correctly
- For Gmail, ensure App Password is used (not regular password)
- Check 2FA is enabled on Google account

### Website Not Updating
- Ensure GitHub Pages is enabled
- Check Actions workflow completed successfully
- Verify `docs/` folder is being committed

### Workflow Fails
- Check Actions logs for error details
- Ensure Python version is correct
- Verify all dependencies install properly

## Data Format

Each conference is stored as:

```json
{
  "id": "conf_2025_abc123",
  "title": "Conference Name",
  "url": "https://conference-website.com",
  "location": "Kuala Lumpur, Malaysia",
  "country": "Malaysia",
  "mode": "Hybrid",
  "topics": ["Energy", "AI", "Sustainability"],
  "abstract_deadline": "2025-09-15",
  "conference_start_date": "2025-11-10",
  "publisher": "IEEE",
  "relevance_score": 0.85,
  "urgency_level": "Medium",
  "action_items": "Full paper submission open"
}
```

## License

MIT License - Feel free to use and modify.

## Support

For issues or questions, open an issue on GitHub.

---

**Note**: This system scrapes public conference listings. Always verify conference details, deadlines, and legitimacy on official websites before submitting.
