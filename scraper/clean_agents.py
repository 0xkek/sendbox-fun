"""
Clean up agents.json: remove academic/research/noise entries that shouldn't be there.
"""
import json
import re
from pathlib import Path

PATH = Path(__file__).parent.parent / "agents.json"

ACADEMIC_TERMS = [
    'dataset', 'benchmark', 'arxiv', 'ethics of', 'survey of',
    'analysis of', 'towards', 'introduction to', 'lecture', 'course',
    'thesis', 'dissertation', 'research paper', 'conference',
    'workshop', 'symposium', 'journal', 'proceedings',
    'simulation', 'evaluation of', 'case study', 'white paper',
    'ai ethics', 'ai safety', 'xai ', 'explainable ai',
    'chapter', 'part 1', 'part 2', 'module', 'curriculum',
    'homework', 'assignment', 'tutorial series',
]

BLOCKED_DOMAINS = [
    'sites.google.com', 'docs.google.com', 'forms.gle',
    'neurips.cc', 'iclr.cc', 'icml.cc', 'aclweb.org',
    'towardsdatascience.com', 'towardsai.net',
    '.edu/', '.ac.uk/', '.ac.jp/', 'umich.edu', 'mit.edu', 'stanford.edu',
    'github.io/courses', 'github.io/lecture', 'github.io/syllabus',
    'kaggle.com/datasets',
]


def should_remove(agent):
    name = agent.get('name', '')
    name_lower = name.lower()
    url = agent.get('url', '').lower()

    # Name length
    if len(name) > 60 or len(name) < 2:
        return True, "name length"
    # Too many words = sentence
    if name.count(' ') > 5:
        return True, "sentence-like name"
    # Academic terms
    for term in ACADEMIC_TERMS:
        if term in name_lower:
            return True, f"academic term: {term}"
    # Long technical IDs
    if '_' in name and name.islower() and len(name) > 25:
        return True, "technical id"
    # Dataset-style names with years
    if re.search(r'\d{4}', name) and ('-' in name or '_' in name):
        return True, "dataset-style name"
    # Blocked domains
    for d in BLOCKED_DOMAINS:
        if d in url:
            return True, f"blocked domain: {d}"
    return False, None


def main():
    with open(PATH) as f:
        data = json.load(f)

    keep = []
    removed = []
    for a in data['agents']:
        # Never remove manually-added or bulk-imported entries
        if a.get('source', '').startswith('manual') or a.get('source') == 'bulk-import':
            keep.append(a)
            continue
        remove, reason = should_remove(a)
        if remove:
            removed.append((a['name'], reason))
        else:
            keep.append(a)

    print(f"Kept: {len(keep)}")
    print(f"Removed: {len(removed)}")
    print("\nSample removals:")
    for name, reason in removed[:30]:
        print(f"  - {name} ({reason})")

    data['agents'] = keep
    with open(PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\nSaved {len(keep)} agents to {PATH}")


if __name__ == '__main__':
    main()
