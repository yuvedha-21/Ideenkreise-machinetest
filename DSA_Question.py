def repeated_chars(s):
    seen = set()
    duplicates = set()
    
    for char in s:
        if char in seen:
            duplicates.add(char)
        seen.add(char)
    
    return list(duplicates)


print(repeated_chars("programming")) 
