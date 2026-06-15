# Roadmap Base64 Fix

Base64 PNG roadmap image cleanup project.

## Files

- `decoded_input.png`: original decoded image from the pasted base64 data URL.
- `redraw_roadmap.py`: regeneration script that redraws the roadmap with wrapped text inside boxes.
- `roadmap_fixed.png`: fixed PNG output.
- `roadmap_fixed_base64.txt`: fixed image as a `data:image/png;base64,...` string.

## Run

```powershell
python redraw_roadmap.py
```
