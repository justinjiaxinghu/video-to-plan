# video-to-plan

Generate production-quality PRDs from video recordings of business calls.

Upload a video + subtitles and get a full Product Requirements Document with user personas, technical architecture, API design, implementation phases, and more.

## How it works

The pipeline runs in three phases:

1. **Visual Extraction** (Gemini 2.5 Pro) — Uploads the video and extracts timestamped observations of everything shown on screen: UI elements, data fields, workflows, tools
2. **Synthesis** (Gemini 2.5 Flash) — Combines visual analysis with the subtitle transcript to identify pain points, user personas, requirements, and market context
3. **PRD Generation** (OpenAI gpt-5.2) — Generates a complete markdown PRD with 13 sections from the synthesized findings

Intermediate results are cached so individual phases can be re-run without reprocessing the video.

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your API keys:

```
GEMINI_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

## Usage

```bash
# Run full pipeline
python video_to_plan.py --video call.mp4 --subtitles call.srt

# Custom output path
python video_to_plan.py --video call.mp4 --subtitles call.srt --output my_plan.md

# Re-run a single phase from cached intermediate output
python video_to_plan.py --video call.mp4 --subtitles call.srt --phase 3
```

### Promote a plan

Package the generated PRD and artifacts into a clean, git-ready directory:

```bash
python promote_plan.py my-product-name
```

This creates a directory with the PRD, cached artifacts, metadata, and a README.

## Output

The pipeline produces:

- `engineering_plan.md` — Full PRD with executive summary, problem statement, user personas, current workflows, proposed solution, user stories, technical architecture, data model, API design, MVP scope, implementation phases, success metrics, and visual evidence appendix
- `.cache/visual_analysis.json` — Timestamped visual observations
- `.cache/synthesis.json` — Structured research findings
