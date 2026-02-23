# HTASO Umpire Evaluation - Flask Web Application

A comprehensive web-based evaluation system for tracking and managing umpire training and performance assessments. This Flask application provides the same functionality as the desktop version with a modern, responsive web interface.

## Features

### Core Functionality
- **Dynamic Evaluation Forms** - Automatically loaded from Excel template
- **6 Evaluator Information Fields** - Capture essential session details
- **5-Point Rating Scale** - With "Not Observed" option for N/A items
- **Section-Based Evaluation** - Organized criteria with subsections
- **Score Calculation** - Automatic averaging and section summaries
- **4 Recommendation Options** - Color-coded for visual clarity
- **Comprehensive Comments** - Four text areas for detailed feedback
- **Form Validation** - Client and server-side validation

### Admin Features
- **Password-Protected Access** - SHA256 hashed authentication
- **Evaluation Dashboard** - View all submissions in one place
- **Trainer Filtering** - Filter evaluations by trainer name
- **Detailed Views** - Complete evaluation breakdown
- **Export Capabilities** - PDF and Word document generation
- **Password Management** - Change admin password securely

### Export Options
- **PDF Reports** - Professional formatted evaluation reports
- **Word Documents** - Editable .docx exports
- **Current Form Export** - Export without saving to system
- **Stored Evaluation Export** - Export from admin dashboard

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Setup Steps

1. **Navigate to the Flask app directory:**
   ```bash
   cd flask_app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment configuration:**
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and set your SECRET_KEY:
   ```
   SECRET_KEY=your-unique-secret-key-here
   ```

6. **Verify directory structure:**
   The application expects the following structure:
   ```
   flask_app/
   ├── evaluation_data/          # Will be created automatically
   ├── Evaluator Training Eval form.xlsx  # Place in parent directory
   └── logo-150.png               # Copied to static/images/
   ```

## Running the Application

### Development Mode

```bash
python app.py
```

The application will start on `http://localhost:8502`

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8502 wsgi:app
```

## Default Credentials

**Admin Password:** `admin123`

⚠️ **IMPORTANT:** Change the default password immediately after first login!

## Usage

### For Evaluators

1. **Navigate to the home page** (`http://localhost:5000`)
2. **Complete the evaluation form:**
   - Fill in Evaluator & Session Details (required fields marked with *)
   - Select Overall Recommendation
   - Rate each criterion using the dropdown menus
   - Provide comments in the four text areas
3. **Submit the evaluation** or **export as PDF/Word**

### For Administrators

1. **Click "Manage Submissions"** in the header
2. **Log in** with admin password
3. **View dashboard** with all submitted evaluations
4. **Filter by trainer** using the dropdown
5. **View details** by clicking the eye icon
6. **Export evaluations** as PDF or Word documents
7. **Change password** using the "Change Password" button

## File Structure

```
flask_app/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── wsgi.py                     # WSGI entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── README.md                   # This file
├── DEPLOYMENT.md               # Deployment guide
├── models/
│   └── evaluation.py           # Data models and business logic
├── routes/
│   ├── main.py                 # Public routes
│   └── admin.py                # Admin routes
├── utils/
│   ├── excel_parser.py         # Excel criteria loading
│   ├── export_pdf.py           # PDF export functionality
│   ├── export_word.py          # Word export functionality
│   └── auth.py                 # Authentication helpers
├── static/
│   ├── css/
│   │   └── style.css           # Custom styles
│   ├── js/
│   │   └── app.js              # Client-side JavaScript
│   └── images/
│       └── logo-150.png        # HTASO logo
└── templates/
    ├── base.html               # Base template
    ├── index.html              # Evaluation form
    └── admin/
        ├── login.html          # Admin login
        ├── dashboard.html      # Admin dashboard
        └── detail.html         # Evaluation detail view
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Data Directory
DATA_DIR=../evaluation_data
ADMIN_CONFIG=../evaluation_data/admin_config.json

# Excel Template
CRITERIA_PATH=../Evaluator Training Eval form.xlsx
```

### Configuration Classes

The application supports three configuration modes:
- **Development** - Debug mode enabled, detailed error pages
- **Production** - Debug disabled, secure cookies, optimized
- **Testing** - For automated testing, CSRF disabled

Set the mode using the `FLASK_ENV` environment variable.

## Data Storage

### JSON File Structure

Evaluations are stored as JSON files in:
```
evaluation_data/
├── admin_config.json           # Admin password hash
└── {Trainer_Name}/
    └── {Evaluator_Name}_{timestamp}.json
```

### Evaluation Data Format

```json
{
  "evaluator_name": "John Doe",
  "trainer_name": "Jane Smith",
  "training_date": "01/13/2026",
  "observation_date": "01/13/2026",
  "training_location": "Training Center A",
  "eval_type": "Initial Training",
  "recommendation": "Approved for Independent Evaluation",
  "ratings": [
    {
      "key": "plate_work_mechanics_01",
      "section": "Plate Work",
      "subsection": "Mechanics",
      "prompt": "Proper stance and positioning",
      "selection": "5 - Excellent",
      "score": 5
    }
  ],
  "average_score": 0.85,
  "score_percentage": 85.0,
  "rated_item_count": 12,
  "total_score": 51,
  "total_possible": 60,
  "section_totals": [
    {
      "section": "Plate Work",
      "score": 25,
      "possible": 30,
      "percentage": 0.833
    }
  ],
  "comments": {
    "strengths": "Strong knowledge of rules...",
    "improvement": "Work on positioning...",
    "development": "Attend advanced clinic...",
    "overall": "Solid performance overall..."
  },
  "submission_date": "01/13/2026 02:30 PM"
}
```

## Security

### Authentication
- Admin password stored as SHA256 hash
- Session-based authentication with secure cookies
- Password minimum length enforced (6 characters)
- Session timeout after 1 hour of inactivity

### Input Validation
- Server-side validation of all form inputs
- Client-side validation for improved UX
- SQL injection prevention (no SQL used)
- XSS prevention through template escaping

### File Security
- Path traversal prevention in file access
- Evaluation IDs validated before file operations
- Admin-only access to stored evaluations

## Troubleshooting

### Excel Template Not Loading

**Issue:** Evaluation criteria not displayed

**Solutions:**
1. Verify the Excel file exists at the configured path
2. Close the Excel file if it's open
3. Check the sheet name is "Eval. & Obser. Criteria"
4. Ensure openpyxl is installed: `pip install openpyxl`

### Logo Not Displaying

**Issue:** Logo image not showing in header

**Solutions:**
1. Verify `logo-150.png` exists in `static/images/`
2. Check file permissions
3. Clear browser cache

### Admin Login Fails

**Issue:** Cannot log in to admin panel

**Solutions:**
1. Try default password: `admin123`
2. Delete `evaluation_data/admin_config.json` to reset
3. Restart the application
4. Check that session secret key is set

### Export Fails

**Issue:** PDF or Word export doesn't work

**Solutions:**
1. Verify reportlab is installed: `pip install reportlab`
2. Verify python-docx is installed: `pip install python-docx`
3. Check that evaluator name is filled in
4. Check server logs for specific error messages

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines. Use flake8 for linting:

```bash
pip install flake8
flake8 .
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes
3. Test thoroughly
4. Update documentation
5. Create pull request

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions including:
- Heroku deployment
- PythonAnywhere deployment
- AWS Elastic Beanstalk
- DigitalOcean App Platform
- Docker containerization

## Support

For issues, questions, or feature requests:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) for deployment issues
3. Contact the development team

## License

Copyright © 2026 HTASO. All rights reserved.

## Changelog

### Version 1.0 (January 2026)
- Initial release
- Complete feature parity with desktop application
- Modern responsive web interface
- Bootstrap 5 design system
- Admin dashboard with filtering
- PDF and Word export functionality
- Comprehensive documentation
