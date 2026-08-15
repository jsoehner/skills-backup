---
name: slack-gif-creator
description: |
  Toolkit for creating animated GIFs optimized for Slack, with validators for size constraints and composable animation primitives. Trigger when requested to design, compile, or optimize animated GIFs, custom Slack emoji animations, reactions, loading spinners, or multi-frame visual assets. Keywords: slack-gif-creator, gif_builder.py, validators.py, GIFBuilder, pillow, imageio, animated emoji, shake, bounce, spin, kaleidoscope, 64KB.

  Toolkit for creating animated GIFs optimized for Slack, with validators for size constraints and composable animation primitives. Trigger when requested to design, compile, or optimize animated GIFs, custom Slack emoji animations, reactions, loading spinners, or multi-frame visual assets. Keywords: slack-gif-creator, gif_builder.py, validators.py, GIFBuilder, pillow, imageio, animated emoji, shake, bounce, spin, kaleidoscope, 64KB.

license: Complete terms in LICENSE.txt
---

# Slack GIF Creator - Expert Toolkit & Workflow

An advanced framework for building high-quality, lightweight animated GIFs optimized for Slack's message and emoji rendering platforms.

## Progressive Disclosure & Importing Resources

This skill utilizes local Python modules under `core/` and `templates/`. These files should be treated as imports. Rather than reading their source code, interface with them via their public functions:

- **Core Engine & Optimization**: `from core.gif_builder import GIFBuilder` (Handles frame accumulation, color quantization, and output compression).
- **Validation**: `from core.validators import validate_gif, check_slack_size` (Checks dimensions and byte-size compliance).
- **Easing & Math**: `from core.easing import interpolate` (Applies ease-in, ease-out, elastic, and bounce easing formulas).
- **Animation Primitives**: Import from `templates.<primitive>` (e.g., `templates.shake`, `templates.spin`, `templates.pulse`).

## Freedom Calibration & Constraints
- **Constraint Level: Medium**
  - **High Rigidity**: Strict byte limits (64KB for emoji, 2MB for messages) and dimensions (128x128 or 480x480).
  - **Medium Rigidity**: Usage of the standard `GIFBuilder` to output correct formats.
  - **High Freedom**: Creative compositions, color themes, speed profiles, and motion curves.

## Decision Tree: Size Optimization & Frame Planning

```
Is the target asset a Slack Custom Emoji or a Rich Message GIF?
 ├─ Slack Custom Emoji (Strict 64KB Limit)
 │   ├─ Max Resolution: 128x128 pixels (Never exceed)
 │   ├─ Target Frame Count: 10 - 15 frames max
 │   ├─ Colors: 32 - 48 colors max (avoid gradients, use solid shapes)
 │   └─ Easing/FPS: 10 - 12 FPS, use snappy easings (e.g., elastic_out or bounce_out)
 │
 └─ Rich Message GIF (2MB Max Limit)
     ├─ Max Resolution: 480x480 pixels
     ├─ Target Frame Count: 30 - 60 frames
     ├─ Colors: 128 - 256 colors (gradients and shadows are acceptable)
     └─ Easing/FPS: 15 - 20 FPS, smooth transitions
```

## Professional Mindset & Design Principles
1. **Optimize Frame Differences (Temporal Compression)**: GIFs compress best when successive frames are identical in most areas. Keep backgrounds static. Only move small foreground elements.
2. **Quantize Intelligently**: Color reduction is the single most effective way to shrink file size. Restrict emoji GIFs to a tight palette of 32 or fewer colors.
3. **Handle Transparency Correctly**: Slack dark/light modes can render transparent borders with ugly black halos. Ensure transparent emojis use clean antialiasing or background-matte colors where necessary.

---

## Core Animation & Composition Reference

### 1. Composability: Combining Translation & Visual Effects
To build high-impact animations, combine physical movement (bounce/move) with shockwaves or outline text.

```python
import math
from PIL import Image
from core.gif_builder import GIFBuilder
from core.easing import interpolate
from core.frame_composer import create_gradient_background, draw_emoji_enhanced
from core.visual_effects import create_impact_flash

# Initialize builder for a message GIF
builder = GIFBuilder(width=480, height=480, fps=20)
num_frames = 20
ground_y = 360

for i in range(num_frames):
    # Create static background to optimize compression
    frame = create_gradient_background(480, 480, (30, 40, 50), (10, 15, 20))
    t = i / (num_frames - 1)
    
    # Bounce easing down
    y = interpolate(100, ground_y, t, easing='bounce_out')
    
    # Impact shockwave on final frames
    if t > 0.8:
        frame = create_impact_flash(frame, position=(240, ground_y + 40), radius=int((t-0.8)*300), intensity=0.5)
        
    draw_emoji_enhanced(frame, '💥', position=(200, int(y)), size=80, shadow=True)
    builder.add_frame(frame)

builder.save('impact.gif', num_colors=128)
```

---

## Critical Anti-Patterns (NEVER List)

| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** exceed 64KB for emoji GIFs | Slack fails to upload or silently fails if emoji files exceed the strict 64KB limit. | Use `check_slack_size('emoji.gif', is_emoji=True)` and dynamically reduce frame counts or color counts on failure. |
| **NEVER** use fine color gradients on emoji GIFs | Gradients introduce hundreds of distinct colors, destroying GIF compression and bloating file size. | Use flat, solid colors or clean 2-3 step block transitions. |
| **NEVER** run high frame counts (>20 frames) for emoji | Each frame contains spatial delta overhead, pushing the size past 64KB. | Keep emoji animations between 8 and 15 frames total. |
| **NEVER** forget to check transparency bounds | Unbounded emoji rendering can cause artifacts on dark-mode Slack themes. | Clear unused pixels in the alpha channel and avoid soft transparent brushes on the image edge. |
| **NEVER** build animations using CPU sleep timers | Using Python's `time.sleep()` inside loop builders creates non-deterministic render speed. | Set frame durations explicitly in the `GIFBuilder` constructor via the `fps` parameter. |

---

## Common Error Scenarios & Fallbacks

### Scenario 1: Output file size is too large (e.g. Emoji GIF is 78KB instead of <64KB)
- **Root Cause**: Too many frames, high color count, or complex backgrounds.
- **Fallback**:
  1. Downsample the color palette (e.g. from 48 colors to 32 or 16).
  2. Drop every second frame (reduce FPS from 12 to 8, or cut duration).
  3. Simplify the background to pure transparent or a solid color.
  ```python
  # Programmatic fallback logic
  passes, info = check_slack_size('emoji.gif', is_emoji=True)
  if not passes:
      # Re-save with aggressive optimization
      builder.save('emoji.gif', num_colors=16, optimize_for_emoji=True)
  ```

### Scenario 2: Ugly black borders or pixelation on transparent edges
- **Root Cause**: Color quantization mapping semi-transparent pixels (alpha between 1 and 254) to black or solid pixels.
- **Fallback**:
  1. Convert frames to 'RGBA' before manipulation.
  2. Apply a binary alpha threshold: force pixels with alpha < 128 to fully transparent, and >= 128 to fully opaque.
  ```python
  def apply_alpha_threshold(image, threshold=128):
      alpha = image.split()[-1]
      binary_alpha = alpha.point(lambda p: 255 if p >= threshold else 0)
      image.putalpha(binary_alpha)
      return image
  ```

### Scenario 3: GIF plays too fast or too slow in Slack
- **Root Cause**: Incorrect frame delay mapping. Slack ignores delays smaller than 0.02s (20ms) and often rounds up delays.
- **Fallback**: Keep FPS between 10 and 20. Target standard delays like 100ms (10 FPS) or 50ms (20 FPS).
