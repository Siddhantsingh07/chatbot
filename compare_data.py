import json

with open('uploaded_dataset/faqs_college.json', 'r', encoding='utf-8') as f:
    college = json.load(f)

with open('uploaded_dataset/faqs_university.json', 'r', encoding='utf-8') as f:
    uni = json.load(f)

print(f"College items: {len(college)}, categories: {set(x['category'] for x in college)}")
print(f"University items: {len(uni)}, categories: {set(x['category'] for x in uni)}")

college_intents = set((x['category'], x['intent']) for x in college)
uni_intents = set((x['category'], x['intent']) for x in uni)

print(f"Common intents: {len(college_intents & uni_intents)}")
print(f"College-only: {len(college_intents - uni_intents)}")
print(f"Uni-only: {len(uni_intents - college_intents)}")
print("College-only samples:", list(college_intents - uni_intents)[:5])
print("Uni-only samples:", list(uni_intents - college_intents)[:5])
