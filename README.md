# news-video-skills

`news-video-skills` is a Codex/Hermes skill for turning AI/news hotspot data into a short-video production workflow.

It is designed for a `news` Agent that already fetches daily hotspot JSON, then needs to:

1. select a video angle from the news data
2. write a short-video script
3. produce a shot-by-shot storyboard
4. prepare MiniMax Token Plan video prompts
5. generate video clips with `minimax-token-plan`
6. concatenate clips into a final MP4
7. verify the final deliverable

## Default Video Format

- Duration: about 75 seconds
- Layout: vertical `9:16`
- Structure: 9 shots
- Content: 3 news items, ordinary-person/business opportunity, risk check, CTA

Default shot order:

1. `001-hook`
2. `002-hotspot-1`
3. `003-impact-1`
4. `004-hotspot-2`
5. `005-impact-2`
6. `006-hotspot-3`
7. `007-money-opportunity`
8. `008-risk-check`
9. `009-cta`

## Files

- `SKILL.md`: skill instructions and workflow
- `agents/openai.yaml`: Codex UI metadata
- `references/storyboard-schema.md`: output schema for `script.md`, `storyboard.json`, and `minimax-prompts.json`
- `scripts/concat_videos.py`: ffmpeg-based video concat helper

## Install Into Hermes news Agent

```bash
mkdir -p ~/.hermes/profiles/news/skills
cp -R news-video-skills ~/.hermes/profiles/news/skills/news-video-skills
news skills list
```

The `news` Agent should also have `minimax-token-plan` installed, because this skill delegates MiniMax API calls to that skill.

## Concatenate Clips

```bash
python scripts/concat_videos.py --clips clips/*.mp4 --out final/news-video.mp4
```

If clips have incompatible codecs, dimensions, or frame rates:

```bash
python scripts/concat_videos.py --clips clips/*.mp4 --out final/news-video.mp4 --reencode
```

The script requires `ffmpeg` and `ffprobe` on `PATH`.
