import json, re
from pathlib import Path
import pdfplumber

src = r'C:\Users\Asus\Downloads\300- SQL Queries.pdf'
out = Path(__file__).parent / 'src' / 'questions.json'
pages = pdfplumber.open(src).pages
items = []
sql_start = re.compile(r'^\s*(SELECT|WITH\s+RECURSIVE|WITH\b|INSERT\b|UPDATE\b|DELETE\b|CREATE\b|ALTER\b|DROP\b|EXPLAIN\b)', re.I)
numbered = re.compile(r'^\s*(\d{1,3})\.\s+(.*)$')
for page in pages[1:]:
    lines = (page.extract_text(layout=False) or '').splitlines()
    current = None
    for raw in lines:
        line = raw.strip()
        if not line or re.match(r'^300 Real SQL Interview Questions Page \d+ of \d+', line):
            continue
        m = numbered.match(line)
        if m:
            if current:
                items.append(current)
            current = {'printed': int(m.group(1)), 'lines': [m.group(2).strip()], 'solution': [], 'in_sql': False}
            continue
        if current is None:
            continue
        if not current['in_sql'] and sql_start.match(line):
            current['in_sql'] = True
        if current['in_sql']:
            current['solution'].append(line)
        else:
            current['lines'].append(line)
    if current:
        items.append(current)

def clean_sql(lines):
    s = ' '.join(lines)
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s*-{3,}\s*THE END\s*-{3,}\s*$', '', s, flags=re.I).strip()
    # Repair line-wrapped SQL identifiers and operators with ordinary spacing.
    return s

questions = []
for n, item in enumerate(items, 1):
    prompt = re.sub(r'\s+', ' ', ' '.join(item['lines'])).strip()
    if not prompt:
        prompt = f'SQL practice question {n}'
    full = (prompt + ' ' + ' '.join(item['solution'])).lower()
    if any(k in full for k in ('window', 'rank(', 'lag(', 'lead(', 'over (', 'recursive', 'streak', 'median', 'percentile', 'cumulative')):
        category, difficulty = 'Window Functions', 'Hard'
    elif any(k in full for k in ('join', 'manager', 'overlapping', 'compare two tables', 'not made any purchase')):
        category, difficulty = 'Joins & Relationships', 'Medium'
    elif any(k in full for k in ('having', 'count(', 'avg(', 'sum(', 'group by', 'aggregate')):
        category, difficulty = 'Aggregations', 'Medium'
    elif any(k in full for k in ('date', 'month', 'year', 'days')):
        category, difficulty = 'Date & Time', 'Medium'
    else:
        category, difficulty = 'SQL Fundamentals', 'Medium'
    questions.append({'id': n, 'sourceNumber': item['printed'], 'question': prompt,
                      'solution': clean_sql(item['solution']), 'category': category,
                      'difficulty': difficulty})
out.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Wrote {len(questions)} questions to {out}')
print('Missing prompt/answer:', sum(not q['question'] for q in questions), sum(not q['solution'] for q in questions))
print('First:', questions[0])
print('Last:', questions[-1])
tables = set()
ctes = set()
for question in questions:
    ctes.update(m.group(1).lower() for m in re.finditer(r'\b([A-Za-z_]\w*)\s+AS\s*\(', question['solution'], re.I))
    for match in re.finditer(r'\b(?:FROM|JOIN|UPDATE|INTO)\s+([A-Za-z_]\w*)', question['solution'], re.I):
        name = match.group(1).lower()
        if name not in {'select', 'values'}:
            tables.add(name)
print('Referenced table names:', ', '.join(sorted(tables - ctes - {'e','e1','e2','m','t2'})))
