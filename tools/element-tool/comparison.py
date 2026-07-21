import json
from pathlib import Path


def load_top_level_object(file_path: Path) -> dict:
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"{file_path.name} 顶层必须是对象")

    return data


def main() -> None:
    current_dir = Path.cwd()
    element_file = current_dir / "elementDescriptions.json"
    old_file = current_dir / "old.json"
    output_dir = current_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    element_data = load_top_level_object(element_file)
    old_data = load_top_level_object(old_file)

    element_keys = set(element_data.keys())
    old_keys = set(old_data.keys())
    missing_in_element = sorted(old_keys - element_keys)

    for name in missing_in_element:
        print(name)
        output_file = output_dir / f"{name}.json"
        with output_file.open("w", encoding="utf-8") as f:
            json.dump({name: old_data[name]}, f, ensure_ascii=False, indent=2)
            f.write("\n")


if __name__ == "__main__":
    main()