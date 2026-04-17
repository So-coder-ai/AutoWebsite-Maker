from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, Any, List
import asyncio
import logging
import requests
from playwright.async_api import async_playwright

class PageScraper:
    def __init__(self):
        pass

    async def scrape_page(self, url: str) -> Dict[str, Any]:
        try:
            try:
                html = await self.scrape_dynamic_page(url)
                js_rendered = True
            except Exception:
                logging.warning("Dynamic scrape failed; falling back to static fetch.")
                html = self.scrape_static_page(url)
                js_rendered = False

            soup = BeautifulSoup(html, 'html.parser')

            page_data = {
                "url": url,
                "raw_html": html,
                "title": self._get_title(soup),
                "meta_description": self._get_meta_description(soup),

                "structure": self._analyze_structure(soup),

                "content": self._extract_content(soup),

                "components": self._identify_components(soup),

                "styles": self._extract_styles(soup, url),
                "images": self._extract_images(soup, url),
                "forms": self._extract_forms(soup),
                "links": self._extract_links(soup, url),

                "js_rendered": js_rendered
            }

            return page_data

        except Exception as e:
            logging.error(f"Playwright scraping failed: {e}")

            return {
                "url": url,
                "raw_html": "",
                "title": "Failed to load",
                "error": str(e),
                "structure": {"type": "unknown"},
                "content": {"sections": []},
                "components": [],
                "styles": {},
                "images": [],
                "forms": [],
                "links": [],
                "js_rendered": False
            }

    def scrape_static_page(self, url: str) -> str:
        response = requests.get(
            url,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()
        return response.text

    async def scrape_dynamic_page(self, url: str) -> str:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)

                context = await browser.new_context(
                    user_agent="Mozilla/5.0"
                )

                page = await context.new_page()

                await page.goto(url, timeout=60000)

                await page.wait_for_load_state("networkidle")

                for _ in range(5):
                    await page.mouse.wheel(0, 3000)
                    await page.wait_for_timeout(1000)

                html = await page.content()

                await browser.close()

                return html

        except Exception as e:
            logging.error(f"Playwright dynamic scraping failed: {e}")
            raise
    
    def _get_title(self, soup: BeautifulSoup) -> str:
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else ""
    
    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        return meta_desc.get('content', '') if meta_desc else ""
    
    def _analyze_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        structure = {
            "has_header": bool(soup.find('header')),
            "has_nav": bool(soup.find('nav')),
            "has_hero": bool(soup.find(['section', 'div'], class_=re.compile(r'hero|banner|jumbotron', re.I))),
            "has_footer": bool(soup.find('footer')),
            "heading_hierarchy": self._get_heading_hierarchy(soup),
            "layout_type": self._detect_layout_type(soup)
        }
        return structure
    
    def _get_heading_hierarchy(self, soup: BeautifulSoup) -> List[str]:
        headings = []
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            if h_tags:
                headings.extend([h.get_text().strip() for h in h_tags[:3]])
        return headings
    
    def _detect_layout_type(self, soup: BeautifulSoup) -> str:
        if soup.find(class_=re.compile(r'container|wrapper', re.I)):
            return "container-based"
        elif soup.find(class_=re.compile(r'grid|flex', re.I)):
            return "modern-css"
        else:
            return "traditional"
    
    def _extract_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        content = {
            "hero_section": self._extract_hero_section(soup),
            "headlines": self._extract_headlines(soup),
            "paragraphs": self._extract_paragraphs(soup),
            "cta_elements": self._extract_cta_elements(soup),
            "sections": self._extract_sections(soup)
        }
        return content
    
    def _extract_hero_section(self, soup: BeautifulSoup) -> Dict[str, Any]:
        hero_selectors = [
            'header', '.hero', '.banner', '.jumbotron', 
            '[class*="hero"]', '[class*="banner"]'
        ]
        
        for selector in hero_selectors:
            hero = soup.select_one(selector)
            if hero:
                return {
                    "html": str(hero),
                    "text": hero.get_text(strip=True),
                    "headlines": [h.get_text().strip() for h in hero.find_all(['h1', 'h2', 'h3'])],
                    "cta": self._find_cta_in_element(hero)
                }
        
        return {"html": "", "text": "", "headlines": [], "cta": ""}
    
    def _extract_headlines(self, soup: BeautifulSoup) -> List[str]:
        headlines = []
        for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = h.get_text().strip()
            if text and len(text) > 5:
                headlines.append(text)
        return headlines[:10]
    
    def _extract_paragraphs(self, soup: BeautifulSoup) -> List[str]:
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 20:
                paragraphs.append(text)
        return paragraphs[:10]
    
    def _extract_cta_elements(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        cta_elements = []
        
        cta_keywords = ['buy', 'shop', 'order', 'sign up', 'register', 'get started', 'learn more', 'contact', 'call']
        
        for element in soup.find_all(['button', 'a'], class_=re.compile(r'btn|button|cta', re.I)):
            text = element.get_text().strip().lower()
            if any(keyword in text for keyword in cta_keywords):
                cta_elements.append({
                    "text": element.get_text().strip(),
                    "type": element.name,
                    "href": element.get('href', ''),
                    "class": element.get('class', [])
                })
        
        return cta_elements
    
    def _extract_sections(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        sections = []
        
        for section in soup.find_all(['section', 'article', 'main']):
            section_data = {
                "tag": section.name,
                "class": section.get('class', []),
                "id": section.get('id', ''),
                "text": section.get_text(strip=True)[:200],
                "headlines": [h.get_text().strip() for h in section.find_all(['h1', 'h2', 'h3', 'h4'])]
            }
            sections.append(section_data)
        
        return sections[:5]  
    
    def _identify_components(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        components = []
        
        component_patterns = {
            'navigation': ['nav', '.nav', '.navbar', '.menu'],
            'hero': ['.hero', '.banner', '.jumbotron'],
            'features': ['.features', '.feature', '.benefits'],
            'testimonials': ['.testimonial', '.review', '.quotes'],
            'pricing': ['.pricing', '.price', '.plans'],
            'contact': ['.contact', '.form', '.get-in-touch'],
            'footer': ['footer', '.footer']
        }
        
        for comp_type, selectors in component_patterns.items():
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements[:2]:
                    components.append({
                        "type": comp_type,
                        "selector": selector,
                        "html": str(element)[:500],
                        "text": element.get_text(strip=True)[:200]
                    })
        
        return components
    
    def _extract_styles(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
        styles = {
            "css_files": [],
            "inline_styles": [],
            "primary_colors": [],
            "fonts": []
        }
        
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                styles["css_files"].append(full_url)
        
        for style in soup.find_all('style'):
            styles["inline_styles"].append(style.get_text())
        
        return styles
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        images = []
        for img in soup.find_all('img')[:10]:
            src = img.get('src')
            if src:
                images.append({
                    "src": urljoin(base_url, src),
                    "alt": img.get('alt', ''),
                    "title": img.get('title', '')
                })
        return images
    
    def _extract_forms(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        forms = []
        for form in soup.find_all('form'):
            form_data = {
                "action": form.get('action', ''),
                "method": form.get('method', 'GET'),
                "fields": []
            }
            
            for input_elem in form.find_all(['input', 'select', 'textarea']):
                field_data = {
                    "type": input_elem.get('type', 'text'),
                    "name": input_elem.get('name', ''),
                    "placeholder": input_elem.get('placeholder', ''),
                    "required": input_elem.has_attr('required')
                }
                form_data["fields"].append(field_data)
            
            forms.append(form_data)
        
        return forms
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        links = []
        for a in soup.find_all('a', href=True)[:20]:
            href = a.get('href')
            if href and not href.startswith('#'):
                links.append({
                    "href": urljoin(base_url, href),
                    "text": a.get_text().strip(),
                    "title": a.get('title', '')
                })
        return links
    
    def _find_cta_in_element(self, element) -> str:
        cta_selectors = ['button', 'a', '[class*="btn"]', '[class*="cta"]']
        
        for selector in cta_selectors:
            cta = element.select_one(selector)
            if cta:
                text = cta.get_text().strip()
                if text:
                    return text
        
        return ""
