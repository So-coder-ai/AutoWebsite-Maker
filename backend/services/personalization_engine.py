import groq
import os
from typing import Dict, Any
import json
import re
import logging
from bs4 import BeautifulSoup
from jinja2 import Template

class PersonalizationEngine:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    async def generate_personalized_page(
        self, 
        ad_analysis: Dict[str, Any], 
        page_content: Dict[str, Any],
        original_url: str
    ) -> Dict[str, Any]:
        
        try:
            optimization_plan = await self._create_optimization_plan(ad_analysis, page_content)
            
            personalized_content = await self._generate_personalized_content(
                ad_analysis, page_content, optimization_plan
            )
            
            enhanced_html = await self._create_enhanced_html(
                page_content, personalized_content, optimization_plan
            )
            
            changes_summary = await self._generate_changes_summary(
                ad_analysis, optimization_plan, personalized_content
            )
            
            return {
                "html": enhanced_html,
                "changes_summary": changes_summary,
                "optimization_plan": optimization_plan,
                "personalized_content": personalized_content
            }
            
        except Exception as e:
            return self._create_fallback_response(page_content, str(e))
    
    async def _create_optimization_plan(
        self, 
        ad_analysis: Dict[str, Any], 
        page_content: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        prompt = f"""
        You are a CRO (Conversion Rate Optimization) expert. Analyze the following data and create an optimization plan:

        AD ANALYSIS:
        {json.dumps(ad_analysis, indent=2)}

        CURRENT PAGE CONTENT:
        Headlines: {page_content.get('content', {}).get('headlines', [])}
        Hero Section: {page_content.get('content', {}).get('hero_section', {}).get('text', '')}
        CTA Elements: {page_content.get('content', {}).get('cta_elements', [])}

        Create a structured optimization plan with:
        1. Headline optimization (match ad messaging)
        2. Tone alignment (ensure consistency)
        3. CTA improvements (clarity and urgency)
        4. Value proposition enhancement
        5. Social proof additions
        6. Trust signals

        Return as JSON with keys: headline_optimization, tone_alignment, cta_improvements, value_prop, social_proof, trust_signals
        """
        
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You are a CRO expert. Create specific, actionable optimization plans."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logging.warning(f"JSON parse failed: {e}, using fallback")
            return self._create_default_optimization_plan()
    
    async def _generate_personalized_content(
        self, 
        ad_analysis: Dict[str, Any], 
        page_content: Dict[str, Any],
        optimization_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        personalized = {}
        
        personalized["headline"] = await self._generate_headline(
            ad_analysis, page_content, optimization_plan
        )
        
        personalized["sub_headlines"] = await self._generate_sub_headlines(
            ad_analysis, page_content, optimization_plan
        )
        
        personalized["cta_text"] = await self._generate_cta_text(
            ad_analysis, page_content, optimization_plan
        )
        
        personalized["value_proposition"] = await self._generate_value_proposition(
            ad_analysis, page_content, optimization_plan
        )
        
        personalized["social_proof"] = await self._generate_social_proof(
            ad_analysis, page_content, optimization_plan
        )
        
        return personalized
    
    async def _generate_headline(
        self, 
        ad_analysis: Dict[str, Any], 
        page_content: Dict[str, Any],
        optimization_plan: Dict[str, Any]
    ) -> str:
        
        current_headlines = page_content.get('content', {}).get('headlines', [])
        ad_headline = ad_analysis.get('headline', '')
        ad_tone = ad_analysis.get('tone', '')
        
        prompt = f"""
        Create an optimized headline that matches the ad creative and improves conversion.

        CURRENT HEADLINES: {current_headlines[:3]}
        AD HEADLINE: {ad_headline}
        AD TONE: {ad_tone}
        TARGET AUDIENCE: {ad_analysis.get('target_audience', '')}
        OFFER: {ad_analysis.get('offer', '')}

        Requirements:
        - Match the tone and messaging from the ad
        - Include the main value proposition
        - Be action-oriented and compelling
        - Keep under 60 characters for SEO
        - Use the same language style as the ad

        Return only the headline text, no quotes.
        """
        
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You are a copywriting expert specializing in conversion optimization."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=100
        )
        
        return response.choices[0].message.content.strip()
    
    async def _generate_sub_headlines(
        self, 
        ad_analysis: Dict[str, Any], 
        page_content: Dict[str, Any],
        optimization_plan: Dict[str, Any]
    ) -> list:
        
        current_headlines = page_content.get('content', {}).get('headlines', [])
        
        prompt = f"""
        Create 2-3 sub-headlines that support the main headline and match the ad creative.

        CURRENT HEADLINES: {current_headlines[3:6]}
        AD TONE: {ad_analysis.get('tone', '')}
        TARGET AUDIENCE: {ad_analysis.get('target_audience', '')}
        OFFER: {ad_analysis.get('offer', '')}

        Requirements:
        - Support the main value proposition
        - Address specific pain points
        - Maintain consistent tone with ad
        - Be benefit-focused

        Return as a JSON array of strings.
        """
        
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You are a copywriting expert. Create compelling sub-headlines."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=200
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logging.warning(f"JSON parse failed: {e}, using fallback")
            return current_headlines[:3]
    
    async def _generate_cta_text(
        self, 
        ad_analysis: Dict[str, Any], 
        page_content: Dict[str, Any],
        optimization_plan: Dict[str, Any]
    ) -> Dict[str, str]:
        
        current_ctas = page_content.get('content', {}).get('cta_elements', [])
        ad_tone = ad_analysis.get('tone', '')
        
        prompt = f"""
        Create optimized CTA button text that matches the ad creative and drives action.

        CURRENT CTAS: {[cta.get('text', '') for cta in current_ctas]}
        AD TONE: {ad_tone}
        OFFER: {ad_analysis.get('offer', '')}
        TARGET AUDIENCE: {ad_analysis.get('target_audience', '')}

        Requirements:
        - Match the tone (urgency, luxury, casual, etc.)
        - Be action-oriented
        - Create urgency or clarity
        - Keep under 25 characters

        Return JSON with keys: primary_cta, secondary_cta
        """
        
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You are a CRO expert specializing in call-to-action optimization."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=150
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logging.warning(f"JSON parse failed: {e}, using fallback")
            return {"primary_cta": "Get Started", "secondary_cta": "Learn More"}
    
    async def _generate_value_proposition(
        self, 
        ad_analysis: Dict[str, Any], 
        page_content: Dict[str, Any],
        optimization_plan: Dict[str, Any]
    ) -> str:
        
        prompt = f"""
        Create a compelling value proposition that aligns with the ad creative.

        AD OFFER: {ad_analysis.get('offer', '')}
        TARGET AUDIENCE: {ad_analysis.get('target_audience', '')}
        BRAND VOICE: {ad_analysis.get('brand_voice', '')}

        Requirements:
        - Highlight key benefits from the ad
        - Address audience pain points
        - Maintain brand voice consistency
        - Be clear and concise

        Return only the value proposition text.
        """
        
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You are a marketing expert specializing in value propositions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()
    
    async def _generate_social_proof(
        self, 
        ad_analysis: Dict[str, Any], 
        page_content: Dict[str, Any],
        optimization_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        return {
            "testimonial": f"See why {ad_analysis.get('target_audience', 'customers')} love our product",
            "stats": [
                {"number": "10,000+", "label": "Happy Customers"},
                {"number": "4.9/5", "label": "Average Rating"},
                {"number": "24/7", "label": "Support"}
            ],
            "trust_badges": ["Money Back Guarantee", "SSL Secured", "Award Winning"]
        }
    
    async def _create_enhanced_html(
        self, 
        page_content: Dict[str, Any],
        personalized_content: Dict[str, Any],
        optimization_plan: Dict[str, Any]
    ) -> str:
        """Create enhanced HTML maintaining original structure"""
        
        # This is a simplified version - in production, you'd want more sophisticated HTML manipulation
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Personalized Landing Page</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 0; line-height: 1.6; }
                .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
                .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 80px 20px; text-align: center; }
                .hero h1 { font-size: 3em; margin-bottom: 20px; }
                .hero p { font-size: 1.2em; margin-bottom: 30px; }
                .cta-button { background: #ff6b6b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; margin: 10px; }
                .cta-button.secondary { background: transparent; border: 2px solid white; }
                .features { padding: 60px 20px; }
                .features h2 { text-align: center; margin-bottom: 40px; }
                .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
                .feature { text-align: center; padding: 20px; }
                .social-proof { background: #f8f9fa; padding: 60px 20px; text-align: center; }
                .stats { display: flex; justify-content: space-around; margin: 40px 0; }
                .stat { text-align: center; }
                .stat-number { font-size: 2em; font-weight: bold; color: #667eea; }
                .trust-badges { display: flex; justify-content: center; gap: 20px; margin-top: 30px; }
                .badge { background: white; padding: 10px 20px; border-radius: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            </style>
        </head>
        <body>
            <header class="hero">
                <div class="container">
                    <h1>{{ personalized_content.headline }}</h1>
                    <p>{{ personalized_content.value_proposition }}</p>
                    <div>
                        <a href="#" class="cta-button">{{ personalized_content.cta_text.primary_cta }}</a>
                        <a href="#" class="cta-button secondary">{{ personalized_content.cta_text.secondary_cta }}</a>
                    </div>
                </div>
            </header>

            <section class="features">
                <div class="container">
                    <h2>Why Choose Us</h2>
                    <div class="feature-grid">
                        {% for sub_headline in personalized_content.sub_headlines %}
                        <div class="feature">
                            <h3>{{ sub_headline }}</h3>
                            <p>Tailored specifically for {{ ad_analysis.target_audience }} with proven results.</p>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </section>

            <section class="social-proof">
                <div class="container">
                    <h2>{{ personalized_content.social_proof.testimonial }}</h2>
                    <div class="stats">
                        {% for stat in personalized_content.social_proof.stats %}
                        <div class="stat">
                            <div class="stat-number">{{ stat.number }}</div>
                            <div>{{ stat.label }}</div>
                        </div>
                        {% endfor %}
                    </div>
                    <div class="trust-badges">
                        {% for badge in personalized_content.social_proof.trust_badges %}
                        <div class="badge">{{ badge }}</div>
                        {% endfor %}
                    </div>
                </div>
            </section>
        </body>
        </html>
        """
        
        template = Template(html_template)
        return template.render(
            personalized_content=personalized_content,
            ad_analysis=ad_analysis
        )
    
    async def _generate_changes_summary(
        self, 
        ad_analysis: Dict[str, Any],
        optimization_plan: Dict[str, Any],
        personalized_content: Dict[str, Any]
    ) -> str:
        
        prompt = f"""
        Create a concise summary of the personalization changes made to the landing page.

        AD ANALYSIS: {json.dumps(ad_analysis, indent=2)}
        OPTIMIZATION PLAN: {json.dumps(optimization_plan, indent=2)}
        PERSONALIZED CONTENT: {json.dumps(personalized_content, indent=2)}

        Create a summary that explains:
        1. What was changed
        2. Why it was changed (CRO reasoning)
        3. How it aligns with the ad creative
        4. Expected impact on conversion

        Keep it under 200 words and be specific about the improvements.
        """
        
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": "You are a CRO expert explaining optimization changes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()
    
    def _create_default_optimization_plan(self) -> Dict[str, Any]:
        return {
            "headline_optimization": "Align headline with ad messaging",
            "tone_alignment": "Match ad tone and voice",
            "cta_improvements": "Increase clarity and urgency",
            "value_prop": "Highlight key benefits",
            "social_proof": "Add testimonials and stats",
            "trust_signals": "Include security badges"
        }
    
    def _create_fallback_response(self, page_content: Dict[str, Any], error: str) -> Dict[str, Any]:
        
        fallback_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Personalized Landing Page</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .error {{ background: #ffebee; padding: 20px; border-left: 4px solid #f44336; }}
            </style>
        </head>
        <body>
            <h1>Enhanced Landing Page</h1>
            <div class="error">
                <p><strong>Note:</strong> AI personalization encountered an issue. Showing enhanced version with basic optimizations.</p>
                <p>Error: {error}</p>
            </div>
            <!-- Include original page content with basic enhancements -->
            <div class="content">
                {page_content.get('content', {}).get('hero_section', {}).get('html', '<p>Content loading...</p>')}
            </div>
        </body>
        </html>
        """
        
        return {
            "html": fallback_html,
            "changes_summary": f"Basic optimizations applied. AI personalization failed: {error}",
            "optimization_plan": {},
            "personalized_content": {},
            "error": error
        }
