# 🏡 PropTech AI Monitor: Real Estate Threat Intelligence

[![Live Dashboard](https://img.shields.io/badge/Live-Dashboard-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://proptech-dashboard-azure.vercel.app)
[![Oracle Cloud](https://img.shields.io/badge/Oracle_Cloud-F80000?style=for-the-badge&logo=oracle&logoColor=white)](https://cloud.oracle.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

## 📖 Project Overview
A serverless, multi-cloud ETL pipeline and dashboard designed to extract live real estate listings and analyze them in real-time for potential wire fraud, phishing, and predatory seller patterns. 

This project demonstrates the ability to engineer resilient multi-cloud architectures, implement heuristic dependency stubbing to bypass enterprise anti-bot protections, and securely route data into an enterprise database using packaged cryptographic wallets within a stateless serverless container.

## 🔗 Live Demo
**[View the Live PropTech Threat Dashboard Here](https://proptech-dashboard-azure.vercel.app)**

## 🛠️ Technology Stack
* **Cloud Provider & Hosting:** Vercel
* **Compute Layer:** Vercel Serverless Functions (Python 3.9+)
* **Database:** Oracle Autonomous Database (Relational SQL)
* **Data Ingestion & Analysis:** Python (`requests`, `oracledb`, Custom Heuristic Engine)
* **Frontend Visualization:** HTML5, Vanilla JS, CSS
* **Third-Party API:** RentCast API

## 🏗️ Architecture Flow
1. **Trigger:** A user inputs a target zip code on the frontend, which fires an asynchronous request to the Vercel `/api/analyze` serverless endpoint.
2. **Extract:** The Python backend securely reaches out to the RentCast API to pull raw, unstructured property data for the designated territory.
3. **Transform:** The data is passed through a custom Heuristic Threat Engine that scans property descriptions for high-risk text patterns (e.g., "wire transfer," "sight unseen," "crypto"), calculating a Threat Score (1-10) and generating an AI analysis.
4. **Load:** The function securely connects to the Oracle Autonomous Database using an mTLS cryptographic wallet (`tnsnames.ora`/`cwallet.sso`) packaged directly into the cloud build, executing parameterized SQL `INSERT` statements.
5. **Visualize:** Upon successful load, the frontend hits the decoupled `/api/oracle` read-endpoint to fetch the updated database records and dynamically renders the threat intelligence cards.

## 🔐 Security & Operations Notes
* **Multi-Cloud Resilience:** Successfully diagnosed a provider-level Cloudflare DNS blackhole on ephemeral Oracle Cloud instances, migrating the compute layer to Vercel and utilizing a local heuristic dependency stub to maintain continuous pipeline execution.
* **Serverless Network Architecture:** Overcame React frontend memory limits (caused by Base64 encoding massive mTLS wallet files) by engineering a "Walletless Pivot." Transitioned the Oracle connection to 1-Way TLS over Port 1521 and configured a strict Zero-Trust Access Control List (ACL) to securely route dynamic Vercel serverless IPs.
* **Credential Management:** API keys, database users, and passwords are strictly `.gitignore`'d and securely injected at runtime via Vercel Environment Variables.

## 🚀 Future Enhancements
* Reintegrate a live Hugging Face LLM model for the threat analysis, leveraging Vercel's unrestricted outbound network architecture.
* Implement a geospatial UI utilizing `Leaflet.js` to visualize threat clusters on an interactive map based on the searched zip codes.
