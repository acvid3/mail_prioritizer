# Mail Prioritizer

AI-powered email sorting system that automatically prioritizes Gmail messages by importance.

## Features

- **OAuth 2.0 Authentication**: Secure Gmail API integration
- **AI Classification**: Rule-based and AI-powered email priority detection
- **Automatic Labeling**: Applies priority labels (IMPORTANT, NORMAL, LOW_PRIORITY)
- **Batch Processing**: Efficiently processes multiple emails
- **Configurable Settings**: Customizable classification and processing options

## Project Structure

```
mail_prioritizer/
├── src/
│   ├── auth/           # OAuth 2.0 authentication
│   ├── gmail/          # Gmail API client
│   ├── ai/             # Email classification
│   ├── core/           # Email processing engine
│   └── utils/          # Configuration and logging
├── config/             # Settings and credentials
├── tests/              # Unit tests
├── docs/               # Documentation
├── main.py             # Application entry point
└── requirements.txt    # Python dependencies
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create new project
   - Enable Gmail API

2. **Create OAuth 2.0 Credentials**:
   - Go to Credentials → Create Credentials → OAuth 2.0 Client ID
   - Select "Desktop application"
   - Download JSON credentials file
   - Save as `config/credentials.json`

3. **Configure Settings**:
   - Edit `config/settings.json` as needed
   - Default settings work out-of-the-box

## Usage

Run the application:
```bash
python main.py
```

First run will open browser for OAuth authentication.

## Configuration

### Gmail Scopes
- `gmail.readonly`: Read emails
- `gmail.modify`: Modify labels

### Classification Types
- `rule_based`: Keyword-based classification
- `ai`: AI-powered classification (requires API key)

### Priority Labels
- **HIGH**: IMPORTANT label
- **MEDIUM**: NORMAL label  
- **LOW**: LOW_PRIORITY label

## Development

### Adding New Classifiers
```python
from src.ai.classifier import EmailClassifier

class CustomClassifier(EmailClassifier):
    def classify_priority(self, email_data):
        # Custom logic here
        return 'high'
```

### Testing
```bash
python -m pytest tests/
```

## Security

- Credentials stored locally in `config/token.json`
- OAuth 2.0 flow ensures secure authentication
- No sensitive data logged

## License

MIT License
