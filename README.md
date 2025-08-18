# Text-to-Video Generation API

A powerful FastAPI-based service that generates videos from text prompts using multiple AI video generation providers including VEO3 Gen and Google Veo3. This service provides a unified interface for text-to-video generation with fallback mechanisms and detailed response handling.

## 🚀 Features

- **Multiple Video Generation Providers**: VEO3 Gen and Google Veo3 support
- **Asynchronous Processing**: Handles long-running video generation tasks
- **Smart Fallback System**: Automatically tries alternative providers if one fails
- **Flexible Quality Options**: Support for different resolutions and aspect ratios
- **Comprehensive Logging**: Detailed status tracking and error handling
- **RESTful API**: Clean, documented API endpoints
- **Local Video Storage**: Generated videos saved locally with unique filenames
- **Containerized Deployment**: Docker support for easy deployment

## 📋 Requirements

- Python 3.11+
- FastAPI
- Uvicorn
- Valid API keys for video generation services

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Youimah1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # Veo3 Gen API (third-party video generation service)
   VEO3_GEN_API_KEY=your_veo3_gen_api_key_here
   
   # Google Veo3 via Gemini API
   GOOGLE_VEO3_API_KEY=your_google_api_key_here
   ```

4. **Alternative: Docker Installation**
   ```bash
   docker-compose up --build
   ```
   This will build and run the application in a Docker container, exposing it on port 8033.

## 🔑 API Keys Setup

### VEO3 Gen API Key
1. Visit [VEO3 Gen website](https://veo3gen.app)
2. Create an account and get your API key
3. Add credits to your account for video generation
4. Add the key to your `.env` file

### Google Veo3 API Key (Gemini API)
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a project and get your API key
3. Add the key to your `.env` file
4. Note: The Google Veo3 service uses Gemini-1.5-pro model to explain that direct video generation is not available through the API

## 🚀 Usage

### Starting the Server

#### Main API Server
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8033
```

The API will be available at:
- **Base URL**: `http://127.0.0.1:8033`
- **Interactive Docs**: `http://127.0.0.1:8033/docs`
- **OpenAPI Schema**: `http://127.0.0.1:8033/openapi.json`

#### Google Veo3 API Server (Optional Standalone Mode)
```bash
python run_google_veo3_api.py
```

The Google Veo3 API server will run on:
- **Base URL**: `http://127.0.0.1:8044`

### API Endpoints

#### Generate Video
**POST** `/generate_video`

Generate a video from a text prompt.

**Request Body:**
```json
{
  "prompt": "A beautiful sunset over a mountain landscape with birds flying",
  "video_ratio": "16:9",
  "video_quality": "720"
},
{
  "prompt": "Cinematic wide shot of a powerful superhero standing on top of a tall building at dusk. The superhero wears a sleek red and gold armored suit with a glowing chest emblem. A gentle breeze moves the cape as the camera slowly pans around the rooftop, revealing a sprawling futuristic city below. Soft orange and purple hues from the sunset light reflect off the skyscrapers. The superhero raises one arm and lightning energy begins to spark around their hand, illuminating the scene. Birds briefly fly across the sky while the camera zooms in for a dramatic close-up of the superhero’s determined face.",
  "video_ratio": "16:9",
  "video_quality": "720"
}

```

**Parameters:**
- `prompt` (string, required): Text description of the video to generate
- `video_ratio` (string, required): Aspect ratio (1:1, 16:9, 9:16, 3:1, 1:3)
- `video_quality` (string, required): Video quality (140, 360, 720, 1080, 2K, 4K)

**Response:**
```json
{
  "success": true,
  "video_url": "/videos/veo3_video_abc12345.mp4",
  "message": "Video generated successfully"
}
```

#### Health Check
**GET** `/`

Returns API status and basic information.

**Response:**
```json
{
  "message": "Text-to-Video API is running!"
}
```

## 🧪 Testing

### Test API Keys
```bash
python test_api_keys.py
```

### Test Complete API Suite
```bash
python test_complete_api.py
```

### Manual API Testing
```bash
python test_video_api.py
```

### Using cURL
```bash
curl -X POST "http://127.0.0.1:8033/generate_video" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "A serene lake with mountains in the background",
       "video_ratio": "16:9",
       "video_quality": "720"
     }'
```

For the standalone Google Veo3 API:
```bash
curl -X POST "http://127.0.0.1:8044/generate_video" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "A serene lake with mountains in the background",
       "video_ratio": "16:9",
       "video_quality": "720"
     }'
```

## 📁 Project Structure

```
Youimah1/
├── app/
│   └── services/
│       └── Text_Video/
│           ├── video.py           # Main video service logic
│           ├── video_route.py     # API routes
│           └── video_schema.py    # Pydantic models
├── videos/                        # Generated videos storage
├── main.py                        # FastAPI application entry point
├── google_veo3_api.py             # Google Veo3 API implementation
├── run_google_veo3_api.py         # Standalone Google Veo3 API server launcher
├── docker-compose.yml             # Docker Compose configuration
├── Dockerfile                     # Docker container definition
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables
├── test.py                        # Basic testing functionality
└── README.md                      # This file
```

## 🔧 Configuration

### Video Quality Mapping
- **Fast Generation** (`veo3-fast`): 140p, 360p, 720p
- **High Quality** (`veo3-quality`): 1080p, 2K, 4K

### Supported Aspect Ratios
- `1:1` - Square format
- `16:9` - Widescreen (default)
- `9:16` - Vertical/Mobile
- `3:1` - Ultra-wide
- `1:3` - Ultra-tall

### Timeout Settings
- **Generation Request**: 30 seconds
- **VEO3 Polling**: 5 minutes (300 seconds)
- **Google Veo3 Polling**: 10 minutes (600 seconds)

## 🚨 Error Handling

The API includes comprehensive error handling for:

- **Invalid API Keys**: Returns proper HTTP 401/403 errors
- **Insufficient Credits**: Detailed credit information in logs
- **Network Issues**: Connection timeout and retry logic
- **Service Unavailability**: Automatic fallback between providers
- **Invalid Parameters**: Validation errors with clear messages

## 🔍 Monitoring and Logging

The application provides detailed logging for:
- API request/response cycles
- Video generation progress
- Error conditions and debugging
- Performance metrics

Logs include:
- Timestamp and log level
- Service provider (VEO3 Gen / Google Veo3)
- Request details and status
- Error messages and stack traces

## 📈 Performance

### Expected Generation Times
- **VEO3 Fast**: 30-60 seconds
- **VEO3 Quality**: 2-5 minutes
- **Google Veo3**: Note that Google's Gemini API does not currently support direct video generation. The API will return an explanation about Gemini's capabilities instead.

### Scaling Considerations
- Use background task queues for production (Celery, RQ)
- Implement caching for repeated requests
- Consider cloud storage for video files
- Monitor API rate limits

## 🛡️ Security

- API keys stored in environment variables
- No sensitive data in source code
- Input validation on all endpoints
- Error messages don't expose internal details

## 🚀 Deployment

### Local Development
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8033
```

### Production
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8033 --workers 4
```

### Docker
The project includes ready-to-use Docker configuration:

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8033
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8033"]
```

**Docker Compose:**
```yaml
version: '3'

services:
  api:
    build: .
    ports:
      - "8033:8033"
    volumes:
      - ./videos:/app/videos
    environment:
      - VEO3_GEN_API_KEY=${VEO3_GEN_API_KEY}
      - GOOGLE_VEO3_API_KEY=${GOOGLE_VEO3_API_KEY}
    restart: unless-stopped
```

To run with Docker Compose:
```bash
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Important Notes

- **Credits Required**: VEO3 Gen requires credits for video generation
- **API Limits**: Both services have rate limits and usage restrictions
- **Storage**: Generated videos are stored locally; consider cloud storage for production
- **Costs**: Video generation may incur charges based on usage
- **Google Veo3 Limitations**: The Google Veo3 component uses Gemini API which doesn't currently support direct video generation. It provides information about capabilities instead.
- **Port Configuration**: The main API runs on port 8033, and the standalone Google Veo3 service runs on port 8044

## 🆘 Troubleshooting

### Common Issues

1. **"Insufficient Credits" Error**
   - Add credits to your VEO3 Gen account
   - Check your account balance

2. **"Connection Failed" Error**
   - Check your internet connection
   - Verify API endpoints are accessible

3. **"Invalid API Key" Error**
   - Verify API keys in `.env` file
   - Check if keys have proper permissions

4. **"Import Error" for Google GenAI**
   - Install missing dependency: `pip install google-generativeai`
   - Make sure you're using Python 3.11+ as specified in requirements

5. **Video Generation Timeout**
   - Complex prompts may take longer
   - Check service status pages
   
6. **Port Already in Use**
   - Change the port in Dockerfile, docker-compose.yml, or when running directly with uvicorn
   - Check for other services using the configured ports (8033, 8044)

### Getting Help

- Check the logs for detailed error information
- Run the test scripts to validate your setup
- Ensure all dependencies are installed
- Verify API keys have sufficient permissions and credits

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Run diagnostic tests
3. Review the API documentation
4. Check service provider status pages

---

**Made with ❤️ using FastAPI and cutting-edge AI video generation technology**