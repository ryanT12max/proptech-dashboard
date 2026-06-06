from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import requests
import oracledb
import os

# 1. EXTRACT
def get_property_data(zip_code):
    # The zip code is now dynamically inserted into the URL
    url = f"https://api.rentcast.io/v1/listings/sale?zipCode={zip_code}&limit=5"
    headers = {
        "accept": "application/json",
        "X-Api-Key": os.environ.get('RENTCAST_API_KEY')
    }
    resp = requests.get(url, headers=headers)
    return resp.json()

# 2. TRANSFORM (Using your successful Dependency Stub)
def analyze_threat(listing):
    description = listing.get('description', 'No description provided.').lower()
    high_risk_keywords = ['wire transfer', 'cash only', 'urgent', 'sight unseen', 'crypto']
    medium_risk_keywords = ['investor special', 'as is', 'quick close', 'motivated']
    
    threat_score = 1
    risk_classification = "Low"
    ai_analysis = "Standard real estate language. No obvious fraud indicators detected."
    
    for word in high_risk_keywords:
        if word in description:
            threat_score = 9
            risk_classification = "High"
            ai_analysis = f"Suspicious phrasing detected ('{word}'). Potential wire fraud or phishing."
            return threat_score, risk_classification, ai_analysis
            
    for word in medium_risk_keywords:
        if word in description:
            threat_score = 5
            risk_classification = "Medium"
            ai_analysis = f"Seller urgency detected ('{word}'). Recommend standard verification."
            return threat_score, risk_classification, ai_analysis
            
    return threat_score, risk_classification, ai_analysis

# 3. LOAD
def load_data_to_oracle(listings):
    # This automatically finds your wallet folder relative to this script
    wallet_path = os.path.join(os.path.dirname(__file__), 'wallet')
    
    connection = oracledb.connect(
        user="ADMIN",
        password="0n@stR8l1n3U",
        dsn="AviationDB_high", 
        config_dir=wallet_path,
        wallet_location=wallet_path,
        wallet_password="Tij79268*"
    )
    
    cursor = connection.cursor()
    sql = """INSERT INTO PROPTECH_THREATS 
             (PROPERTY_ADDRESS, LIST_PRICE, LISTING_DESC, THREAT_SCORE, RISK_CLASSIFICATION, AI_ANALYSIS) 
             VALUES (:1, :2, :3, :4, :5, :6)"""
             
    for item in listings:
        address = item.get('formattedAddress', 'Unknown')
        price = item.get('price', 0)
        description = item.get('description', 'No description provided.')
        
        threat_score, risk_classification, ai_analysis = analyze_threat(item)
        cursor.execute(sql, [address, price, description, threat_score, risk_classification, ai_analysis])
        
    connection.commit()
    cursor.close()
    connection.close()

# 4. VERCEL SERVERLESS HANDLER
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Extract the zip code from the Vercel API URL
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            zip_code = query_params.get('zipCode', ['77063'])[0]
            
            # Run the pipeline
            listings = get_property_data(zip_code)
            if listings:
                load_data_to_oracle(listings)
            
            # Send Success Response to Frontend
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "Pipeline Executed Successfully", "zip": zip_code}).encode('utf-8'))
            
        except Exception as e:
            # Send Error Response
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))