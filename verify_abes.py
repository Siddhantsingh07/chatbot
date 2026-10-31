import json

with open('backend/data/faqs.json', 'r', encoding='utf-8') as f:
    current = json.load(f)

print(f"Current ABES dataset has {len(current)} FAQs.")
categories = sorted(list(set(x['category'] for x in current)))
print("Categories:", categories)
total_questions = sum(len(x.get('questions', [])) for x in current)
print(f"Total training questions across all FAQs: {total_questions}")
