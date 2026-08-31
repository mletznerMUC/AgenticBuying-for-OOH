#!/usr/bin/env python3
"""Consistency checks for the additions registry, release manifests and links.

Run from the repository root:  python3 scripts/validate.py

Checks:
  1. Every addition file has parseable front matter with the required keys.
  2. The ID in the front matter matches the file name, and IDs are unique.
  3. Field values are in the allowed sets (status, applies_to, target surfaces).
  4. Versions are valid SemVer, and a `stable` addition is >= 1.0.0.
  5. REGISTRY.md lists every addition, at the version its front matter declares.
  6. Every release manifest pins versions that exist.
  7. Every relative markdown link in the repository resolves.
"""
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADD_DIR = os.path.join(ROOT, "additions")

REQUIRED = {"id", "title", "version", "status", "supersedes", "superseded_by",
            "origin", "targets", "applies_to", "protocol_ownership",
            "upstream_status"}
PROTOCOLS = {"adcp", "aamp"}
UPSTREAM = {"exists", "partial", "gap"}
STATUSES = {"draft", "review", "stable", "deprecated", "superseded", "withdrawn"}
APPLIES = {"programmatic", "io"}
ADCP = {"media-buy", "creative", "signals", "accounts", "governance",
        "accounts-and-governance", "trusted-match"}
AAMP = {"artf", "agentic-direct", "agentic-audiences", "registry",
        "agent-sdks-and-registry", "trust-and-transparency", "buyer-agent"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

errors, warnings = [], []


def err(m):
    errors.append(m)


def warn(m):
    warnings.append(m)


def front_matter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    return yaml.safe_load(text[4:end])


def check_additions():
    additions = {}
    files = sorted(
        os.path.relpath(os.path.join(dp, f), ADD_DIR)
        for dp, _, fns in os.walk(ADD_DIR)
        for f in fns
        if f.startswith("ADD-") and f.endswith(".md"))
    if not files:
        err("no addition files found")
    for fn in files:
        path = os.path.join(ADD_DIR, fn)
        fm = front_matter(path)
        if fm is None:
            err(f"{fn}: missing or unparseable front matter")
            continue
        missing = REQUIRED - set(fm)
        if missing:
            err(f"{fn}: front matter missing keys: {sorted(missing)}")
            continue

        base = os.path.basename(fn)
        file_id = base.split("-")[0] + "-" + base.split("-")[1]
        if fm["id"] != file_id:
            err(f"{fn}: front matter id {fm['id']!r} != file name id {file_id!r}")
        if fm["id"] in additions:
            err(f"{fn}: duplicate id {fm['id']}")
        additions[fm["id"]] = (fm, fn)

        if not SEMVER.match(str(fm["version"])):
            err(f"{fn}: version {fm['version']!r} is not MAJOR.MINOR.PATCH")
        if fm["status"] not in STATUSES:
            err(f"{fn}: unknown status {fm['status']!r}")
        if fm["status"] == "stable" and str(fm["version"]).startswith("0."):
            err(f"{fn}: status 'stable' requires version >= 1.0.0")
        if fm["status"] == "superseded" and not fm.get("superseded_by"):
            err(f"{fn}: status 'superseded' but superseded_by is empty")

        own = fm.get("protocol_ownership") or {}
        owner = own.get("owner")
        if owner not in PROTOCOLS:
            err(f"{fn}: protocol_ownership.owner must be one of {sorted(PROTOCOLS)}")
        else:
            expected_dir = owner
            actual_dir = os.path.dirname(fn)
            if actual_dir != expected_dir:
                err(f"{fn}: owner is {owner!r} so the file must live in "
                    f"additions/{expected_dir}/, not additions/{actual_dir or '.'}/")
        bad_sec = set(own.get("secondary") or []) - PROTOCOLS
        if bad_sec:
            err(f"{fn}: unknown secondary protocol(s) {sorted(bad_sec)}")
        if owner in (own.get("secondary") or []):
            err(f"{fn}: owner {owner!r} also listed as secondary")
        if fm.get("upstream_status") not in UPSTREAM:
            err(f"{fn}: upstream_status must be one of {sorted(UPSTREAM)}")

        bad = set(fm["applies_to"]) - APPLIES
        if bad:
            err(f"{fn}: unknown applies_to values {sorted(bad)}")
        if not fm["applies_to"]:
            err(f"{fn}: applies_to is empty")

        for proto, allowed in (("adcp", ADCP), ("aamp", AAMP)):
            bad = set(fm["targets"].get(proto) or []) - allowed
            if bad:
                warn(f"{fn}: unrecognised {proto} target(s) {sorted(bad)}")
        if not (fm["targets"].get("adcp") or fm["targets"].get("aamp")):
            err(f"{fn}: no target surfaces declared")

        if "## Changelog" not in open(path, encoding="utf-8").read():
            err(f"{fn}: no '## Changelog' section")
    return additions


def check_registry(additions):
    path = os.path.join(ADD_DIR, "REGISTRY.md")
    text = open(path, encoding="utf-8").read()
    for add_id, (fm, fn) in sorted(additions.items()):
        if add_id not in text:
            err(f"REGISTRY.md: {add_id} is not listed")
            continue
        row = next((l for l in text.splitlines()
                    if l.startswith(f"| [{add_id}]")), None)
        if row is None:
            err(f"REGISTRY.md: {add_id} has no table row")
            continue
        if fn.replace(os.sep, "/") not in row:
            err(f"REGISTRY.md: {add_id} row does not link to {fn}")
        if f"| {fm['version']} |" not in row:
            err(f"REGISTRY.md: {add_id} row version disagrees with front matter "
                f"({fm['version']})")
        if f"`{fm['status']}`" not in row:
            err(f"REGISTRY.md: {add_id} row status disagrees with front matter "
                f"({fm['status']})")


def check_releases(additions):
    rel_dir = os.path.join(ADD_DIR, "releases")
    for fn in sorted(os.listdir(rel_dir)):
        if fn == "README.md" or not re.match(r"^R\d+\.\d+\.md$", fn):
            continue
        text = open(os.path.join(rel_dir, fn), encoding="utf-8").read()
        pinned = re.findall(r"^\| (ADD-\d{3}) \| (\d+\.\d+\.\d+) \|", text, re.M)
        if not pinned:
            err(f"releases/{fn}: no pinned additions found")
        for add_id, ver in pinned:
            if add_id not in additions:
                err(f"releases/{fn}: pins unknown {add_id}")
            elif additions[add_id][0]["version"] != ver:
                warn(f"releases/{fn}: pins {add_id}@{ver} but current version is "
                     f"{additions[add_id][0]['version']} (expected for a frozen release)")


def check_links():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            text = open(path, encoding="utf-8").read()
            for m in re.finditer(r"\]\(([^)]+)\)", text):
                target = m.group(1)
                if target.startswith(("http", "#", "mailto")):
                    continue
                resolved = os.path.normpath(
                    os.path.join(dirpath, target.split("#")[0]))
                if not os.path.exists(resolved):
                    err(f"{os.path.relpath(path, ROOT)}: broken link -> {target}")


def main():
    additions = check_additions()
    if additions:
        check_registry(additions)
        check_releases(additions)
    check_links()

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(additions)} additions · {len(errors)} errors · "
          f"{len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
