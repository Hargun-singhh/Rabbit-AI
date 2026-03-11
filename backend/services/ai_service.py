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
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-flash-latest')
        
        
        # We only send aggregated logic to the AI, NEVER the raw row data
        prompt = f"""
        You are an expert data analyst giving an executive briefing. Based on the following statistical summary of a dataset, provide a highly crisp, professional natural language summary of the key findings.
        
        CRITICAL INSTRUCTIONS for formatting:
        1. Keep the insights very concise and actionable.
        2. Format the response entirely in beautiful Markdown.
        3. Use Markdown headings (e.g. ###) for distinct sections.
        4. Use short bullet points for the metrics and trends.
        5. DO NOT write long paragraphs. Make it easy to read at a glance.

        Dataset Aggregated Analysis (JSON structure):
        {json.dumps(analysis_results, indent=2)}
        """
        
        response = model.generate_content(
    prompt,
    generation_config={"max_output_tokens": 200}
)
        return response.text
    except Exception as e:
        logger.error(f"Error generating AI summary: {str(e)}")
        return "An error occurred while generating the AI summary."
