# Todo API Lambda Function

A production-ready serverless Todo API built with AWS Lambda, DynamoDB, and Python 3.13.

## Features

- **RESTful API** - Complete CRUD operations for todos
- **DynamoDB Integration** - Persistent storage with point-in-time recovery
- **Input Validation** - Title length limits and field validation
- **CORS Support** - Cross-origin requests with preflight handling
- **Security Headers** - Production-ready security configurations
- **Comprehensive Logging** - Structured logging with error tracking
- **Unit Tests** - 17 passing tests with mock services
- **Python 3.13** - Runs on the AWS Lambda python3.13 runtime; uses modern Python features (walrus operator, positional-only params)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos` | Get all todos (optional `?completed=true/false` filter) |
| GET | `/todos/{id}` | Get specific todo by ID |
| POST | `/todos` | Create new todo |
| PUT | `/todos/{id}` | Update existing todo |
| DELETE | `/todos/{id}` | Delete todo |
| OPTIONS | `/todos` | CORS preflight |

## Request/Response Examples

### Create Todo
```bash
POST /todos
{
  "title": "Learn AWS Lambda"
}
```

### Update Todo
```bash
PUT /todos/{id}
{
  "title": "Learn AWS Lambda and DynamoDB",
  "completed": true
}
```

### Response Format
```json
{
  "id": "uuid-string",
  "title": "Learn AWS Lambda",
  "completed": false,
  "created_at": "2025-11-15T17:30:00.000Z",
  "updated_at": "2025-11-15T17:30:00.000Z"
}
```

## Prerequisites

- AWS CLI configured
- SAM CLI installed
- Python 3.13+
- pytest (for testing)

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/venuvasu/todoapilambda.git
cd todoapilambda
```

### 2. Build Application
```bash
sam build
```

### 3. Run Tests
```bash
python -m pytest test/ -v
```

### 4. Deploy to AWS
```bash
sam deploy --guided
```

## Project Structure

```
├── src/
│   ├── lambda_function.py      # Main Lambda handler
│   ├── todo_service.py         # DynamoDB service layer
│   ├── mock_todo_service.py    # Mock service for testing
│   ├── models.py               # Todo data model
│   └── requirements.txt        # Python dependencies
├── test/
│   ├── test_lambda_function.py # Lambda handler tests
│   ├── test_todo_service.py    # Service layer tests
│   └── test_models.py          # Model tests
├── template.yaml               # SAM template
└── pytest.ini                 # Test configuration
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DYNAMODB_TABLE` | `todos` | DynamoDB table name |
| `MAX_TITLE_LENGTH` | `200` | Maximum todo title length |

## Testing

Run all tests:
```bash
python -m pytest test/ -v
```

Run specific test file:
```bash
python -m pytest test/test_lambda_function.py -v
```

## Local Development

### Start Local API
```bash
sam local start-api
```

### Invoke Function Locally
```bash
sam local invoke TodoApiFunction -e events/event.json
```

## Deployment

### First Time Deployment
```bash
sam deploy --guided
```

### Subsequent Deployments
```bash
sam deploy
```

### Deploy to Specific Environment
```bash
sam deploy --parameter-overrides Environment=prod
```

## Infrastructure

The SAM template creates:
- **Lambda Function** - Python 3.13 runtime with 30s timeout
- **DynamoDB Table** - Pay-per-request billing with point-in-time recovery
- **API Gateway** - RESTful endpoints with CORS
- **IAM Roles** - Least privilege permissions

## Security Features

- Input validation and sanitization
- CORS headers with proper configuration
- Error messages without sensitive information
- Structured logging for monitoring
- IAM permissions following least privilege

## Monitoring

The function includes:
- CloudWatch Logs integration
- Structured logging with request tracking
- Error logging with stack traces
- Timestamp tracking for all operations

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing issues for solutions
- Review the test files for usage examples
