import requests
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoService:
    def __init__(self):
        self.veo3_gen_api_key = os.getenv("VEO3_GEN_API_KEY")
        self.google_veo3_api_key = os.getenv("GOOGLE_VEO3_API_KEY")
        self.timeout = 30  # 30 seconds timeout
        self.base_url = 'https://api.veo3gen.app'
        
        # Initialize VEO3 session
        if self.veo3_gen_api_key:
            self.veo3_session = requests.Session()
            self.veo3_session.headers.update({
                'Authorization': f'Bearer {self.veo3_gen_api_key}',
                'Content-Type': 'application/json'
            })

    def generate_video_veo3_gen(self, prompt: str, video_ratio: str, video_quality: str, video_model: str = None) -> str:
        """Generates a video using Veo3 Gen with proper async handling."""
        
        if not self.veo3_gen_api_key:
            logger.warning("VEO3_GEN_API_KEY not found in environment variables")
            return None
        
        # Use provided video_model or fallback to quality-based mapping
        if video_model:
            model = video_model
        else:
            # Fallback: Map quality to model type
            if video_quality in ["140", "360", "720"]:
                model = "veo3-fast"
            else:
                model = "veo3-quality"
        
        # Map quality to resolution
        if video_quality in ["140", "360", "720"]:
            resolution = "720p"
        else:
            resolution = "1080p"
        
        # Map video_ratio to proper format if needed
        aspect_ratio = video_ratio  # Keep as is for now
        
        try:
            logger.info(f"Starting VEO3 video generation...")
            logger.info(f"Prompt: {prompt[:50]}...")
            logger.info(f"Model: {model}, Resolution: {resolution}")
            
            # Step 1: Start generation
            generation_data = {
                'model': model,
                'prompt': prompt,
                'audio': True,
                'options': {
                    'resolution': resolution,
                    'aspect_ratio': aspect_ratio,
                    'duration': 5
                }
            }
            
            response = self.veo3_session.post(f'{self.base_url}/api/generate', json=generation_data)
            
            if not response.ok:
                error_msg = response.json().get("error", "Unknown error")
                logger.error(f'VEO3 generation request failed: {error_msg}')
                return None
            
            result = response.json()
            task_id = result.get("taskId")
            if not task_id:
                logger.error("No task ID returned from VEO3 generation")
                return None
                
            logger.info(f'VEO3 generation started with task ID: {task_id}')
            
            # Step 2: Poll for completion (with timeout)
            return self._poll_veo3_completion(task_id, max_wait_time=300)
            
        except requests.exceptions.Timeout:
            logger.error("VEO3 Gen API request timed out")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"VEO3 Gen Connection Error: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"VEO3 Gen HTTP Error: {e}")
            if e.response and e.response.status_code == 400:
                try:
                    error_data = e.response.json()
                    if error_data.get("errorType") == "INSUFFICIENT_CREDITS":
                        logger.error(f"Insufficient credits for VEO3 Gen: Required {error_data.get('required', 'unknown')}, Available {error_data.get('available', 'unknown')}")
                    else:
                        logger.error(f"VEO3 Gen validation error: {error_data.get('error', 'Unknown error')}")
                except:
                    logger.error(f"Response content: {e.response.text if e.response else 'No response'}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"VEO3 Gen Request Error: {e}")
            return None
    
    def _poll_veo3_completion(self, task_id: str, max_wait_time: int = 300) -> str:
        """Poll VEO3 status until completion"""
        start_time = time.time()
        logger.info(f'Polling VEO3 status for task: {task_id}')
        
        while time.time() - start_time < max_wait_time:
            try:
                # Check status
                response = self.veo3_session.get(f'{self.base_url}/api/status/{task_id}')
                
                if not response.ok:
                    error_msg = response.json().get('error', 'Unknown error')
                    logger.error(f'VEO3 status check failed: {error_msg}')
                    return None
                
                status_data = response.json()
                current_status = status_data.get('status')
                logger.info(f'VEO3 status: {current_status}')
                
                if current_status == 'completed':
                    logger.info('VEO3 video generation completed successfully!')
                    video_url = status_data.get('result', {}).get('videoUrl')
                    if video_url:
                        return video_url
                    else:
                        logger.error("No video URL in completed response")
                        return None
                        
                elif current_status == 'failed':
                    error_msg = status_data.get('error', {}).get('message', 'Unknown error')
                    logger.error(f'VEO3 video generation failed: {error_msg}')
                    return None
                
                # Still processing, wait before next check
                logger.info('VEO3 video still processing, waiting 10 seconds...')
                time.sleep(10)
                
            except Exception as e:
                logger.error(f"Error while polling VEO3 status: {e}")
                return None
        
        logger.error('VEO3 video generation timed out')
        return None

    def generate_video_google_veo3(self, prompt: str, video_ratio: str, video_quality: str, video_model: str = None) -> str:
        """Generates a video using Google Veo3 via official Google GenAI client."""
        
        if not self.google_veo3_api_key:
            logger.warning("GOOGLE_VEO3_API_KEY not found in environment variables")
            return None
        
        try:
            # Import Google GenAI client
            import google.generativeai as genai
            
            # Configure the API key
            genai.configure(api_key=self.google_veo3_api_key)
            
            logger.info(f"Starting Google Veo3 video generation...")
            logger.info(f"Prompt: {prompt[:50]}...")
            
            # Get the Gemini model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Generate video
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.4,
                    response_mime_type="video/mp4"
                )
            )
            
            logger.info("Google Veo3 video generation complete")
            
            # Log the response structure for debugging
            logger.info(f"Response type: {type(response)}")
            logger.info(f"Response attributes: {dir(response)}")
            
            # Check if there are parts in the response
            if not hasattr(response, 'parts') or len(response.parts) == 0:
                logger.error("No parts found in the response")
                return None
            
            # Find the video part (should be video/mp4)
            video_part = None
            for part in response.parts:
                if hasattr(part, 'mime_type') and part.mime_type and 'video' in part.mime_type:
                    video_part = part
                    break
            
            if not video_part:
                logger.error("No video part found in response")
                return None
            
            # Log the video part details
            logger.info(f"Found video part with mime type: {video_part.mime_type}")
                
            # If we have video data, save it to a file
            logger.info("Google Veo3 video generation completed successfully!")
            
            # Generate a unique filename
            import uuid
            video_filename = f"veo3_video_{uuid.uuid4().hex[:8]}.mp4"
            video_path = os.path.join("videos", video_filename)
            
            # Make sure the videos directory exists
            os.makedirs("videos", exist_ok=True)
            
            # Download and save the video
            try:
                # Check if the part has a data attribute
                if hasattr(video_part, 'data') and video_part.data:
                    with open(video_path, "wb") as f:
                        f.write(video_part.data)
                    
                    # Return the local file path (you might want to upload to cloud storage)
                    video_url = f"/videos/{video_filename}"  # Adjust based on your file serving setup
                    logger.info(f"Video saved as: {video_path}")
                    return video_url
                    
                    # Return the local file path (you might want to upload to cloud storage)
                    video_url = f"/videos/{video_filename}"  # Adjust based on your file serving setup
                    logger.info(f"Video saved as: {video_path}")
                    return video_url
                else:
                    logger.error("No video data found in the response part")
                    return None
            except Exception as e:
                logger.error(f"Failed to save Google Veo3 video: {e}")
                return None
            
        except ImportError:
            logger.error("Google GenAI library not installed. Install with: pip install google-generativeai")
            return None
        except Exception as e:
            logger.error(f"Google Veo3 Error: {e}")
            return None

    def generate_video(self, prompt: str, video_ratio: str, video_quality: str, video_model: str = None) -> str:
        """Attempts to generate a video with Veo3 Gen, falls back to Google Veo3."""
        logger.info(f"Starting video generation for prompt: {prompt[:50]}...")
        logger.info(f"Using video model: {video_model if video_model else 'auto-detected from quality'}")
        
        # Try Veo3 Gen first
        video_url = self.generate_video_veo3_gen(prompt, video_ratio, video_quality, video_model)
        if video_url:
            logger.info("Successfully generated video with Veo3 Gen")
            return video_url
        
        # Fall back to Google Veo3
        logger.info("Veo3 Gen failed, trying Google Veo3...")
        video_url = self.generate_video_google_veo3(prompt, video_ratio, video_quality, video_model)
        if video_url:
            logger.info("Successfully generated video with Google Veo3")
            return video_url
        
        # Both APIs failed or unavailable
        logger.error("Video generation failed with both providers")
        return None