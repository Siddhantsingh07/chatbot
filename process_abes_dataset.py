import json

with open('uploaded_dataset/faqs_college.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    en = item.get('answer_en', '')
    hi = item.get('answer_hi', '')
    
    # Replace generic college/chatbot references with ABES & Help Desk
    en = en.replace('College Student Support Assistant', 'ABES Student Support Help Desk')
    en = en.replace('College Student Support Chatbot', 'ABES Student Support Help Desk')
    en = en.replace('College Support Chatbot', 'ABES Student Help Desk')
    en = en.replace('the chatbot', 'the ABES Help Desk')
    en = en.replace('chatbot', 'help desk')
    en = en.replace('Chatbot', 'Help Desk')
    en = en.replace('the college', 'ABES Engineering College')
    en = en.replace('The college', 'ABES Engineering College')
    en = en.replace('our college', 'ABES Engineering College')
    en = en.replace('college portal', 'ABES student portal (abes.ac.in)')
    en = en.replace('info@college.edu', 'info@abes.ac.in')
    en = en.replace('admissions@college.edu', 'admissions@abes.ac.in')
    en = en.replace('examcell@college.edu', 'examcell@abes.ac.in')
    en = en.replace('placements@college.edu', 'placements@abes.ac.in')
    en = en.replace('hostel@college.edu', 'hostel@abes.ac.in')
    en = en.replace('scholarship@college.edu', 'scholarship@abes.ac.in')
    en = en.replace('principal@college.edu', 'director@abes.ac.in')
    
    hi = hi.replace('कॉलेज स्टूडेंट सपोर्ट चैटबॉट', 'ABES स्टूडेंट सपोर्ट हेल्प डेस्क')
    hi = hi.replace('स्टूडेंट सपोर्ट असिस्टेंट', 'ABES स्टूडेंट हेल्प डेस्क')
    hi = hi.replace('चैटबॉट', 'हेल्प डेस्क')
    hi = hi.replace('कॉलेज', 'ABES इंजीनियरिंग कॉलेज')
    
    item['answer_en'] = en
    item['answer_hi'] = hi
    item['answer'] = en  # For backward compatibility with existing code

# Save updated dataset to backend/data/faqs.json
with open('backend/data/faqs.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Successfully processed and saved {len(data)} FAQs for ABES Help Desk!")
