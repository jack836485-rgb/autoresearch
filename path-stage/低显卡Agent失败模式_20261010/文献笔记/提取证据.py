import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1] / '资料'
for aid in sys.argv[1:]:
    path = root / (aid + '正文.json')
    if not path.exists():
        print('尚未保存:', aid)
        continue
    data = json.loads(path.read_text(encoding='utf-8'))
    text = data.get('text', '')
    print('\n论文', aid, '全文长度', len(text), '截断', data.get('text_truncated'))
    print('标题与机构:', data.get('paper', {}).get('title'), data.get('paper', {}).get('author_block'))
    for term in ['Limitations', '6.7 Agent Error Analysis', '3.2 Beyond Information Loss', '3.3 Compression', 'Table 1', 'Table 3', 'Table 4']:
        matches = list(re.finditer(re.escape(term), text, re.I))
        if matches:
            match = matches[-1] if term == 'Limitations' else matches[0]
            print('\n位置', term, '\n', text[max(0, match.start()-150):match.start()+2400])
