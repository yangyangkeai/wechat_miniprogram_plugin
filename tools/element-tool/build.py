import glob

output_file = "elementDescriptions.json"

parts = []

for filename in sorted(glob.glob("output/*.json")):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().strip()

        if content.startswith("{"):
            content = content[1:]
        if content.endswith("}"):
            content = content[:-1]

        content = content.strip()

        if content:
            parts.append(content)

result = "{\n" + ",\n".join(parts) + "\n}\n"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(result)

print(f"合并完成，共 {len(parts)} 个文件 -> {output_file}")
