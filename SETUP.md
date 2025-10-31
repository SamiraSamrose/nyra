## File: SETUP.md

```markdown
# NYRA Setup Guide

## Prerequisites

- Python 3.9 or higher
- Node.js 16+ (for frontend tooling)
- Google Cloud Platform account
- Firebase project
- Chrome browser (for Chrome AI APIs)

## Step 1: Environment Setup

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Install System Dependencies

```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-dev build-essential

# For macOS
brew install python@3.9
```

## Step 2: Google Cloud Configuration

### Enable Required APIs

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable translate.googleapis.com
gcloud services enable firestore.googleapis.com
```

### Create Service Account

```bash
gcloud iam service-accounts create nyra-service \
    --display-name="NYRA Service Account"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:nyra-service@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud iam service-accounts keys create config/service-account.json \
    --iam-account=nyra-service@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

## Step 3: Firebase Setup

1. Go to Firebase Console (https://console.firebase.google.com)
2. Create new project or select existing
3. Enable Authentication (Email/Password, Google)
4. Enable Firestore Database
5. Download config and save to `config/firebase_config.json`

## Step 4: Environment Variables

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
GOOGLE_CLOUD_PROJECT=your-project-id
GEMINI_API_KEY=your-gemini-api-key
FIREBASE_CONFIG_PATH=config/firebase_config.json
BIGQUERY_DATASET=nyra_analytics
PORT=5000
```

## Step 5: Database Initialization

```bash
python backend/utils/init_db.py
```

## Step 6: Run Application

```bash
# Development mode
python backend/app.py

# Production mode with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

## Step 7: Verify Installation

Open browser to http://localhost:5000

Test features:
1. Prompt API - Generate text completions
2. Summarizer - Summarize content
3. Translator - Translate text
4. SQL Optimizer - Analyze queries
5. DevOps Analyzer - Review infrastructure code

## Troubleshooting

### Chrome AI APIs not available
- Ensure Chrome version 127+
- Enable flags: chrome://flags/#optimization-guide-on-device-model
- Restart browser

### Firebase connection errors
- Verify firebase_config.json is valid
- Check service account permissions

### Gemini API errors
- Verify API key is active
- Check quota limits in GCP console

## Development

```bash
# Run tests
pytest tests/

# Code formatting
black backend/
pylint backend/

# Type checking
mypy backend/
```