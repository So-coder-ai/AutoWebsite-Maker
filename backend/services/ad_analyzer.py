import groq
import requests
from PIL import Image
import io
import base64
from typing import Dict, Any, Optional
import os
from bs4 import BeautifulSoup

class AdAnalyzer:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    async def analyze_image(self, image_content: bytes, filename: str) -> Dict[str, Any]:
        try:
            base64_image = base64.b64encode(image_content).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{base64_image}"
            
            response = self.client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are an expert marketing analyst. Analyze this ad creative image and extract:
                        1. Headline/main text visible
                        2. Tone (urgency, luxury, casual, professional, etc.)
                        3. Offer (discounts, free trial, CTA, value proposition)
                        4. Target audience signals (demographics, interests, pain points)
                        5. Visual elements and design characteristics
                        6. Brand voice characteristics
                        
                        Return as structured JSON with keys: headline, tone, offer, target_audience, visual_elements, brand_voice
                        """
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url
                                }
                            },
                            {
                                "type": "text",
                                "text": f"Analyze this ad creative image (filename: {filename}) and extract key marketing insights."
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                "headline": "Ad Creative Headline",
                "tone": "professional",
                "offer": "Special offer available",
                "target_audience": "General audience",
                "visual_elements": ["Image content", "Text overlay"],
                "brand_voice": "Professional",
                "error": str(e)
            }
    
    async def analyze_from_url(self, ad_url: str) -> Dict[str, Any]:
        try:
            response = requests.get(ad_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            text_content = soup.get_text(strip=True)
            analysis_response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        Analyze this ad content and extract marketing insights:
                        - Headline/main message
                        - Tone and style
                        - Offer or value proposition
                        - Target audience
                        - Call to action
                        
                        Return as JSON with keys: headline, tone, offer, target_audience, cta, brand_voice
                        """
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this ad content: {text_content[:2000]}"
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            import json
            return json.loads(analysis_response.choices[0].message.content)
            
        except Exception as e:
            return {
                "headline": "Failed to extract from URL",
                "tone": "unknown",
                "offer": "Unknown",
                "target_audience": "Unknown",
                "cta": "Unknown",
                "brand_voice": "Unknown",
                "error": str(e)
            }
    
    async def analyze_text(self, ad_text: str) -> Dict[str, Any]:
        try:
            analysis_response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are a marketing expert. Analyze this ad copy and extract:
                        1. Headline/main message
                        2. Tone (urgency, luxury, casual, professional)
                        3. Offer (discounts, benefits, value proposition)
                        4. Target audience characteristics
                        5. Call to action
                        6. Brand voice
                        
                        Return as JSON with these exact keys.
                        """
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this ad copy: {ad_text}"
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            import json
            return json.loads(analysis_response.choices[0].message.content)
            
        except Exception as e:
            return {
                "headline": ad_text[:50] + "..." if len(ad_text) > 50 else ad_text,
                "tone": "professional",
                "offer": "Value proposition in text",
                "target_audience": "General audience",
                "cta": "Learn more",
                "brand_voice": "Professional",
                "error": str(e)
            }
