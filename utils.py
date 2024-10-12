import re

def parse_diff(diff_text):
    files_changes = []
    current_file = None
    current_changes = None
    search_buffer = []
    replace_buffer = []
    is_in_search = False
    is_in_replace = False

    for line in diff_text.splitlines():
        # Detect filename
        match_filename = re.match(r'^([\w\/\.]+)$', line.replace("**", ""))
        print("Check match_filename", match_filename)
        if match_filename:
            if current_file and current_changes:
                # Save previous file's changes
                files_changes.append({
                    "filename": current_file,
                    "changes": current_changes
                })
            # Start a new file
            current_file = match_filename.group(1).replace("*", "")
            print("Current file", current_file)
            current_changes = []
            search_buffer = []
            replace_buffer = []
            is_in_search = False
            is_in_replace = False
            continue

        # Detect search block start
        if line.startswith("<<<<<<< SEARCH"):
            is_in_search = True
            search_buffer = []
            continue
        
        if line.startswith("======="):
            is_in_search = False
            is_in_replace = True
            replace_buffer = []
            continue
        
        if line.startswith(">>>>>>> REPLACE"):
            is_in_replace = True
            continue

        # Detect the end of replace block
        if is_in_replace and line.startswith("```"):
            # Save the change
            current_changes.append({
                "search": "\n".join(search_buffer).strip(),
                "replace": "\n".join(replace_buffer).strip()
            })
            search_buffer = []
            replace_buffer = []
            is_in_replace = False
            continue

        # Collect lines for the current search/replace block
        if is_in_search:
            search_buffer.append(line)
        elif is_in_replace:
            replace_buffer.append(line)

    # Save the last file's changes if any
    if current_file and current_changes:
        files_changes.append({
            "filename": current_file,
            "changes": current_changes
        })

    return files_changes
