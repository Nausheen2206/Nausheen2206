import json
from pathlib import Path


DATA = {
    "proficiencies": {
        "AI/ML": {
            "level": 90,
            "skills": ["LLMs", "Deep Learning", "NLP", "PyTorch", "TensorFlow"]
        },
        "Systems": {
            "level": 85,
            "skills": ["C/C++", "Networking", "Algorithms", "Data Structures", "OS"]
        },
        "Web Dev": {
            "level": 76,
            "skills": ["React", "Node.js", "Full Stack", "Databases", "APIs"]
        },
        "Algorithms": {
            "level": 92,
            "skills": ["Graph Theory", "DP", "Sorting", "Search", "Optimization"]
        },
        "Databases": {
            "level": 82,
            "skills": ["SQL", "PostgreSQL", "MongoDB", "Redis", "Query Optimization"]
        }
    }
}


def make_radar_svg(data=DATA, output_file="assets/skills-radar.svg"):
    categories = list(data["proficiencies"].keys())
    values = [data["proficiencies"][cat]["level"] for cat in categories]

    cx, cy, r = 300, 250, 190
    angles = []
    for i in range(len(categories)):
        angle = -90 + (360 / len(categories)) * i
        angles.append(angle)

    polygon_points = []
    for i, value in enumerate(values):
        angle_rad = (angles[i] * 3.141592653589793) / 180
        x = cx + (value / 100) * r * __import__("math").cos(angle_rad)
        y = cy + (value / 100) * r * __import__("math").sin(angle_rad)
        polygon_points.append(f"{x:.1f},{y:.1f}")

    poly = " ".join(polygon_points)

    label_entries = []
    for i, category in enumerate(categories):
        angle_rad = (angles[i] * 3.141592653589793) / 180
        label_r = r + 32
        lx = cx + label_r * __import__("math").cos(angle_rad)
        ly = cy + label_r * __import__("math").sin(angle_rad)
        label_entries.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" fill="#E2E8F0" font-family="Arial, sans-serif" font-size="17" font-weight="700">{category}</text>'
        )

    grid_levels = []
    for level in [20, 40, 60, 80, 100]:
        points = []
        for angle in angles:
            rad = (angle * 3.141592653589793) / 180
            x = cx + (level / 100) * r * __import__("math").cos(rad)
            y = cy + (level / 100) * r * __import__("math").sin(rad)
            points.append(f"{x:.1f},{y:.1f}")
        grid_levels.append(f'<polygon points="{" ".join(points)}" fill="none" stroke="#374151" stroke-width="1"/>')

    svg = f'''<svg width="600" height="520" viewBox="0 0 600 520" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="radarGrad" x1="120" y1="80" x2="500" y2="440" gradientUnits="userSpaceOnUse">
      <stop stop-color="#A855F7"/>
      <stop offset="1" stop-color="#22D3EE"/>
    </linearGradient>
  </defs>
  <rect width="600" height="520" rx="24" fill="#0F172A"/>
  <g>
    <line x1="300" y1="250" x2="300" y2="60" stroke="#475569"/>
    <line x1="300" y1="250" x2="500" y2="250" stroke="#475569"/>
    <line x1="300" y1="250" x2="100" y2="250" stroke="#475569"/>
    <line x1="300" y1="250" x2="435" y2="143" stroke="#475569"/>
    <line x1="300" y1="250" x2="435" y2="357" stroke="#475569"/>
    <line x1="300" y1="250" x2="165" y2="357" stroke="#475569"/>
    <line x1="300" y1="250" x2="165" y2="143" stroke="#475569"/>
  </g>

  {' '.join(grid_levels)}
  <polygon points="{poly}" fill="url(#radarGrad)" fill-opacity="0.25" stroke="url(#radarGrad)" stroke-width="3"/>
  {' '.join(label_entries)}
</svg>'''

    out = Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print(f"✓ Skills radar created: {output_file}")


if __name__ == "__main__":
    make_radar_svg(DATA, "assets/skills-radar.svg")
