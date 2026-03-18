import os
import random
import string
from pathlib import Path

# =========================
# SETTINGS
# =========================
TARGET_FOLDER = "."          # current folder; চাইলে path দাও
FILE_EXTENSION = ".html"
TOKEN_LENGTH = 6

# =========================
# HELPERS
# =========================
used_tokens = set()
used_filenames = set()

def random_token(length=6):
    chars = string.ascii_lowercase + string.digits
    while True:
        token = ''.join(random.choices(chars, k=length))
        if token not in used_tokens:
            used_tokens.add(token)
            return token

def is_ascii_english_part(part: str) -> bool:
    """
    Return True if part contains only ASCII letters/numbers/underscore.
    Example: xxx, abc123, i8ct3z => keep unchanged
    """
    if not part:
        return True

    allowed = set(string.ascii_letters + string.digits + "_")
    return all(ch in allowed for ch in part)

def build_new_name(stem: str, suffix: str) -> str:
    parts = stem.split("-")
    new_parts = []

    for part in parts:
        if is_ascii_english_part(part):
            new_parts.append(part)
        else:
            new_parts.append(random_token(TOKEN_LENGTH))

    new_name = "-".join(new_parts) + suffix

    # Avoid filename collision
    while new_name in used_filenames or Path(TARGET_FOLDER, new_name).exists():
        parts2 = []
        for old_part, new_part in zip(parts, new_parts):
            if is_ascii_english_part(old_part):
                parts2.append(old_part)
            else:
                parts2.append(random_token(TOKEN_LENGTH))
        new_name = "-".join(parts2) + suffix

    used_filenames.add(new_name)
    return new_name

# =========================
# MAIN
# =========================
def main():
    folder = Path(TARGET_FOLDER)

    if not folder.exists():
        print(f"Folder not found: {folder}")
        return

    files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == FILE_EXTENSION]

    if not files:
        print("No .html files found.")
        return

    renamed_count = 0
    skipped_count = 0

    for file_path in files:
        old_name = file_path.name
        stem = file_path.stem
        suffix = file_path.suffix

        new_name = build_new_name(stem, suffix)

        if new_name == old_name:
            skipped_count += 1
            print(f"SKIPPED: {old_name}")
            continue

        new_path = file_path.with_name(new_name)

        try:
            file_path.rename(new_path)
            renamed_count += 1
            print(f"RENAMED: {old_name}  -->  {new_name}")
        except Exception as e:
            print(f"ERROR: {old_name} -> {e}")

    print("\nDone.")
    print(f"Renamed: {renamed_count}")
    print(f"Skipped: {skipped_count}")

if __name__ == "__main__":
    main()