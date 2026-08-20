# Contributing

This package is meant to be forked and adapted by districts. Corrections back to the
upstream copy are welcome — especially the two things that go stale fastest.

## The two most valuable contributions

**1. A console path that moved.** Google reorganizes the Admin console regularly. If a
path in these docs no longer matches what you see, open an issue or PR with:

- the doc and section
- the path as written
- the path as it actually is now
- a link to the current Google article

**2. A `[VERIFY]` tag you can resolve.** Search the repo for `[VERIFY]` — each one marks
something that could not be confirmed against current documentation on 2026-08-20. If you
can confirm it in a live console, that's a real contribution. Say which edition your
tenant is, since some of them are edition-dependent.

## Set up the commit guard first

```bash
./tools/install-hooks.sh
```

This installs a pre-commit hook that **blocks district-identifying data** — real
domains, filled-in OU paths, the bulk-sender inventory. This package is a public
template; committing your own values publishes a targeting map of your environment
that survives in git history even if you revert it. Keep real values in an internal
doc or a private repo.

## Ground rules

- **No PII, ever.** No student, staff, or guardian names, addresses, or IDs — not in
  issues, not in PRs, not in example output. Redact before you paste. This is a FERPA
  context and it applies to contributors too.
- **No real district domains** in examples. Use the `<PRIMARY_DOMAIN>` tokens.
- **Cite, don't assert.** A changed recommendation needs a source URL. If you can't cite
  it, mark it `[VERIFY]` rather than stating it.
- **Don't weaken a default.** Recommendations move settings toward stricter, or leave them
  alone. If you think something here is too strict, that's a legitimate issue to open —
  argue it with the blast radius, not by loosening it quietly.
- **Keep the six fields.** Every setting carries path, per-OU values, edition, impact,
  rollback, and source. See [CLAUDE.md](CLAUDE.md).

## Rebuilding the published editions

The web and PDF editions are generated from the markdown — never hand-edited.

```bash
python3 tools/build-site.py     # -> site/index.html
./tools/make-pdfs.sh            # -> dist/*.pdf  (needs Chrome)
```

No third-party Python packages are required.

## What this repo is not

It is not a compliance certification, a substitute for your own verification, or a
complete security program. It covers Google Workspace configuration and response. See the
scope boundary in the [README](README.md).
