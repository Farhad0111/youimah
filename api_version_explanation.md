# Google Video Generation Explained

## API Version Differences

It appears that the example code you provided:

```python
import time
from google import genai
from google.genai import types

client = genai.Client()

prompt = "..."

operation = client.models.generate_videos(
    model="veo-3.0-generate-preview",
    prompt=prompt,
)
```

Is using a different version of the Google GenAI API than what's publicly available in the Python SDK we're using.

## Current Limitations

The current publicly available Google GenerativeAI Python SDK (`google-generativeai` version 0.8.5) doesn't support direct video generation through the API. When we try to use `response_mime_type="video/mp4"`, we get this error:

```
400 * GenerateContentRequest.generation_config.response_mime_type: allowed mimetypes are `text/plain`, `application/json`, `application/xml`, `application/yaml` and `text/x.enum`.
```

This shows that the current public API only supports text and structured data outputs, not video.

## Possible Explanations

1. **Private Alpha/Beta Access**: The example code might be using a private alpha or beta version of the API that isn't yet publicly available.

2. **Different Service**: The example might be using a completely different service than the Gemini API.

3. **Future Feature**: The example might be demonstrating functionality that will be available in a future release.

## How to Proceed

1. **Contact Google**: If you have access to Google support, ask about the video generation capabilities and when they will be publicly available.

2. **Use Alternative Services**: Consider using other specialized video generation APIs for your needs.

3. **Wait for Updates**: Monitor the Google GenAI SDK for updates that might introduce video generation capabilities.

4. **Use Gemini for Planning**: While Gemini can't generate videos directly, it can help create scripts, storyboards, and other planning materials for video production.

## Testing

The `test.py` script demonstrates the current limitations and confirms that video generation isn't yet supported in the public SDK.
