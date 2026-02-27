#!/usr/bin/env python3
"""
Video Understanding → Engineering Plan Generator

Multi-phase pipeline that uses AI video understanding + subtitles to generate
a full PRD-level engineering plan for a product that solves the problems discussed.

Pipeline:
  Video + SRT → Phase 1 (Gemini 2.5 Pro: Visual Extraction)
              → Phase 2 (Gemini 2.5 Flash: Synthesis)
              → Phase 3 (OpenAI: PRD Generation)
              → engineering_plan.md
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types as genai_types
import openai


# ---------------------------------------------------------------------------
# Phase 1 — Visual Extraction (Gemini 2.5 Pro)
# ---------------------------------------------------------------------------

PHASE1_PROMPT = """\
You are a meticulous video analyst. You will be given a video recording of a \
business call and its SRT subtitle transcript. Your job is to walk through the \
video chronologically and extract structured observations about everything \
shown on screen.

## SRT Transcript
{srt_content}

## Instructions
Walk through the video from beginning to end. For each distinct visual segment \
(screen share, UI shown, document, spreadsheet, app, etc.), record:

1. **timestamp** — approximate start time (MM:SS or HH:MM:SS)
2. **end_timestamp** — approximate end time
3. **type** — one of: "screen_share", "spreadsheet", "app_ui", "document", \
"presentation", "website", "map", "chart", "other"
4. **description** — what is being shown on screen in detail
5. **data_fields** — any specific data fields, column headers, form fields, \
or labels visible
6. **ui_elements** — buttons, menus, navigation elements, tabs visible
7. **workflow_action** — what the user is doing (scrolling, clicking, entering data, etc.)
8. **spoken_context** — what is being said at this moment (reference the subtitles)

Also extract:
- **app_names** — names of any applications or websites shown
- **data_sources** — any data sources mentioned or visible (APIs, databases, services)
- **pain_points_visual** — any visual evidence of friction, manual work, or workarounds

Return your analysis as a JSON object with this structure:
{{
  "observations": [
    {{
      "timestamp": "MM:SS",
      "end_timestamp": "MM:SS",
      "type": "screen_share",
      "description": "...",
      "data_fields": ["field1", "field2"],
      "ui_elements": ["button1", "menu1"],
      "workflow_action": "...",
      "spoken_context": "..."
    }}
  ],
  "app_names": ["app1", "app2"],
  "data_sources": ["source1", "source2"],
  "pain_points_visual": ["pain1", "pain2"]
}}

Be extremely thorough. Capture every screen transition, every spreadsheet shown, \
every data entry moment. Include specific field names, column headers, and UI labels \
exactly as they appear on screen.

Return ONLY valid JSON, no markdown fences.
"""


def _elapsed(start: float) -> str:
    """Format elapsed time since start."""
    secs = int(time.time() - start)
    if secs < 60:
        return f"{secs}s"
    return f"{secs // 60}m {secs % 60}s"


def _strip_fences(text: str) -> str:
    """Strip markdown code fences from text."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        text = text.strip()
    return text


def _progress(msg: str) -> None:
    """Print a progress line, flushing immediately."""
    print(msg, flush=True)


def _stream_gemini(client, model: str, contents, label: str) -> str:
    """Stream a Gemini response, printing periodic progress. Returns full text."""
    _progress(f"  Streaming from {model}...")
    start = time.time()
    chunks = []
    char_count = 0
    last_report = 0

    response = client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=genai_types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=65536,
        ),
    )

    for chunk in response:
        if chunk.text:
            chunks.append(chunk.text)
            char_count += len(chunk.text)
            # Print progress every 2000 chars to avoid spam
            if char_count - last_report >= 2000:
                _progress(f"  ... {label}: {char_count:,} chars ({_elapsed(start)})")
                last_report = char_count

    _progress(f"  ✓ {label}: {char_count:,} chars total ({_elapsed(start)})")
    return "".join(chunks)


def run_phase1(video_path: str, srt_content: str, gemini_key: str, cache_dir: Path) -> dict:
    """Upload video to Gemini and extract visual observations."""
    phase_start = time.time()
    print("=" * 60)
    print("PHASE 1: Visual Extraction (Gemini 2.5 Pro)")
    print("=" * 60)

    client = genai.Client(api_key=gemini_key)

    # Upload video file
    file_size_mb = Path(video_path).stat().st_size / (1024 * 1024)
    _progress(f"  Uploading video: {video_path} ({file_size_mb:.1f} MB)")
    upload_start = time.time()
    video_file = client.files.upload(file=video_path)
    _progress(f"  ✓ Upload complete in {_elapsed(upload_start)}. File: {video_file.name}")

    # Poll until file is ACTIVE
    _progress("  Waiting for file processing...")
    poll_start = time.time()
    while video_file.state.name == "PROCESSING":
        time.sleep(5)
        video_file = client.files.get(name=video_file.name)
        _progress(f"  ... still processing ({_elapsed(poll_start)})")

    if video_file.state.name == "FAILED":
        raise RuntimeError(f"Video processing failed: {video_file.state.name}")

    _progress(f"  ✓ File ready ({_elapsed(poll_start)})")

    # Build prompt
    prompt = PHASE1_PROMPT.format(srt_content=srt_content)

    # Call Gemini with video + prompt (streaming)
    contents = [
        genai_types.Content(
            parts=[
                genai_types.Part.from_uri(
                    file_uri=video_file.uri,
                    mime_type=video_file.mime_type,
                ),
                genai_types.Part.from_text(text=prompt),
            ]
        )
    ]

    raw_text = _stream_gemini(client, "gemini-2.5-pro", contents, "Visual analysis")
    raw_text = _strip_fences(raw_text)

    result = json.loads(raw_text)

    # Save to cache
    out_path = cache_dir / "visual_analysis.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    obs_count = len(result.get('observations', []))
    print(f"  Saved: {out_path}")
    print(f"  {obs_count} visual observations extracted")

    # Clean up uploaded file
    try:
        client.files.delete(name=video_file.name)
        print("  Cleaned up uploaded video file.")
    except Exception:
        pass

    print(f"  Phase 1 total: {_elapsed(phase_start)}")
    return result


# ---------------------------------------------------------------------------
# Phase 2 — Synthesis (Gemini 2.5 Flash)
# ---------------------------------------------------------------------------

PHASE2_PROMPT = """\
You are a product analyst. You will be given two inputs:
1. A structured visual analysis of a video call (JSON with timestamped observations)
2. The full SRT subtitle transcript of the same call

Your job is to synthesize these into a structured product research document.

## Visual Analysis
{visual_analysis}

## SRT Transcript
{srt_content}

## Instructions
Analyze both inputs together and produce a structured JSON document covering:

1. **pain_points** — specific problems discussed, with evidence from both visual \
and verbal sources. Each should have: description, severity (critical/high/medium/low), \
evidence (quotes or visual references), and timestamp.

2. **current_workflows** — step-by-step descriptions of how users currently do their \
work. Reference specific tools, screens, and data sources observed.

3. **data_sources** — all data sources mentioned or shown: name, type, what data they \
provide, how they're accessed, any limitations mentioned.

4. **user_personas** — distinct user types discussed, their roles, goals, frustrations, \
and tech sophistication.

5. **stated_requirements** — any explicit feature requests or requirements mentioned. \
Include who stated them and the context.

6. **implicit_requirements** — requirements implied by the pain points and workflows \
but not explicitly stated.

7. **market_context** — industry, market size, competitors mentioned, regulatory \
considerations, any market-specific details.

8. **key_metrics** — any numbers, KPIs, or benchmarks mentioned (deal sizes, time \
spent, accuracy rates, etc.).

9. **technical_constraints** — any technical limitations, integration requirements, \
or platform preferences mentioned.

10. **visual_evidence_summary** — the most important visual observations that inform \
product decisions, organized by theme.

Return as JSON:
{{
  "pain_points": [...],
  "current_workflows": [...],
  "data_sources": [...],
  "user_personas": [...],
  "stated_requirements": [...],
  "implicit_requirements": [...],
  "market_context": {{...}},
  "key_metrics": [...],
  "technical_constraints": [...],
  "visual_evidence_summary": [...]
}}

Be specific. Reference timestamps. Quote the speakers when possible. \
Do not generalize — use the actual details from the video.

Return ONLY valid JSON, no markdown fences.
"""


def run_phase2(visual_analysis: dict, srt_content: str, gemini_key: str, cache_dir: Path) -> dict:
    """Synthesize visual analysis + transcript into structured findings."""
    phase_start = time.time()
    print("\n" + "=" * 60)
    print("PHASE 2: Synthesis (Gemini 2.5 Flash)")
    print("=" * 60)

    client = genai.Client(api_key=gemini_key)

    prompt = PHASE2_PROMPT.format(
        visual_analysis=json.dumps(visual_analysis, indent=2, ensure_ascii=False),
        srt_content=srt_content,
    )

    raw_text = _stream_gemini(client, "gemini-2.5-flash", prompt, "Synthesis")
    raw_text = _strip_fences(raw_text)

    result = json.loads(raw_text)

    out_path = cache_dir / "synthesis.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"  Saved: {out_path}")
    print(f"  {len(result.get('pain_points', []))} pain points identified")
    print(f"  {len(result.get('current_workflows', []))} workflows documented")
    print(f"  {len(result.get('user_personas', []))} user personas identified")
    print(f"  Phase 2 total: {_elapsed(phase_start)}")

    return result


# ---------------------------------------------------------------------------
# Phase 3 — PRD Generation (OpenAI gpt-5.2)
# ---------------------------------------------------------------------------

PHASE3_PROMPT = """\
You are a senior product manager and technical architect. You will be given a \
structured synthesis document from a user research video call. Your job is to \
generate a complete, production-quality Product Requirements Document (PRD) and \
engineering plan.

## Synthesis Document
{synthesis}

## Instructions
Generate a complete PRD in Markdown format with the following sections. Each \
section should be thorough and reference specific findings from the synthesis.

### Required Sections

1. **Executive Summary** — 2-3 paragraph overview of the product opportunity, \
target users, and proposed solution.

2. **Problem Statement** — detailed description of the problems being solved. \
Include specific examples from the video call (reference timestamps and quotes).

3. **User Personas** — detailed persona cards for each user type identified. \
Include goals, frustrations, technical proficiency, and day-in-the-life scenarios.

4. **Current Workflow** — step-by-step walkthrough of how users accomplish their \
tasks today, with specific tools and data sources referenced. Highlight friction \
points at each step.

5. **Proposed Solution** — high-level description of the product. What it does, \
how it differs from current approaches, and the core value proposition.

6. **User Stories** — organized by priority:
   - P0 (Must Have for MVP)
   - P1 (Should Have for V1)
   - P2 (Nice to Have for V2)
   Format: "As a [persona], I want to [action] so that [benefit]" with acceptance criteria.

7. **Technical Architecture** — system architecture including:
   - High-level architecture diagram (described textually)
   - Key components and their responsibilities
   - Data flow between components
   - Third-party integrations required

8. **Data Model** — key entities, their attributes, and relationships. \
Present as a schema description.

9. **API Design** — key API endpoints with methods, paths, request/response shapes. \
Focus on the core domain operations.

10. **MVP Scope** — clearly defined MVP boundary. What's in, what's out, and why.

11. **Implementation Phases**:
    - **MVP** (4-6 weeks): core features, minimum viable product
    - **V1** (8-12 weeks): full feature set for initial launch
    - **V2** (16-24 weeks): advanced features, scale, optimization
    Each phase should list specific features, technical tasks, and milestones.

12. **Success Metrics** — quantitative and qualitative metrics to measure product \
success. Include baseline measurements where available from the synthesis.

13. **Appendix: Visual Evidence** — key observations from screen shares organized \
by theme. Reference specific tools, data fields, and UI patterns observed in the \
video. This section should help engineers understand the domain by seeing what \
users actually work with.

### Writing Guidelines
- Be specific, not generic. Reference actual data fields, tool names, and \
workflows from the synthesis.
- Include concrete numbers where available.
- User stories should have clear acceptance criteria.
- Technical sections should be implementable by an engineering team.
- The PRD should stand alone — a reader shouldn't need to watch the video.

Output the complete PRD in Markdown format.
"""


def run_phase3(synthesis: dict, openai_key: str, output_path: Path) -> str:
    """Generate the full PRD from synthesis using OpenAI."""
    phase_start = time.time()
    print("\n" + "=" * 60)
    print("PHASE 3: PRD Generation (OpenAI gpt-5.2)")
    print("=" * 60)

    client = openai.OpenAI(api_key=openai_key)

    prompt = PHASE3_PROMPT.format(
        synthesis=json.dumps(synthesis, indent=2, ensure_ascii=False),
    )

    _progress("  Streaming from gpt-5.2...")
    start = time.time()
    chunks = []
    char_count = 0
    last_report = 0

    stream = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {"role": "system", "content": "You are a senior product manager and technical architect producing a detailed PRD."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_completion_tokens=16384,
        stream=True,
    )

    for event in stream:
        delta = event.choices[0].delta.content if event.choices[0].delta else None
        if delta:
            chunks.append(delta)
            char_count += len(delta)
            if char_count - last_report >= 2000:
                _progress(f"  ... PRD generation: {char_count:,} chars ({_elapsed(start)})")
                last_report = char_count

    _progress(f"  ✓ PRD generation: {char_count:,} chars total ({_elapsed(start)})")

    prd_content = "".join(chunks)

    output_path.write_text(prd_content, encoding="utf-8")
    print(f"  Saved: {output_path}")

    # Count sections
    section_count = sum(1 for line in prd_content.split("\n") if line.startswith("## "))
    word_count = len(prd_content.split())
    print(f"  {section_count} top-level sections, {word_count:,} words")
    print(f"  Phase 3 total: {_elapsed(phase_start)}")

    return prd_content


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Video Understanding → Engineering Plan Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python video_to_plan.py --video call.mp4 --subtitles call.srt
  python video_to_plan.py --video call.mp4 --subtitles call.srt --phase 3
  python video_to_plan.py --video call.mp4 --subtitles call.srt --output my_plan.md
        """,
    )
    parser.add_argument("--video", required=True, help="Path to video file (e.g. .mp4)")
    parser.add_argument("--subtitles", required=True, help="Path to SRT subtitle file")
    parser.add_argument("--output", default="engineering_plan.md", help="Output PRD path (default: engineering_plan.md)")
    parser.add_argument("--gemini-key", default=None, help="Gemini API key (or set GEMINI_API_KEY)")
    parser.add_argument("--openai-key", default=None, help="OpenAI API key (or set OPENAI_API_KEY)")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3], default=None,
                        help="Re-run a specific phase from cached intermediate output")

    args = parser.parse_args()

    # Resolve API keys
    gemini_key = args.gemini_key or os.environ.get("GEMINI_API_KEY")
    openai_key = args.openai_key or os.environ.get("OPENAI_API_KEY")

    # Determine which phases need which keys
    phases_to_run = [1, 2, 3] if args.phase is None else [args.phase]

    if any(p in [1, 2] for p in phases_to_run) and not gemini_key:
        print("Error: Gemini API key required for phases 1-2. Set GEMINI_API_KEY or use --gemini-key.", file=sys.stderr)
        sys.exit(1)
    if 3 in phases_to_run and not openai_key:
        print("Error: OpenAI API key required for phase 3. Set OPENAI_API_KEY or use --openai-key.", file=sys.stderr)
        sys.exit(1)

    # Resolve paths
    video_path = Path(args.video).resolve()
    srt_path = Path(args.subtitles).resolve()
    output_path = Path(args.output).resolve()
    cache_dir = output_path.parent / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    if not video_path.exists():
        print(f"Error: Video file not found: {video_path}", file=sys.stderr)
        sys.exit(1)
    if not srt_path.exists():
        print(f"Error: Subtitle file not found: {srt_path}", file=sys.stderr)
        sys.exit(1)

    # Read SRT content
    srt_content = srt_path.read_text(encoding="utf-8")

    total_start = time.time()
    print(f"Video:     {video_path}")
    print(f"Subtitles: {srt_path}")
    print(f"Output:    {output_path}")
    print(f"Cache:     {cache_dir}")
    print(f"Phases:    {phases_to_run}")
    print()

    # --- Phase 1 ---
    visual_analysis = None
    if 1 in phases_to_run:
        visual_analysis = run_phase1(str(video_path), srt_content, gemini_key, cache_dir)
    else:
        cached = cache_dir / "visual_analysis.json"
        if cached.exists():
            visual_analysis = json.loads(cached.read_text())
            print(f"Loaded cached visual analysis: {cached}")
        elif any(p in [2] for p in phases_to_run):
            print(f"Error: Phase 2 requires visual_analysis.json in {cache_dir}. Run phase 1 first.", file=sys.stderr)
            sys.exit(1)

    # --- Phase 2 ---
    synthesis = None
    if 2 in phases_to_run:
        synthesis = run_phase2(visual_analysis, srt_content, gemini_key, cache_dir)
    else:
        cached = cache_dir / "synthesis.json"
        if cached.exists():
            synthesis = json.loads(cached.read_text())
            print(f"Loaded cached synthesis: {cached}")
        elif 3 in phases_to_run:
            print(f"Error: Phase 3 requires synthesis.json in {cache_dir}. Run phase 2 first.", file=sys.stderr)
            sys.exit(1)

    # --- Phase 3 ---
    if 3 in phases_to_run:
        prd = run_phase3(synthesis, openai_key, output_path)

    print("\n" + "=" * 60)
    print(f"DONE — total time: {_elapsed(total_start)}")
    print("=" * 60)
    if 3 in phases_to_run:
        print(f"PRD written to: {output_path}")


if __name__ == "__main__":
    main()
