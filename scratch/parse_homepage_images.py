from bs4 import BeautifulSoup

def main():
    filepath = r"C:\Users\abdul\.gemini\antigravity\brain\b44bddd3-46fe-42cc-82f2-e2e384a3bb65\.system_generated\steps\3467\content.md"
    with open(filepath, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Let's find headings with "Yeni Eklenenler"
    headings = soup.find_all(["h2", "h3"])
    for h in headings:
        if "Yeni Eklenenler" in h.text:
            print(f"Found Section: {h.text.strip()}")
            # Go up to the section or parent
            parent = h.find_parent("section")
            if parent:
                # Find all articles/images inside this section
                images = parent.find_all("img")
                print(f"Found {len(images)} images in this section:")
                for img in images:
                    print(f"  Alt: {img.get('alt')} | Src: {img.get('src')}")
            else:
                print("Could not find parent section.")
                
if __name__ == "__main__":
    main()
