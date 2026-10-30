#!/usr/bin/env python3
"""Compute LOC removed if every DELETE verdict in the WorldArchitect.AI
zero-code/strict-ZFC audit (run 2 + run-1 intent pilot) were applied.

Read-only: reads audit markdown under ~/workspace/plans/audit/ and the code
tree under ~/workspace/repos/worldarchitect.ai. Prints a JSON summary.

Method:
- Whole-file DELETEs: file-verdict tables / module-verdict headers stating
  DELETE (not DELETE-heavy, not MIXED, not conditional, not "DELETE from a
  claim"). Lines = exact `wc -l` of the file in the local tree.
- In-file DELETE symbols: table rows / frontend Phase-2 bullets whose
  verdict is DELETE. Spans: Python via AST (def/class/assign/import-alias
  spans, decorator-inclusive), JS via brace matching. Overlapping spans
  per file are merged so nested defs / methods of a deleted class count
  once. A bare name with several defs counts only when the file has at
  least as many DELETE rows naming it as there are defs (i.e. all of them
  are deleted); otherwise it is uncounted as ambiguous.
- Excluded: ADAPT, KEEP, MIXED (except explicitly named DELETE subsets in
  split rows, listed below), conditional/future DELETEs, test-only rework
  notes, branch-level deletions inside KEEP symbols (listed separately,
  no lines claimed), and anything whose span cannot be determined
  reliably (those go to `uncounted`, never into the total).
- Split-row manual mappings (audit text names the DELETE subset):
  * state memory_utils constants row -> MEMORY_SIMILARITY_THRESHOLD,
    AUTO_MEMORY_PREFIX
  * state game_state_merge constants row -> AMBIGUOUS_UPDATE_MARGIN,
    _CORE_MEMORY_VERB_KEYS
  * state firestore_service constants row -> REWARD_CLAIM_XP,
    REWARD_CLAIM_TANGIBLE, _RECONCILE_OWNED_STATE_KEYS,
    _RECONCILE_GAINED_SAFE_MAGNITUDE
    (_EXPERIENCE_READ_PROJECTION_KEYS left uncounted: subset ambiguous)
  * agents entity_instructions globals row -> entity_enforcement_checker,
    location_enforcer (+ their classes if uniquely resolvable)
"""
import ast
import fnmatch
import json
import re
from pathlib import Path

AUDIT = Path.home() / "workspace" / "plans" / "audit"
TREE = Path.home() / "workspace" / "repos" / "worldarchitect.ai"

GROUPS = {
    "gateway": "gateway-call-path.md",
    "state": "state-storage.md",
    "schema": "schema-parsing.md",
    "dice": "dice-mechanics.md",
    "godmode": "godmode-levelup-rewards.md",
    "faction": "faction-worldsim-time.md",
    "providers": "providers-auth.md",
    "logging": "logging-ops-incident.md",
    "scripts": "scripts-tests.md",
    "frontend": "frontend.md",
    "agents": "agents-prompts.md",
    "intent": "intent_classifier.md",
}

STATED = {
    "gateway": 38,
    "state": 100,   # 91 plain + 9 conditional
    "schema": 50,   # units (grouped rows expanded)
    "dice": 7,
    "logging": 3,   # 1 symbol row + 2 whole files
    "faction": 46,  # Phase 2 rows; Phase 1 files separate
    "godmode": 28,  # rows; +2 docs files separate
    "providers": 36,
    "scripts": 80,
    "frontend": None,
    "agents": None,
    "intent": 52,   # symbols, covered by 2 whole files
}

FILE_RE = re.compile(r"^[\w./-]+\.(?:py|js|css|md|html|txt|sh|json)$")
BACKTICK_RE = re.compile(r"`([^`]+)`")
HEADER_FILE_RE = re.compile(r"[`]?([\w./-]+\.(?:py|js|css|md|html|txt|sh|json))[`]?")
SKIP_SECTION_RE = re.compile(
    r"verdict totals|verdict counts|coverage —|coverage \(|remaining work|"
    r"what remains|conflicts flagged|method note|enumeration|prior-ledger|"
    r"retry plan|per-group files|coverage base|cross-checks|"
    r"top-level enumeration",
    re.IGNORECASE,
)
COND_PAREN = ("per-turn", "turn path", "corrector", "value reconciliation",
              "server function")

SPLIT_MIXED = {
    ("state", "memory_utils.py"): ["MEMORY_SIMILARITY_THRESHOLD", "AUTO_MEMORY_PREFIX"],
    ("state", "game_state_merge.py"): ["AMBIGUOUS_UPDATE_MARGIN", "_CORE_MEMORY_VERB_KEYS"],
    ("state", "firestore_service.py"): [
        "REWARD_CLAIM_XP", "REWARD_CLAIM_TANGIBLE",
        "_RECONCILE_OWNED_STATE_KEYS", "_RECONCILE_GAINED_SAFE_MAGNITUDE",
    ],
}
# Manual tree-wide symbol lookups (audit prose names a DELETE symbol whose
# row lives outside a table, e.g. frontend §9 verification notes).
MANUAL_TREE_SYMBOLS = [
    ("frontend", "assemble_campaign_portrait_context"),
]


def clean_cell(cell):
    return cell.strip().strip("*").strip()


def is_filename_token(tok):
    tok = tok.strip().rstrip("†").strip()
    tok = re.sub(r"\s*\(.*\)\s*$", "", tok)
    return bool(FILE_RE.match(tok))


def filename_of(tok):
    tok = tok.strip().rstrip("†").strip()
    tok = re.sub(r"\s*\(.*\)\s*$", "", tok)
    return tok


def norm_symbol(tok):
    tok = tok.strip()
    tok = re.sub(r"\(.*\)$", "", tok)
    return tok.strip()


def symbol_ok(tok):
    if not tok or " " in tok or '"' in tok or "'" in tok:
        return False
    if "/" in tok:
        return False
    if tok.startswith("L") and tok[1:].isdigit():
        return False
    return bool(re.match(r"^[A-Za-z_][\w.]*$", tok))


def verdict_segment(row_text, cells):
    """Extract the verdict-bearing segment of a symbol row."""
    m = re.search(r"Verdict:\s*(.+?)(?:\||$)", row_text)
    if m:
        return m.group(1).strip()
    m = re.search(r"\*\*(DELETE|KEEP|ADAPT)\b[^*]*\*\*", row_text)
    if m:
        return m.group(0)
    if cells:
        last = cells[-1].strip()
        if last:
            return last
    return row_text


def is_conditional(seg):
    if re.search(r"DELETE\s*\(([^)]*)\)", seg):
        paren = re.search(r"DELETE\s*\(([^)]*)\)", seg).group(1).lower()
        if any(p in paren for p in COND_PAREN):
            return True
    if "/ ADAPT" in seg and seg.startswith("DELETE"):
        return True
    if re.search(r"DELETE\b.*\bkeep\b.*\bonly\b", seg, re.IGNORECASE):
        return True
    if re.search(r"DELETE\b.*ADAPT\b.*migration", seg, re.IGNORECASE):
        return True
    return False


def row_verdict(row_text, cells):
    """'delete', 'conditional', 'mixed', or None for a symbol (non-file) row."""
    seg = verdict_segment(row_text, cells)
    if re.search(r"\bMIXED\b", seg) and "DELETE" not in seg:
        return "mixed"
    if re.search(r"\bMIXED\b", seg):
        return "mixed"
    # bold DELETE (with optional parenthetical inside the bold)
    if re.search(r"\*\*DELETE\b[^*]*\*\*", row_text):
        # a row that is really KEEP-with-deleted-branches is not a DELETE row
        if re.search(r"\*\*KEEP\b", row_text) and "branches deleted" in row_text:
            return None
        if is_conditional(seg):
            return "conditional"
        return "delete"
    if re.search(r"Verdict:\s*DELETE\b", row_text):
        if is_conditional(seg):
            return "conditional"
        return "delete"
    stripped = row_text.strip().rstrip("|").strip()
    if re.search(r"→\s*DELETE\s*$", stripped):
        return "delete"
    if cells:
        last = cells[-1].strip()
        if last == "DELETE" or re.search(r"(?:^|\s)DELETE\.?$", last):
            return "delete"
    return None


def parse_group(group, fname):
    text = (AUDIT / fname).read_text()
    whole = set()
    rows = []
    cond = 0
    cond_detail = []
    splits = []
    branch_notes = []
    context = None
    bullet_mode = False
    skip_mode = False
    for line in text.splitlines():
        s = line.strip()
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            level, head = m.group(1), m.group(2)
            if SKIP_SECTION_RE.search(head):
                skip_mode = True
                context = None
                bullet_mode = False
                continue
            skip_mode = False
            if level == "##":
                bullet_mode = bool(group == "frontend"
                                   and "Phase 2" in head)
            fm = HEADER_FILE_RE.search(head)
            if fm:
                context = fm.group(1)
                low = head.lower()
                if "delete" in low and (
                    "whole file" in low or "as a module" in low
                    or "in full" in low or "module verdict: delete" in low
                    or "file verdict: delete" in low
                    or "delete from the shipped path" in low
                ):
                    if "except" in low and "except nothing" not in low:
                        pass  # partial: symbol rows govern
                    else:
                        whole.add(context)
            elif level == "##":
                context = None
            continue
        if skip_mode:
            continue
        if context and re.search(
                r"(module|file) verdict:\s*DELETE\b", s, re.IGNORECASE):
            low = s.lower()
            if "except" in low and "except nothing" not in low:
                pass
            else:
                whole.add(context)
            continue
        if group == "frontend":
            bm = re.match(r"^\*\*`([^`]+)`\s*—\s*DELETE \(whole file", s)
            if bm:
                whole.add(bm.group(1))
                context = bm.group(1)
                continue
        if bullet_mode and s.startswith("- ") and "`" in s:
            tail_txt = ""
            em = s.rfind("—")
            if em != -1:
                tail_txt = s[em + 1:].strip()
            head_part = s.split(":", 1)[0]
            toks = [norm_symbol(t) for t in BACKTICK_RE.findall(head_part)]
            syms = [t for t in toks if symbol_ok(t)]
            if re.match(r"^DELETE\b", tail_txt):
                if "or delete it with the group" in s:
                    mm = re.search(r"make `([^`]+)`", s)
                    if mm and mm.group(1) in syms:
                        syms = [x for x in syms if x != mm.group(1)]
                        splits.append(("frontend-bullet-alt", context, s[:120]))
                if syms and context:
                    rows.append({"file": context, "symbols": syms, "raw": s[:160]})
            elif re.search(r"ADAPT:.*DELETE\s+`", s):
                idx = s.find("DELETE")
                after = BACKTICK_RE.findall(s[idx:])
                syms2 = [norm_symbol(t) for t in after if symbol_ok(norm_symbol(t))]
                if syms2 and context:
                    rows.append({"file": context, "symbols": syms2, "raw": s[:160]})
            continue
        if not s.startswith("|"):
            continue
        if re.match(r"^\|[\s:|-]+\|$", s):
            continue
        cells = [c.strip() for c in s.strip().strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        if first.lower() in ("file", "symbol", "unit", "files") or (
                len(cells) > 1 and cells[1].lower() == "status"):
            continue
        toks = BACKTICK_RE.findall(first)
        file_toks = [filename_of(t) for t in toks if is_filename_token(t)]
        is_file_row = False
        if toks and file_toks and len(file_toks) == len(toks):
            is_file_row = True
        elif not toks and is_filename_token(first):
            file_toks = [filename_of(first)]
            is_file_row = True
        if is_file_row:
            # verdict: any cell starting with DELETE, or last cell ending
            # with bold **DELETE** (scripts-style per-file rows)
            v_delete = False
            v_cond = False
            for c in cells[1:]:
                cc = clean_cell(c)
                if re.match(r"^DELETE\b", cc, re.IGNORECASE) \
                        and "delete-heavy" not in cc.lower() \
                        and "mixed" not in cc.lower() \
                        and " or adapt" not in cc.lower() \
                        and "delete from any runtime" not in cc.lower():
                    if is_conditional(cc):
                        v_cond = True
                    else:
                        v_delete = True
            last = cells[-1] if cells else ""
            if re.search(r"\*\*DELETE\b[^*]*\*\*\s*$", last):
                v_delete = True
            if v_delete and not v_cond:
                for f in file_toks:
                    whole.add(f)
            elif v_cond:
                cond += 1
            continue
        # symbol row: extract symbols first (shared by delete/cond paths)
        fref = context
        syms = []
        first_trunc = first.split("(incl.")[0]
        toks_trunc = BACKTICK_RE.findall(first_trunc)
        for t in toks_trunc:
            if "::" in t:
                fref = t.split("::", 1)[0]
                sym = norm_symbol(t.split("::", 1)[1])
                if symbol_ok(sym):
                    syms.append(sym)
            else:
                sym = norm_symbol(t)
                if symbol_ok(sym):
                    syms.append(sym)
        if not toks_trunc:
            plain = re.sub(r"\s*\(.*\)\s*$", "", first).strip()
            for part in re.split(r"[,/]", plain):
                part = part.strip()
                if symbol_ok(part):
                    syms.append(part)
        v = row_verdict(s, cells)
        if v == "conditional":
            cond += 1
            if syms and fref:
                cond_detail.append({"file": fref, "symbols": syms,
                                    "raw": s[:160]})
            continue
        if v == "mixed":
            splits.append(("mixed", context, s[:200]))
            continue
        if v is None:
            # KEEP row naming deleted branches (branch-level, unspanned)
            if re.search(r"\bKEEP\b", s) and (
                    "branches deleted" in s or "branch DELETEs" in s):
                branch_notes.append((context, s[:160]))
            continue
        if re.search(r"\*\*KEEP\b", s) and re.search(r"\*\*DELETE\b", s):
            splits.append(("both-bold", context, s[:200]))
            continue
        if syms and fref:
            rows.append({"file": fref, "symbols": syms, "raw": s[:160]})
        elif syms and not fref:
            splits.append(("no-context", None, s[:160]))
    return whole, rows, cond, cond_detail, splits, branch_notes


# ---------------- tree index & resolution ----------------

def build_index():
    relpaths = set()
    by_base = {}
    for p in TREE.rglob("*"):
        if p.is_file():
            rel = str(p.relative_to(TREE))
            relpaths.add(rel)
            by_base.setdefault(p.name, []).append(rel)
    return relpaths, by_base


RELPATHS, BY_BASE = build_index()


def _pick(cands, group):
    if not cands:
        return None
    if len(cands) == 1:
        return cands[0]

    def score(p):
        if group == "scripts":
            if p.startswith("scripts/"):
                return 0
            if "/" not in p:
                return 1
            if p.startswith("mvp_site/") and "/tests/" not in p:
                return 2
            return 3
        if p.startswith("mvp_site/") and "/tests/" not in p:
            return 0
        if p.startswith("mvp_site/"):
            return 1
        if "/" not in p:
            return 2
        return 3

    ranked = sorted(cands, key=score)
    if len(ranked) > 1 and score(ranked[0]) == score(ranked[1]):
        return None
    return ranked[0]


def resolve(ref, group):
    if "/" in ref and ref in RELPATHS:
        return ref
    cands = [p for p in RELPATHS if p.endswith("/" + ref)]
    if not cands:
        cands = BY_BASE.get(ref.split("/")[-1], [])
    return _pick(cands, group)


def resolve_glob(ref, group):
    if "*" not in ref:
        return []
    base_pat = ref.split("/")[-1]
    dir_part = "/".join(ref.split("/")[:-1])
    out = []
    for p in RELPATHS:
        if dir_part and ("/" + dir_part + "/") not in ("/" + p):
            continue
        if fnmatch.fnmatch(p.split("/")[-1], base_pat):
            out.append(p)
    return sorted(out)


def wc_lines(rel):
    data = (TREE / rel).read_bytes()
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


# ---------------- spans ----------------

def py_spans(rel):
    try:
        src = (TREE / rel).read_text()
        tree = ast.parse(src)
    except Exception:
        return None
    index = {}

    def add(key, span):
        if key not in index:
            index[key] = []
        if span not in index[key]:
            index[key].append(span)

    def visit(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                q = f"{prefix}.{child.name}" if prefix else child.name
                span = (child.lineno, child.end_lineno or child.lineno)
                add(child.name, span)
                if q != child.name:
                    add(q, span)
                visit(child, q)
            elif isinstance(child, ast.Assign):
                span = (child.lineno, child.end_lineno or child.lineno)
                for t in child.targets:
                    if isinstance(t, ast.Name):
                        add(t.id, span)
                    elif isinstance(t, (ast.Tuple, ast.List)):
                        for el in t.elts:
                            if isinstance(el, ast.Name):
                                add(el.id, span)
            elif isinstance(child, ast.AnnAssign):
                span = (child.lineno, child.end_lineno or child.lineno)
                if isinstance(child.target, ast.Name):
                    add(child.target.id, span)
            elif isinstance(child, ast.ImportFrom):
                span = (child.lineno, child.end_lineno or child.lineno)
                for a in child.names:
                    add(a.asname or a.name, span)
            elif isinstance(child, ast.Import):
                span = (child.lineno, child.end_lineno or child.lineno)
                for a in child.names:
                    add(a.asname or a.name.split(".")[0], span)
            else:
                visit(child, prefix)

    visit(tree, "")
    return index


def py_toplevel_spans(rel):
    """{name: span} for direct module children only; None if unparseable.
    A name defined twice at top level maps to None (ambiguous)."""
    try:
        src = (TREE / rel).read_text()
        tree = ast.parse(src)
    except Exception:
        return None
    out = {}

    def put(name, span):
        if name in out:
            out[name] = None
        else:
            out[name] = span

    for child in tree.body:
        span = (child.lineno, child.end_lineno or child.lineno)
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            put(child.name, span)
        elif isinstance(child, ast.Assign):
            for t in child.targets:
                if isinstance(t, ast.Name):
                    put(t.id, span)
                elif isinstance(t, (ast.Tuple, ast.List)):
                    for el in t.elts:
                        if isinstance(el, ast.Name):
                            put(el.id, span)
        elif isinstance(child, ast.AnnAssign):
            if isinstance(child.target, ast.Name):
                put(child.target.id, span)
        elif isinstance(child, ast.ImportFrom):
            for a in child.names:
                put(a.asname or a.name, span)
        elif isinstance(child, ast.Import):
            for a in child.names:
                put(a.asname or a.name.split(".")[0], span)
    return out


def merge_intervals(intervals):
    if not intervals:
        return []
    iv = sorted(intervals)
    out = [list(iv[0])]
    for s, e in iv[1:]:
        if s <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def js_span(lines, symbol):
    name = symbol.split(".")[-1]
    pats = [
        re.compile(r"\bfunction\s+" + re.escape(name) + r"\s*\("),
        re.compile(r"\b" + re.escape(name) + r"\s*=\s*async\s*\("),
        re.compile(r"\b" + re.escape(name) + r"\s*=\s*function\s*\("),
        re.compile(r"\b(?:const|let|var)\s+" + re.escape(name) + r"\s*="),
        re.compile(r"\b" + re.escape(name) + r"\s*:\s*function\s*\("),
        re.compile(r"\b" + re.escape(name) + r"\s*\([^)]*\)\s*\{"),
        re.compile(r"\b" + re.escape(name) + r"\s*=\s*\{"),
    ]
    for i, ln in enumerate(lines):
        for pat in pats:
            m = pat.search(ln)
            if not m:
                continue
            for j in range(i, min(i + 7, len(lines))):
                k = lines[j].find("{", m.end() if j == i else 0)
                if k != -1:
                    depth = 0
                    for jj in range(j, len(lines)):
                        seg = re.sub(r"//.*", "", lines[jj])
                        depth += seg.count("{") - seg.count("}")
                        if depth == 0 and jj >= j:
                            return (i + 1, jj + 1)
                    return None
            return None
    return None


# ---------------- driver ----------------

def main():
    result = {"whole_files": {}, "in_file": {}, "uncounted": [],
              "per_group": {}, "branch_notes": [], "cond_detail": []}
    whole_resolved = {}
    whole_missing = []
    whole_glob = {}
    for group, fname in GROUPS.items():
        if group == "intent":
            continue
        whole, rows, cond, cond_detail, splits, branch_notes = parse_group(
            group, fname)
        result["cond_detail"].extend(
            {"group": group, **cd} for cd in cond_detail)
        expanded = set()
        for ref in whole:
            if "*" in ref:
                hits = resolve_glob(ref, group)
                whole_glob[ref] = hits
                expanded.update(hits)
            else:
                expanded.add(ref)
        resolved_whole = {}
        for ref in expanded:
            r = ref if ("/" in ref and ref in RELPATHS) else resolve(ref, group)
            if r:
                resolved_whole[r] = ref
                whole_resolved.setdefault(r, (group, ref))
            else:
                whole_missing.append((group, ref))
        result["per_group"][group] = {
            "whole_file_refs": sorted(expanded),
            "whole_resolved": resolved_whole,
            "delete_rows_found": len(rows),
            "cond_rows": cond,
            "split_rows": splits,
            "symbol_rows": rows,
        }
        result["branch_notes"].extend(
            {"group": group, "file": b[0], "raw": b[1]} for b in branch_notes)
    for ref in ("mvp_site/intent_classifier.py",
                "mvp_site/intent_classifier_warmup.py"):
        whole_resolved[ref] = ("intent", ref)
    # godmode docs: prose-only whole-file DELETE (2 files in dir)
    for rel in ("mvp_site/docs/zfc_audit/FULL_AUDIT.md",
                "mvp_site/docs/zfc_audit/SUMMARY.md"):
        if rel in RELPATHS:
            whole_resolved.setdefault(rel, ("godmode", "mvp_site/docs/zfc_audit/"))
    result["per_group"]["intent"] = {
        "whole_file_refs": ["mvp_site/intent_classifier.py",
                            "mvp_site/intent_classifier_warmup.py"],
        "whole_resolved": {r: r for r in
                           ("mvp_site/intent_classifier.py",
                            "mvp_site/intent_classifier_warmup.py")},
        "delete_rows_found": 52, "cond_rows": 0, "split_rows": [],
        "symbol_rows": [],
    }
    manual = [
        ("state", "memory_utils.py", SPLIT_MIXED[("state", "memory_utils.py")]),
        ("state", "game_state_merge.py", SPLIT_MIXED[("state", "game_state_merge.py")]),
        ("state", "firestore_service.py", SPLIT_MIXED[("state", "firestore_service.py")]),
        ("agents", "entity_instructions.py",
         ["entity_enforcement_checker", "location_enforcer"]),
        # logging DELETE row covers log_dice_roll "with its DICE_TABLE constant"
        ("logging", "bq_logging.py", ["DICE_TABLE"]),
    ]
    whole_table = []
    for rel in sorted(whole_resolved):
        grp, ref = whole_resolved[rel]
        try:
            n = wc_lines(rel)
        except Exception:
            n = None
        whole_table.append({"file": rel, "group": grp, "ref": ref, "lines": n})
    result["whole_files"] = {"table": whole_table,
                             "missing": whole_missing,
                             "glob_expansions": whole_glob}
    py_cache = {}
    in_file_rows = []
    uncounted = []

    def resolve_symbol(group, rel, symbol, row_count):
        """Return span list or None (caller records uncounted)."""
        ext = rel.rsplit(".", 1)[-1]
        if ext == "py":
            if rel not in py_cache:
                py_cache[rel] = py_spans(rel)
            idx = py_cache[rel]
            if idx is None:
                return None, "AST parse failed"
            spans = idx.get(symbol)
            if not spans:
                alt = symbol.split(".")[-1]
                spans = idx.get(alt) if alt != symbol else None
            if not spans:
                return None, "symbol not found in AST"
            if len(spans) > 1 and row_count < len(spans):
                return None, f"ambiguous subset ({row_count} rows, {len(spans)} defs)"
            return spans, None
        if ext == "js":
            lines = (TREE / rel).read_text(errors="replace").splitlines()
            sp = js_span(lines, symbol)
            if sp:
                return [sp], None
            return None, "JS span not determinable"
        return None, f"no span method for .{ext}"

    # row multiplicity per (group, file, symbol) for the ambiguous rule
    row_counts = {}
    all_rows = []
    for group, fname in GROUPS.items():
        if group == "intent":
            continue
        for row in result["per_group"][group]["symbol_rows"]:
            all_rows.append((group, row))
            fref = row["file"]
            rel = fref if ("/" in fref and fref in RELPATHS) else resolve(fref, group)
            if rel:
                for s in row["symbols"]:
                    row_counts[(group, rel, s)] = row_counts.get((group, rel, s), 0) + 1
    for group, row in all_rows:
        fref = row["file"]
        rel = fref if ("/" in fref and fref in RELPATHS) else resolve(fref, group)
        if not rel:
            for s in row["symbols"]:
                uncounted.append({"group": group, "file_ref": fref,
                                  "symbol": s, "reason": "file unresolvable"})
            continue
        if rel in whole_resolved:
            continue
        module_state = "(module state)" in row["raw"]
        for s in row["symbols"]:
            if module_state and rel.endswith(".py"):
                tls = py_toplevel_spans(rel)
                if tls is not None and tls.get(s):
                    in_file_rows.append({"group": group, "file": rel,
                                         "symbol": s, "span": tls[s],
                                         "note": "module-state top-level"})
                    continue
                if tls is not None:
                    uncounted.append({"group": group, "file": rel,
                                      "symbol": s,
                                      "reason": "module-state span not isolated at top level"})
                    continue
            rc = row_counts.get((group, rel, s), 1)
            spans, err = resolve_symbol(group, rel, s, rc)
            if spans:
                for sp in spans:
                    in_file_rows.append({"group": group, "file": rel,
                                         "symbol": s, "span": sp})
            else:
                uncounted.append({"group": group, "file": rel,
                                  "symbol": s, "reason": err})
    for group, base, syms in manual:
        rel = resolve(base, group)
        if not rel:
            for s in syms:
                uncounted.append({"group": group, "file_ref": base, "symbol": s,
                                  "reason": "file unresolvable"})
            continue
        if rel not in py_cache:
            py_cache[rel] = py_spans(rel)
        idx = py_cache[rel] or {}
        for s in syms:
            spans = idx.get(s)
            if spans and len(spans) == 1:
                in_file_rows.append({"group": group, "file": rel, "symbol": s,
                                     "span": spans[0], "note": "split-row subset"})
            else:
                uncounted.append({"group": group, "file": rel, "symbol": s,
                                  "reason": "split-row symbol not uniquely found"})
    # Manual tree-wide symbol (frontend §9 verification note). Grep first
    # so only files actually defining the symbol get AST-parsed.
    for group, symbol in MANUAL_TREE_SYMBOLS:
        hits = []
        for rel in sorted(RELPATHS):
            if not rel.startswith("mvp_site/") or not rel.endswith(".py"):
                continue
            if "/tests/" in rel or rel.split("/")[-1].startswith("test_"):
                continue  # prod def only; test callers are rework, not removal
            try:
                with open(TREE / rel, "rb") as fh:
                    if ("def " + symbol + "(").encode() not in fh.read():
                        continue
            except Exception:
                continue
            if rel not in py_cache:
                py_cache[rel] = py_spans(rel)
            idx = py_cache[rel] or {}
            if symbol in idx and len(idx[symbol]) == 1:
                hits.append((rel, idx[symbol][0]))
        if len(hits) == 1:
            in_file_rows.append({"group": group, "file": hits[0][0],
                                 "symbol": symbol, "span": hits[0][1],
                                 "note": "§9 verification note"})
        else:
            uncounted.append({"group": group, "file_ref": "tree-wide",
                              "symbol": symbol,
                              "reason": f"tree-wide lookup found {len(hits)} defs"})
    # agents globals row: classes named with the globals, if uniquely found
    rel_ei = resolve("entity_instructions.py", "agents")
    if rel_ei:
        if rel_ei not in py_cache:
            py_cache[rel_ei] = py_spans(rel_ei)
        idx = py_cache[rel_ei] or {}
        for cls in ("EntityEnforcementChecker", "LocationEntityEnforcer",
                    "LocationEnforcer", "EntityEnforcement"):
            if cls in idx and len(idx[cls]) == 1:
                in_file_rows.append({"group": "agents", "file": rel_ei,
                                     "symbol": cls, "span": idx[cls][0],
                                     "note": "globals row 'with their classes'"})
    by_file = {}
    for r in in_file_rows:
        by_file.setdefault(r["file"], []).append(r["span"])
    in_file_table = []
    for rel in sorted(by_file):
        merged = merge_intervals(by_file[rel])
        total = sum(e - s + 1 for s, e in merged)
        in_file_table.append({"file": rel, "symbols": len(by_file[rel]),
                              "merged_spans": merged, "lines": total})
    result["in_file"] = {"table": in_file_table, "rows": in_file_rows}
    result["uncounted"] = uncounted
    pg = {}
    for r in in_file_rows:
        pg.setdefault(r["group"], []).append(r)
    result["per_group_in_file"] = {}
    for g, rs in pg.items():
        bf = {}
        for r in rs:
            bf.setdefault(r["file"], []).append(r["span"])
        tot = 0
        for rel, spans in bf.items():
            for s, e in merge_intervals(spans):
                tot += e - s + 1
        result["per_group_in_file"][g] = {"symbols": len(rs), "lines": tot}
    print(json.dumps(result, indent=1, default=str))


if __name__ == "__main__":
    main()
