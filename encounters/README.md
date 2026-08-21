# Encounters

One file per persona per session, validated by `../schemas/encounter.schema.json`.

```
encounters/<persona_id>/<persona_id>--<artifact-slug>--<YYYY-MM-DD>--<n>.json
```

Written by the persona **before it returns**. A subagent becomes unreachable roughly 30
seconds after it finishes, so a return value is not a durable record. The file is.

`verbatim` is authoritative and never edited. Structured `findings` are a lossy extraction
kept beside it, so any conclusion can be checked against what was actually said.

See `../docs/persona-memory.md` for the contract.
