# video-to-plan

Multi-phase AI pipeline that generates PRD-level engineering plans from video recordings of business calls.

## Architecture

```
Video + SRT → Phase 1 (Gemini 2.5 Pro: Visual Extraction)
            → Phase 2 (Gemini 2.5 Flash: Synthesis)
            → Phase 3 (OpenAI gpt-5.2: PRD Generation)
            → engineering_plan.md
```

- **Phase 1**: Uploads video to Gemini Files API, extracts timestamped visual observations (screens, UI, data fields, workflows)
- **Phase 2**: Synthesizes visual analysis + SRT transcript into structured findings (pain points, personas, requirements)
- **Phase 3**: Generates full markdown PRD with 13 sections from synthesis

Intermediate results cached in `.cache/` — individual phases can be re-run with `--phase N`.

## Key Files

- `video_to_plan.py` — Main pipeline CLI (all 3 phases)
- `promote_plan.py` — Package a plan + artifacts into a git-ready directory
- `requirements.txt` — Dependencies: `google-genai`, `openai`
- `.env` — API keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`); see `.env.example`

## Commands

```bash
# Full pipeline
python video_to_plan.py --video call.mp4 --subtitles call.srt

# Re-run single phase from cache
python video_to_plan.py --video call.mp4 --subtitles call.srt --phase 3

# Promote plan to named directory
python promote_plan.py <name>
```

## Conventions

- All API calls use streaming with progress reporting
- Gemini responses use `_stream_gemini()` helper; OpenAI streams inline
- Prompts return raw JSON (phases 1-2) or markdown (phase 3)
- `_strip_fences()` handles models that wrap output in markdown code fences
- OpenAI uses `max_completion_tokens` (not `max_tokens`) for gpt-5.2
