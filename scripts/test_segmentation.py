import pymupdf, re, json

doc = pymupdf.open(r'c:\Users\abdal\Desktop\RE4E\CCNA 1 Examen final du cours ITNv7 Questions et Réponses.pdf')

def is_noise(text):
    noise_patterns = [
        r'^CCNA 1 Examen final',
        r'^CCNA 1 ITN \(Version 7\.00\)',
        r'^https?://ccnareponses\.com',
        r'^\d{1,2}/\d{1,2}/\d{4}',
        r'^\d{1,2}/\d{1,2}$',
        r'^(Copy Link|Facebook|Twitter|WhatsApp|Contents)$',
        r'^Updated:',
        r'^\d+\s+commentaires',
        r'^CCNA 1$',
        r'^Français$'
    ]
    for pat in noise_patterns:
        if re.search(pat, text.strip()):
            return True
    return False

lines = []
for p_idx, page in enumerate(doc):
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if 'lines' in b:
            for l in b['lines']:
                line_text = ' '.join(s['text'].strip() for s in l['spans'] if s['text'].strip())
                if not line_text or is_noise(line_text):
                    continue
                is_red = any(s['color'] == 0xff0000 for s in l['spans'])
                lines.append({
                    'text': line_text,
                    'is_red': is_red,
                    'page': p_idx + 1
                })

print(f'Clean lines: {len(lines)}')

questions = []
curr_q = None

for l in lines:
    m = re.match(r'^(\d{1,3})\.\s+(.*)$', l['text'])
    if m:
        if curr_q:
            questions.append(curr_q)
        curr_q = {
            'num': int(m.group(1)),
            'title_lines': [m.group(2)],
            'page': l['page'],
            'content_lines': []
        }
    else:
        if curr_q:
            curr_q['content_lines'].append(l)

if curr_q:
    questions.append(curr_q)

print(f'Total questions segmented: {len(questions)}')
red_count = 0
no_red = []
for q in questions:
    reds = [cl['text'] for cl in q['content_lines'] if cl['is_red']]
    if reds:
        red_count += 1
    else:
        no_red.append(q)

print(f'Questions with detected red answers: {red_count}')
print(f'Questions without red answers: {len(no_red)}')
for nr in no_red:
    t = ' '.join(nr['title_lines'])
    print(f"  P{nr['page']}: Q{nr['num']} -> {t[:70]}")
