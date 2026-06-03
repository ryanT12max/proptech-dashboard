from http.server import BaseHTTPRequestHandler
import json
import oracledb
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Securely locate the local wallet folder
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
            
            # Pull the intelligence feed from the database
            cursor.execute("""
                SELECT PROPERTY_ADDRESS, LIST_PRICE, LISTING_DESC, THREAT_SCORE, RISK_CLASSIFICATION, AI_ANALYSIS 
                FROM PROPTECH_THREATS 
                ORDER BY THREAT_SCORE DESC
            """)
            
            rows = cursor.fetchall()
            feed_data = []
            
            # Format the data into JSON for the frontend dashboard
            for row in rows:
                feed_data.append({
                    "address": str(row[0]),
                    "price": row[1],
                    "description": str(row[2]),
                    "threat_score": row[3],
                    "risk_classification": str(row[4]),
                    "ai_analysis": str(row[5])
                })
                
            cursor.close()
            connection.close()
            
            # Send the JSON payload securely to the frontend
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') # Ensures the browser doesn't block the data
            self.end_headers()
            self.wfile.write(json.dumps(feed_data).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))