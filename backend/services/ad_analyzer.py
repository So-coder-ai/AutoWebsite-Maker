from groq import Groq
import os
from PIL import Image
import io
import json
import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
from urllib.parse import urlparse


class AdAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    async def analyze_image(self, image_content: bytes, filename: str) -> Dict[str, Any]:
        try:
            image = Image.open(io.BytesIO(image_content))

            prompt = """
Analyze this ad and return ONLY JSON:

{
  "headline": "",
  "tone": "",
  "offer": "",
  "target_audience": "",
  "cta": ""
}
"""

            width, height = image.size
            prompt += f"\nImage metadata: filename={filename}, size={width}x{height}, mode={image.mode}"
            response_text = self._generate_text(prompt)
            return self._parse_and_normalize(response_text)

        except Exception as e:
            print("Groq Error:", e)
            return self.fallback(filename=filename)

    async def analyze_text(self, ad_text: str) -> Dict[str, Any]:
        try:
            prompt = f"""
Analyze this ad copy and return ONLY JSON:

Ad:
{ad_text}

Format:
{{
  "headline": "",
  "tone": "",
  "offer": "",
  "target_audience": "",
  "cta": ""
}}
"""

            response_text = self._generate_text(prompt)
            return self._parse_and_normalize(response_text)

        except Exception as e:
            print("Groq Error:", e)
            return self.fallback(source_text=ad_text)

    async def analyze_from_url(self, ad_url: str) -> Dict[str, Any]:
        try:
            response = requests.get(ad_url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")

            text_content = soup.get_text(separator=" ", strip=True)[:2000]

            prompt = f"""
Analyze this ad content and return ONLY JSON:

Content:
{text_content}

Format:
{{
  "headline": "",
  "tone": "",
  "offer": "",
  "target_audience": "",
  "cta": "",
  "brand_voice": ""
}}
"""

            response_text = self._generate_text(prompt)
            return self._parse_and_normalize(response_text)

        except Exception as e:
            print("Groq Error:", e)
            return self.fallback(source_url=ad_url)

    def fallback(
        self,
        source_text: str = "",
        source_url: str = "",
        filename: str = ""
    ) -> Dict[str, Any]:
        headline = "Special Offer"
        cta = "Learn More"
        audience = "online shoppers"
        offer = "Limited-time promotion"
        tone = "persuasive"

        if source_text:
            short = re.sub(r"\s+", " ", source_text).strip()
            if short:
                headline = short[:80]
            lower_text = short.lower()
            if any(word in lower_text for word in ["discount", "off", "sale", "deal"]):
                offer = "Promotional discount"
                cta = "Claim Offer"

        if source_url:
            domain = urlparse(source_url).netloc.replace("www.", "")
            if domain:
                brand_hint = domain.split(".")[0].replace("-", " ").strip()
                if brand_hint:
                    headline = f"{brand_hint.title()} - Featured Offer"

        if filename:
            ext = filename.split(".")[-1].lower() if "." in filename else ""
            if ext:
                audience = "ad campaign visitors"

        return {
            "headline": headline,
            "tone": tone,
            "offer": offer,
            "target_audience": audience,
            "cta": cta,
            "visual_elements": ["hero image", "promotional badge"],
            "brand_voice": "Clear and benefit-focused"
        }

    def _parse_and_normalize(self, response_text: str) -> Dict[str, Any]:
        text = (response_text or "").strip()
        if not text:
            raise ValueError("Empty Groq response")

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                raise
            data = json.loads(match.group(0))

        return self._normalize_schema(data)

    def _generate_text(self, prompt: str) -> str:
        if not self.client:
            raise ValueError("GROQ_API_KEY is not configured")

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Return strict JSON only. No markdown fences.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=500,
        )
        return completion.choices[0].message.content or ""

    def _normalize_schema(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "headline": str(data.get("headline", "Special Offer")).strip() or "Special Offer",
            "tone": str(data.get("tone", "persuasive")).strip() or "persuasive",
            "offer": str(data.get("offer", "Limited-time promotion")).strip() or "Limited-time promotion",
            "target_audience": str(data.get("target_audience", "online shoppers")).strip() or "online shoppers",
            "cta": str(data.get("cta", "Learn More")).strip() or "Learn More",
            "brand_voice": str(data.get("brand_voice", "Clear and benefit-focused")).strip() or "Clear and benefit-focused"
        }