import random
import pandas as pd

keywords = {
    'CC': {
        'colorectal cancer': ['colon', 'rectal', 'tumor', 'polyp', 'screening', 'bowel', 'adenocarcinoma'],
        'cell culture': ['medium', 'serum', 'flask', 'incubation', 'confluent', 'passage', 'cells'],
        'cervical cancer': ['HPV', 'screening', 'women', 'pap', 'uterine', 'cervix', 'gynecologic']
    },
    'CP': {
        'chronic pain': ['persistent', 'management', 'opioid', 'fibromyalgia', 'neuropathic', 'syndrome'],
        'chest pain': ['cardiac', 'angina', 'myocardial', 'thoracic', 'ECG', 'infarction'],
        'cerebral palsy': ['motor', 'developmental', 'spastic', 'children', 'disability', 'pediatric']
    },
    'SA': {
        'surface area': ['volume', 'ratio', 'measurement', 'calculated', 'cm2', 'size'],
        'sleep apnea': ['obstructive', 'CPAP', 'snoring', 'breathing', 'apneic', 'episodes'],
        'substance abuse': ['addiction', 'drugs', 'alcohol', 'treatment', 'dependence', 'rehabilitation']
    }
}

templates = [
    "Patient with {abbrev} showing {kw1} and {kw2} findings",
    "The {abbrev} diagnosis revealed {kw1} with {kw2} present",
    "Treatment for {abbrev} included {kw1} and {kw2} interventions",
    "Study examined {abbrev} patients with {kw1} and {kw2}",
    "{abbrev} assessment showed {kw1} and {kw2} indicators",
    "Research on {abbrev} identified {kw1} and {kw2} patterns",
    "Clinical presentation of {abbrev} included {kw1} and {kw2}",
    "Analysis of {abbrev} demonstrated {kw1} with {kw2}",
    "The {abbrev} case exhibited {kw1} and {kw2} characteristics",
    "Evaluation of {abbrev} detected {kw1} and {kw2} markers",
    "Investigation into {abbrev} found {kw1} with {kw2} evidence",
    "Medical report documented {abbrev} with {kw1} and {kw2}",
    "Screening for {abbrev} revealed {kw1} and {kw2} signs",
    "Diagnosis of {abbrev} confirmed {kw1} and {kw2} features",
    "Monitoring {abbrev} showed {kw1} and {kw2} progression"
]

synthetic_data = []
examples_per_meaning = 200
seen_texts = set()

for abbrev, meanings in keywords.items():
    for meaning, kw_list in meanings.items():
        generated = 0
        attempts = 0
        max_attempts = examples_per_meaning * 10
        
        while generated < examples_per_meaning and attempts < max_attempts:
            template = random.choice(templates)
            kw1 = random.choice(kw_list)
            kw2 = random.choice(kw_list)
            
            text = template.format(abbrev=abbrev, kw1=kw1, kw2=kw2)
            
            if text not in seen_texts:
                seen_texts.add(text)
                words = text.split()
                location = words.index(abbrev)
                
                synthetic_data.append({
                    'abbreviation': abbrev,
                    'text': text,
                    'location': location,
                    'label': meaning
                })
                generated += 1
            
            attempts += 1

synthetic_df = pd.DataFrame(synthetic_data)
synthetic_df.to_csv('./data/synthetic_dataset.csv', index=False)
print(f"Generated {len(synthetic_data)} unique synthetic examples")

