# Deployment Guide - HTASO Umpire Evaluation Flask App

This guide provides detailed instructions for deploying the HTASO Umpire Evaluation Flask application to various hosting platforms.

## Table of Contents
1. [General Prerequisites](#general-prerequisites)
2. [Heroku Deployment](#heroku-deployment)
3. [PythonAnywhere Deployment](#pythonanywhere-deployment)
4. [AWS Elastic Beanstalk](#aws-elastic-beanstalk)
5. [DigitalOcean App Platform](#digitalocean-app-platform)
6. [Render Deployment](#render-deployment)
7. [Docker Deployment](#docker-deployment)
8. [Production Checklist](#production-checklist)

---

## General Prerequisites

Before deploying to any platform, ensure:

1. **Generate a secure SECRET_KEY:**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Set production environment variables:**
   ```bash
   SECRET_KEY=<generated-secret-key>
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

3. **Verify all dependencies are in requirements.txt:**
   ```bash
   pip freeze > requirements.txt
   ```

4. **Test locally first:**
   ```bash
   FLASK_ENV=production python app.py
   ```

---

## Heroku Deployment

### Step 1: Install Heroku CLI

Download from [heroku.com/downloads](https://www.heroku.com/downloads)

### Step 2: Create Procfile

Create `Procfile` in the `flask_app/` directory:
```
web: gunicorn wsgi:app
```

### Step 3: Add Gunicorn to requirements.txt

```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

### Step 4: Initialize Git (if not already done)

```bash
cd flask_app
git init
git add .
git commit -m "Initial commit"
```

### Step 5: Create Heroku App

```bash
heroku login
heroku create htaso-umpire-eval
```

### Step 6: Set Environment Variables

```bash
heroku config:set SECRET_KEY=<your-secret-key>
heroku config:set FLASK_ENV=production
heroku config:set DATA_DIR=evaluation_data
heroku config:set ADMIN_CONFIG=evaluation_data/admin_config.json
heroku config:set CRITERIA_PATH=Evaluator_Training_Eval_form.xlsx
```

### Step 7: Upload Files to Heroku

Since evaluation data and Excel file aren't in Git, you'll need to handle them separately:

**Option A: Use Heroku Postgres** (recommended for production)
- Migrate from JSON to database storage

**Option B: Use S3 or similar** for file storage

### Step 8: Deploy

```bash
git push heroku main
```

### Step 9: Scale the App

```bash
heroku ps:scale web=1
```

### Step 10: Open the App

```bash
heroku open
```

### Heroku-Specific Notes

- Free tier sleeps after 30 minutes of inactivity
- File system is ephemeral (resets on each deploy)
- Consider using Heroku Postgres + file storage for production
- Set up SSL automatically with Heroku

---

## PythonAnywhere Deployment

### Step 1: Sign Up

Create account at [pythonanywhere.com](https://www.pythonanywhere.com)

### Step 2: Upload Files

Use the Files tab to upload your project or clone from Git:
```bash
git clone <your-repo-url> ~/htaso-eval
```

### Step 3: Create Virtual Environment

In Bash console:
```bash
cd ~/htaso-eval/flask_app
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration" and Python 3.10
4. Set source code directory: `/home/yourusername/htaso-eval/flask_app`
5. Set virtualenv: `/home/yourusername/htaso-eval/flask_app/venv`

### Step 5: Edit WSGI Configuration

Click on WSGI configuration file link and replace with:
```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/htaso-eval/flask_app'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from app import create_app
application = create_app('production')
```

### Step 6: Set Static Files Mapping

In Web tab, add static files mapping:
- URL: `/static/`
- Directory: `/home/yourusername/htaso-eval/flask_app/static/`

### Step 7: Create Data Directories

In Bash console:
```bash
mkdir -p ~/htaso-eval/evaluation_data
```

### Step 8: Reload Web App

Click "Reload" button in Web tab

### PythonAnywhere Notes

- Free tier has limited CPU time
- Persistent file storage included
- No need for external database for JSON storage
- HTTPS included on all apps

---

## AWS Elastic Beanstalk

### Step 1: Install EB CLI

```bash
pip install awsebcli
```

### Step 2: Initialize EB

```bash
cd flask_app
eb init -p python-3.10 htaso-eval
```

### Step 3: Create Environment

```bash
eb create htaso-eval-env
```

### Step 4: Set Environment Variables

```bash
eb setenv SECRET_KEY=<your-secret-key> FLASK_ENV=production
```

### Step 5: Deploy

```bash
eb deploy
```

### Step 6: Open Application

```bash
eb open
```

### AWS-Specific Configuration

Create `.ebextensions/python.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: wsgi:application
  aws:elasticbeanstalk:application:environment:
    FLASK_ENV: production
```

### AWS Notes

- Use RDS for database if migrating from JSON
- Use S3 for file storage
- Configure security groups properly
- Set up CloudFront for CDN
- Costs vary based on instance type

---

## DigitalOcean App Platform

### Step 1: Push Code to Git

Ensure code is in GitHub, GitLab, or Bitbucket

### Step 2: Create New App

1. Go to [cloud.digitalocean.com/apps](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect repository

### Step 3: Configure Build Settings

**Build Command:**
```bash
pip install -r requirements.txt
```

**Run Command:**
```bash
gunicorn --worker-tmp-dir /dev/shm wsgi:app
```

### Step 4: Set Environment Variables

Add in App settings:
```
SECRET_KEY=<your-secret-key>
FLASK_ENV=production
DATA_DIR=/data/evaluation_data
```

### Step 5: Add Persistent Storage

1. Go to Components → Add Component
2. Choose "Database" or "Volume" for evaluation data
3. Mount at `/data`

### Step 6: Deploy

Click "Deploy" and wait for build

### DigitalOcean Notes

- $5/month basic tier available
- Automatic HTTPS with Let's Encrypt
- Auto-scaling options
- Built-in monitoring

---

## Render Deployment

### Step 1: Push to Git

Ensure code is on GitHub

### Step 2: Create New Web Service

1. Go to [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub repository

### Step 3: Configure Service

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn wsgi:app
```

**Environment:** Python 3

### Step 4: Add Environment Variables

```
SECRET_KEY=<your-secret-key>
FLASK_ENV=production
PYTHON_VERSION=3.10.0
```

### Step 5: Add Disk Storage

For persistent evaluation data:
1. Go to "Disks" tab
2. Add disk mounted at `/opt/render/project/src/evaluation_data`

### Step 6: Deploy

Click "Create Web Service"

### Render Notes

- Free tier available (with limitations)
- Automatic HTTPS
- Zero-downtime deploys
- Easy to set up

---

## Docker Deployment

### Step 1: Create Dockerfile

Create `Dockerfile` in `flask_app/`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directory
RUN mkdir -p /app/evaluation_data

# Expose port
EXPOSE 8502

# Set environment variables
ENV FLASK_ENV=production

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8502", "--workers", "4", "wsgi:app"]
```

### Step 2: Create .dockerignore

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.git
.gitignore
*.log
```

### Step 3: Build Image

```bash
docker build -t htaso-eval:latest .
```

### Step 4: Run Container

```bash
docker run -d -p 8502:8502 \
  -e SECRET_KEY=your-secret-key \
  -e FLASK_ENV=production \
  -v $(pwd)/evaluation_data:/app/evaluation_data \
  --name htaso-eval \
  htaso-eval:latest
```

### Step 5: Docker Compose (Optional)

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8502:8502"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=production
    volumes:
      - ./evaluation_data:/app/evaluation_data
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

### Docker Notes

- Easy to deploy anywhere Docker runs
- Consistent environment
- Easy scaling with orchestration (Kubernetes, Swarm)
- Volume for persistent data

---

## Production Checklist

### Security

- [ ] Changed default admin password
- [ ] Set strong SECRET_KEY (at least 32 random characters)
- [ ] Set `FLASK_DEBUG=False`
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS (SSL/TLS certificate)
- [ ] Set secure cookie flags in production config
- [ ] Review and limit CORS if applicable
- [ ] Implement rate limiting for login attempts
- [ ] Regular security audits

### Performance

- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Set appropriate number of workers (2-4 × CPU cores)
- [ ] Enable gzip compression
- [ ] Configure static file caching
- [ ] Set up CDN for static assets (optional)
- [ ] Monitor memory usage
- [ ] Set up logging and monitoring

### Data Management

- [ ] Set up automated backups of evaluation_data
- [ ] Test backup restoration process
- [ ] Plan for data migration if scaling
- [ ] Set up log rotation
- [ ] Monitor disk space usage

### Availability

- [ ] Set up health check endpoint
- [ ] Configure automatic restarts on failure
- [ ] Set up uptime monitoring
- [ ] Plan for zero-downtime deployments
- [ ] Document rollback procedure

### Monitoring & Logging

- [ ] Set up error tracking (Sentry, Rollbar)
- [ ] Configure application logging
- [ ] Set up performance monitoring (New Relic, DataDog)
- [ ] Create alerts for critical errors
- [ ] Monitor evaluation submission rate

### Documentation

- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document environment variables
- [ ] Create admin guide
- [ ] Document backup/restore procedures

---

## Maintenance

### Regular Tasks

**Weekly:**
- Review error logs
- Check disk space
- Verify backups are working

**Monthly:**
- Update dependencies
- Review security advisories
- Test backup restoration
- Review access logs

**Quarterly:**
- Security audit
- Performance review
- Dependency vulnerability scan
- Disaster recovery drill

### Updating the Application

1. **Test updates locally first**
2. **Create backup:**
   ```bash
   tar -czf backup-$(date +%Y%m%d).tar.gz evaluation_data/
   ```
3. **Deploy updates**
4. **Monitor for errors**
5. **Rollback if needed**

---

## Troubleshooting Production Issues

### Application Won't Start

1. Check logs: `heroku logs --tail` or platform equivalent
2. Verify environment variables are set
3. Check that all dependencies installed
4. Verify WSGI configuration

### 502 Bad Gateway

1. Check if application is running
2. Verify port binding (0.0.0.0 not localhost)
3. Check worker processes
4. Review memory limits

### Slow Performance

1. Increase worker count
2. Enable caching
3. Profile slow endpoints
4. Check database queries (if migrated to DB)
5. Review concurrent user load

### Data Loss

1. Restore from backup
2. Check file system persistence
3. Review deployment process
4. Consider migrating to database

---

## Support

For deployment issues:
1. Check platform-specific documentation
2. Review this guide thoroughly
3. Check error logs
4. Contact platform support
5. Refer to Flask deployment documentation

## Additional Resources

- [Flask Deployment Options](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [OWASP Security Guidelines](https://owasp.org/www-project-web-security-testing-guide/)
