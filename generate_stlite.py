import json
from pathlib import Path

files_to_embed = [
    'app.py',
    'style.css',
    'rules.pl',
    'modules/__init__.py',
    'modules/agent_rules.py',
    'modules/navigator.py',
    'modules/game_zone.py',
    'modules/comfort.py',
    'modules/insights.py'
]

file_dict = {}
for f in files_to_embed:
    p = Path(f)
    if p.exists():
        file_dict[f] = p.read_text(encoding='utf-8')

json_data = json.dumps(file_dict)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <title>CampusMind - AI Student Dashboard</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/browser@0.85.1/build/stlite.css" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎓</text></svg>">
  <style>
    body {{
      margin: 0;
      background-color: #F4F7FB;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    #loading-screen {{
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: #F4F7FB;
      z-index: 9999;
      transition: opacity 0.4s ease;
    }}
    .loading-card {{
      background: #FFFFFF;
      padding: 2.2rem 2.8rem;
      border-radius: 16px;
      box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
      border: 1px solid #E2E8F0;
      text-align: center;
      max-width: 440px;
      width: 90%;
    }}
    .loading-icon {{
      font-size: 3rem;
      margin-bottom: 0.5rem;
      animation: bounce 1.8s infinite ease-in-out;
    }}
    @keyframes bounce {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-8px); }}
    }}
    .loading-title {{
      font-size: 1.5rem;
      font-weight: 700;
      color: #1E293B;
      margin-bottom: 0.25rem;
    }}
    .loading-subtitle {{
      font-size: 0.88rem;
      color: #64748B;
      margin-bottom: 1.5rem;
    }}
    .progress-bar-container {{
      width: 100%;
      height: 6px;
      background: #EEF2FF;
      border-radius: 999px;
      overflow: hidden;
      margin-bottom: 1rem;
    }}
    .progress-bar-fill {{
      height: 100%;
      width: 40%;
      background: linear-gradient(90deg, #4F46E5, #14B8A6);
      border-radius: 999px;
      animation: indeterminate 1.8s infinite ease-in-out;
    }}
    @keyframes indeterminate {{
      0% {{ transform: translateX(-100%); width: 30%; }}
      50% {{ transform: translateX(50%); width: 60%; }}
      100% {{ transform: translateX(300%); width: 30%; }}
    }}
    .loading-status {{
      font-size: 0.82rem;
      color: #4F46E5;
      font-weight: 600;
      min-height: 1.2rem;
    }}
    .loading-note {{
      font-size: 0.75rem;
      color: #94A3B8;
      margin-top: 0.6rem;
      line-height: 1.4;
    }}
  </style>
</head>
<body>
  <div id="loading-screen">
    <div class="loading-card">
      <div class="loading-icon">🎓</div>
      <div class="loading-title">CampusMind</div>
      <div class="loading-subtitle">AI Academic Student Dashboard</div>
      <div class="progress-bar-container">
        <div class="progress-bar-fill"></div>
      </div>
      <div id="loading-status" class="loading-status">Bootstrapping Python WebAssembly...</div>
      <div class="loading-note">Initializing Pyodide &amp; AI packages (NumPy, SciPy, Scikit-Learn, Fuzzy Control).</div>
    </div>
  </div>

  <div id="root"></div>

  <script type="module">
    import {{ mount }} from "https://cdn.jsdelivr.net/npm/@stlite/browser@0.85.1/build/stlite.js";

    const statusEl = document.getElementById("loading-status");
    const loaderEl = document.getElementById("loading-screen");

    const appFiles = {json_data};

    try {{
      if (statusEl) statusEl.innerText = "Loading AI models & Streamlit runtime...";

      mount({{
        requirements: ["scikit-fuzzy", "scikit-learn", "matplotlib", "pandas", "numpy", "scipy"],
        entrypoint: "app.py",
        files: appFiles
      }}, document.getElementById("root"));

      // Fade out loading screen once stlite mounts
      const observer = new MutationObserver((mutations, obs) => {{
        const root = document.getElementById("root");
        if (root && root.children.length > 0 && root.querySelector("[class*='stApp']")) {{
          if (loaderEl) {{
            loaderEl.style.opacity = "0";
            setTimeout(() => loaderEl.remove(), 400);
          }}
          obs.disconnect();
        }}
      }});
      observer.observe(document.getElementById("root"), {{ childList: true, subtree: true }});

      // Safety timeout to dismiss loading card if observer misses class
      setTimeout(() => {{
        if (loaderEl) {{
          loaderEl.style.opacity = "0";
          setTimeout(() => loaderEl.remove(), 400);
        }}
      }}, 12000);

    }} catch (err) {{
      console.error("Stlite mount error:", err);
      if (statusEl) {{
        statusEl.innerText = "Load failed: " + (err.message || err);
        statusEl.style.color = "#DC2626";
      }}
    }}
  </script>
</body>
</html>
"""

Path("index.html").write_text(html_content, encoding="utf-8")
print("index.html with modern ES module and branded loading screen generated successfully!")
