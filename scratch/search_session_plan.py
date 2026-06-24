def main():
    filepath = r"E:\Projeler\MeteorGaleri\session-ses_20da.md"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        print("Total lines:", len(lines))
        for i, line in enumerate(lines):
            if "plan" in line.lower() or "adım" in line.lower() or "step" in line.lower():
                if len(line.strip()) < 120 and len(line.strip()) > 5:
                    print(f"Line {i+1}: {line.strip()}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
