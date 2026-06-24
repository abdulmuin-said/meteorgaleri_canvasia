def main():
    filepath = r"E:\Projeler\MeteorGaleri\meteorgaleriminimaxilkprompçıktısı.md"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        print("Total lines:", len(lines))
        
        # Search for headings or bullet points like "1." or "- [ ]" or "[ ]" or similar.
        # Let's search for "adım" or "maddel" or "plan"
        for i, line in enumerate(lines):
            if "plan" in line.lower() or "adım" in line.lower() or "step" in line.lower() or "roadmap" in line.lower():
                if len(line.strip()) < 100:
                    print(f"Line {i+1}: {line.strip()}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
