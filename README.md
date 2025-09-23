# Youimah - Text-to-Video API

A FastAPI-based REST API service that generates videos from text prompts using Google's VEO3 model. This service provides an easy-to-use interface for creating high-quality videos from descriptive text.

## 🚀 Features

- **Text-to-Video Generation**: Convert text prompts into high-quality videos
- **Multiple Video Models**: Support for `veo3-fast` and `veo3-quality` models
- **Flexible Video Options**: 
  - Multiple aspect ratios: `1:1`, `16:9`, `9:16`, `3:1`, `1:3`
  - Various quality settings: `140`, `360`, `720`, `1080`, `2K`, `4K`
- **RESTful API**: Clean and intuitive REST endpoints
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Environment Configuration**: Secure API key management with environment variables

## 📋 Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- VEO3 Gen API Key
- Google VEO3 API Key

## 🛠️ Installation

### Option 1: Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/smtaidev/youimah_AI.git
   cd youimah_AI
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   VEO3_GEN_API_KEY=your_veo3_gen_api_key_here
   GOOGLE_VEO3_API_KEY=your_google_veo3_api_key_here
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8033
   ```

### Option 2: Docker Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/smtaidev/youimah_AI.git
   cd youimah_AI
   ```

2. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   VEO3_GEN_API_KEY=your_veo3_gen_api_key_here
   GOOGLE_VEO3_API_KEY=your_google_veo3_api_key_here
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

## 🔧 API Usage

### Base URL
```
http://localhost:8033
```

### Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "Text-to-Video API is running!"
}
```

### Generate Video
```http
POST /generate_video
```

**Request Body:**
```json
{
  "prompt": "A beautiful sunset over the ocean with waves gently crashing on the shore",
  "video_ratio": "16:9",
  "video_quality": "1080",
  "video_model": "veo3-quality"
}
```

**Parameters:**
- `prompt` (string, required): Text description for the video
- `video_ratio` (string, required): Aspect ratio - one of `1:1`, `16:9`, `9:16`, `3:1`, `1:3`
- `video_quality` (string, required): Quality setting - one of `140`, `360`, `720`, `1080`, `2K`, `4K`
- `video_model` (string, required): Model to use - `veo3-fast` or `veo3-quality`

**Success Response:**
```json
{
  "success": true,
  "video_url": "https://example.com/generated-video.mp4",
  "message": "Video generated successfully"
}
```

**Error Response:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

## 📝 Example Usage

### Using cURL
```bash
curl -X POST "http://localhost:8033/generate_video" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "A cat playing with a ball of yarn in a cozy living room",
       "video_ratio": "16:9",
       "video_quality": "720",
       "video_model": "veo3-fast"
     }'
```

### Using Python requests
```python
import requests

response = requests.post(
    "http://localhost:8033/generate_video",
    json={
        "prompt": "A serene forest with sunlight filtering through the trees",
        "video_ratio": "16:9",
        "video_quality": "1080",
        "video_model": "veo3-quality"
    }
)

if response.status_code == 200:
    result = response.json()
    print(f"Video URL: {result['video_url']}")
else:
    print(f"Error: {response.json()['detail']}")
```

## 🏗️ Project Structure

```
youimah_AI/
├── app/
│   └── services/
│       └── Text_Video/
│           ├── video.py          # Core video generation service
│           ├── video_route.py    # API route handlers
│           └── video_schema.py   # Pydantic models for request validation
├── videos/                       # Directory for generated videos
├── main.py                       # FastAPI application entry point
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
└── README.md                    # Project documentation
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VEO3_GEN_API_KEY` | API key for VEO3 Gen service | Yes |
| `GOOGLE_VEO3_API_KEY` | API key for Google VEO3 service | Yes |

### Model Selection Guide

- **veo3-fast**: Faster generation, suitable for lower quality requirements
- **veo3-quality**: Higher quality output, longer generation time

### Quality Settings

- **140, 360, 720**: Standard definition, faster processing
- **1080, 2K, 4K**: High definition, slower processing, better quality

## 🚀 Deployment

### Production Deployment

1. **Set up environment variables** in your production environment
2. **Use Docker for deployment**:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```
3. **Configure reverse proxy** (nginx, Apache) for production use
4. **Set up SSL/TLS** for secure connections

### Scaling

The application can be scaled horizontally by running multiple instances behind a load balancer. Each instance should have access to the same environment variables and API keys.

## 🔧 Development

### Running Tests
```bash
# Add your test commands here when tests are implemented
pytest
```

### Code Formatting
```bash
# Format code with black
black .

# Sort imports
isort .
```

## 📚 API Documentation

When the application is running, you can access:
- **Interactive API Documentation**: http://localhost:8033/docs
- **Alternative API Documentation**: http://localhost:8033/redoc

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your VEO3 API keys are correctly set in the `.env` file
2. **Port Conflicts**: If port 8033 is in use, change it in both `Dockerfile` and `docker-compose.yml`
3. **Video Generation Failures**: Check your API key validity and account limits

### Logs

To view application logs:
```bash
# Docker logs
docker-compose logs -f

# Local development logs
# Logs are output to console when running locally
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

## 🙏 Acknowledgments

- Google VEO3 for providing the video generation models
- FastAPI for the excellent web framework
- The open-source community for various tools and libraries used

---

**Made with ❤️ by [smtaidev](https://github.com/smtaidev)**
