"""LiteLLM wrapper for AI calls. Supports OpenAI and Claude via model config."""

import json
import os

from litellm import completion

# Default model — override via AI_MODEL env var
# Examples: "gpt-4o-mini", "gpt-4o", "claude-sonnet-4-20250514"
DEFAULT_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")


def _call_llm(system_prompt: str, user_prompt: str, model: str | None = None) -> str:
    """Make a call to the LLM and return the text response."""
    response = completion(
        model=model or DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


def extract_company_info(raw_text: str, model: str | None = None) -> dict:
    """Extract structured company info from scraped text."""
    system_prompt = """You are a data extraction assistant. Extract structured company information from the provided website text.

Return ONLY valid JSON with this structure:
{
    "name": "Company Name",
    "website": "https://www.company.com",
    "description": "Brief company description",
    "industry": "Industry category",
    "country": "Country",
    "founded_year": 2020,
    "products": [
        {"name": "Product Name", "description": "Brief description"}
    ],
    "people": [
        {"name": "Person Name", "title": "Job Title", "email": "person@company.com", "linkedin_url": "https://linkedin.com/in/...", "role_type": "founder|cxo|board|manager"}
    ]
}

Rules:
- founded_year should be null if not found
- role_type must be one of: founder, cxo, board, manager
- Only include people whose names and titles are clearly stated
- For email and linkedin_url: only include if explicitly found in the text. Use null if not found. NEVER make up or guess emails.
- For website: extract the company's official website URL if mentioned. Use null if not found. Do NOT use the URL of the page being scraped — only the company's own domain.
- Keep descriptions concise (1-2 sentences)"""

    result = _call_llm(system_prompt, raw_text, model)

    # Strip markdown code fences if present
    result = result.strip()
    if result.startswith("```"):
        result = result.split("\n", 1)[1]
        result = result.rsplit("```", 1)[0]

    return json.loads(result)


def extract_companies_from_page(raw_text: str, model: str | None = None) -> list[dict]:
    """Extract multiple companies from a page (e.g. listicle, ranking article)."""
    system_prompt = """You are a data extraction assistant. The provided text is from a web page that may mention one or more companies. Extract ALL distinct companies mentioned.

Return ONLY valid JSON — an array of objects:
[
    {
        "name": "Company Name",
        "website": "https://www.company.com",
        "description": "Brief description (1-2 sentences)",
        "industry": "Industry category",
        "country": "Country"
    }
]

Rules:
- Extract every real company mentioned (not the article's own site)
- website: include the company's official website if mentioned or if it can be inferred from the source URL domain. Use null if truly unknown.
- Keep descriptions concise
- If no companies are found, return an empty array []
- Maximum 10 companies per page"""

    result = _call_llm(system_prompt, raw_text, model)

    result = result.strip()
    if result.startswith("```"):
        result = result.split("\n", 1)[1]
        result = result.rsplit("```", 1)[0]

    return json.loads(result)


def generate_pitch(
    company_info: str,
    person_name: str,
    person_title: str,
    user_product: str,
    model: str | None = None,
) -> str:
    """Generate a personalized sales pitch."""
    system_prompt = """You are an expert sales copywriter. Write a concise, personalized sales pitch email.

Rules:
- Keep it under 200 words
- Be professional but conversational
- Reference specific details about the target company
- Clearly explain the value proposition
- Include a clear call to action
- Don't be pushy or use cliché sales language"""

    user_prompt = f"""Write a pitch for:

Target company info:
{company_info}

Target person: {person_name} ({person_title})

Product/service being pitched:
{user_product}"""

    return _call_llm(system_prompt, user_prompt, model)


def recommend_targets(
    company_info: str,
    people_json: str,
    user_product: str,
    model: str | None = None,
) -> list[dict]:
    """Rank people at a company by how relevant they are for a pitch."""
    system_prompt = """You are a sales strategist. Given a company, its people, and a product being pitched, rank the people by how relevant they are as pitch targets.

Return ONLY valid JSON — an array of objects:
[
    {"name": "Person Name", "title": "Title", "score": 9, "reason": "Why they're a good target"}
]

Score from 1-10. Sort by score descending."""

    user_prompt = f"""Company info:
{company_info}

People at the company:
{people_json}

Product being pitched:
{user_product}"""

    result = _call_llm(system_prompt, user_prompt, model)

    result = result.strip()
    if result.startswith("```"):
        result = result.split("\n", 1)[1]
        result = result.rsplit("```", 1)[0]

    return json.loads(result)
