import json

def main():
    filepath = r"C:\Users\abdul\.gemini\antigravity\brain\b44bddd3-46fe-42cc-82f2-e2e384a3bb65\.system_generated\logs\transcript_full.jsonl"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f):
                try:
                    data = json.loads(line)
                    content = data.get("content", "")
                    if "7ANRPS48.com" in content and "100" in content:
                        print(f"Match found in full log at line {line_idx+1}")
                        # Let's save this content to a separate file
                        out_path = r"E:\Projeler\MeteorGaleri\scratch\extracted_100_step_plan.md"
                        with open(out_path, "w", encoding="utf-8") as out_f:
                            out_f.write(content)
                        print(f"Extracted content saved to {out_path}")
                        # Print length and first 500 chars
                        print(f"Length of content: {len(content)}")
                        print(content[:500])
                        print("...")
                except Exception as e:
                    pass
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
