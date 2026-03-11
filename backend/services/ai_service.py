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
        model = genai.GenerativeModel('gemini-pro')
        
        # We only send aggregated logic to the AI, NEVER the raw row data
        prompt = f"""
        You are an expert data analyst. Based on the following statistical summary of a dataset, provide a concise, insightful natural language summary of the key findings. 
        Highlight any interesting trends, dominant categories, or notable metrics.
        Keep the response professional, clear, and easy to read.

        Dataset Aggregated Analysis (JSON structure):
        {json.dumps(analysis_results, indent=2)}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating AI summary: {str(e)}")
        return "An error occurred while generating the AI summary."
