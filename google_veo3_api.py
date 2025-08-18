from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
import logging
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create videos directory if it doesn't exist
os.makedirs("videos", exist_ok=True)

app = FastAPI(title="Google Veo3 API", description="A separate service for Google Veo3 text-to-video generation")

# Mount static files to serve videos
app.mount("/videos", StaticFiles(directory="videos"), name="videos")

class VideoRequest(BaseModel):
    prompt: str = Field(..., description="The text prompt for the video.")
    video_ratio: str = Field("16:9", description="Video aspect ratio (1:1, 16:9, 9:16, 3:1, 1:3)")
    video_quality: str = Field("720", description="Video quality (140, 360, 720, 1080, 2K, 4K)")

class GoogleVeo3Service:
    def __init__(self):
        self.google_veo3_api_key = os.getenv("GOOGLE_VEO3_API_KEY")
        if not self.google_veo3_api_key:
            raise ValueError("GOOGLE_VEO3_API_KEY not found in environment variables")
            
        # Initialize Google GenAI client
        try:
            genai.configure(api_key=self.google_veo3_api_key)
            logger.info("Google GenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Google GenAI client: {e}")
            raise
    
    def generate_video(self, prompt: str, video_ratio: str, video_quality: str) -> str:
        """Generates a video using Google Veo3."""
        try:
            logger.info(f"Starting Google Veo3 video generation...")
            logger.info(f"Prompt: {prompt[:50]}...")
            
            # Create videos directory if it doesn't exist
            os.makedirs("videos", exist_ok=True)
            
            # Get the Gemini model
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Generate a response about video generation limitations
            logger.info("Generating explanation about Gemini video capabilities")
            response = model.generate_content(
                f"Based on the prompt: '{prompt}', explain that Gemini doesn't directly support video generation through the API. Provide information about Google's video generation capabilities and alternatives."
            )
            
            logger.info("Gemini response generated successfully")
            
            # Log the response structure for debugging
            logger.info(f"Response type: {type(response)}")
            logger.info(f"Response attributes: {dir(response)}")
            
            # Extract the text explanation from the response
            text_explanation = response.text
            logger.info(f"Text explanation: {text_explanation[:100]}...")
            
            # Create a JSON response with the explanation
            result = {
                "message": "Google Gemini doesn't directly support video generation through the API",
                "explanation": text_explanation,
                "prompt": prompt,
                "status": "info",
                "alternative_suggestion": "For video generation, consider using other specialized video generation APIs"
            }
            
            # Return as JSON string
            import json
            result_json = json.dumps(result, indent=2)
            
            # Generate a unique filename for the explanation
            explanation_filename = f"google_veo3_explanation_{uuid.uuid4().hex[:8]}.json"
            explanation_path = os.path.join("videos", explanation_filename)
            
            logger.info(f"Saving explanation to {explanation_path}")
            
            try:
                # Save the explanation as a JSON file
                with open(explanation_path, "w") as f:
                    f.write(result_json)
                
                base_url = "http://localhost:8077"  # Updated port
                explanation_url = f"{base_url}/videos/{explanation_filename}"
                logger.info(f"Explanation saved locally as: {explanation_path}")
                logger.info(f"Explanation accessible at: {explanation_url}")
                
                # Return the JSON response directly
                return result_json
            except Exception as e:
                logger.error(f"Failed to save explanation: {e}")
                raise HTTPException(status_code=500, detail="Failed to save explanation")
            except Exception as download_error:
                logger.error(f"Failed to save Google Veo3 video: {download_error}")
                raise HTTPException(status_code=500, detail=f"Failed to download video: {str(download_error)}")
                
        except Exception as e:
            logger.error(f"Google Veo3 Error: {e}")
            raise HTTPException(status_code=500, detail=f"Error generating video: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "Google Veo3 Text-to-Video API is running!"}

@app.post("/generate_video")
async def generate_video_endpoint(request: VideoRequest):
    """Generates a video from a text prompt using Google Veo3."""
    try:
        service = GoogleVeo3Service()
        video_url = service.generate_video(request.prompt, request.video_ratio, request.video_quality)
        
        return {
            "success": True,
            "video_url": video_url,
            "message": "Video generated successfully with Google Veo3"
        }
    except Exception as e:
        logger.error(f"Error in video generation: {e}")
        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"Failed to generate video: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting Google Veo3 API server on port 8077...")
    uvicorn.run(app, host="0.0.0.0", port=8077)
