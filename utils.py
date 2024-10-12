def get_diff(message: str) -> str:
    return message.split("```diff")[1].split("```")[0].strip()

def parse_udiff(udiff):
    changes = {}
    current_file = None

    for line in udiff.splitlines():
        if line.startswith('--- '):
            # Get the old file name
            current_file = line[4:].strip()  # Remove the '--- ' prefix
            changes[current_file] = []  # Initialize a list for changes
        elif line.startswith('+++ '):
            # Get the new file name
            new_file = line[4:].strip()  # Remove the '+++ ' prefix
            if current_file:
                changes[current_file].append({'new_file': new_file, 'changes': []})
        elif line.startswith('@@'):
            # This marks the start of a chunk of changes
            continue
        elif line.startswith('-'):
            # This line was removed
            if current_file and changes[current_file]:
                changes[current_file][-1]['changes'].append({'removed': line[1:].strip()})
        elif line.startswith('+'):
            # This line was added
            if current_file and changes[current_file]:
                changes[current_file][-1]['changes'].append({'added': line[1:].strip()})

    return changes
