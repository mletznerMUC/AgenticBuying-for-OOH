# Scripts

| Script | Purpose |
| --- | --- |
| [`validate.py`](validate.py) | Consistency checks across additions, the registry, release manifests and links |

## validate.py

```
python3 scripts/validate.py     # from the repository root; exit 1 on error
```

Requires PyYAML. Checks:

1. Every addition has parseable front matter with the required keys.
2. The front-matter `id` matches the file name, and IDs are unique.
3. `status`, `applies_to` and target surfaces are in the allowed sets.
4. Versions are valid SemVer, and a `stable` addition is at `>= 1.0.0`.
5. `REGISTRY.md` lists every addition, with the version and status its front matter
   declares.
6. Release manifests pin additions that exist — and warn when a pinned version has since
   moved on, which is expected for a frozen release but worth seeing.
7. Every relative markdown link in the repository resolves.

Run it before committing a change to any addition. The registry and manifests are meant
to be derivable from front matter, so a disagreement is a bug in one of them.
