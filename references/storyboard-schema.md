# Storyboard Schema

Create a project folder per video. Recommended layout:

```text
project-name/
├── input-news.json
├── script.md
├── storyboard.json
├── minimax-prompts.json
├── clips/
└── final/
```

## script.md

Use this structure:

```markdown
# Title

## Angle
One sentence describing the chosen content angle.

## Video Specs
- Duration: 75 seconds
- Aspect ratio: 9:16
- Audience: AI赚钱情报站普通用户
- Structure: 9 shots, 3 news items, opportunity, risk, CTA

## Script
| Time | Narration | On-screen text | Source |
|---|---|---|---|
| 0-8s | ... | ... | ... |

## CTA
...

## Caveats
...
```

## storyboard.json

```json
{
  "title": "短视频标题",
  "angle": "本视频的叙事角度",
  "duration_seconds": 75,
  "aspect_ratio": "9:16",
  "audience": "AI赚钱情报站普通用户",
  "default_visual_style": "tech news cinematic documentary, realistic, vertical video, consistent lighting",
  "structure": [
    "001-hook",
    "002-hotspot-1",
    "003-impact-1",
    "004-hotspot-2",
    "005-impact-2",
    "006-hotspot-3",
    "007-money-opportunity",
    "008-risk-check",
    "009-cta"
  ],
  "claims": [
    {
      "claim": "可核验事实",
      "source_refs": ["source name or URL"],
      "confidence": "high|medium|low"
    }
  ],
  "shots": [
    {
      "id": "001",
      "purpose": "hook",
      "duration_seconds": 8,
      "narration": "口播文案",
      "onscreen_text": "屏幕字幕",
      "visual_prompt": "MiniMax visual prompt, no readable text",
      "visual_style": "tech news cinematic documentary, realistic, vertical video",
      "asset_type": "generated_video",
      "camera": "slow push-in",
      "transition": "cut",
      "edit_notes": "Add large Chinese subtitle overlay in post; do not ask MiniMax to render text.",
      "generation_status": "pending",
      "source_refs": ["source name or URL"],
      "risk_notes": []
    }
  ]
}
```

## minimax-prompts.json

```json
{
  "model": "MiniMax-Hailuo-2.3-Fast",
  "resolution": "768P",
  "aspect_ratio": "9:16",
  "default_duration_seconds": 8,
  "visual_style": "tech news cinematic documentary, realistic, vertical video, consistent lighting",
  "shots": [
    {
      "id": "001",
      "out": "clips/001-hook.mp4",
      "command": "video-t2v",
      "duration_seconds": 8,
      "asset_type": "generated_video",
      "generation_status": "pending",
      "prompt": "Prompt to pass to minimax-token-plan.mjs"
    }
  ]
}
```

## Purpose Defaults

Use this exact structure unless the user asks for another duration:

| Shot | Purpose | Duration | Asset type |
|---|---|---:|---|
| 001 | hook | 8s | generated_video or text_card |
| 002 | hotspot-1 | 8s | generated_video |
| 003 | impact-1 | 8s | broll or chart |
| 004 | hotspot-2 | 8s | generated_video |
| 005 | impact-2 | 8s | broll or chart |
| 006 | hotspot-3 | 8s | generated_video |
| 007 | money-opportunity | 9s | generated_video or chart |
| 008 | risk-check | 8s | text_card or broll |
| 009 | CTA | 10s | text_card or generated_video |

Total target duration: 75 seconds.

## Quality Bar

- Every narration claim should map to at least one `source_refs` entry.
- Every shot should be visually specific enough to generate a useful video clip.
- Avoid visual prompts that require exact UI text, logos, news article screenshots, or readable captions.
- Keep `onscreen_text` for editing overlays, not for model-rendered video.
- Keep `visual_style` consistent across shots unless there is a clear reason to switch.
- Use `transition` and `edit_notes` to make concatenation feel edited rather than mechanically joined.
- Keep `generation_status` current during batch generation and retries.
