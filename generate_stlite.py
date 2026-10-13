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
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/browser@0.74.0/build/stlite.css" />
  <style>
    body {{
      margin: 0;
      background-color: #F4F7FB;
    }}
  </style>
</head>
<body>
  <div id="root"></div>
  <script src="https://cdn.jsdelivr.net/npm/@stlite/browser@0.74.0/build/stlite.js"></script>
  <script>
    const appFiles = {json_data};
    stlite.mount({{
      requirements: ["scikit-fuzzy", "scikit-learn", "matplotlib", "pandas", "numpy"],
      entrypoint: "app.py",
      files: appFiles
    }}, document.getElementById("root"));
  </script>
</body>
</html>
"""

Path("index.html").write_text(html_content, encoding="utf-8")
print("index.html generated successfully!")
