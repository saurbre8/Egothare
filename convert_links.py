import re
import glob
import os

def build_file_map():
    # Map to store file titles to their actual paths
    file_map = {}
    
    # Search through all markdown files in the docs directory
    for file_path in glob.glob("docs/**/*.md", recursive=True):
        # Get the file name without extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        # Get the relative path without 'docs/' prefix and .md extension
        relative_path = os.path.splitext(file_path[5:])[0]  # Remove 'docs/' prefix
        # Store both the simple name and full path as keys
        file_map[file_name] = relative_path
        file_map[relative_path] = relative_path
    
    return file_map

def convert_obsidian_links(content, file_map):
    def replace_link(match):
        link_text = match.group(1)
        # Split the link if it has a display text (using |)
        if '|' in link_text:
            link_path, display_text = link_text.split('|', 1)
        else:
            display_text = link_path = link_text
        
        # Look up the actual path in our file map
        actual_path = file_map.get(link_path, link_path)
        
        # Just add trailing slash, no leading slash or Egothare
        final_path = f"{actual_path}/"
        
        # Return the markdown link format
        return f"[{display_text}]({final_path})"

    # Find all Obsidian-style links and replace them
    content = re.sub(r'\[\[(.*?)\]\]', replace_link, content)
    
    return content

def process_files():
    # First build the map of all files
    file_map = build_file_map()
    
    # Then process each file
    for file_path in glob.glob("docs/**/*.md", recursive=True):
        print(f"Processing {file_path}...")
        with open(file_path, "r", encoding='utf-8') as file:
            content = file.read()
        
        # Convert links using our file map
        content = convert_obsidian_links(content, file_map)
        
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(content)

if __name__ == "__main__":
    process_files()