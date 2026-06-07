from http.server import BaseHTTPRequestHandler
import json
import oracledb
import os
import base64

class handler(BaseHTTPRequestHandler):
def do_GET(self):
        try:
            # 1. Rebuild the wallet inside the cloud's temporary storage
            wallet_path = '/tmp/wallet'
            os.makedirs(wallet_path, exist_ok=True)
            wallet_file = os.path.join(wallet_path, 'cwallet.sso')
            
            # Only decode and write the file if it hasn't been created in this container yet
            if not os.path.exists(wallet_file):
                wallet_data = os.environ.get('WALLET_BASE64')
                with open(wallet_file, 'wb') as f:
                    f.write(base64.b64decode(wallet_data))
            
            # 2. Connect using the rebuilt file and full DSN string
            connection = oracledb.connect(
                user=os.environ.get('ORACLE_DB_USER', 'ADMIN'),
                password=os.environ.get('ORACLE_DB_PASSWORD'),
                dsn=os.environ.get('ORACLE_DSN'), 
                config_dir=wallet_path,
                wallet_location=wallet_path,
                wallet_password=os.environ.get('WALLET_PASSWORD')
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