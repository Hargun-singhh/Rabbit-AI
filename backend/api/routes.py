import io
import pandas as pd
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Optional
import json

from api.schemas import AnalysisResponse, HealthCheckResponse
from services.analysis_service import analyze_dataframe
from services.ai_service import generate_ai_summary
from services.email_service import send_report_email
from core.config import settings

router = APIRouter()

ALLOWED_MIMETYPES = [
    "text/csv", 
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel"
]

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(status="ok", version=settings.VERSION)

@router.post("/analyze", response_model=AnalysisResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
    email: Optional[str] = Form(None)
):
    # Validate file type
    if file.content_type not in ALLOWED_MIMETYPES:
        if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only CSV and XLSX are allowed."
            )
            
    try:
        content = await file.read()
        
        # Validate size (convert MAX_UPLOAD_SIZE_MB to bytes)
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if len(content) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum allowed size is {settings.MAX_UPLOAD_SIZE_MB}MB."
            )
            
        # Parse data
        if file.filename.endswith('.csv') or file.content_type == "text/csv":
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error parsing file: {str(e)}"
        )
        
    # Analysis Step
    try:
        analysis_results = analyze_dataframe(df)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during data analysis: {str(e)}"
        )
        
    # AI Summary Step
    ai_summary = None
    if settings.ENABLE_AI_SUMMARY:
        ai_summary = generate_ai_summary(analysis_results)
        
    # Email Step
    email_sent = False
    if email:
        subject = f"AI Data Analysis Report: {file.filename}"
        
        report_lines = [
            f"Here is your automated report for {file.filename}.",
            "",
            "📊 Data Summary:",
            json.dumps(analysis_results['summary'], indent=2),
            "",
            "🤖 AI Summary:",
            ai_summary if ai_summary else "N/A"
        ]
        
        body = "\n".join(report_lines)
        email_sent = send_report_email(to_email=email, subject=subject, body=body)

    return AnalysisResponse(
        filename=file.filename,
        content_type=file.content_type,
        analysis=analysis_results,
        ai_summary=ai_summary,
        email_sent=email_sent if email else None
    )
