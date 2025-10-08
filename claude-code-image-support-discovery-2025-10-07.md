# Claude Code Image Support Discovery Session
**Date**: October 7, 2025
**Session Type**: Research & Information Discovery
**Status**: ✅ Successfully Documented

---

## 🎯 Session Objective

User wanted to confirm whether Claude Code supports images in its interactive CLI mode and understand the technical implementation, specifically:
- Does Claude Code support image pasting in the terminal?
- Is the image converted to base64 (or similar) when transmitted?
- What are the current capabilities and limitations?

---

## ✅ Key Findings: User Intuition Was CORRECT

### 1. **Claude Code DOES Support Images** (as of 2025)

**Three Methods to Send Images:**

1. **Paste from Clipboard**: Use `Ctrl+V` (NOT `Cmd+V` on Mac)
   - Image is captured from clipboard and transmitted

2. **Drag & Drop**: Drag image files directly into Claude Code terminal
   - Most reliable method across platforms

3. **File Path Reference**: Provide path in natural language
   ```
   "Analyze this image: /path/to/your/image.png"
   ```

### 2. **Base64 Encoding Confirmed** ✓

**Technical Implementation:**
- Images ARE converted to **base64-encoded strings** for API transmission
- Alternative: Images can be provided as URLs
- This happens automatically when pasting or providing file paths
- The CLI handles conversion transparently

**API/Programmatic Usage:**
```python
# Images sent to Claude API as base64
{
  "type": "image",
  "source": {
    "type": "base64",
    "media_type": "image/jpeg",
    "data": "<base64_encoded_string>"
  }
}
```

### 3. **Supported Formats & Limits**

**Image Formats:**
- JPEG (image/jpeg)
- PNG (image/png)
- GIF (image/gif)
- WebP (image/webp)

**Size/Quality Guidelines:**
- **Max file size**: ~30MB
- **Recommended resolution**: ≥1000×1000 pixels
- **Best practice**: Crop to relevant region before sending
- **Preprocessing**: Reduce size for faster transmission

---

## 🐛 Known Issues (2025)

### Critical Bug: Keyboard Shortcut Inconsistency

**Problem**: `Cmd+V` doesn't work reliably for pasting images

**Root Cause Analysis:**
- The editor intercepts `Cmd+V` and runs its own paste handler
- This handler only reads `text/plain` from clipboard
- Does NOT read image data (image/png, image/jpeg, etc.)

**Platform-Specific Behavior:**

| Platform | `Cmd+V` / `Win+V` | `Ctrl+V` | Drag & Drop |
|----------|-------------------|----------|-------------|
| macOS    | ❌ Broken (text only) | ✅ Works | ✅ Works |
| Linux    | ⚠️ Inconsistent | ✅ Works | ✅ Works |
| Windows  | ⚠️ Struggles | ✅ Works | ✅ Works |

**GitHub Issues Tracking This:**
- Issue #834: "Unable to paste images into Claude Code TUI interface"
- Issue #1361: "[BUG] Can't paste image from clipboard"
- Issue #2266: "Feature Request: Terminal Graphics Protocol Support"

### Workarounds (Until Fixed):

1. **Use `Ctrl+V` instead of `Cmd+V`** (most reliable)
2. **Drag & Drop** (most consistent cross-platform)
3. **Use file path references** (always works)
4. **Hold Shift while dragging** (some terminals require this)

---

## 📚 Use Cases for Images in Claude Code

### 1. **Screenshot Debugging**
```
"Here's a screenshot of the error. What's causing it?"
```

### 2. **UI/UX Analysis**
```
"Describe the UI elements in this screenshot"
"What accessibility issues do you see?"
```

### 3. **Design-to-Code**
```
"Generate CSS to match this design mockup"
"Create React components based on this wireframe"
```

### 4. **Data Visualization Analysis**
```
"Extract data from this chart"
"What trends do you see in this graph?"
```

### 5. **Error Message Capture**
```
"Debug this error message" [paste screenshot]
```

---

## 🔍 Research Sources

### Official Documentation:
- **Claude Code Common Workflows**: https://docs.claude.com/en/docs/claude-code/common-workflows
- **Claude Vision Capabilities**: https://docs.claude.com/en/docs/build-with-claude/vision

### Key Articles Found:
1. **CometAPI Guide** (2025): "Can Claude Code see images— and how does that work in 2025?"
   - Confirmed base64 encoding method
   - API integration details

2. **Arsturn Blog**: "How to Paste Images in Claude Code: The `Control+V` Fix"
   - Documented the Ctrl+V workaround

3. **eesel.ai Developer Reference**: "A developer's Claude Code CLI reference (2025 guide)"
   - Comprehensive CLI capabilities overview

### GitHub Issues:
- #834: TUI interface paste issues (Ubuntu)
- #1361: Clipboard paste bug (cross-platform)
- #608: Screenshot pasting feature request
- #2266: Terminal graphics protocol support

---

## 💡 Technical Implementation Details

### Image Transmission Flow:

```
User Action (Paste/Drag/Path)
    ↓
CLI Captures Image Data
    ↓
Encode to Base64 String
    ↓
Wrap in API Message Format
    ↓
Send to Claude API (Sonnet 4.5)
    ↓
Model Processes with Vision
    ↓
Return Analysis/Code/Insights
```

### API Message Structure:
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": "iVBORw0KGgoAAAANS..."
          }
        },
        {
          "type": "text",
          "text": "What does this screenshot show?"
        }
      ]
    }
  ]
}
```

---

## 🎓 Best Practices

### For Users:

1. **Use `Ctrl+V` for pasting** (not Cmd+V)
2. **Drag & drop when possible** (most reliable)
3. **Preprocess large images** before sending
4. **Crop to relevant region** to reduce size
5. **Use high-quality images** (≥1000×1000px)

### For Developers/Scripts:

```python
import base64

# Convert image to base64 for API
with open('screenshot.png', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

# Send to Claude API
message = {
    "type": "image",
    "source": {
        "type": "base64",
        "media_type": "image/png",
        "data": image_data
    }
}
```

---

## 🔧 Troubleshooting Guide

### Issue: Can't Paste Images

**Try in order:**
1. Use `Ctrl+V` instead of `Cmd+V`
2. Try drag & drop
3. Save image and provide file path
4. Check clipboard contains image (not just file path)

### Issue: "Image too large" Error

**Solutions:**
1. Resize/compress image before sending
2. Crop to relevant area
3. Convert to JPEG (smaller than PNG)
4. Use image optimization tools

### Issue: Image Not Recognized

**Check:**
1. File format is supported (JPEG/PNG/GIF/WebP)
2. File is not corrupted
3. Permissions allow reading file
4. Path is absolute (not relative)

---

## 📊 Session Summary

| Aspect | Result |
|--------|--------|
| **User's Hypothesis** | ✅ CONFIRMED - Images converted to base64 |
| **Image Support Status** | ✅ ACTIVE (with known bugs) |
| **Best Method** | Drag & Drop > Ctrl+V > File Path |
| **Supported Formats** | JPEG, PNG, GIF, WebP |
| **Max File Size** | ~30MB |
| **Known Issues** | Cmd+V broken, clipboard handling buggy |
| **Documentation Quality** | Limited - mostly community-sourced |

---

## 🚀 Future Improvements Needed

Based on GitHub issues and user feedback:

1. **Fix `Cmd+V` paste handler** to read image data
2. **Implement terminal graphics protocols** (Sixel, Kitty, iTerm2)
3. **Better clipboard integration** across platforms
4. **Official documentation** of image capabilities
5. **Image preview** in terminal before sending
6. **Batch image support** (multiple images in one message)

---

## 📝 Related Resources

- **Claude API Vision Docs**: https://docs.claude.com/en/docs/build-with-claude/vision
- **Messages API Reference**: https://docs.claude.com/en/api/messages
- **Claude Code Setup Guide**: https://docs.claude.com/en/docs/claude-code/setup
- **Builder.io Claude Code Guide**: https://www.builder.io/blog/claude-code

---

## 🏷️ Tags

`claude-code` `image-support` `base64` `vision` `cli` `terminal` `screenshots` `api` `debugging` `2025`

---

**Session Conclusion**: User's understanding was accurate. Claude Code does support images via base64 encoding when pasted/provided, though clipboard pasting has platform-specific bugs requiring `Ctrl+V` workaround.
