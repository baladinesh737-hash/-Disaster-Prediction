"""
Script to remove all emojis from project files
"""
import re
import os

def remove_emojis(text):
    """Remove all emojis from text"""
    # Emoji pattern
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub('', text)

def process_file(filepath):
    """Remove emojis from a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = remove_emojis(content)
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Processed: {filepath}")
            return True
        else:
            print(f"- No emojis: {filepath}")
            return False
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Process all project files"""
    files_to_process = [
        "backend/app.py",
        "frontend/admin.html",
        "frontend/user.html",
        "frontend/index.html",
        "frontend/rescue.html",
        "frontend/government.html"
    ]
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    processed = 0
    
    print("=" * 60)
    print("REMOVING EMOJIS FROM PROJECT FILES")
    print("=" * 60)
    print()
    
    for file in files_to_process:
        filepath = os.path.join(base_path, file)
        if os.path.exists(filepath):
            if process_file(filepath):
                processed += 1
        else:
            print(f"✗ File not found: {filepath}")
    
    print()
    print("=" * 60)
    print(f"COMPLETE: {processed} files updated")
    print("=" * 60)

if __name__ == "__main__":
    main()
