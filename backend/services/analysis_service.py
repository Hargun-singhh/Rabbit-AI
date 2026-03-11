import os
import pandas as pd
from typing import Dict, Any

def analyze_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes basic analytics on a uploaded pandas DataFrame.
    """
    
    row_count = len(df)
    col_count = len(df.columns)
    
    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    analysis = {
        "summary": {
            "total_rows": row_count,
            "total_columns": col_count,
        },
        "numeric_metrics": {},
        "categorical_metrics": {}
    }
    
    # Compute aggregations for numeric columns
    for col in numeric_cols:
        col_data = df[col].dropna()
        if not col_data.empty:
            analysis["numeric_metrics"][col] = {
                "sum": float(col_data.sum()),
                "mean": float(col_data.mean()),
                "median": float(col_data.median()),
                "min": float(col_data.min()),
                "max": float(col_data.max()),
                "std_dev": float(col_data.std()) if len(col_data) > 1 else 0.0
            }
            
    # Compute top categories for categorical columns
    for col in categorical_cols:
        col_data = df[col].dropna()
        if not col_data.empty:
            top_values = col_data.value_counts().head(5).to_dict()
            analysis["categorical_metrics"][col] = {
                "unique_values_count": int(col_data.nunique()),
                "top_5_values": {str(k): int(v) for k, v in top_values.items()}
            }
            
    return analysis
