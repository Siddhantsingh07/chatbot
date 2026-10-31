import json

with open('uploaded_dataset/faqs_college.json', 'r', encoding='utf-8') as f:
    college = json.load(f)

for item in college:
    q = " | ".join(item['questions'][:2])
    en = item.get('answer_en', '')
    if any(k in en.lower() for k in ['university', 'college', 'chatbot', 'bot', 'assistant']):
        print(f"ID {item['id']} ({item['category']}/{item['intent']}):")
        print(f"  Q: {q}")
        print(f"  EN: {en[:120]}")
