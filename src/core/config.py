"""
VayuRakshak AI - Configuration & Environment Constants
Author: Bhomesh Razdan (Lead Architect)
"""

import os

class Settings:
    PROJECT_NAME: str = "VayuRakshak AI"
    VERSION: str = "1.0.0"
    HACKATHON_EVENT: str = "Bharat Builds Tour: Environmental Hacks (WeMakeDevs x AWS)"
    LEAD_ARCHITECT: str = "Bhomesh Razdan"
    
    # AWS Settings
    AWS_REGION: str = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")
    DYNAMODB_TABLE_AQI: str = os.getenv("DYNAMODB_TABLE_AQI", "VayuRakshak-AQI-Telemetry")
    DYNAMODB_TABLE_FIRES: str = os.getenv("DYNAMODB_TABLE_FIRES", "VayuRakshak-Stubble-Fires")
    SNS_ALERT_TOPIC_ARN: str = os.getenv("SNS_ALERT_TOPIC_ARN", "arn:aws:sns:ap-south-1:123456789012:VayuRakshak-Alerts")
    OPENSEARCH_ENDPOINT: str = os.getenv("OPENSEARCH_ENDPOINT", "https://search-vayurakshak-domain.ap-south-1.es.amazonaws.com")
    
    # LocalStack / Development Flags
    USE_LOCALSTACK: bool = os.getenv("USE_LOCALSTACK", "true").lower() == "true"
    LOCALSTACK_ENDPOINT: str = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
    
    # Default Coordinates (Delhi NCR Center - DTU Hackathon build venue)
    DTU_COORDINATES = {"lat": 28.7499, "lon": 77.1170, "name": "Delhi Technological University (DTU)"}
    DELHI_CENTER = {"lat": 28.6139, "lon": 77.2090, "name": "Central Delhi"}

settings = Settings()
