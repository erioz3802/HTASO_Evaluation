# Getting Started Checklist

Use this checklist to get your Flask web application up and running!

## ☑️ Pre-Flight Checklist

### Environment Setup

- [ ] Python 3.8+ installed
- [ ] pip installed
- [ ] Git installed (optional)
- [ ] Text editor ready (VS Code, PyCharm, etc.)

### Files Verified

- [ ] `flask_app/` directory exists
- [ ] `Evaluator Training Eval form.xlsx` in parent directory
- [ ] `logo-150.png` copied to `static/images/`
- [ ] `evaluation_data/` directory exists (or will be auto-created)

---

## 🚀 Step-by-Step Launch

### 1. Open Terminal

```bash
cd "C:\Users\c65917\OneDrive - Microchip Technology Inc\Documents\Personal\JES Baseball\Umpire Evaluation\flask_app"
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-3.0.0 ...
```

### 5. Create Environment File

```bash
copy .env.example .env
```

**Edit `.env` and set:**
```
SECRET_KEY=change-this-to-random-string
FLASK_ENV=development
FLASK_DEBUG=True
```

### 6. Verify Configuration

```bash
python -c "from config import config; print('Config OK!')"
```

### 7. Run the Application

```bash
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:8502
```

### 8. Open Browser

Navigate to: **http://localhost:8502**

You should see the HTASO Umpire Evaluation form!

---

## ✅ Verification Tests

### Test 1: Home Page

- [ ] Page loads without errors
- [ ] Logo displays in header
- [ ] Form fields are visible
- [ ] Dropdowns work
- [ ] CSS styles are applied

**If it doesn't work:**
- Check console for errors (F12 in browser)
- Verify all dependencies installed
- Check that logo file exists

### Test 2: Submit Evaluation

- [ ] Fill in Evaluator Name
- [ ] Fill in Trainer Name
- [ ] Fill in Training Date
- [ ] Select a Recommendation
- [ ] Rate at least one criterion
- [ ] Add a comment
- [ ] Click "Submit Evaluation"
- [ ] Success message appears
- [ ] Data saved to `evaluation_data/`

**If it doesn't work:**
- Check required fields are filled
- Verify `evaluation_data/` directory exists
- Check browser console for JavaScript errors

### Test 3: Admin Login

- [ ] Click "Manage Submissions" in header
- [ ] Enter password: `admin123`
- [ ] Click Login
- [ ] Dashboard appears with submitted evaluations
- [ ] Filter dropdown works
- [ ] View details button works

**If it doesn't work:**
- Verify `admin_config.json` exists
- Try deleting `admin_config.json` and restart app
- Check that data directory path is correct

### Test 4: View Evaluation

- [ ] From dashboard, click eye icon on an evaluation
- [ ] Detail page loads
- [ ] All information displays correctly
- [ ] Export PDF button works
- [ ] Export Word button works

**If it doesn't work:**
- Verify evaluation JSON file exists
- Check file permissions
- Verify reportlab and python-docx installed

### Test 5: Export from Form

- [ ] Fill out evaluation form (without submitting)
- [ ] Click "Export PDF Report"
- [ ] PDF downloads successfully
- [ ] PDF contains form data
- [ ] Repeat for "Export Word Report"

**If it doesn't work:**
- Verify evaluator name is filled in
- Check that logo file exists
- Verify export libraries installed

### Test 6: Change Password

- [ ] Log in to admin panel
- [ ] Click "Change Password"
- [ ] Enter current password: `admin123`
- [ ] Enter new password (min 6 chars)
- [ ] Confirm new password
- [ ] Click "Change Password"
- [ ] Success message appears
- [ ] Log out and log back in with new password

**If it doesn't work:**
- Verify current password is correct
- Ensure new passwords match
- Check password length (min 6)

---

## 🎯 Quick Fixes

### Port Already in Use

**Error:** `Address already in use`

**Fix:**
```bash
# Edit app.py and change port 8502 to another port like 8503
```

Or kill existing process:
```bash
# Windows
netstat -ano | findstr :8502
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8502 | xargs kill -9
```

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Fix:**
```bash
# Verify virtual environment is activated
pip install -r requirements.txt
```

### Excel Template Not Found

**Error:** Criteria not loading

**Fix:**
1. Verify file exists: `ls "../Evaluator Training Eval form.xlsx"`
2. Update path in `.env`: `CRITERIA_PATH=../Evaluator Training Eval form.xlsx`
3. Restart application

### Logo Not Displaying

**Error:** Logo image missing

**Fix:**
```bash
# Copy logo from parent directory
copy "..\logo-150.png" "static\images\"
```

### Permission Denied on evaluation_data

**Error:** Cannot write to directory

**Fix:**
```bash
# Create directory with proper permissions
mkdir -p evaluation_data
chmod 755 evaluation_data  # macOS/Linux
```

---

## 📚 Next Steps

### You're Up and Running! Now What?

1. **Read Full Documentation**
   - [ ] Review [README.md](README.md)
   - [ ] Check [MIGRATION.md](MIGRATION.md) if coming from desktop app
   - [ ] Review [DEPLOYMENT.md](DEPLOYMENT.md) for production

2. **Customize (Optional)**
   - [ ] Change admin password from default
   - [ ] Update logo in `static/images/`
   - [ ] Modify colors in `static/css/style.css`
   - [ ] Add additional fields if needed

3. **Test Thoroughly**
   - [ ] Submit multiple evaluations
   - [ ] Test all export functions
   - [ ] Verify data appears in admin panel
   - [ ] Test on different browsers
   - [ ] Test on mobile device

4. **Deploy (When Ready)**
   - [ ] Choose hosting platform (Heroku, PythonAnywhere, etc.)
   - [ ] Follow [DEPLOYMENT.md](DEPLOYMENT.md) guide
   - [ ] Set production environment variables
   - [ ] Test deployed application
   - [ ] Update admin password in production

5. **Share with Team**
   - [ ] Train administrators
   - [ ] Create user guide if needed
   - [ ] Set up backup procedures
   - [ ] Monitor usage and feedback

---

## 🆘 Getting Help

### Resources

1. **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
2. **Full Documentation:** [README.md](README.md)
3. **Migration Guide:** [MIGRATION.md](MIGRATION.md)
4. **Deployment:** [DEPLOYMENT.md](DEPLOYMENT.md)
5. **Project Summary:** [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### Troubleshooting Process

1. Check error message in terminal
2. Check browser console (F12 → Console tab)
3. Review relevant documentation section
4. Verify configuration in `.env`
5. Check file permissions
6. Restart application
7. Create minimal test case

### Common Issues Database

**Issue:** App won't start
**Solution:** Check Python version, verify dependencies

**Issue:** Page not loading
**Solution:** Check URL, verify port, check firewall

**Issue:** Form won't submit
**Solution:** Check required fields, check browser console

**Issue:** Admin login fails
**Solution:** Verify password, check admin_config.json

**Issue:** Exports fail
**Solution:** Verify libraries installed, check file paths

---

## 🎉 Success Indicators

You know it's working when:

✅ Application starts without errors
✅ Home page displays with logo and form
✅ Evaluations can be submitted
✅ Data saves to JSON files
✅ Admin panel accessible
✅ Evaluations viewable in dashboard
✅ Exports generate successfully
✅ Password can be changed

---

## 🔄 Development Workflow

### Making Changes

1. **Edit code** in your text editor
2. **Save changes**
3. **Restart application** (Ctrl+C, then `python app.py`)
4. **Refresh browser** (F5)
5. **Test changes**

**Tip:** Set `FLASK_DEBUG=True` for auto-reload on file changes!

### Version Control (Recommended)

```bash
git init
git add .
git commit -m "Initial Flask web app"
```

---

## 📊 Performance Monitoring

### What to Monitor

- Response times (should be < 1 second)
- Error rates (should be near 0%)
- Memory usage (should be stable)
- Disk space (for evaluation_data)

### Simple Monitoring

```bash
# Check app logs
tail -f app.log  # If logging configured

# Check disk space
df -h  # macOS/Linux
dir evaluation_data  # Windows

# Monitor memory
top  # macOS/Linux
taskmgr  # Windows
```

---

## 🎓 Learning Resources

### Flask Documentation
- https://flask.palletsprojects.com/

### Bootstrap Documentation
- https://getbootstrap.com/docs/5.3/

### Python Documentation
- https://docs.python.org/3/

---

## ✨ You Did It!

Congratulations! Your Flask web application is now running. You've successfully:

✅ Set up the development environment
✅ Installed all dependencies
✅ Configured the application
✅ Tested all features
✅ Verified everything works

**Time to celebrate!** 🎉

Then proceed to deploy to production using [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Last Updated:** January 13, 2026
**Application Version:** 1.0
**Status:** Production Ready ✅
