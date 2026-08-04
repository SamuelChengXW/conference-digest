# Conference Digest - Setup Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click "+" → "New repository"
3. Name it: `conference-digest`
4. Make it **Public** (required for free GitHub Pages)
5. Click "Create repository"

### Step 2: Upload Files

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/YOUR_USERNAME/conference-digest.git
cd conference-digest

# Copy all files from this folder into the repository
# Then:
git add .
git commit -m "Initial commit: Conference digest system"
git push origin main
```

**Option B: Using GitHub Web Interface**
1. In your new repository, click "uploading an existing file"
2. Drag and drop all files from this folder
3. Click "Commit changes"

### Step 3: Configure Email Secrets ⚙️

1. Go to your repository → **Settings** tab
2. Click **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets one by one:

| Secret Name | Value Example | Required? |
|-------------|--------------|-----------|
| `EMAIL_SMTP_SERVER` | `smtp.gmail.com` | Yes |
| `EMAIL_SMTP_PORT` | `587` | Yes |
| `EMAIL_USERNAME` | `yourname@gmail.com` | Yes |
| `EMAIL_PASSWORD` | `xxxx xxxx xxxx xxxx` | Yes |
| `EMAIL_FROM` | `yourname@gmail.com` | Yes |
| `EMAIL_TO` | `yourname@gmail.com` | Yes |

#### 🔐 Getting Gmail App Password

If using Gmail:

1. Go to [Google Account](https://myaccount.google.com/)
2. Security → 2-Step Verification (enable if not enabled)
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select "Mail" and your device
5. Copy the 16-character password
6. Use this as `EMAIL_PASSWORD`

**For other email providers:**
- Outlook/Hotmail: `smtp-mail.outlook.com`, port 587
- Yahoo: `smtp.mail.yahoo.com`, port 587
- Custom domain: Use your provider's SMTP settings

### Step 4: Enable GitHub Pages 🌐

1. Settings → **Pages**
2. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: Select **gh-pages** (will be created automatically)
   - Folder: **/** (root)
3. Click **Save**

### Step 5: Enable GitHub Actions ⚡

1. Go to **Actions** tab
2. You'll see "Conference Digest Weekly" workflow
3. Click **"I understand my workflows, go ahead and enable them"**

### Step 6: Run First Manual Trigger 🎯

1. In Actions tab, click "Conference Digest Weekly"
2. Click **"Run workflow"** button
3. Select branch: `main`
4. Click **"Run workflow"**

### Step 7: Wait for Completion ⏱️

The workflow will:
1. Install Python dependencies
2. Run the conference scraper
3. Generate website files
4. Deploy to GitHub Pages
5. Send email (if configured)

This takes 2-5 minutes.

### Step 8: View Your Website 🎉

After successful deployment:

```
https://YOUR_USERNAME.github.io/conference-digest/
```

You should see a beautiful website with sample conferences!

---

## 📧 Testing Email Delivery

After first successful run:

1. Check your inbox for the digest email
2. If not received, check:
   - Actions logs for errors
   - Spam folder
   - Secret configuration

---

## 🔧 Troubleshooting

### Workflow Fails Immediately

**Error: Permission denied**
- Go to Settings → Actions → General
- Under "Workflow permissions", select "Read and write permissions"
- Save and re-run

### No Conferences Found

This is normal initially - real scraping depends on source availability.
The sample data demonstrates the format.

### Email Not Sent

1. Verify all 6 email secrets are set correctly
2. For Gmail, ensure you're using App Password (not regular password)
3. Check 2FA is enabled on Google account
4. Review Actions logs for specific error

### Website Shows Sample Data Only

The scraper may not find real conferences due to:
- Website blocking automated access
- Changed website structure
- No matching conferences in deadline window

**Solutions:**
- Add more sources in `src/config.py`
- Adjust topic filters
- Use search API (Serper, Google Custom Search)

### GitHub Pages Not Updating

1. Check Actions workflow completed successfully
2. Verify Pages is configured for `gh-pages` branch
3. Wait 2-3 minutes after deployment
4. Hard refresh browser (Ctrl+Shift+R)

---

## 📅 Automatic Schedule

The workflow runs automatically every **Sunday at 8:00 AM Malaysia Time**.

To change schedule, edit `.github/workflows/digest.yml`:

```yaml
schedule:
  - cron: '0 0 * * 0'  # Sunday 00:00 UTC = 8:00 AM MYT
```

Cron format: `minute hour day month weekday`

Common schedules:
- Every Monday 8 AM MYT: `0 0 * * 1`
- Every Wednesday 8 AM MYT: `0 0 * * 3`
- Daily 8 AM MYT: `0 0 * * *`

---

## 🎨 Customization

### Change Topics

Edit `src/config.py` - modify the `TOPICS` list:

```python
TOPICS = [
    "Your Topic Here",
    "Another Topic",
    # ...
]
```

### Change Deadline Window

Edit `src/config.py`:

```python
DEADLINE_WINDOW_DAYS = 120  # Change to 60, 90, 180, etc.
```

### Change Location Focus

Edit `src/config.py` - modify `ALLOWED_COUNTRIES` list.

### Add More Sources

Edit `src/config.py` - add to `CONFERENCE_SOURCES`:

```python
{"name": "new_source", "url": "https://example.com", "type": "html"},
```

---

## 📊 What You Get

### Weekly Email
- Beautiful HTML formatted digest
- Conference summary table
- Detailed listings with deadlines
- Direct links to conference websites
- Urgency indicators

### Website Features
- Responsive design (mobile-friendly)
- Filter by topic
- Statistics dashboard
- Archive of all conferences
- RSS feed for subscription
- Automatic updates every week

### Database
- JSON format for easy editing
- Prevents duplicate entries
- Tracks conference history
- Stores relevance scores

---

## 💡 Pro Tips

1. **First Run**: Always trigger manually first to test
2. **Monitor Logs**: Check Actions tab for any issues
3. **Backup Data**: Download `data/conferences.json` periodically
4. **Custom Domain**: Can add custom domain in Pages settings
5. **Multiple Recipients**: Separate emails with commas in `EMAIL_TO`

---

## 🆘 Need Help?

1. Check [README.md](README.md) for detailed documentation
2. Review GitHub Actions logs for errors
3. Open an issue on GitHub for bugs
4. Verify all configuration steps above

---

## ✅ Checklist

Before your first run, ensure:

- [ ] Repository created and files uploaded
- [ ] All 6 email secrets configured
- [ ] GitHub Pages enabled for `gh-pages` branch
- [ ] GitHub Actions enabled
- [ ] Manual workflow trigger completed successfully
- [ ] Website accessible at your username URL
- [ ] Email received (check spam folder)

**Congratulations! Your automated conference digest is now running! 🎉**

Every Sunday morning, you'll receive fresh conference opportunities directly in your inbox!
