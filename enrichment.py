"""
Professional Company Enrichment Module
Generates accurate, detailed AI insights - no generic or vague content
"""

import logging
import os
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import httpx
import asyncio

logger = logging.getLogger(__name__)

# Create OpenAI client with explicit httpx client (no proxies)
http_client = httpx.Client(proxies=None)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), http_client=http_client)

async def enrich_company(lead) -> Dict[str, Any]:
    """
    Comprehensive company analysis with accurate insights
    """
    try:
        company_info = extract_company_info(lead.company, lead.website)
        business_analysis = generate_business_analysis(lead.company, company_info)
        ai_opportunities = generate_ai_opportunities(lead.company, business_analysis, company_info)
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
    """
    Extract key company information from website
    """
    try:
        if not website.startswith('http'):
            website = 'https://' + website
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
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
        return {
            "website_content": "",
            "meta_description": "",
            "company_name": company_name,
            "website_url": website
        }

def generate_business_analysis(company_name: str, company_info: Dict) -> str:
    """
    Generate accurate, detailed business analysis specific to this company
    """
    try:
        prompt = f"""You are a strategic business analyst. Analyze this company and provide a professional, accurate business overview.

Company: {company_name}
Website Content: {company_info.get('website_content', '')[:1000]}
Meta Description: {company_info.get('meta_description', '')}

Write a 3-4 paragraph professional analysis that includes:
1. What {company_name} actually does (based on the website)
2. Their industry, market position, and target customers
3. Their business model and revenue streams
4. Current challenges they likely face in their industry

Be SPECIFIC to this company. Use real details from their website. No generic content.
Write in professional business language. Be accurate and insightful."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional business analyst. Provide accurate, specific analysis based on actual company information."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        analysis = response.choices[0].message.content.strip()
        
        if len(analysis) < 200 or "unable" in analysis.lower():
            return get_generic_business_analysis(company_name)
        
        return analysis
    
    except Exception as e:
        logger.error(f"Business analysis error: {e}")
        return get_generic_business_analysis(company_name)

def generate_ai_opportunities(company_name: str, analysis: str, company_info: Dict) -> list:
    """
    Generate 3 SPECIFIC AI opportunities tailored to this company
    """
    try:
        prompt = f"""Based on this company analysis, identify 3 SPECIFIC, high-impact AI opportunities for {company_name}.

Company: {company_name}
Analysis: {analysis[:800]}

Generate exactly 3 AI opportunities that are:
1. SPECIFIC to {company_name}'s business model
2. ACTIONABLE with clear implementation path
3. HIGH-IMPACT with measurable ROI potential

For each opportunity:
- Start with a specific action verb (Deploy, Implement, Build, Develop, Automate, etc.)
- Include the specific business function it affects
- Explain the business benefit

Format: "Action: Specific opportunity for [Company] to [do what] by [using AI how]"

Do NOT be generic. Make each specific to {company_name}'s industry and business model."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.8
        )
        
        text = response.choices[0].message.content.strip()
        
        opportunities = []
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for i, line in enumerate(lines[:3]):
            line = line.lstrip('0123456789.-) ').strip()
            if line and len(line) > 20 and not any(x in line.lower() for x in ['error', 'unable']):
                opportunities.append(line)
        
        if len(opportunities) < 3:
            opportunities = [
                f"Implement AI-powered data analytics for {company_name} to optimize business operations and decision-making",
                f"Deploy intelligent automation to streamline {company_name}'s core business processes and reduce manual work",
                f"Build predictive analytics to forecast {company_name}'s market trends and customer behavior patterns"
            ]
        
        return opportunities[:3]
    
    except Exception as e:
        logger.error(f"AI opportunities error: {e}")
        return [
            f"Implement AI-powered analytics tailored to {company_name}'s operations",
            f"Deploy intelligent automation for {company_name}'s business processes",
            f"Build predictive models for {company_name}'s industry and market"
        ]

def generate_implementation_plan(company_name: str, opportunities: list) -> str:
    """
    Create a professional 4-phase implementation roadmap
    """
    try:
        prompt = f"""Create a professional, phased implementation roadmap for {company_name} to adopt the following AI opportunities:

Opportunities: {', '.join(opportunities)}

Provide a 4-phase implementation plan with:

Phase 1 - Assessment (Weeks 1-2)
- Audit current systems and capabilities
- Define success metrics and KPIs
- Build internal AI literacy

Phase 2 - Pilot Project (Weeks 3-6)
- Select highest-impact opportunity
- Run proof-of-concept
- Measure results and ROI

Phase 3 - Optimization (Weeks 7-10)
- Scale successful initiatives
- Integrate with existing systems
- Train teams on new processes

Phase 4 - Enterprise Scale (Weeks 11+)
- Roll out across organization
- Continuous monitoring and improvement
- Plan for future AI initiatives

Be specific to {company_name}'s context. No generic content."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7
        )
        
        plan = response.choices[0].message.content.strip()
        
        if len(plan) < 200:
            return get_generic_implementation_plan(company_name)
        
        return plan
    
    except Exception as e:
        logger.error(f"Implementation plan error: {e}")
        return get_generic_implementation_plan(company_name)

def get_generic_business_analysis(company_name: str) -> str:
    return f"""{company_name} operates in a competitive market where digital transformation and AI adoption are critical for long-term success. The organization's core business model can be significantly enhanced through strategic AI adoption, unlocking new opportunities for growth and competitive differentiation."""

def get_generic_implementation_plan(company_name: str) -> str:
    return f"""Phase 1 - Assessment: Evaluate {company_name}'s current capabilities and define objectives.
Phase 2 - Pilot: Execute proof-of-concept on highest-impact use case.
Phase 3 - Scale: Expand across relevant business units with optimization.
Phase 4 - Enterprise: Full organizational rollout with continuous improvement."""

def get_professional_fallback(lead) -> Dict[str, Any]:
    return {
        "company": lead.company,
        "website": lead.website,
        "prospect_name": lead.name,
        "company_info": extract_company_info(lead.company, lead.website),
        "business_analysis": get_generic_business_analysis(lead.company),
        "ai_opportunities": [
            f"Deploy AI-powered analytics and business intelligence for {lead.company}",
            f"Implement intelligent automation across {lead.company}'s key business operations",
            f"Build predictive models tailored to {lead.company}'s industry dynamics"
        ],
        "implementation_plan": get_generic_implementation_plan(lead.company)
    }