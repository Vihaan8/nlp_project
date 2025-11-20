import pandas as pd
from collections import Counter

file_path = './data/full_data.csv'
chunk_size = 50000
abbrev_counter = Counter()
total_processed = 0

print("Counting abbreviations...")
for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    for _, row in chunk.iterrows():
        text_words = row['TEXT'].split()
        locations = [int(x) for x in str(row['LOCATION']).split('|')]
        labels = str(row['LABEL']).split('|')
        
        for loc, label in zip(locations, labels):
            if loc < len(text_words):
                abbrev = text_words[loc].upper()
                abbrev_counter[(abbrev, label.lower())] += 1
        
        total_processed += 1

print(f"Total processed: {total_processed}")

# Filter to multi-word labels where first letters match
valid_counter = Counter()
for (abbrev, label), count in abbrev_counter.items():
    if ' ' in label:
        words = label.split()
        if len(words) >= 2:
            initials = ''.join([w[0].upper() for w in words[:len(abbrev)]])
            if initials == abbrev:
                valid_counter[(abbrev, label)] = count

# Get abbreviations with at least 3 valid meanings
abbrev_meanings = {}
for abbrev in set(a for (a, l) in valid_counter.keys()):
    meanings = [(a, l) for (a, l) in valid_counter.keys() if a == abbrev]
    if len(meanings) >= 3:
        total = sum(valid_counter[p] for p in meanings)
        abbrev_meanings[abbrev] = total

# Top abbreviations
top_abbrevs = sorted(abbrev_meanings.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop abbreviations:")
for abbrev, total in top_abbrevs:
    pairs = [(a, l) for (a, l) in valid_counter.keys() if a == abbrev]
    top_3 = sorted(pairs, key=lambda x: valid_counter[x], reverse=True)[:3]
    print(f"{abbrev} (total: {total:,}, meanings: {len(pairs)})")

# Selected abbreviations and meanings
selected = {
    'CC': ['colorectal cancer', 'cell culture', 'cervical cancer'],
    'CP': ['chronic pain', 'chest pain', 'cerebral palsy'],
    'SA': ['surface area', 'sleep apnea', 'substance abuse']
}

# Filter dataset
print("\nFiltering dataset...")
filtered_rows = []

for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    for _, row in chunk.iterrows():
        text_words = row['TEXT'].split()
        locations = [int(x) for x in str(row['LOCATION']).split('|')]
        labels = str(row['LABEL']).split('|')
        
        for loc, label in zip(locations, labels):
            if loc < len(text_words):
                abbrev = text_words[loc].upper()
                label_clean = label.lower()
                
                if abbrev in selected and label_clean in selected[abbrev]:
                    filtered_rows.append({
                        'abbreviation': abbrev,
                        'text': row['TEXT'],
                        'location': loc,
                        'label': label_clean
                    })

filtered_df = pd.DataFrame(filtered_rows)
filtered_df.to_csv('./data/filtered_dataset.csv', index=False)
print(f"Saved {len(filtered_rows)} examples to filtered_dataset.csv")