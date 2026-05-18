"""
Professional Company Enrichment Module
Powered by 100% Free Google Gemini API
"""

import logging
import os
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup
from google import genai

logger = logging.getLogger(__name__)

# Setup Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
    AI_AVAILABLE = True
else:
    logger.warning("GEMINI_API_KEY not found.")
    AI_AVAILABLE = False


async def enrich_company(lead) -> Dict[str, Any]:
    try:
        company_info = extract_company_info(lead.company, lead.website)
        business_analysis = generate_business_analysis(lead.company, company_info)
        ai_opportunities = generate_ai_opportunities(lead.company, business_analysis)
        implementation_plan = generate_implementation_plan(lead.company, ai_opportunities)

        return {
            "company": lead.company,
            "website": lead.website,
            "prospect_name": lead.name,
            "company_info": company_info,
            "business_analysis": business_analysis,
            "ai_opportunities": ai_opportunities,
            "implementation_plan": implementation_plan
        }

    except Exception as e:
        logger.error(f"Enrichment error: {e}")
        return get_professional_fallback(lead)


def extract_company_info(company_name: str, website: str) -> Dict[str, str]:
    try:
        if not website.startswith("http"):
            website = "https://" + website

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        response = requests.get(website, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = " ".join(chunk for chunk in chunks if chunk)

        meta_desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            meta_desc = meta.get("content", "")

        return {
            "website_content": text[:2000],
            "meta_description": meta_desc,
            "company_name": company_name,
            "website_url": website
        }

    except Exception as e:
        logger.warning(f"Website extraction error: {e}")
        return {
            "website_content": "",
            "meta_description": "",
            "company_name": company_name,
            "website_url": website
        }


def generate_business_analysis(company_name: str, company_info: Dict) -> str:
    if not AI_AVAILABLE:
        return get_generic_business_analysis(company_name)

    try:
        prompt = (
            f"Analyze {company_name}. "
            f"Website content: {company_info.get('website_content', '')[:500]}. "
            f"Write 3 professional paragraphs about their business, industry, and challenges."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        logger.error(f"Business analysis error: {e}")
        return get_generic_business_analysis(company_name)


def generate_ai_opportunities(company_name: str, analysis: str) -> list:
    if not AI_AVAILABLE:
        return get_default_ai_opportunities(company_name)

    try:
        prompt = (
            f"List 3 specific AI business opportunities for {company_name} based on this "
            f"analysis: {analysis[:400]}. Format them clearly as bullet points or lines."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        text = response.text.strip()

        opportunities = [
            line.strip("-•1234567890. ")
            for line in text.split("\n")
            if line.strip()
        ]
        return opportunities[:3] if len(opportunities) >= 3 else get_default_ai_opportunities(company_name)

    except Exception as e:
        logger.error(f"AI opportunities error: {e}")
        return get_default_ai_opportunities(company_name)


def generate_implementation_plan(company_name: str, opportunities: list) -> str:
    if not AI_AVAILABLE:
        return get_generic_implementation_plan(company_name)

    try:
        primary_opportunity = opportunities[0] if opportunities else "AI transformation"
        prompt = (
            f"Create a detailed 4-phase AI implementation roadmap for {company_name} "
            f"focused on: {primary_opportunity}"
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        logger.error(f"Implementation plan error: {e}")
        return get_generic_implementation_plan(company_name)


def get_default_ai_opportunities(company_name: str) -> list:
    return [
        f"Deploy AI-powered customer insights for {company_name}",
        f"Implement workflow automation for {company_name}",
        f"Build predictive analytics systems for {company_name}"
    ]


def get_generic_business_analysis(company_name: str) -> str:
    return (
        f"{company_name} operates in a competitive business environment where "
        f"efficiency, innovation, and customer experience are essential. "
        f"Strategic AI adoption can improve operations, optimize decision-making, "
        f"and unlock scalable growth opportunities."
    )


def get_generic_implementation_plan(company_name: str) -> str:
    return (
        f"Phase 1: Assess {company_name}'s current operational landscape and identify AI opportunities. "
        f"Phase 2: Launch pilot automation initiatives. "
        f"Phase 3: Scale successful AI implementations across departments. "
        f"Phase 4: Establish long-term AI governance and continuous optimization."
    )


def get_professional_fallback(lead) -> Dict[str, Any]:
    return {
        "company": lead.company,
        "website": lead.website,
        "prospect_name": lead.name,
        "company_info": extract_company_info(lead.company, lead.website),
        "business_analysis": get_generic_business_analysis(lead.company),
        "ai_opportunities": get_default_ai_opportunities(lead.company),
        "implementation_plan": get_generic_implementation_plan(lead.company)
    }