import os
import base64

path = 'api/wallet/ewallet.pem'
folder = 'api/wallet'

if os.path.exists(path):
    with open(path, 'rb') as f:
        print("\nSUCCESS! --- COPY THE TEXT BELOW ---")
        print(base64.b64encode(f.read()).decode('utf-8'))
        print("--- END OF TEXT ---\n")
elif os.path.exists(folder):
    print("\nERROR: ewallet.pem does not exist in the folder.")
    print("Here are the files you DO have:")
    for file in os.listdir(folder):
        print(f"- {file}")
else:
    print("\nERROR: The api/wallet folder cannot be found at all.")