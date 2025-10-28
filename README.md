# Clinic AI Patient Management System

AI-powered hospital and clinic patient management system with multilingual support, automated scheduling, and intelligent communication.

## Features

### MVP Features (F01-F04)
- **F01: Multi-Channel AI Support** - AI chatbot on SMS, KakaoTalk, WeChat, and LINE
- **F02: Real-Time Two-Way Translation** - Seamless translation between Korean, English, Chinese, and Japanese
- **F03: AI Voice Agent** - Automated phone call handling with voice synthesis and recognition
- **F04: Automated Scheduling Engine** - Smart appointment matching and optimization

## Architecture

This project follows SOLID principles with composition over inheritance:
- **Single Responsibility**: Each module handles one concern
- **Open/Closed**: Modules extensible without modification
- **Liskov Substitution**: Interface implementations interchangeable
- **Interface Segregation**: Clients depend only on needed interfaces
- **Dependency Inversion**: High-level modules depend on abstractions

### Key Design Patterns Used
- **Strategy Pattern**: Pluggable AI services, translation backends
- **Composite Pattern**: Message processors combining multiple services
- **Template Method**: Scheduling workflows
- **Observer Pattern**: Event-driven notifications

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery
- **AI**: OpenAI GPT-4, Google Translate
- **Communication**: KakaoTalk, WeChat, LINE, Twilio
- **Testing**: pytest with factory-boy and faker

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/[username]/clinic-ai-patient-management.git
cd clinic-ai-patient-management
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start development server:
```bash
python manage.py runserver
```

## Project Structure

```
clinic_ai/
├── core/              # Core models and interfaces
│   ├── models.py
│   ├── interfaces.py
│   └── config.py
├── messaging/         # Multi-channel message handling
│   ├── ai_service.py
│   ├── translation.py
│   └── handlers.py
├── voice/             # Voice call processing
├── scheduling/        # Appointment management
├── web/               # Django views and templates
└── api/               # REST API endpoints
```

## API Keys Required

- OpenAI API Key
- Google Translate API Key
- KakaoTalk Business API Token
- WeChat App Credentials
- LINE Channel Access Token
- Twilio Account SID and Token

## Testing

Run the full test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=clinic_ai --cov-report=html
```

## Deployment

The system is designed for cloud deployment with Docker and Kubernetes support (coming in future versions).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following SOLID principles
4. Add comprehensive tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## DHH Philosophy

This project follows David Heinemeier Hansson's principles:
- Focus on what works, not what's perfect
- Remove complexity, embrace simplicity
- Build software for people who use it
- Ship early, iterate often
- Question every feature's necessity