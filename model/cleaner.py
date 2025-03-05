import re

def remove_unwanted_patterns(content):
    unwanted_patterns = [
        r"\n| {2}—|—+",  
        r"\\u[\dA-Fa-f]{4}|[\uf075\uf0b7]|[\u202a-\u202e]",  
    ]
    for pattern in unwanted_patterns:
        content = re.sub(pattern, "", content)
    return content

def normalize_whitespace_and_hyphens(content):
    
    content = re.sub(r"(\w+)-\n(\w+)", r"\1\2", content)
    content = re.sub(r"(\w)\s*-\s*(\w)", r"\1-\2", content)
    content = re.sub(r"[^\w\s]\s+", " ", content)
    content = re.sub(r"\s+", " ", content)

    return content

def clean_text(content):
    content = remove_unwanted_patterns(content)
    content = normalize_whitespace_and_hyphens(content)
    return content.strip()