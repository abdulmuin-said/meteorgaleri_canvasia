import os

def main():
    folder = r"E:\Projeler\MeteorGaleri\_ProjDökümanveScriptler"
    files = ["eklenmesi gereken özellikler.txt", "prompt türkçe.txt", "prompt ingilizce .txt", "ilk gönderdiğim prompt codex.txt"]
    for fn in files:
        filepath = os.path.join(folder, fn)
        if not os.path.exists(filepath):
            continue
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"File: {fn} | Size: {len(content)}")
            # Look for 100 or plan
            if "100" in content or "plan" in content.lower() or "adım" in content.lower():
                print(f"  -> Found keyword '100' or 'plan' or 'adım'")
                # print first 500 characters
                print(content[:500])
                print("-" * 40)
        except Exception as e:
            print("Error in", fn, e)

if __name__ == "__main__":
    main()
