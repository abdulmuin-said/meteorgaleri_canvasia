import json
import re

def main():
    filepath = r"C:\Users\abdul\.gemini\antigravity\brain\b44bddd3-46fe-42cc-82f2-e2e384a3bb65\.system_generated\logs\transcript_full.jsonl"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f):
                try:
                    data = json.loads(line)
                    # Check tool_calls
                    tool_calls = data.get("tool_calls", [])
                    if not tool_calls:
                        # Sometimes it is under planner response tool_calls
                        continue
                    
                    for tc in tool_calls:
                        args = tc.get("args", {})
                        target_file = args.get("TargetFile", "")
                        if "implementation_plan.md" in target_file:
                            content = args.get("CodeContent", "") or args.get("ReplacementContent", "")
                            if "7ANRPS48.com" in content or "100" in content:
                                print(f"Found implementation_plan write in tool call at line {line_idx+1}")
                                out_path = r"E:\Projeler\MeteorGaleri\scratch\extracted_100_step_plan_actual.md"
                                with open(out_path, "w", encoding="utf-8") as out_f:
                                    out_f.write(content)
                                print(f"Saved actual 100 step plan to {out_path}")
                                print(f"Plan size: {len(content)} characters.")
                except Exception as e:
                    pass
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
