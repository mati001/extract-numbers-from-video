import os
import shutil
import kagglehub

# 1. Setup paths relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DB = os.path.join(SCRIPT_DIR, "..", "DB")

# 2. Define the datasets to download
# ICDAR 2015 & 2019 for detecting WHERE text is.
# SVHN for recognizing WHAT the numbers are.
datasets = {
    "ICDAR2015": "bestofbests9/icdar2015",
    "ICDAR2019": "zubairalibhutto/mlt-19-ocr-dataset",
    "SVHN": "stanfordu/street-view-house-numbers"
}

def sync_dataset(name, slug):
    target_path = os.path.join(ROOT_DB, name)
    
    # Simple, per-dataset status messages
    print(f"[1/2] Downloading {name} from Kaggle...")
    
    # Note: kagglehub.dataset_download is a single call. 
    # It won't show a bar, but it is working in the background.
    downloaded_cache_path = kagglehub.dataset_download(slug)
    
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    print(f"[2/2] Syncing {name} files to local DB folder...")
    for item in os.listdir(downloaded_cache_path):
        s = os.path.join(downloaded_cache_path, item)
        d = os.path.join(target_path, item)
        
        if os.path.isdir(s):
            if os.path.exists(d): shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
            
    print(f"--- {name} Complete ---\n")

# Main Execution Loop
print("Starting Database Synchronization...\n" + "="*40)

for folder_name, kaggle_slug in datasets.items():
    try:
        sync_dataset(folder_name, kaggle_slug)
    except Exception as e:
        print(f"(!) Failed to process {folder_name}: {e}")

print("="*40 + "\nAll datasets are now local and ready for use.")