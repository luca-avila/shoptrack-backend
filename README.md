# ShopTrack - Inventory Management System

A modern Flask-based inventory management system with authentication, stock tracking, and transaction history. Built using the Flask factory pattern for clean, modular architecture.

## 🚀 Live Demo

**Try ShopTrack right now!** Visit my live demo at: **[https://shop-track-one.vercel.app/](https://shop-track-one.vercel.app/)**

The demo includes all features:
- User registration and authentication
- Product management (create, read, update, delete)
- Real-time stock tracking
- Complete transaction history
- RESTful API endpoints

## ✨ Features

- **🔐 User Authentication** - Secure token-based authentication with session management
- **📦 Product Management** - Create, read, update, and delete products with full CRUD operations
- **📊 Stock Tracking** - Add and remove inventory with automatic history tracking
- **📈 Transaction History** - Complete audit trail of all stock operations with timestamps
- **✅ Input Validation** - Comprehensive data validation and error handling
- **🌐 RESTful API** - Clean, consistent API design following REST principles
- **🛡️ Database Security** - SQL injection protection and ownership validation
- **🔒 Multi-User Support** - Each user can only access their own data
- **📱 CORS Enabled** - Ready for frontend integration

## 🛠️ Technology Stack

- **Backend**: Flask 3.1.1 with Factory Pattern
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Custom token-based system with Werkzeug password hashing
- **Deployment**: Vercel with Gunicorn
- **Testing**: pytest with comprehensive test coverage
- **CORS**: flask-cors for cross-origin requests

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepassword"
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
PATCH /stock/{id}/stock/add
Authorization: Bearer your-auth-token
Content-Type: application/json

{
  "stock": 5
}
```

#### Remove Stock
```http
PATCH /stock/{id}/stock/remove
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
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku/Vercel deployment
├── runtime.txt               # Python runtime version
└── README.md                # This file
```

## 🧪 Testing

The project includes comprehensive tests covering all functionality:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=shoptrack
```

### Test Coverage
- **Authentication Tests** (`test_auth.py`) - User registration, login, logout
- **Stock Management Tests** (`test_stock.py`) - Product CRUD operations
- **Database Tests** (`test_db.py`) - Database connection and utilities
- **Factory Tests** (`test_factory.py`) - Application factory pattern

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV` - Set to `development` or `production`
- `SECRET_KEY` - Flask secret key for session security
- `DATABASE_URL` - PostgreSQL connection string (production)
- `DATABASE` - SQLite database file path (development)

### Database Schema
The application uses a relational database with the following tables:
- `user` - User accounts and authentication
- `product` - Product inventory with ownership
- `history` - Transaction history with timestamps
- `sessions` - Authentication sessions with expiration

## 🛡️ Security Features

- **🔐 Token-based Authentication** - Secure session management with expiration
- **🔒 Password Hashing** - Secure password storage using Werkzeug
- **🛡️ Input Validation** - Comprehensive data validation and sanitization
- **💉 SQL Injection Protection** - Parameterized queries throughout
- **👤 Ownership Validation** - Users can only access their own data
- **🔑 CORS Configuration** - Secure cross-origin request handling

## 🚀 Development Setup

For developers who want to run the project locally:

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd shoptrack-factory-v2

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment
export FLASK_APP=shoptrack
export FLASK_ENV=development

# Initialize database
flask init-db

# Run the application
flask run
```

The application will be available at `http://localhost:5000`

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For questions, issues, or feature requests, please open an issue on the project repository.

---

**Ready to try ShopTrack?** Visit **[https://shop-track-one.vercel.app/](https://shop-track-one.vercel.app/)** to start managing your inventory today!
