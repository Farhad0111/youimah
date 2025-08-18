from pydantic import BaseModel, Field
from typing import Optional

class VideoRequest(BaseModel):
    prompt: str = Field(..., description="The text prompt for the video.")
    video_ratio: str = Field(..., description="Video aspect ratio (1:1, 16:9, 9:16, 3:1, 1:3)")
    video_quality: str = Field(..., description="Video quality (140, 360, 720, 1080, 2K, 4K)")