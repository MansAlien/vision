# Django Vision 🚀

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-latest-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-latest-red.svg)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/Docker-enabled-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A powerful Django REST Framework starter project with modern features and best practices. 🌟

## ✨ Features

### Backend 🔧
- **🔐 JWT Authentication**: Secure user authentication with JSON Web Tokens
- **📊 Silk Profiling**: Performance monitoring and request profiling
- **🔍 Advanced Filtering**: Powerful API endpoint filtering with django-filter
- **🎯 REST API**: Fully featured REST API using Django REST Framework

### DevOps 🛠
- **🐳 Docker Support**: Containerized development and deployment
- **🔄 CI/CD Ready**: Prepared for continuous integration/deployment
- **📝 Code Quality**: Integrated with Ruff for code linting

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Docker (optional)
- Virtual Environment (recommended)

### Installation 📥

1. **Clone the repository**
   ```bash
   git clone https://github.com/MansAlien/drf_setup.git
   cd drf_setup
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

### Docker Setup 🐳

1. **Build and run with Docker**
   ```bash
   docker-compose up --build
   ```

## 📚 API Documentation

- API documentation is available at `/api/docs/`
- Swagger UI is available at `/api/swagger/`

## 🔍 Development Tools

- **Silk Profiler**: Access at `/silk/` when DEBUG=True
- **Admin Interface**: Access at `/admin/`

## 🧪 Testing

```bash
python manage.py test
```

## 📈 Performance Monitoring

- Access Silk dashboard at `/silk/` for:
  - Request profiling
  - Database query analysis
  - Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- GitHub: [@MansAlien](https://github.com/MansAlien)

---

⭐️ Star this repository if you find it helpful!
