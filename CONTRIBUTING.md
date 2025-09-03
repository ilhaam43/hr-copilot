# Contributing to HR Chatbot System

Terima kasih atas minat Anda untuk berkontribusi pada HR Chatbot System! Panduan ini akan membantu Anda memahami cara berkontribusi secara efektif.

## Daftar Isi
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Contributing Guidelines](#contributing-guidelines)
5. [Pull Request Process](#pull-request-process)
6. [Coding Standards](#coding-standards)
7. [Testing Guidelines](#testing-guidelines)
8. [Documentation](#documentation)
9. [Issue Reporting](#issue-reporting)
10. [Community](#community)

---

## Code of Conduct

Proyek ini mengikuti [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Dengan berpartisipasi, Anda diharapkan untuk menjunjung tinggi kode etik ini.

### Our Pledge
- Menciptakan lingkungan yang ramah dan inklusif
- Menghormati sudut pandang dan pengalaman yang berbeda
- Menerima kritik konstruktif dengan baik
- Fokus pada apa yang terbaik untuk komunitas

---

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- PostgreSQL atau MySQL
- Ollama (untuk AI features)
- Node.js (untuk frontend assets)

### Quick Start
1. Fork repository ini
2. Clone fork Anda:
   ```bash
   git clone https://github.com/your-username/hrcopilot.git
   cd hrcopilot
   ```
3. Setup development environment (lihat [Development Setup](#development-setup))
4. Buat branch untuk fitur Anda:
   ```bash
   git checkout -b feature/amazing-feature
   ```
5. Mulai coding!

---

## Development Setup

### 1. Environment Setup
```bash
# Create virtual environment
python3 -m venv ai/.venv
source ai/.venv/bin/activate  # Linux/Mac
# atau
ai\.venv\Scripts\activate  # Windows

# Install dependencies
cd horilla
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### 2. Database Setup
```bash
# PostgreSQL
createdb hrbot_dev

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 3. Ollama Setup
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# Start Ollama service
ollama serve
```

### 4. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

### 5. Run Development Server
```bash
# Start Django development server
python manage.py runserver

# In another terminal, start frontend development (if applicable)
npm run dev
```

### 6. Verify Setup
```bash
# Run tests
python manage.py test

# Test Ollama integration
python test_ollama_integration.py

# Test chatbot functionality
python nlp_engine/demo_chatbot_examples.py
```

---

## Contributing Guidelines

### Types of Contributions

#### 🐛 Bug Fixes
- Fix existing functionality yang tidak bekerja dengan benar
- Improve error handling
- Performance improvements

#### ✨ New Features
- Add new chatbot intents
- Implement new AI capabilities
- Create new API endpoints
- Add new integrations

#### 📚 Documentation
- Improve existing documentation
- Add new guides atau tutorials
- Fix typos atau unclear explanations
- Translate documentation

#### 🧪 Testing
- Add unit tests
- Improve test coverage
- Add integration tests
- Performance testing

#### 🎨 UI/UX Improvements
- Improve user interface
- Enhance user experience
- Add accessibility features
- Mobile responsiveness

### Contribution Workflow

1. **Check existing issues**: Lihat apakah ada issue yang relevan
2. **Create issue**: Jika belum ada, buat issue baru untuk diskusi
3. **Get assignment**: Tunggu assignment atau minta untuk di-assign
4. **Fork & branch**: Fork repo dan buat feature branch
5. **Develop**: Implement changes dengan mengikuti coding standards
6. **Test**: Pastikan semua tests pass
7. **Document**: Update documentation jika diperlukan
8. **Submit PR**: Create pull request dengan deskripsi yang jelas
9. **Review**: Respond to feedback dan make necessary changes
10. **Merge**: Setelah approved, changes akan di-merge

---

## Pull Request Process

### Before Submitting
- [ ] Code follows project coding standards
- [ ] All tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with main branch

### PR Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### Review Process
1. **Automated checks**: CI/CD pipeline akan run automated tests
2. **Code review**: Maintainers akan review code changes
3. **Feedback**: Reviewer akan provide feedback atau request changes
4. **Iteration**: Make requested changes dan push updates
5. **Approval**: Setelah approved, PR akan di-merge

---

## Coding Standards

### Python Code Style

#### PEP 8 Compliance
```python
# Good
def process_user_message(message: str, user_id: str) -> dict:
    """Process user message and return chatbot response.
    
    Args:
        message: User input message
        user_id: Unique user identifier
        
    Returns:
        Dictionary containing response data
    """
    if not message.strip():
        return {"error": "Empty message"}
    
    # Process message logic here
    return {"response": "Processed message"}

# Bad
def processUserMessage(message,user_id):
    if not message.strip():return {"error":"Empty message"}
    return {"response":"Processed message"}
```

#### Type Hints
```python
# Always use type hints
from typing import List, Dict, Optional, Union

def get_employee_info(employee_id: str) -> Optional[Dict[str, Union[str, int]]]:
    """Get employee information by ID."""
    pass

def process_intents(messages: List[str]) -> List[Dict[str, float]]:
    """Process multiple messages for intent detection."""
    pass
```

#### Docstrings
```python
def detect_intent(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Detect intent from user message.
    
    This method analyzes the user's message to determine their intent
    using both rule-based matching and AI-powered classification.
    
    Args:
        message: The user's input message to analyze
        context: Optional context information including user preferences,
                session data, and conversation history
                
    Returns:
        Dictionary containing:
            - intent: Detected intent name (str)
            - confidence: Confidence score (float, 0-1)
            - entities: Extracted entities (List[Dict])
            - suggestions: Suggested follow-up actions (List[str])
            
    Raises:
        ValueError: If message is empty or invalid
        OllamaServiceError: If AI service is unavailable
        
    Example:
        >>> chatbot = HRChatbot()
        >>> result = chatbot.detect_intent("What's my leave balance?")
        >>> print(result['intent'])  # 'leave_balance'
        >>> print(result['confidence'])  # 0.95
    """
    pass
```

### JavaScript Code Style

#### ES6+ Features
```javascript
// Use modern JavaScript features
const sendMessage = async (message, sessionId) => {
    try {
        const response = await fetch('/api/v1/chat/message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({ message, session_id: sessionId })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
};
```

### Database Models

#### Model Design
```python
from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    """Represents a chat session between user and chatbot."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'chat_sessions'
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['is_active', 'updated_at']),
        ]
        
    def __str__(self):
        return f"Chat Session {self.id} - {self.user.username}"
```

---

## Testing Guidelines

### Test Structure
```
tests/
├── unit/
│   ├── test_chatbot.py
│   ├── test_ollama_service.py
│   └── test_intent_detection.py
├── integration/
│   ├── test_api_endpoints.py
│   └── test_ollama_integration.py
├── e2e/
│   └── test_chatbot_flow.py
└── fixtures/
    └── test_data.json
```

### Unit Tests
```python
import unittest
from unittest.mock import Mock, patch
from nlp_engine.chatbot import HRChatbot

class TestHRChatbot(unittest.TestCase):
    """Test cases for HR Chatbot functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.chatbot = HRChatbot()
        self.sample_message = "What's my leave balance?"
        
    def test_detect_intent_leave_balance(self):
        """Test intent detection for leave balance queries."""
        result = self.chatbot.detect_intent(self.sample_message)
        
        self.assertEqual(result['intent'], 'leave_balance')
        self.assertGreater(result['confidence'], 0.8)
        self.assertIn('entities', result)
        
    @patch('nlp_engine.ollama_service.OllamaService.generate_text')
    def test_generate_response_with_mock(self, mock_generate):
        """Test response generation with mocked Ollama service."""
        mock_generate.return_value = "Your leave balance is 15 days."
        
        response = self.chatbot.generate_response(
            intent='leave_balance',
            message=self.sample_message,
            context={'user_id': 'test_user'}
        )
        
        self.assertIn('response', response)
        self.assertTrue(response['success'])
        mock_generate.assert_called_once()
        
    def test_empty_message_handling(self):
        """Test handling of empty or invalid messages."""
        with self.assertRaises(ValueError):
            self.chatbot.detect_intent("")
            
        with self.assertRaises(ValueError):
            self.chatbot.detect_intent(None)
```

### Integration Tests
```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class ChatAPIIntegrationTest(TestCase):
    """Integration tests for Chat API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        
    def test_send_message_api(self):
        """Test sending message through API."""
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token.key}'}
        
        response = self.client.post(
            '/api/v1/chat/message/',
            {
                'message': 'Hello, I need help with my leave balance',
                'user_id': str(self.user.id),
                'session_id': 'test_session_123'
            },
            content_type='application/json',
            **headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('response', data['data'])
        self.assertIn('intent', data['data'])
```

### Test Coverage
```bash
# Install coverage tool
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test

# Generate coverage report
coverage report
coverage html  # Generate HTML report

# Target coverage: 80%+ for new code
```

---

## Documentation

### Documentation Standards

#### Code Comments
```python
# Good: Explain WHY, not WHAT
def calculate_leave_balance(employee, leave_type):
    # Use fiscal year calculation to match company policy
    fiscal_year_start = get_fiscal_year_start()
    
    # Include carried over days from previous year (max 5 days)
    carried_over = min(employee.previous_year_balance, 5)
    
    return base_allocation + carried_over - used_days

# Bad: Explain obvious things
def calculate_leave_balance(employee, leave_type):
    # Get fiscal year start
    fiscal_year_start = get_fiscal_year_start()
    
    # Add carried over days
    carried_over = min(employee.previous_year_balance, 5)
    
    # Return calculation
    return base_allocation + carried_over - used_days
```

#### API Documentation
```python
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    operation_description="Send message to HR chatbot",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['message'],
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='User message'),
            'session_id': openapi.Schema(type=openapi.TYPE_STRING, description='Chat session ID'),
            'context': openapi.Schema(type=openapi.TYPE_OBJECT, description='Additional context')
        }
    ),
    responses={
        200: openapi.Response(
            description="Successful response",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'data': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'response': openapi.Schema(type=openapi.TYPE_STRING),
                            'intent': openapi.Schema(type=openapi.TYPE_STRING),
                            'confidence': openapi.Schema(type=openapi.TYPE_NUMBER)
                        }
                    )
                }
            )
        )
    }
)
@api_view(['POST'])
def send_message(request):
    """Send message to HR chatbot and get response."""
    pass
```

---

## Issue Reporting

### Bug Reports
Gunakan template berikut untuk melaporkan bug:

```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Ubuntu 20.04]
 - Python Version: [e.g. 3.9.7]
 - Django Version: [e.g. 4.2.7]
 - Browser: [e.g. Chrome 91.0]

**Additional Context**
Add any other context about the problem here.

**Logs**
Include relevant log output if available.
```

### Feature Requests
```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.

**Implementation Ideas**
If you have ideas about how this could be implemented, please share them.
```

---

## Community

### Communication Channels
- **GitHub Issues**: Bug reports dan feature requests
- **GitHub Discussions**: General discussions dan Q&A
- **Email**: development@your-domain.com untuk private inquiries

### Getting Help
1. **Check Documentation**: Lihat dokumentasi lengkap di `DOCUMENTATION.md`
2. **Search Issues**: Cari existing issues untuk masalah serupa
3. **Ask Questions**: Buat discussion atau issue baru
4. **Join Community**: Bergabung dengan developer community

### Recognition
Kontributor akan diakui dalam:
- `CONTRIBUTORS.md` file
- Release notes
- Project documentation
- Annual contributor highlights

---

## Development Tools

### Recommended IDE Setup
- **VS Code** dengan extensions:
  - Python
  - Django
  - GitLens
  - Prettier
  - ESLint

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Code Quality Tools
```bash
# Linting
flake8 .
black --check .
isort --check-only .

# Type checking
mypy nlp_engine/

# Security scanning
bandit -r .
safety check
```

---

## Release Process

### Version Numbering
Menggunakan [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] Security review completed
- [ ] Performance testing done
- [ ] Migration scripts tested

---

Terima kasih telah berkontribusi pada HR Chatbot System! Kontribusi Anda membantu membuat sistem ini lebih baik untuk semua pengguna.

**Questions?** Jangan ragu untuk bertanya melalui GitHub Issues atau email kami di development@your-domain.com.

---

**Contributing Guide Version**: 1.0  
**Last Updated**: January 20, 2025  
**Maintained by**: HR Chatbot Development Team