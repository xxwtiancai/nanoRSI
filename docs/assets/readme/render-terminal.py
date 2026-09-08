"""Render the recorded fixture output as an accessible, script-free SVG."""
import html
import json
from pathlib import Path

root = Path(__file__).resolve().parent
captured = json.loads((root / 'demo-evidence.json').read_text())
assert captured['offline'] and captured['paid_calls'] is False
assert all(c['exit_code'] == 0 for c in captured['commands'])
commands = captured['commands']
baseline = json.loads(commands[1]['stdout'])
step = json.loads(commands[2]['stdout'])
rows = [
    ('$ ' + commands[0]['command'], '#ffad88'),
    (commands[0]['stdout'], '#e5e7eb'),
    ('', '#fff'),
    ('$ ' + commands[1]['command'], '#ffad88'),
    (json.dumps({'generation': baseline['generation'], 'gate_metrics': baseline['gate_metrics']}), '#d5d9df'),
    ('', '#fff'),
    ('$ ' + commands[2]['command'], '#ffad88'),
    (json.dumps({k: step[k] for k in ['decision', 'generation', 'attempt_id']}), '#8fe0ad'),
    ('', '#fff'),
    ('$ ' + commands[4]['command'], '#ffad88'),
    (commands[4]['stdout'], '#8fe0ad'),
]
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="526" viewBox="0 0 1120 526" role="img" aria-labelledby="title desc">',
         '<title id="title">Recorded nanoRSI offline fixture demo</title>',
         '<desc id="desc">Actual CLI fixture output with selected JSON fields: create an experiment, establish a baseline, accept a candidate and verify the lineage. This uses a scripted proposer and makes no model API calls.</desc>',
         '<rect width="1120" height="526" rx="20" fill="#161b22"/>',
         '<path d="M0 57H1120" stroke="#30363d"/>',
         '<circle cx="31" cy="29" r="6" fill="#fa6b61"/><circle cx="53" cy="29" r="6" fill="#f0c85b"/><circle cx="75" cy="29" r="6" fill="#59c68e"/>',
         '<text x="105" y="35" font-family="Arial,sans-serif" font-size="17" fill="#b8c0cc">nanoRSI / scripted offline demo</text>',
         '<rect x="869" y="15" width="217" height="28" rx="14" fill="#25372d"/><text x="977" y="34" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" font-weight="700" fill="#9cddb3">NO MODEL API CALLS</text>',
         '<g font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="21">']
for index, (text, color) in enumerate(rows):
    parts.append(f'<text x="35" y="{101 + index*33}" fill="{color}">{html.escape(text)}</text>')
parts += ['</g>', '<path d="M35 464H1085" stroke="#30363d"/>',
          '<text x="35" y="498" fill="#929dab" font-family="Arial,sans-serif" font-size="15">Recorded fixture output · selected JSON fields · full transcript linked in README</text>', '</svg>']
(root / 'terminal-demo.svg').write_text('\n'.join(parts) + '\n')
