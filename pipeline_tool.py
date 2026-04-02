import os
import shutil
import json

SOURCE_FOLDER = "assets"

# load config
with open("config.json", "r") as f:
    FOLDER_TYPES = json.load(f)

report = []
warnings = []

print("Running pipeline tool...\n")

# create folders
for folder in FOLDER_TYPES:
    os.makedirs(os.path.join(SOURCE_FOLDER, folder), exist_ok=True)

# process files
for file in os.listdir(SOURCE_FOLDER):
    path = os.path.join(SOURCE_FOLDER, file)

    # skip folders
    if not os.path.isfile(path):
        continue

    name, ext = os.path.splitext(file)
    ext = ext.lower()

    moved = False

    for folder, types in FOLDER_TYPES.items():
        if ext in types:

            prefix = folder[:-1].lower()  # model / texture / audio

            # clean name
            clean_name = name.replace(" ", "_").lower()

            # remove existing prefixes
            while clean_name.startswith(prefix + "_"):
                clean_name = clean_name[len(prefix) + 1:]

            # create new name
            new_name = f"{prefix}_{clean_name}{ext}"
            new_path = os.path.join(SOURCE_FOLDER, folder, new_name)

            # handle duplicates
            count = 1
            while os.path.exists(new_path):
                new_name = f"{prefix}_{clean_name}_{count}{ext}"
                new_path = os.path.join(SOURCE_FOLDER, folder, new_name)
                count += 1

            # move file
            shutil.move(path, new_path)

            report.append(f"{file} -> {folder}/{new_name}")
            moved = True
            break

    if not moved:
        warnings.append(f"{file} -> unsupported type")

# ALWAYS write report (even if empty)
with open("pipeline_report.txt", "w") as f:
    f.write("Pipeline Report\n\n")

    f.write("Moved Files:\n")
    if report:
        for r in report:
            f.write("- " + r + "\n")
    else:
        f.write("None\n")

    f.write("\nWarnings:\n")
    if warnings:
        for w in warnings:
            f.write("- " + w + "\n")
    else:
        f.write("None\n")

print("Done.")
print(f"Moved {len(report)} files, {len(warnings)} warnings.")