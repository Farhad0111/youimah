from fastapi import APIRouter, Depends, HTTPException
from app.services.Text_Video.video import VideoService
from app.services.Text_Video.video_schema import VideoRequest
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/generate_video")
async def generate_video_endpoint(request: VideoRequest, video_service: VideoService = Depends(VideoService)):
    """Generates a video from a text prompt."""
    try:
        logger.info(f"Received video generation request: {request.prompt[:50]}...")
        logger.info(f"Video model: {request.video_model}")
        
        video_url = video_service.generate_video(
            request.prompt, 
            request.video_ratio, 
            request.video_quality,
            request.video_model
        )

        if video_url:
            return {
                "success": True,
                "video_url": video_url,
                "message": "Video generated successfully"
            }
        else:
            raise HTTPException(
                status_code=500, 
                detail="Failed to generate video with all available providers. Please check your API keys and try again."
            )
            
    except Exception as e:
        logger.error(f"Unexpected error in video generation: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )