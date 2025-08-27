# ShopTrack - Inventory Management System

A modern Flask-based inventory management system with authentication, stock tracking, and transaction history. Built using the Flask factory pattern for clean, modular architecture.

https://shop-track-one.vercel.app/

## 🚀 Features

- **User Authentication** - Secure token-based authentication
- **Product Management** - Create, read, update, and delete products
- **Stock Tracking** - Add and remove inventory with automatic history
- **Transaction History** - Complete audit trail of all stock operations
- **Input Validation** - Comprehensive data validation and error handling
- **RESTful API** - Clean, consistent API design
- **Database Security** - SQL injection protection and ownership validation

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd shoptrack-factory-v2
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install the project**
   ```bash
   pip install -e .
   ```

4. **Initialize the database**
   ```bash
   flask init-db
   ```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
# Set Flask environment
export FLASK_APP=shoptrack
export FLASK_ENV=development

# Run the application
flask run
```

The application will be available at `http://localhost:5000`

### Production Mode
```bash
# Set production environment
export FLASK_ENV=production

# Run with production server (e.g., gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 "shoptrack:create_app()"
```

## 📚 API Documentation

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "message": "User registered successfully."
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "username",
  "password": "password"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "token": "your-auth-token",
  "user": {
    "id": 1,
    "username": "username"
  }
}
```

#### Logout
```http
POST /auth/logout
Authorization: Bearer your-auth-token
```

### Product Management

#### Get All Products
```http
GET /stock/
Authorization: Bearer your-auth-token
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Product Name",
    "stock": 10,
    "price": 29.99,
    "description": "Product description",
    "owner_id": 1,
    "created": "2024-01-01T12:00:00"
  }
]
```

#### Get Single Product
```http
GET /stock/{id}
Authorization: Bearer your-auth-token
```

#### Create Product
```http
POST /stock/
Authorization: Bearer your-auth-token
Content-Type: application/json

{
  "name": "New Product",
  "stock": 5,
  "price": 19.99,
  "description": "Product description"
}
```

#### Update Product
```http
PUT /stock/{id}
Authorization: Bearer your-auth-token
Content-Type: application/json

{
  "name": "Updated Product",
  "stock": 15,
  "price": 24.99,
  "description": "Updated description"
}
```

#### Delete Product
```http
DELETE /stock/{id}
Authorization: Bearer your-auth-token
```

### Stock Operations

#### Add Stock
```http
POST /stock/{id}/stock
Authorization: Bearer your-auth-token
Content-Type: application/json

{
  "stock": 5
}
```

#### Remove Stock
```http
DELETE /stock/{id}/stock
Authorization: Bearer your-auth-token
Content-Type: application/json

{
  "stock": 3
}
```

### Transaction History

#### Get All History
```http
GET /stock/history
Authorization: Bearer your-auth-token
```

#### Get Product History
```http
GET /stock/{id}/history
Authorization: Bearer your-auth-token
```

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=shoptrack
```

### Test Structure
- `tests/test_auth.py` - Authentication tests
- `tests/test_stock.py` - Product and stock management tests
- `tests/conftest.py` - Test configuration and fixtures
- `tests/data.sql` - Test data setup

## 🏗️ Project Structure

```
shoptrack-factory-v2/
├── shoptrack/                 # Main application package
│   ├── __init__.py           # Flask factory pattern
│   ├── auth.py               # Authentication system
│   ├── db.py                 # Database utilities
│   ├── stock.py              # Stock management API
│   ├── validation.py         # Input validation
│   └── schema.sql            # Database schema
├── tests/                    # Test suite
│   ├── conftest.py           # Test configuration
│   ├── test_auth.py          # Authentication tests
│   ├── test_stock.py         # Stock management tests
│   └── data.sql              # Test data
├── instance/                 # Instance-specific files
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV` - Set to `development` or `production`
- `SECRET_KEY` - Flask secret key (auto-generated in development)
- `DATABASE` - Database file path (defaults to `instance/shoptrack.sqlite`)

### Database Schema
The application uses SQLite with the following tables:
- `user` - User accounts and authentication
- `product` - Product inventory
- `history` - Transaction history
- `sessions` - Authentication sessions

## 🛡️ Security Features

- **Token-based Authentication** - Secure JWT-like tokens
- **Input Validation** - Comprehensive data validation
- **SQL Injection Protection** - Parameterized queries
- **Ownership Validation** - Users can only access their own data
- **Password Hashing** - Secure password storage with Werkzeug

## 🚀 Development

### Adding New Features
1. Create new blueprint in `shoptrack/`
2. Register blueprint in `shoptrack/__init__.py`
3. Add validation functions in `shoptrack/validation.py`
4. Write tests in `tests/`
5. Update this README

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions
- Write comprehensive tests

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📞 Support

For questions or issues, please open an issue on the project repository.
