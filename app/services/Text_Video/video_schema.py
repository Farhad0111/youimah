from pydantic import BaseModel, Field, validator
from typing import Optional

class VideoRequest(BaseModel):
    prompt: str = Field(..., description="The text prompt for the video.")
    video_ratio: str = Field(..., description="Video aspect ratio (1:1, 16:9, 9:16, 3:1, 1:3)")
    video_quality: str = Field(..., description="Video quality (140, 360, 720, 1080, 2K, 4K)")
    video_model: str = Field(..., description="Video model to use (veo3-fast, veo3-quality)")
    
    @validator('video_model')
    def validate_video_model(cls, v):
        allowed_models = ['veo3-fast', 'veo3-quality']
        if v not in allowed_models:
            raise ValueError(f'video_model must be one of {allowed_models}')
        return v
    
    @validator('video_ratio')
    def validate_video_ratio(cls, v):
        allowed_ratios = ['1:1', '16:9', '9:16', '3:1', '1:3']
        if v not in allowed_ratios:
            raise ValueError(f'video_ratio must be one of {allowed_ratios}')
        return v
    
    @validator('video_quality')
    def validate_video_quality(cls, v):
        allowed_qualities = ['140', '360', '720', '1080', '2K', '4K']
        if v not in allowed_qualities:
            raise ValueError(f'video_quality must be one of {allowed_qualities}')
        return v