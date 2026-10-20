import html
import textwrap
from pathlib import Path


PROJECTS = [
    {
        "slug": "course-in-llms",
        "name": "Course-in-LLM-s",
        "description": [
            "Hands-on deep-learning coursework exploring the foundations",
            "behind large language models and modern AI systems.",
        ],
        "stack": ["Python", "Jupyter", "Deep Learning", "PyTorch"],
        "accent": "#A78BFA",
        "icon": """
            <circle cx="12" cy="7" r="3"/>
            <circle cx="5" cy="19" r="3"/>
            <circle cx="19" cy="19" r="3"/>
            <path d="M10.5 9.5 6.5 16.5M13.5 9.5l4 7M8 19h8"/>
        """,
    },
    {
        "slug": "enterprise-network-firewall",
        "name": "Enterprise Network Firewall",
        "description": [
            "Firewall simulation with protocol filtering, VLANs, ACLs,",
            "NAT, and core services for an enterprise network.",
        ],
        "stack": ["Python", "ACLs", "VLAN", "NAT"],
        "accent": "#22D3EE",
        "icon": """
            <path d="M12 3 21 7v5c0 5-3.8 8.2-9 10-5.2-1.8-9-5-9-10V7l9-4Z"/>
            <path d="m8.5 12 2.3 2.3 4.8-5"/>
        """,
    },
    {
        "slug": "code-plagiarism-detector",
        "name": "Code Plagiarism Detector",
        "description": [
            "Compares C++ source using rolling hashes, tries, and graph",
            "similarity to identify shared code patterns.",
        ],
        "stack": ["C++", "Rolling Hash", "Trie", "Graph Similarity"],
        "accent": "#F472B6",
        "icon": """
            <path d="m8 7-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>
        """,
    },
    {
        "slug": "tale-treasury",
        "name": "Tale-Treasury",
        "description": [
            "An interactive story world with branching tales, reader",
            "accounts, and collectible trophies.",
        ],
        "stack": ["React", "Vite", "Node.js", "Express", "MongoDB", "Groq"],
        "accent": "#FBBF24",
        "icon": """
            <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v17H6.5A2.5 2.5 0 0 1 4 17.5v-12Z"/>
            <path d="M4 6h13M8 10h8M8 13h6M8 16h5"/>
            <path d="m19 3 1 2 2 .3-1.5 1.4.4 2-1.9-1-1.9 1 .4-2L17 5.3l2-.3 1-2Z" transform="translate(-2 1) scale(.8)"/>
        """,
    },
    {
        "slug": "studyflow-ai",
        "name": "StudyFlow AI",
        "description": [
            "A student companion with an AI tutor, quiz generator,",
            "smart study planner, notes, and focus tools.",
        ],
        "stack": ["React", "Express", "MongoDB", "Gemini AI"],
        "accent": "#34D399",
        "icon": """
            <path d="m3 8 9-5 9 5-9 5-9-5Z"/>
            <path d="M6 10v6c3.5 3 8.5 3 12 0v-6M21 8v7"/>
            <circle cx="21" cy="17" r="1.5"/>
        """,
    },
    {
        "slug": "phishing-email-detection",
        "name": "Phishing Email Detection",
        "description": [
            "Email threat detection experiments using text processing,",
            "classical machine learning, and deep-learning models.",
        ],
        "stack": ["Python", "TensorFlow", "Scikit-learn", "NLP"],
        "accent": "#FB7185",
        "icon": """
            <rect x="3" y="5" width="18" height="14" rx="2"/>
            <path d="m4 7 8 6 8-6M16.5 16.5l2 2 3.5-4"/>
        """,
    },
]


def render_card(project, index):
    name = html.escape(project["name"])
    title = html.escape(project["name"])
    description = [html.escape(line) for line in project["description"]]
    accent = project["accent"]
    chips = []
    chip_x = 28
    chip_y = 176

    for label in project["stack"]:
        label = html.escape(label)
        chip_width = max(54, len(label) * 7 + 24)
        if chip_x + chip_width > 612:
            chip_x = 28
            chip_y += 32
        chips.append(
            f'<g><rect x="{chip_x}" y="{chip_y}" width="{chip_width}" height="24" rx="12" fill="#202938" stroke="#364152"/>'
            f'<circle cx="{chip_x + 12}" cy="{chip_y + 12}" r="3" fill="{accent}"/>'
            f'<text x="{chip_x + 21}" y="{chip_y + 16}" class="tag">{label}</text></g>'
        )
        chip_x += chip_width + 8

    icon = textwrap.dedent(project["icon"]).strip()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="280" viewBox="0 0 640 280" role="img" aria-labelledby="title description">
  <title id="title">{title} project card</title>
  <desc id="description">{description[0]} {description[1]}</desc>
  <defs>
    <linearGradient id="surface" x1="0" y1="0" x2="640" y2="280" gradientUnits="userSpaceOnUse">
      <stop stop-color="#151D2B"/>
      <stop offset="1" stop-color="#101722"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="640" y2="280" gradientUnits="userSpaceOnUse">
      <stop stop-color="{accent}" stop-opacity=".72"/>
      <stop offset="1" stop-color="#334155" stop-opacity=".7"/>
    </linearGradient>
    <style>
      .title {{ fill: #F1F5F9; font: 600 19px 'Segoe UI', Arial, sans-serif; }}
      .copy {{ fill: #AAB7C8; font: 13px 'Segoe UI', Arial, sans-serif; }}
      .tag {{ fill: #D8E1EC; font: 11px 'Segoe UI', Arial, sans-serif; }}
      .meta {{ fill: #78879A; font: 10px 'Segoe UI', Arial, sans-serif; letter-spacing: 1.4px; }}
      .action {{ fill: {accent}; font: 600 11px 'Segoe UI', Arial, sans-serif; letter-spacing: 1px; }}
      .card-surface {{ transition: stroke .2s ease, fill .2s ease; }}
      svg:hover .card-surface {{ stroke: {accent}; }}
    </style>
  </defs>
  <rect class="card-surface" x="1" y="1" width="638" height="278" rx="18" fill="url(#surface)" stroke="url(#edge)" stroke-width="1.5"/>
  <path d="M520 1h100a18 18 0 0 1 18 18v92c-45-13-88-44-118-110Z" fill="{accent}" opacity=".055"/>
  <rect x="24" y="24" width="48" height="48" rx="14" fill="{accent}" fill-opacity=".12" stroke="{accent}" stroke-opacity=".35"/>
  <g transform="translate(36 36)" fill="none" stroke="{accent}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
    {icon}
  </g>
  <text x="90" y="35" class="meta">SELECTED PROJECT  /  {index:02d}</text>
  <text x="90" y="61" class="title">{name}</text>
  <path d="M28 91h584" stroke="#263244"/>
  <text x="28" y="119" class="copy">{description[0]}</text>
  <text x="28" y="140" class="copy">{description[1]}</text>
  <text x="28" y="163" class="meta">TECH STACK</text>
  {"".join(chips)}
  <path d="M28 235h584" stroke="#263244"/>
  <text x="28" y="258" class="action">OPEN REPOSITORY</text>
  <path d="M151 254h22m-7-7 7 7-7 7" fill="none" stroke="{accent}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="603" cy="253" r="3" fill="{accent}" opacity=".8"/>
</svg>
"""


def generate_project_cards(output_dir="assets/project-cards"):
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)

    for index, project in enumerate(PROJECTS, start=1):
        output_file = directory / f'{project["slug"]}.svg'
        output_file.write_text(render_card(project, index), encoding="utf-8")
        print(f"Project card created: {output_file}")


if __name__ == "__main__":
    generate_project_cards()
