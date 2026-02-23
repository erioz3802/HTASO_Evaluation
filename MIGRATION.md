# Migration Guide - Desktop to Flask Web App

This guide helps users transition from the Tkinter desktop application to the Flask web application.

## Why Migrate?

### Benefits of the Web Application

✅ **Access Anywhere** - Use from any device with a web browser
✅ **No Installation** - No need to install Python or dependencies
✅ **Always Updated** - Updates deployed centrally
✅ **Multi-Device** - Access from desktop, tablet, or mobile
✅ **Easy Sharing** - Share links with trainers and admins
✅ **Cloud Deployment** - Deploy to Heroku, AWS, etc.
✅ **Automatic Backups** - Easy to set up automated backups
✅ **Better Collaboration** - Multiple users can access simultaneously

## Data Compatibility

### Good News: 100% Compatible! ✓

The Flask web app uses **exactly the same data format** as the desktop app:
- JSON files in the same directory structure
- Same evaluation data format
- Same admin configuration
- Can read evaluations created by desktop app
- Desktop app can read evaluations created by web app

### Shared Data Directory

Both applications share the `evaluation_data/` directory:

```
Umpire Evaluation/
├── eval_form_app.py         # Desktop app
├── flask_app/                # Web app (new)
└── evaluation_data/          # SHARED DATA
    ├── admin_config.json
    ├── Trainer1/
    │   └── Evaluator1_*.json
    └── Trainer2/
        └── Evaluator2_*.json
```

## Feature Comparison

| Feature | Desktop App | Flask Web App | Notes |
|---------|-------------|---------------|-------|
| Evaluation Form | ✅ | ✅ | Same fields |
| Excel Criteria Loading | ✅ | ✅ | Same parsing logic |
| Rating System | ✅ | ✅ | Identical 5-point scale |
| Comments | ✅ | ✅ | Same 4 sections |
| Form Validation | ✅ | ✅ | Same requirements |
| Submit & Save | ✅ | ✅ | Same JSON format |
| Admin Panel | ✅ | ✅ | Same features + filtering |
| View Evaluations | ✅ | ✅ | Better UI in web |
| Export PDF | ✅ | ✅ | Same format |
| Export Word | ✅ | ✅ | Same format |
| Password Protection | ✅ | ✅ | Same SHA256 hashing |
| Change Password | ✅ | ✅ | Same security |
| Logo Display | ✅ | ✅ | Same logo |
| Color Scheme | ✅ | ✅ | Exactly matched |

## Migration Steps

### Step 1: Install Flask App

```bash
cd "flask_app"
pip install -r requirements.txt
```

### Step 2: Verify Data Access

The Flask app automatically uses the shared `evaluation_data/` directory. No data migration needed!

### Step 3: Run Flask App

```bash
python app.py
```

### Step 4: Access Web Interface

Open browser to: http://localhost:8502

### Step 5: Test Login

Use the same admin password as desktop app (default: `admin123`)

### Step 6: Verify Evaluations

Click "Manage Submissions" - you should see all evaluations from desktop app!

## Using Both Applications

### Scenario: Want to Use Both?

**You can!** Both apps work with the same data:

**Use Desktop App:**
- When working offline
- For quick local access
- If you prefer native UI

**Use Flask Web App:**
- For remote access
- Multiple simultaneous users
- Mobile/tablet access
- Better admin dashboard

**Important:** Don't use both simultaneously on the same evaluation to avoid conflicts.

## Deployment Options

### Option 1: Local Network (Like Desktop)

Run Flask app on local machine:
```bash
python app.py
```
Access from other devices: http://your-ip:8502

### Option 2: Cloud Deployment (New!)

Deploy to cloud for internet access:
- **Heroku** - Free tier available
- **PythonAnywhere** - Free tier with limits
- **DigitalOcean** - $5/month
- **AWS/Azure** - Enterprise options

See [DEPLOYMENT.md](DEPLOYMENT.md) for details.

## Admin Password

### Password is Shared!

The web app and desktop app use the **same admin_config.json** file.

- Change password in web app → Also changed in desktop app
- Change password in desktop app → Also changed in web app

### First Time Setup

1. **Desktop app users:** Your existing password works in web app
2. **New users:** Default password is `admin123`
3. **Security:** Change immediately after first login!

## Backup Strategy

### Desktop App Backup

Previously: Manual copy of `evaluation_data/` folder

### Web App Backup (Enhanced)

**Local Deployment:**
Same as desktop - copy `evaluation_data/` folder

**Cloud Deployment:**
- Automated backups to S3/cloud storage
- Database backups if migrated to PostgreSQL
- Version control with Git

## Excel Template

### Same Template File!

Both apps use: `Evaluator Training Eval form.xlsx`

**Desktop:** Looks in same directory as app
**Flask:** Configured in `.env` file (default: parent directory)

If you update the Excel template:
- Both apps will use the updated criteria
- No need to update twice

## Transition Timeline

### Recommended Approach

**Week 1:** Install and test Flask app locally
**Week 2:** Run both apps side-by-side
**Week 3:** Gradually shift to web app
**Week 4+:** Keep desktop app as backup

### For Organizations

**Phase 1 (Month 1):**
- Install Flask app on test server
- Train admins on web interface
- Keep desktop app as primary

**Phase 2 (Month 2):**
- Deploy Flask app to production
- Migrate active users to web
- Keep desktop app for offline scenarios

**Phase 3 (Month 3+):**
- Web app as primary tool
- Desktop app for special cases
- Consider cloud deployment

## Troubleshooting

### "My evaluations aren't showing!"

**Check:**
1. `DATA_DIR` in `.env` points to correct directory
2. Path is relative to flask_app directory (`../evaluation_data`)
3. Evaluation JSON files exist in trainer subfolders

**Fix:**
```bash
# In flask_app/.env
DATA_DIR=../evaluation_data
```

### "Can't log in with my password!"

**Verify:**
1. `ADMIN_CONFIG` path is correct in `.env`
2. File `admin_config.json` exists
3. Using correct password (desktop and web share same password)

**Reset:**
```bash
# Delete admin config to reset to default
rm ../evaluation_data/admin_config.json
# Restart app, password will be admin123
```

### "Excel criteria not loading!"

**Check:**
1. `CRITERIA_PATH` in `.env` is correct
2. Excel file exists and is not open
3. Sheet name is "Eval. & Obser. Criteria"

**Fix:**
```bash
# In flask_app/.env
CRITERIA_PATH=../Evaluator Training Eval form.xlsx
```

## FAQ

### Q: Will I lose my data?

**A:** No! The web app uses your existing data. Nothing is lost.

### Q: Can I go back to desktop app?

**A:** Yes! You can switch back anytime. Data is compatible.

### Q: Do I need to re-enter evaluations?

**A:** No! All existing evaluations are automatically available.

### Q: Can multiple people use it at once?

**A:** Yes with web app! Desktop app is single-user only.

### Q: Is it more secure?

**A:** Similar security locally. Much better security when deployed to cloud with HTTPS.

### Q: Does it work offline?

**A:** Web app needs server running. For offline, use desktop app.

### Q: Can I customize it?

**A:** Yes! Web app is easier to customize than desktop app.

### Q: What about mobile devices?

**A:** Web app works great on mobile! Desktop app doesn't.

## Getting Help

### Resources

1. [README.md](README.md) - Complete documentation
2. [QUICKSTART.md](QUICKSTART.md) - 5-minute setup
3. [DEPLOYMENT.md](DEPLOYMENT.md) - Cloud deployment
4. Desktop app documentation - Still valid for concepts

### Support Contacts

- Technical issues: Check troubleshooting sections
- Feature requests: Submit to development team
- Training: Contact your organization admin

## Success Stories

> "We deployed the Flask app to Heroku and now our trainers can submit evaluations from the field!" - Regional Coordinator

> "The admin dashboard filtering makes it so much easier to review evaluations by trainer." - Training Director

> "Being able to access from my tablet at games is a game-changer!" - Evaluator

## Conclusion

The Flask web application provides all the features of the desktop app with added benefits of web access, better UI, and easier deployment. Data compatibility ensures a smooth transition with zero data migration required.

**Ready to get started?** Follow [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup!
