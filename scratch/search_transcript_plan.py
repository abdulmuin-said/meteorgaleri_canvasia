import json

def main():
    filepath = r"C:\Users\abdul\.gemini\antigravity\brain\b44bddd3-46fe-42cc-82f2-e2e384a3bb65\.system_generated\logs\transcript.jsonl"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f):
                try:
                    data = json.loads(line)
                    content = data.get("content", "")
                    if not content:
                        continue
                    
                    if "100 maddelik" in content.lower() or "100 maddeli" in content.lower() or "100 adım" in content.lower() or "100-step" in content.lower():
                        print(f"Line {line_idx+1} matches!")
                        # print some preview
                        print(content[:300])
                        print("-" * 50)
                except Exception as e:
                    pass
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
