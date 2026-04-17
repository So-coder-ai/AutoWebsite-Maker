from typing import Dict, Any
import logging
from bs4 import BeautifulSoup


class PersonalizationEngine:
    def __init__(self):
        pass

    async def generate_personalized_page(
        self,
        ad_analysis: Dict[str, Any],
        page_content: Dict[str, Any],
        original_url: str
    ) -> Dict[str, Any]:

        try:
            headline = ad_analysis.get("headline", "Special Offer")
            cta = ad_analysis.get("cta", "Shop Now")
            audience = ad_analysis.get("target_audience", "customers")
            offer = ad_analysis.get("offer", "Limited-time promotion")
            tone = ad_analysis.get("tone", "persuasive")

            enhanced_html = self._modify_real_html(
                page_content,
                headline,
                cta,
                audience,
                offer,
                tone
            )

            return {
                "html": enhanced_html,
                "changes_summary": "Enhanced existing page structure with ad-aligned headline, CTA, urgency banner, and CRO proof points.",
                "optimization_plan": {},
                "personalized_content": {
                    "headline": headline,
                    "cta": cta,
                    "audience": audience
                },
                "model_used": "dom-modification"
            }

        except Exception as e:
            logging.error(f"Error: {e}")

            return {
                "html": "<h1>Fallback Page</h1>",
                "changes_summary": "Fallback applied",
                "optimization_plan": {},
                "personalized_content": {},
                "model_used": "fallback"
            }

    def _modify_real_html(
        self,
        page_content: Dict[str, Any],
        headline: str,
        cta: str,
        audience: str,
        offer: str,
        tone: str
    ) -> str:
        html = self._extract_source_html(page_content)

        if not html:
            return self._fallback_html(headline, cta, audience, offer)

        soup = BeautifulSoup(html, "html.parser")
        if not soup.body:
            return self._fallback_html(headline, cta, audience, offer)

        hero = self._find_hero_container(soup)
        self._insert_urgency_banner(soup, headline, offer)
        self._personalize_headline_and_subcopy(soup, hero, headline, audience, offer, tone)
        self._personalize_cta(soup, hero, cta)
        self._inject_proof_points(soup, audience, offer)

        return str(soup)

    def _extract_source_html(self, page_content: Dict[str, Any]) -> str:
        html = page_content.get("raw_html", "") or page_content.get("html", "")
        if html:
            return html

        content = page_content.get("content", {}) or {}
        hero_html = (content.get("hero_section", {}) or {}).get("html", "")
        if hero_html:
            return f"<!DOCTYPE html><html><body>{hero_html}</body></html>"

        sections = content.get("sections", []) or []
        section_html = "".join(
            f"<section><h2>{(sec.get('headlines') or [''])[0]}</h2><p>{sec.get('text', '')}</p></section>"
            for sec in sections[:3]
        )
        if section_html:
            return f"<!DOCTYPE html><html><body>{section_html}</body></html>"
        return ""

    def _find_hero_container(self, soup: BeautifulSoup):
        selectors = [
            "header",
            "section[class*='hero']",
            "div[class*='hero']",
            "section[class*='banner']",
            "main",
            "body",
        ]
        for selector in selectors:
            candidate = soup.select_one(selector)
            if candidate:
                return candidate
        return soup.body

    def _insert_urgency_banner(self, soup: BeautifulSoup, headline: str, offer: str) -> None:
        existing = soup.find(id="ai-urgency-banner")
        if existing:
            existing.decompose()

        banner = soup.new_tag("div", id="ai-urgency-banner")
        banner.string = f"🔥 {headline} — {offer}"
        banner["style"] = (
            "background:linear-gradient(90deg,#7c3aed,#4f46e5);color:#fff;padding:12px;"
            "text-align:center;font-weight:700;font-size:16px;position:sticky;top:0;z-index:2147483647;"
        )
        soup.body.insert(0, banner)

    def _personalize_headline_and_subcopy(
        self,
        soup: BeautifulSoup,
        hero,
        headline: str,
        audience: str,
        offer: str,
        tone: str,
    ) -> None:
        heading_target = None
        search_scope = hero if hero else soup
        for tag in search_scope.find_all(["h1", "h2", "h3"]):
            if len(tag.get_text(" ", strip=True)) > 8:
                heading_target = tag
                break

        if not heading_target:
            heading_target = soup.find(["h1", "h2", "h3"])

        if heading_target:
            heading_target.string = headline

        paragraph_target = None
        for tag in search_scope.find_all("p"):
            if len(tag.get_text(" ", strip=True)) > 20:
                paragraph_target = tag
                break

        if paragraph_target:
            paragraph_target.string = (
                f"Tailored for {audience}. {offer}. Built with a {tone} conversion-focused message."
            )

    def _personalize_cta(self, soup: BeautifulSoup, hero, cta: str) -> None:
        updated = 0
        keywords = ["shop", "buy", "order", "get", "start", "trial", "learn", "sign up", "register"]
        for btn in soup.find_all(["button", "a"]):
            text = btn.get_text(" ", strip=True).lower()
            class_text = " ".join(btn.get("class", [])).lower() if btn.get("class") else ""
            if any(key in text for key in keywords) or any(key in class_text for key in ["btn", "button", "cta"]):
                btn.string = cta
                updated += 1
                if updated >= 2:
                    break

        if updated == 0 and hero is not None:
            button = soup.new_tag("button")
            button.string = cta
            button["style"] = (
                "margin-top:16px;padding:12px 22px;background:#4f46e5;color:#fff;border:none;"
                "border-radius:8px;font-weight:600;cursor:pointer;"
            )
            hero.append(button)

    def _inject_proof_points(self, soup: BeautifulSoup, audience: str, offer: str) -> None:
        existing = soup.find(id="ai-proof-points")
        if existing:
            existing.decompose()

        section = soup.new_tag("section", id="ai-proof-points")
        section["style"] = (
            "margin:24px auto;padding:20px;max-width:900px;border:1px solid #e5e7eb;"
            "border-radius:12px;background:#f8fafc;"
        )
        title = soup.new_tag("h3")
        title.string = "Why this offer fits"
        title["style"] = "margin:0 0 10px 0;font-size:22px;"
        section.append(title)

        ul = soup.new_tag("ul")
        ul["style"] = "margin:0;padding-left:20px;line-height:1.8;"
        points = [
            f"Message aligned for {audience}.",
            f"Offer emphasis: {offer}.",
            "Focused CTA placement to improve conversion intent.",
        ]
        for point in points:
            li = soup.new_tag("li")
            li.string = point
            ul.append(li)
        section.append(ul)

        banner = soup.find(id="ai-urgency-banner")
        if banner and banner.next_sibling:
            banner.insert_after(section)
        else:
            soup.body.insert(1, section)

    def _fallback_html(self, headline: str, cta: str, audience: str, offer: str) -> str:
        return f"""
        <!DOCTYPE html>
        <html>
        <body>
            <div style="background:linear-gradient(90deg,#7c3aed,#4f46e5);color:white;padding:12px;text-align:center;font-weight:700;">
                🔥 {headline} — {offer}
            </div>
            <main style="max-width:960px;margin:24px auto;font-family:Arial,sans-serif;">
                <section style="padding:22px;border:1px solid #e5e7eb;border-radius:12px;">
                    <h1>{headline}</h1>
                    <p>Tailored for {audience}. Personalized as an enhancement workflow with CRO-focused messaging.</p>
                    <button style="padding:12px 22px;background:#4f46e5;color:#fff;border:none;border-radius:8px;">{cta}</button>
                </section>
            </main>
        </body>
        </html>
        """