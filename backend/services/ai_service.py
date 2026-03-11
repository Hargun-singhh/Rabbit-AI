import json
import logging
from typing import Dict, Any
import google.generativeai as genai
from core.config import settings

logger = logging.getLogger(__name__)

def generate_ai_summary(analysis_results: Dict[str, Any]) -> str:
    """
    Generates a natural language summary of the analysis results using Gemini API.
    """

    if not settings.ENABLE_AI_SUMMARY:
        return "AI summary generation is disabled."

    if not settings.GEMINI_API_KEY:
        logger.warning("Gemini API key not found. Skipping AI summary.")
        return "AI summary could not be generated: Missing API key."

    try:
        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Use faster model to avoid Render timeout
        model = genai.GenerativeModel("gemini-flash-latest")

        prompt = f"""
You are an expert data analyst giving an executive briefing.

Based on the following statistical summary of a dataset, produce a crisp and professional analysis.

Formatting rules:
- Use Markdown
- Use headings (###)
- Use short bullet points
- Keep it concise and executive-friendly

Dataset Analysis:
{json.dumps(analysis_results, indent=2)}
"""

        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 150,
                "temperature": 0.4
            }
        )

        return response.text

    except Exception as e:
        logger.error(f"Error generating AI summary: {str(e)}")

        # Fallback so UI never breaks
        return "⚠️ AI summary unavailable due to API timeout. Statistical insights are still shown above."


