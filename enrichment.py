"""
Professional Company Enrichment Module
"""

import logging
import os
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup
import time

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.0-flash")
    GEMINI_AVAILABLE = True
except Exception as e:
    logger.warning(f"Gemini initialization failed: {e}")
    GEMINI_AVAILABLE = False

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
        if not website.startswith('http'):
            website = 'https://' + website
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(website, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(['script', 'style']):
            script.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        meta_desc = ""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta:
            meta_desc = meta.get('content', '')
        
        return {
            "website_content": text[:2000],
            "meta_description": meta_desc,
            "company_name": company_name,
            "website_url": website
        }
    except Exception as e:
        logger.warning(f"Website extraction error: {e}")
        return {"website_content": "", "meta_description": "", "company_name": company_name, "website_url": website}

def generate_business_analysis(company_name: str, company_info: Dict) -> str:
    if not GEMINI_AVAILABLE:
        return get_generic_business_analysis(company_name)
    
    try:
        prompt = f"Analyze {company_name}. Website: {company_info.get('website_content', '')[:500]}. Write 3 paragraphs about their business, industry, and challenges."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Business analysis error: {e}")
        return get_generic_business_analysis(company_name)

def generate_ai_opportunities(company_name: str, analysis: str) -> list:
    if not GEMINI_AVAILABLE:
        return [
            f"Deploy AI analytics for {company_name}",
            f"Implement automation for {company_name}",
            f"Build predictive models for {company_name}"
        ]
    
    try:
        prompt = f"List 3 specific AI opportunities for {company_name}. Analysis: {analysis[:400]}"
        response = model.generate_content(prompt)
        text = response.text.strip()
        opportunities = [line.strip() for line in text.split('\n') if line.strip()][:3]
        
        if len(opportunities) < 3:
            return [
                f"Deploy AI analytics for {company_name}",
                f"Implement automation for {company_name}",
                f"Build predictive models for {company_name}"
            ]
        return opportunities
    except Exception as e:
        logger.error(f"AI opportunities error: {e}")
        return [
            f"Deploy AI analytics for {company_name}",
            f"Implement automation for {company_name}",
            f"Build predictive models for {company_name}"
        ]

def generate_implementation_plan(company_name: str, opportunities: list) -> str:
    if not GEMINI_AVAILABLE:
        return get_generic_implementation_plan(company_name)
    
    try:
        prompt = f"Create 4-phase implementation roadmap for {company_name}: {opportunities[0] if opportunities else 'AI adoption'}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Implementation plan error: {e}")
        return get_generic_implementation_plan(company_name)

def get_generic_business_analysis(company_name: str) -> str:
    return f"{company_name} is a company operating in a competitive market. They face challenges with operational efficiency, data management, and customer engagement. Strategic AI adoption can help them improve decision-making and create competitive advantages."

def get_generic_implementation_plan(company_name: str) -> str:
    return f"Phase 1: Assessment of {company_name}'s current capabilities. Phase 2: Pilot project on highest-impact use case. Phase 3: Scale successful initiatives. Phase 4: Enterprise rollout with continuous improvement."

def get_professional_fallback(lead) -> Dict[str, Any]:
    return {
        "company": lead.company,
        "website": lead.website,
        "prospect_name": lead.name,
        "company_info": extract_company_info(lead.company, lead.website),
        "business_analysis": get_generic_business_analysis(lead.company),
        "ai_opportunities": [
            f"Deploy AI for {lead.company}",
            f"Implement automation for {lead.company}",
            f"Build analytics for {lead.company}"
        ],
        "implementation_plan": get_generic_implementation_plan(lead.company)
    }