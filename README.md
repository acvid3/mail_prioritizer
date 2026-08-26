# Mail Prioritizer

AI-powered email sorting system that automatically prioritizes Gmail messages by importance.

## Features

- **OAuth 2.0 Authentication**: Secure Gmail API integration
- **AI Classification**: AI-powered email priority detection with keyword fallback
- **Automatic Labeling**: Applies priority labels (IMPORTANT, NORMAL, LOW_PRIORITY)
- **Batch Processing**: Efficiently processes multiple emails
- **Configurable Settings**: Customizable classification and processing options

## Project Structure

```
mail_prioritizer/
├── app/
│   ├── config.py        # Central config: all URLs and secrets from .env
│   ├── interfaces/      # Pydantic models and protocols (requests/responses)
│   ├── routes/          # FastAPI routers (oauth, emails, classify, labels)
│   └── services/        # Gmail OAuth, Gmail API client, helpers
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── Dockerfile
├── nginx_fastapi.conf
└── .env.example         # Copy to .env and fill in values
```

## Installation

1. Clone the repository
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Setup

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create new project
   - Enable Gmail API

2. **Create OAuth 2.0 Credentials**:
   - Go to Credentials → Create Credentials → OAuth 2.0 Client ID
   - Add the redirect URI (e.g. `https://your-domain/rest/oauth2-credential/callback`) to the authorized redirect URIs
   - Copy `GMAIL_CLIENT_ID` and `GMAIL_CLIENT_SECRET` to `.env`

3. **Configure the app**:
   - `cp .env.example .env` and fill in all values (OAuth, OpenAI, URLs, port)

## Usage

Run the application:
```bash
python main.py
```

First run will open browser for OAuth authentication.

## Configuration

All settings live in `.env` (see `.env.example`). URLs and keys:

| Variable | Purpose |
|---|---|
| `GMAIL_CLIENT_ID` / `GMAIL_CLIENT_SECRET` | Google OAuth credentials |
| `OAUTH_REDIRECT_URI` | OAuth callback URL (must match the console) |
| `GMAIL_SCOPES` | Space-separated list of Gmail OAuth scopes |
| `OPENAI_API_KEY` / `OPENAI_ASSISTANT_ID` | AI classification |
| `GOOGLE_AUTH_URL` / `GOOGLE_TOKEN_URL` / `GOOGLE_USERINFO_URL` | Google OAuth endpoints |
| `GMAIL_API_BASE_URL` | Gmail API base endpoint |
| `PORT` | HTTP port (default `8082`) |

### Gmail Scopes
- `gmail.readonly`: Read emails
- `gmail.modify`: Modify labels

### Classification
- `ai`: OpenAI Assistant classifies email importance (requires `OPENAI_API_KEY` and `OPENAI_ASSISTANT_ID`)
- Keyword fallback: payment/invoice/overdue keywords mark an email as urgent when AI fails

### Priority Labels
- **URGENT**: `AI_URGENT` label
- **IMPORTANT**: `AI_IMPORTANT` label

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/rest/oauth2-credential/login` | Start Google OAuth flow |
| GET | `/rest/oauth2-credential/callback` | OAuth callback |
| GET | `/emails` | List emails (Bearer token) |
| POST | `/classify` | Classify an email (Bearer token) |
| GET | `/labels` | List Gmail labels (Bearer token) |
| POST | `/labels/create` | Create a label (Bearer token) |
| POST | `/emails/move` | Move email to a label (Bearer token) |

Interactive docs at `/docs`.

## Security

- Credentials are stored in `.env` (gitignored), never in code
- OAuth 2.0 flow ensures secure authentication
- No sensitive data logged

## License

MIT License
