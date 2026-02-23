
# Render Deployment Guide - Flask + PostgreSQL (FREE)

Complete guide to deploy the HTASO Umpire Evaluation system on Render with PostgreSQL.

## ✅ What You Get (FREE)

- **Web Service** - Flask application (free tier)
- **PostgreSQL Database** - 90 days data retention (free tier)
- **Persistent Storage** - All evaluations saved in database
- **HTTPS** - Automatic SSL certificate
- **Auto-Deploy** - Deploys from Git on every push

## 📋 Prerequisites

1. GitHub account
2. Render account (free) - https://render.com
3. Git installed locally
4. Your code committed to GitHub

---

## Step 1: Push Code to GitHub

If not already done:

```bash
cd "C:\Users\c65917\OneDrive - Microchip Technology Inc\Documents\Personal\JES Baseball\Umpire Evaluation\flask_app"

# Initialize git (if not already)
git init

# Add files
git add .

# Commit
git commit -m "PostgreSQL database version ready for Render"

# Create GitHub repo and push
# Follow GitHub instructions to add remote and push
```

---

## Step 2: Create PostgreSQL Database on Render

1. **Go to Render Dashboard** - https://dashboard.render.com
2. **Click "New +"** → Select **"PostgreSQL"**
3. **Configure Database:**
   - **Name**: `htaso-eval-db`
   - **Database**: `htaso_eval_db`
   - **User**: `htaso_user`
   - **Region**: Oregon (US West) - recommended
   - **Instance Type**: **Free**
4. **Click "Create Database"**
5. **Wait 2-3 minutes** for database to provision
6. **Copy the "Internal Database URL"** (we'll need this shortly)

---

## Step 3: Create Web Service on Render

1. **Click "New +"** → Select **"Web Service"**
2. **Connect Your GitHub Repository**
   - Click "Connect account" if first time
   - Select your repository
   - Click "Connect"

3. **Configure Web Service:**

   **Basic Settings:**
   - **Name**: `htaso-umpire-eval`
   - **Region**: Oregon (same as database)
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave blank OR set to `flask_app` if at repo root
   - **Environment**: **Python 3**
   - **Build Command**:
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```
     gunicorn wsgi:app
     ```

4. **Instance Type**: Select **Free**

---

## Step 4: Set Environment Variables

In the **Environment** section, add these variables:

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | *Paste Internal Database URL from Step 2* | Auto-connects to PostgreSQL |
| `SECRET_KEY` | *Click "Generate"* | Render will create secure key |
| `FLASK_ENV` | `production` | Production mode |
| `FLASK_DEBUG` | `False` | Disable debug in production |
| `PORT` | `8502` | Port number (optional) |

**Important:** Make sure `DATABASE_URL` points to your Render PostgreSQL database!

---

## Step 5: Deploy!

1. **Click "Create Web Service"**
2. **Watch the logs** as Render:
   - Clones your repository
   - Installs dependencies
   - Starts your application
3. **Wait 3-5 minutes** for first deployment
4. **Look for** "Your service is live" message

---

## Step 6: Initialize Database

After first deployment, the database tables are created automatically!

The app will:
- ✅ Create `admin` and `evaluations` tables
- ✅ Initialize admin with default password: `admin123`
- ✅ Be ready to accept submissions

---

## Step 7: Test Your Deployment

1. **Click the URL** Render provides (e.g., `https://htaso-umpire-eval.onrender.com`)
2. **Test the evaluation form** - should load correctly
3. **Submit a test evaluation**
4. **Login to admin panel** - Click "Manage Submissions"
   - Password: `admin123`
   - **IMPORTANT**: Change password immediately!
5. **Verify evaluation appears** in admin dashboard

---

## 🎉 You're Live!

Your application is now:
- ✅ Running on Render's infrastructure
- ✅ Using PostgreSQL database
- ✅ All data persists (won't be lost on restart!)
- ✅ Accessible via HTTPS
- ✅ Completely FREE

---

## 📊 What Happens on Free Tier?

### Good News ✅
- **Data persists forever** (in database)
- **Evaluations are never lost**
- **Database always running**

### Minor Limitation ⚠️
- **Web service spins down after 15 min inactivity**
- **First request after inactivity takes 30-60 seconds** (cold start)
- **Then works normally**
- **Does NOT affect data** - everything saved in database!

### How It Feels to Users:
- **Active use**: Fast and responsive
- **After 15 min idle**: First page load slow, then normal
- **Data**: Always safe and available

---

## 🔧 Customization

### Change Default Admin Password

**Option 1: Via Web Interface (Recommended)**
1. Login with `admin123`
2. Click "Change Password"
3. Enter new password

**Option 2: Via Render Shell**
1. Go to Render Dashboard → Your Web Service
2. Click "Shell" tab
3. Run:
```python
python
from app import create_app
from models.database import db, Admin
import hashlib

app = create_app('production')
with app.app_context():
    admin = Admin.query.first()
    admin.password_hash = hashlib.sha256("your-new-password".encode()).hexdigest()
    db.session.commit()
    print("Password updated!")
```

### Custom Domain

1. Go to your Web Service settings
2. Click "Custom Domain"
3. Add your domain
4. Follow DNS configuration instructions

---

## 🔄 Updating Your App

### Automatic Deployment

Every time you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push
```

Render automatically:
1. Detects the push
2. Builds new version
3. Deploys (with zero downtime!)
4. Database data is preserved

### Manual Deployment

In Render Dashboard:
1. Go to your Web Service
2. Click "Manual Deploy" → "Deploy latest commit"

---

## 📈 Monitoring

### View Logs

1. **Render Dashboard** → Your Web Service
2. Click **"Logs"** tab
3. See real-time application logs
4. Check for errors or activity

### Check Database

1. **Render Dashboard** → Your PostgreSQL Database
2. Click **"Connect"** for connection details
3. Use any PostgreSQL client (pgAdmin, DBeaver, etc.)

---

## 💾 Backup & Data Management

### Manual Database Backup

1. Go to PostgreSQL database in Render
2. Click "Connect" → Copy External Database URL
3. Use `pg_dump`:
```bash
pg_dump "external-database-url" > backup.sql
```

### Restore from Backup

```bash
psql "external-database-url" < backup.sql
```

### Export All Evaluations (Via App)

Add this route to your app for easy backup:
```python
@admin_bp.route('/export/all')
@admin_required
def export_all():
    import json
    from models.evaluation_service import list_evaluations

    evals = list_evaluations()
    data = json.dumps(evals, indent=2)

    return send_file(
        BytesIO(data.encode()),
        as_attachment=True,
        download_name=f'all_evaluations_{datetime.now().strftime("%Y%m%d")}.json',
        mimetype='application/json'
    )
```

---

## 🆘 Troubleshooting

### App Won't Start

**Check logs** for errors:
1. Render Dashboard → Logs
2. Look for Python errors
3. Common issues:
   - Missing dependencies → Check requirements.txt
   - Database connection → Verify DATABASE_URL
   - Import errors → Check all files uploaded

### Database Connection Error

**Symptoms:**
```
psycopg2.OperationalError: connection failed
```

**Solution:**
1. Verify `DATABASE_URL` environment variable is set
2. Make sure it's the **Internal Database URL** (not External)
3. Check database is running (should show "Available")

### Slow First Load

**Expected behavior** on free tier:
- After 15 min inactivity, service spins down
- First request wakes it up (30-60 seconds)
- Subsequent requests are fast

**Not a bug!** This is how free tier works.

**Solutions:**
- Upgrade to paid tier ($7/month) for always-on
- Use uptime monitoring to ping every 14 minutes (keeps it awake)
- Accept cold starts (users wait once, then fast)

### Admin Login Fails

**Solutions:**
1. Try default password: `admin123`
2. Check logs for database errors
3. Reinitialize admin:
```bash
# In Render Shell
python
from app import create_app
from utils.auth import init_admin_db

app = create_app('production')
with app.app_context():
    init_admin_db()
```

---

## 🔐 Security Best Practices

### Must Do:
1. ✅ Change admin password from `admin123`
2. ✅ Keep `SECRET_KEY` secure (don't commit to Git)
3. ✅ Use HTTPS (automatic on Render)
4. ✅ Keep dependencies updated

### Optional but Recommended:
- Rate limiting on login
- IP whitelist for admin panel
- Two-factor authentication
- Regular backups

---

## 💰 Cost Breakdown

| Service | Free Tier | Paid Option |
|---------|-----------|-------------|
| **Web Service** | 750 hrs/month | $7/month (always-on) |
| **PostgreSQL** | 90 days data | $7/month (unlimited) |
| **Total** | **$0/month** | $14/month (pro features) |

**Free tier is perfect for:**
- Small teams
- Low to moderate traffic
- Development/testing
- Budget-conscious deployments

**Upgrade when:**
- Need always-on (no cold starts)
- Want >90 days data retention
- High traffic (>100k requests/month)

---

## 📞 Getting Help

### Render Support
- https://render.com/docs
- Community forum: https://community.render.com
- Email: support@render.com (paid plans)

### Application Issues
- Check logs in Render Dashboard
- Review README.md in your repository
- Verify environment variables

---

## 🎓 Next Steps

1. ✅ **Change admin password**
2. ✅ **Test thoroughly** with real evaluations
3. ✅ **Share URL** with your team
4. ✅ **Set up custom domain** (optional)
5. ✅ **Schedule regular backups**
6. ✅ **Monitor usage** in Render dashboard

---

## ✨ Success!

Your HTASO Umpire Evaluation system is now:
- 🌐 **Live on the internet**
- 💾 **Data-persistent** (PostgreSQL)
- 🔒 **Secure** (HTTPS)
- 🆓 **Free** (Render free tier)
- 📱 **Accessible anywhere**

**Congratulations!** 🎉

You've successfully deployed a production-ready web application with database persistence, all on the free tier!
