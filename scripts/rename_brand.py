import os

target_dirs = [
    r"D:\Backend\finbot-ai\app\templates",
    r"D:\Backend\finbot-ai\app\services",
    r"D:\Backend\finbot-ai\app\static\css",
    r"D:\Backend\finbot-ai\README.md",
    r"D:\Backend\finbot-ai\tests",
    r"D:\Backend\finbot-ai\scripts"
]

count = 0
for tdir in target_dirs:
    if os.path.isfile(tdir):
        files_to_check = [tdir]
    else:
        files_to_check = []
        for root, _, files in os.walk(tdir):
            for f in files:
                if f.endswith((".html", ".py", ".md", ".css")):
                    files_to_check.append(os.path.join(root, f))

    for path in files_to_check:
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            new_content = content.replace("ArthSaathi AI", "ArthSaathi AI")
            new_content = new_content.replace("ArthSaathi", "ArthSaathi")
            new_content = new_content.replace("ARTHSAATHI", "ARTHSAATHI")

            if new_content != content:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(new_content)
                count += 1
                print(f"Updated brand in: {path}")
        except Exception as e:
            print(f"Error {path}: {e}")

print(f"Done! Updated {count} files with ArthSaathi AI brand.")
