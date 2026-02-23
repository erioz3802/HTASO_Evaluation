# Quick Start Guide - HTASO Flask App

Get up and running in 5 minutes!

## 1. Install Dependencies

```bash
cd flask_app
pip install -r requirements.txt
```

## 2. Set Up Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env and set your SECRET_KEY
# Or use default for development
```

## 3. Run the Application

```bash
python app.py
```

## 4. Access the Application

Open your browser to: **http://localhost:8502**

## 5. Login as Admin

- Click "Manage Submissions" in the header
- Default password: **admin123**
- **IMPORTANT:** Change password after first login!

## That's It!

You're now running the HTASO Umpire Evaluation system.

## Next Steps

- Read [README.md](README.md) for full documentation
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Submit a test evaluation to verify everything works

## Common Issues

### Port Already in Use
```bash
# Use a different port (edit app.py and change 8502 to another port)
```

### Missing Excel Template
- Place `Evaluator Training Eval form.xlsx` in parent directory
- Or update `CRITERIA_PATH` in `.env`

### Logo Not Showing
- Verify `logo-150.png` is in `static/images/`
- Clear browser cache

## Need Help?

Check the [README.md](README.md) troubleshooting section or contact support.
