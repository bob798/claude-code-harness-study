# Public trace data manifest (A0-02b)

Source used for manual web inspection:
- Dataset: https://huggingface.co/datasets/trace-commons/agent-traces
- Session: `sessions/claude_code/674e0f5c-c481-4830-b2ef-3e1e069a2b7f.jsonl`
- Session viewer: https://huggingface.co/datasets/trace-commons/agent-traces/blob/main/sessions/claude_code/674e0f5c-c481-4830-b2ef-3e1e069a2b7f.jsonl
- Version observed in public native records: `2.1.177`
- Dataset license shown: CC BY 4.0
- Local raw file downloaded: **NO** (current isolated execution container has no network path to Hugging Face).
- File hash / immutable dataset commit: **NOT VERIFIED** (do not invent).
- Programmatic real-session metrics: **NOT MEASURED**.

Additional candidate: https://huggingface.co/datasets/ultralazr/claude-code-traces (card says `license: other`; not included in public redistribution).

Procedure: review dataset authorization and redaction; download to a private temporary location; calculate sha256; pin revision; run the session adapter; publish only non-sensitive aggregate output.

Do not archive raw donated sessions in this project repository.
