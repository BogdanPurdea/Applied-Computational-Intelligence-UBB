import os

DATASET_ROOT = "/kaggle/input/gtsrb-german-traffic-sign"

print("=" * 60)
print("  GTSRB DATASET FOLDER INSPECTION")
print("=" * 60)

# Top-level folders
print(f"\nRoot: {DATASET_ROOT}")
top_level = sorted(os.listdir(DATASET_ROOT))
print(f"  Top-level contents ({len(top_level)} items):")
for item in top_level:
    full = os.path.join(DATASET_ROOT, item)
    kind = "DIR " if os.path.isdir(full) else "FILE"
    print(f"    [{kind}]  {item}")

# Inspect each subfolder
print("\n" + "-" * 60)
for item in top_level:
    full = os.path.join(DATASET_ROOT, item)
    if os.path.isdir(full):
        subfolders = sorted(os.listdir(full))
        img_count = 0
        non_dir = []
        for s in subfolders:
            s_path = os.path.join(full, s)
            if os.path.isdir(s_path):
                imgs = [f for f in os.listdir(s_path)
                        if f.lower().endswith((".png", ".jpg", ".jpeg", ".ppm"))]
                img_count += len(imgs)
            else:
                non_dir.append(s)

        dirs_only = [s for s in subfolders if os.path.isdir(os.path.join(full, s))]

        print(f"\n  Folder: {item}/")
        print(f"    Subfolders : {len(dirs_only)}")
        print(f"    Total imgs : {img_count:,}")
        if dirs_only:
            print(f"    First 5 subfolder names : {dirs_only[:5]}")
            print(f"    Last  5 subfolder names : {dirs_only[-5:]}")

            # Show image count per first 5 subfolders
            print(f"    Sample counts:")
            for sf in dirs_only[:5]:
                sf_path = os.path.join(full, sf)
                n = len([f for f in os.listdir(sf_path)
                         if f.lower().endswith((".png", ".jpg", ".jpeg", ".ppm"))])
                print(f"      {sf}/  ->  {n} images")
        if non_dir:
            print(f"    Non-folder files: {non_dir[:5]}")

print("\n" + "=" * 60)