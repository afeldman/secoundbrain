"""
Fabric adapter for secondbrain.

Purpose:
- Apply optional text structuring patterns inspired by Fabric
- Operates only on human-readable Markdown
- Does not evaluate or change meaning

This is presentation, not reasoning.
"""

from decouple import config

USE_FABRIC = config("SECONDBRAIN_USE_FABRIC", default="false").lower() == "true"

def apply_fabric_patterns(text: str) -> str:
    if not USE_FABRIC:
        return text

    # Simple deterministic structuring:
    lines = text.splitlines()
    structured = []
    for line in lines:
        # Normalize headings: ensure space after '#'
        if line.startswith('#'):
            line = line.replace('#', '# ', 1) if not line.startswith('# ') else line
        # Normalize bullets: use '- ' for all unordered lists
        if line.strip().startswith(('* ', '+ ', '- ')):
            line = '- ' + line.lstrip('*+- ').strip()
        structured.append(line)
    # Add section separation (double newline between headings)
    result = []
    for i, line in enumerate(structured):
        result.append(line)
        if line.startswith('#') and (i+1 < len(structured)) and not structured[i+1].startswith('#'):
            result.append('')
    return '\n'.join(result)
