import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('uploaded_dataset/faqs_college.json', 'r', encoding='utf-8') as f:
    college_data = json.load(f)

print(f"Total college FAQs: {len(college_data)}")
for item in college_data[:8]:
    print(f"ID: {item['id']} | Cat: {item['category']} | Intent: {item['intent']}")
    print(f"Questions: {item['questions'][:4]}")
    print(f"Answer EN: {item.get('answer_en', '')[:100]}...")
    print(f"Answer HI: {item.get('answer_hi', '')[:100]}...")
    print("-" * 50)
