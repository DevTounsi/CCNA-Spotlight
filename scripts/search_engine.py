import json
import unicodedata
import re
import os

class CCNAEngine:
    def __init__(self, data_path=None):
        if data_path is None:
            try:
                base_dir = sys._MEIPASS
            except AttributeError:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, 'data', 'ccna1_exam.json')
            
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
            
        for item in self.data:
            item['norm_q'] = self.normalize(item['question'])
            item['norm_ans'] = self.normalize(' '.join(item.get('correct_answers', [])))
            item['norm_exp'] = self.normalize(item.get('explanation') or '')

    @staticmethod
    def normalize(text):
        if not text:
            return ""
        # Remove accents
        text = unicodedata.normalize('NFD', text.lower())
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        # Replace non-alphanumeric with spaces
        return re.sub(r'[^a-z0-9\s]', ' ', text)

    def search(self, query, limit=10):
        cleaned = query.strip()
        if not cleaned:
            return []
            
        norm_query = self.normalize(cleaned)
        words = norm_query.split()
        if not words:
            return []
            
        results = []
        for item in self.data:
            score = 0
            q_text = item['norm_q']
            ans_text = item['norm_ans']
            exp_text = item['norm_exp']
            
            # Exact substring match in question
            if norm_query in q_text:
                score += 200
                
            # All query tokens present in question
            if all(w in q_text for w in words):
                score += 100
                
            for w in words:
                # Word in question
                if w in q_text:
                    score += 30
                # Prefix match in question tokens
                elif any(tok.startswith(w) for tok in q_text.split()):
                    score += 15
                    
                # Word in answers
                if w in ans_text:
                    score += 25
                    
                # Word in explanation
                if w in exp_text:
                    score += 10

            if score > 0:
                results.append((score, item))
                
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]

if __name__ == '__main__':
    engine = CCNAEngine()
    test_queries = ['masque 4', 'glissement', 'cheval troie', 'port 69', 'dimensionnement', 'rj45', 'show ip int brief']
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    for q in test_queries:
        res = engine.search(q, limit=1)
        if res:
            print(f"[{q}] -> Q{res[0]['original_number']}: {res[0]['question'][:50]}... | R: {res[0]['correct_answers'][0][:40]}")
