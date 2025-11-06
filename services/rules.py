import re
import unicodedata
from difflib import SequenceMatcher
from typing import Tuple, Dict, Optional

# Lightweight rules module to detect document type keywords and apply a rule-based boost/override

KEYWORDS = {
    "Factura": ["factura", "fact.", "fact"],
    "Remito": ["remito", "rem."],
    "Nota de Credito": ["nota de credito", "nota credito", "nota_credito", "nota de crédito", "nota crédito"],
    "Nota de Debito": ["nota de debito", "nota debito", "nota_debito", "nota de débito", "nota débito"],
}


def normalize(text: str) -> str:
    t = text.lower()
    t = unicodedata.normalize("NFD", t)
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    return t


def fuzzy_match(a: str, b: str) -> float:
    # Return a similarity ratio 0..100 using SequenceMatcher
    return int(SequenceMatcher(None, a, b).ratio() * 100)


def keyword_in_text(text: str, variants: list, fuzzy_thresh: int = 85) -> Tuple[bool, str]:
    norm = normalize(text)
    for v in variants:
        vnorm = normalize(v)
        if vnorm in norm:
            return True, "exact"
        # check fuzzy on short snippets
        score = fuzzy_match(vnorm, norm)
        if score >= fuzzy_thresh:
            return True, "fuzzy"
    return False, "none"


def extract_header_lines(text: str, max_lines: int = 6) -> str:
    # take first max_lines non-empty lines
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return "\n".join(lines[:max_lines])


def detect_document_keyword(text: str) -> Tuple[Optional[str], str, str]:
    """
    Inspect header and full text for document keywords.
    Returns (label, where, kind) where where in {'header','body'}, kind in {'exact','fuzzy','none'}
    """
    header = extract_header_lines(text, max_lines=6)
    # Check each header line individually and record matches with position
    lines = [ln.strip() for ln in header.splitlines() if ln.strip()]
    matches = []  # list of tuples (label, line_index, kind, match_variant)
    for i, line in enumerate(lines):
        for label, variants in KEYWORDS.items():
            for v in variants:
                vnorm = normalize(v)
                lnorm = normalize(line)
                if vnorm in lnorm:
                    matches.append((label, i, 'exact', v))
                else:
                    score = fuzzy_match(vnorm, lnorm)
                    if score >= 85:
                        matches.append((label, i, 'fuzzy', v))

    if matches:
        # sort by: kind (exact first), then line index (smaller first), then length of variant (longer first)
        def score_key(m):
            kind_rank = 0 if m[2] == 'exact' else 1
            return (kind_rank, m[1], -len(m[3]))

        best = sorted(matches, key=score_key)[0]
        return best[0], 'header', best[2]

    # fallback to whole text (body) - simpler check
    for label, variants in KEYWORDS.items():
        found, kind = keyword_in_text(text, variants)
        if found:
            return label, 'body', kind

    return None, 'none', 'none'


def apply_rule_boost(predicted_label: str, probs: Dict[str, float], text: str,
                     boost_amount: float = 0.25, fuzzy_thresh: int = 85) -> Tuple[str, str]:
    """
    Apply a rule-based boost or override.
    - If exact header match -> override (return rule label)
    - Else if fuzzy/header -> boost probability for rule label and return top label
    - Otherwise return original prediction
    Returns (final_label, reason)
    """
    rule_label, where, kind = detect_document_keyword(text)
    if not rule_label:
        return predicted_label, "no_rule"

    # aggressive override for exact header matches
    if where == "header" and kind == "exact":
        return rule_label, "rule_override_header_exact"

    # otherwise boost the probability for the rule label
    probs = probs.copy()
    if rule_label in probs:
        probs[rule_label] = min(1.0, probs[rule_label] + boost_amount)
    else:
        # if label not present in probs mapping, add small score
        probs[rule_label] = boost_amount

    # choose max
    final_label = max(probs.items(), key=lambda kv: kv[1])[0]
    return final_label, f"rule_boost_{where}_{kind}"
