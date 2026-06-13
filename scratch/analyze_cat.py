import re

with open("E:/Projeler/MeteorGaleri/scratch/category_html.txt", "r", encoding="utf-8") as f:
    text = f.read()

# find first 5 occurrences of "aslan" and print context
matches = [m.start() for m in re.finditer(r'aslan', text, re.IGNORECASE)][:5]
for m in matches:
    start = max(0, m - 100)
    end = min(len(text), m + 100)
    print("Context around 'aslan':")
    print(text[start:end])
    print("-" * 50)
    
# also let's just see if there is an array of products in json
match = re.search(r'products\s*=\s*(\[.*?\]);', text, re.DOTALL | re.IGNORECASE)
if match:
    print("Found products array:", match.group(1)[:200])
