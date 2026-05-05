---
name: news-video-skills
description: "Convert AI/news hotspot JSON into a short-video production package: curated topic list, narrative video script, shot-by-shot storyboard, MiniMax Token Plan video prompts, generated clip workflow, ffmpeg concatenation, and final delivery checks. Use when the user asks to turn news Agent output, ai_news_fetcher.py JSON, daily AI热点, 热点新闻数据, or AI赚钱情报 into short videos, video scripts, 分镜, MiniMax/Hailuo video tasks, or assembled MP4 videos."
---

# News Video Skills

## Workflow

Use this skill as the production coordinator for news-to-video jobs. Pair it with `$minimax-token-plan` whenever clips must be generated through MiniMax Token Plan.

1. **Collect input**
   - Accept `ai_news_fetcher.py` JSON, a JSON file path, pasted `items`, or a plain-text hot-news list.
   - Prefer aggregated `items`; if only `raw_items` exists, cluster related stories before writing.
   - Keep source names, URLs, `hot_score`, `money_grade`, and `risk_notes` available for factual checks.

2. **Select the video angle**
   - Default to a 75-second, 3-story roundup for daily hotspot videos.
   - Use a 45-60 second single-story video only when one topic is clearly stronger than the rest.
   - Use 2-3 minutes only for a proven topic that deserves deeper opportunity analysis.
   - Prioritize strong evidence, high public curiosity, concrete ordinary-person impact, and visual explainability.
   - Downgrade or avoid stories that are single-source, legal/medical/financial high-risk, or hard to visualize.

3. **Create the production package**
   - Write `script.md` with hook, narration, on-screen text, and CTA.
   - Write `storyboard.json` using the schema in `references/storyboard-schema.md`.
   - Write `minimax-prompts.json` with one prompt per shot, including duration, aspect ratio, model, and continuity notes.
   - Keep each shot visually concrete. Avoid asking the video model to render readable text; put text overlays in post-production if needed.

4. **Generate clips**
   - Load and use `$minimax-token-plan`.
   - For each shot, run its bundled script, usually:
     `node <minimax-token-plan>/scripts/minimax-token-plan.mjs video-t2v --prompt "..." --model MiniMax-Hailuo-2.3-Fast --duration 6 --resolution 768P`
   - Query tasks until complete, then download each file into `clips/` with stable names like `001-hook.mp4`.
   - If a shot depends on a prior image or frame, use `video-i2v` and document the image source.

5. **Assemble**
   - Use `scripts/concat_videos.py` to concatenate downloaded clips:
     `python scripts/concat_videos.py --clips clips/*.mp4 --out final/news-video.mp4`
   - If clips have incompatible codecs, rerun with `--reencode`.
   - Keep narration/audio separate unless the user asks for voiceover; MiniMax video generation should focus on picture.

6. **Verify**
   - Confirm the final MP4 exists and has nonzero duration.
   - Spot-check every downloaded clip name and order.
   - Check that factual claims in narration are supported by the input sources.
   - Report any failed MiniMax tasks, missing clips, or source reliability caveats.

## Writing Rules

- Use Chinese by default when the input/news Agent context is Chinese.
- Make the first 3 seconds specific and curiosity-driven, not generic.
- Turn every claim into ordinary-person consequences: "what changed", "who benefits", "what to try", "what to avoid".
- Separate factual narration from opinion or speculation.
- For risky topics, add a neutral caveat instead of hype.
- Keep generated visual prompts cinematic and inspectable, with no readable text unless explicitly required.

## Shot Design

Default to a 75-second, 9-shot structure for daily hotspot videos:

1. `001-hook`: curiosity hook
2. `002-hotspot-1`: first news item
3. `003-impact-1`: why the first item matters
4. `004-hotspot-2`: second news item
5. `005-impact-2`: why the second item matters
6. `006-hotspot-3`: third news item
7. `007-money-opportunity`: ordinary-person/business opportunity
8. `008-risk-check`: caveat, uncertainty, or compliance reminder
9. `009-cta`: concise ending and next action

Use 6-8 seconds per shot. Keep 9 shots unless the user asks for a different length.

Each shot needs:
- `id`: two or three digit order, e.g. `001`
- `purpose`: hook, hotspot-1, impact-1, hotspot-2, impact-2, hotspot-3, money-opportunity, risk-check, CTA
- `duration_seconds`: usually 6-8
- `narration`: spoken line for this shot
- `onscreen_text`: short overlay text for editing, not for MiniMax prompt rendering
- `visual_prompt`: MiniMax video prompt
- `visual_style`: consistent style such as `tech news cinematic documentary, vertical video`
- `asset_type`: `generated_video`, `news_screenshot`, `chart`, `text_card`, or `broll`
- `transition`: `cut`, `match_cut`, `push`, `fade`, or another explicit edit transition
- `edit_notes`: post-production instructions such as captions, sound cues, charts, or logo avoidance
- `generation_status`: `pending`, `task_created`, `downloaded`, `failed`, or `needs_regen`
- `source_refs`: source names or URLs supporting the narration
- `risk_notes`: empty list unless the shot needs caution

Do not force every shot through video generation. Use `asset_type` to route work:

- `generated_video`: create a MiniMax clip from `visual_prompt`.
- `news_screenshot`: capture or use a source screenshot only when legally and visually appropriate.
- `chart`: create a simple data visual in post-production.
- `text_card`: render text in editing software, not inside MiniMax generated footage.
- `broll`: use a generated or existing background clip.

## MiniMax Prompt Guidance

Write prompts as visual direction, not article summaries:

- Good: "A close-up of a laptop browser settings page, subtle AI chip icon reflected on glass, clean modern desk, slow push-in, realistic documentary style"
- Weak: "A video about Chrome installing an AI model"

Always add continuity controls when needed:
- "same office, same laptop, same lighting"
- "slow dolly-in, no cuts"
- "documentary realism, natural light"
- "consistent visual style across all shots"

The `$minimax-token-plan` script automatically appends a no-text/no-watermark rule for visual generation. Do not pass `--allow-text true` unless readable text is required.

## Resources

- `references/storyboard-schema.md`: exact JSON structure for production packages.
- `scripts/concat_videos.py`: deterministic ffmpeg concat helper with optional re-encode mode.

## Deliverable Shape

When completing a video-production task, return:

- selected angle and why it was chosen
- paths to `script.md`, `storyboard.json`, and `minimax-prompts.json`
- MiniMax task IDs and downloaded clip paths, if generation ran
- final MP4 path, if assembly ran
- verification notes and any failed sources/tasks
