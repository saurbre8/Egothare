import re
import glob
import os

def convert_obsidian_links(content, file_path):
    # Get the directory of the current file
    current_dir = os.path.dirname(file_path)
    
    def replace_link(match):
        link_text = match.group(1)
        # Split the link if it has a display text (using |)
        if '|' in link_text:
            display_text, link_path = link_text.split('|', 1)
        else:
            display_text = link_path = link_text
            
        # Remove any file extension from the link path
        link_path = re.sub(r'\.md$', '', link_path)
        
        # Convert the link path to a relative path
        # If the link is in the same directory, just use the filename
        # If it's in a different directory, use the full path
        if '/' in link_path:
            # Keep the path as is, but ensure it's relative to docs
            final_path = link_path
        else:
            # For files in the same directory
            final_path = link_path
            
        # Add trailing slash instead of .md extension
        final_path = f"{final_path}/"
        
        # Return the markdown link format
        return f"[{display_text}]({final_path})"

    # Find all Obsidian-style links and replace them
    # This regex matches [[link]] or [[link|display text]]
    content = re.sub(r'\[\[(.*?)\]\]', replace_link, content)
    
    return content

def process_file(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        content = file.read()
    
    # Convert Obsidian links
    content = convert_obsidian_links(content, file_path)
    
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(content)

# Process all markdown files in the docs directory
for md_file in glob.glob("docs/**/*.md", recursive=True):
    print(f"Processing {md_file}...")
    process_file(md_file)