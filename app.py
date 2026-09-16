from flask import Flask, render_template_string, request
from src.guardrail import evaluate

app = Flask(__name__)
PAGE = r'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Security Gateway Demo</title><style>
:root{font-family:Inter,system-ui,Arial,sans-serif}body{margin:0;background:#f4f7fb;color:#14213d}.wrap{max-width:860px;margin:48px auto;padding:0 20px}.card{background:#fff;border:1px solid #dbe3ef;border-radius:16px;padding:28px;box-shadow:0 8px 30px #102a4312}h1{margin:0 0 8px;font-size:32px}.sub{color:#52657a;margin-bottom:24px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}label{display:block;font-weight:700;margin:12px 0 6px}textarea,select{box-sizing:border-box;width:100%;padding:12px;border:1px solid #b8c6d9;border-radius:9px;background:#fff;font:inherit}textarea{min-height:180px}button{margin-top:16px;padding:12px 20px;border:0;border-radius:9px;background:#1261a0;color:white;font-weight:700;cursor:pointer}.result{margin-top:22px;padding:18px;border-radius:12px;background:#f7f9fc;border:1px solid #dbe3ef}.badge{display:inline-block;padding:6px 10px;border-radius:999px;background:#e8eef7;font-weight:800}.note{font-size:13px;color:#66788a;margin-top:18px}@media(max-width:650px){.grid{grid-template-columns:1fr}}
</style></head><body><div class="wrap"><div class="card"><h1>AI Security Gateway</h1><div class="sub">Think before you share — reference demo for approved tools, data checks, human review and audit decisions.</div><form method="post"><div class="grid"><div><label>AI tool</label><select name="tool"><option>company-chat-ai</option><option>public-ai-demo</option><option>unapproved-ai</option></select></div><div><label>Data classification</label><select name="data_class"><option>public</option><option>internal</option><option>customer</option><option>confidential</option></select></div></div><label>Text you plan to share</label><textarea name="text" required placeholder="Use synthetic demo text only — never paste real secrets or confidential data.">{{ text }}</textarea><button>Check Before Sharing</button></form>{% if result %}<div class="result"><span class="badge">{{ result.decision }}</span><p>{{ result.reason }}</p><p><b>Finding categories:</b> {{ result.findings|join(', ') if result.findings else 'None' }}</p></div>{% endif %}<div class="note">Educational starter kit only. An ALLOW result is not a guarantee that content is safe.</div></div></div></body></html>'''

@app.route("/", methods=["GET", "POST"])
def home():
    result, text = None, ""
    if request.method == "POST":
        text = request.form["text"]
        result = evaluate(request.form["tool"], text, request.form["data_class"])
    return render_template_string(PAGE, result=result, text=text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
