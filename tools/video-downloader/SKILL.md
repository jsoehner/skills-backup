---

name: video-downloader

description: |

  Toolkit for downloading, converting, and archiving online video content from YouTube and other platforms using command-line utilities. Trigger when requested to download, save, rip, extract audio from, or archive online videos or playlists. Keywords: video-downloader, yt-dlp, ffmpeg, download youtube, download playlist, convert video, extract mp3.



  Toolkit for downloading, converting, and archiving online video content from YouTube and other platforms using command-line utilities. Trigger when requested to download, save, rip, extract audio from, or archive online videos or playlists. Keywords: video-downloader, yt-dlp, ffmpeg, download youtube, download playlist, convert video, extract mp3.



license: Complete terms in LICENSE.txt

---



# Video Downloader - Command-Line Operations & Workflows



A technical framework for downloading, converting, and archiving video/audio streams using CLI utilities like `yt-dlp` and `ffmpeg`.



## Progressive Disclosure & Self-Containment



- **Self-Contained Instruction**: This is a self-contained skill. Do NOT load external files or reference directories. All execution guidelines and CLI configurations are detailed directly below.

- **Dependency Trigger**: Before executing download commands, verify that `yt-dlp` and `ffmpeg` are installed and up to date on the host system.



## Freedom Calibration & Constraints

- **Constraint Level: Low-Medium**

  - **High Rigidity**: Strict syntax for `yt-dlp` format selection, cookie authentication passing, rate limit safety, and error handling.

  - **Medium Freedom**: Selection of output destination folders, naming patterns, and custom quality boundaries (720p vs. 1080p).



## Decision Tree: Formats & Quality Matrix



```

What is the target asset type and delivery constraint?

 ├─ Video Asset

 │   ├─ High Compatibility / Web Streaming → Download as: MP4 (H.264 + AAC)

 │   │   └─ Command arg: -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" --merge-output-format mp4

 │   └─ Archive Quality / Master Edition → Download as: Best Available (usually WebM/VP9)

 │       └─ Command arg: -f bestvideo+bestaudio --merge-output-format mkv

 └─ Audio Only

     ├─ Podcast / Talk Show (Voice) → Extract as: MP3 / AAC (128kbps)

     │   └─ Command arg: -x --audio-format mp3 --audio-quality 128K

     └─ High-Fidelity Music / Sound FX → Extract as: FLAC / WAV (Lossless)

         └─ Command arg: -x --audio-format flac

```



## Professional Mindset & Design Principles

1. **Network Safety & Rate Limiting**: Avoid slamming host platforms. Use sleep intervals, user-agents, and bandwidth limits to prevent temporary or permanent IP bans (HTTP 429).

2. **Metadata & Archival Quality**: Maintain structural integrity of archives. Download thumbnail art, write JSON metadata files, and preserve upload timestamps where possible.

3. **Format Merging Heuristics**: Modern streaming sites serve high-definition video (1080p+) and audio streams as separate files. `ffmpeg` must be present on the system path to merge these streams dynamically after download.



---



## Core Command-Line Workflows



### 1. High-Definition Video Download (1080p, MP4 Container)

Merges best video (capped at 1080p) and best audio into a single MP4 file:

```bash

yt-dlp -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080][ext=mp4]" \

       --merge-output-format mp4 \

       -o "%(title)s.%(ext)s" \

       "https://www.youtube.com/watch?v=VIDEO_ID"

```



### 2. Audio Extraction (MP3 Format, High Quality)

Downloads the source stream, extracts the audio track, and encodes to MP3:

```bash

yt-dlp -x --audio-format mp3 \

       --audio-quality 320K \

       -o "%(title)s.%(ext)s" \

       "https://www.youtube.com/watch?v=VIDEO_ID"

```



### 3. Playlist Archiving (With Metadata and Rate Limiting)

Safely downloads a playlist with rate limits to prevent IP blocks:

```bash

yt-dlp -f "bestvideo[height<=1080]+bestaudio/best" \

       --sleep-interval 5 --max-sleep-interval 15 \

       --limit-rate 5M \

       --write-thumbnail --write-info-json \

       -o "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" \

       "PLAYLIST_URL"

```



---



## Critical Anti-Patterns (NEVER List)



| Anti-Pattern | Description | Alternative / Solution |

| :--- | :--- | :--- |

| **NEVER** run high-volume loops without sleep intervals | Triggering rapid, sequential downloads of large playlists causes immediate IP bans (HTTP 429). | Use `--sleep-interval 5` or similar spacing parameters. |

| **NEVER** attempt HD downloads without `ffmpeg` | Without `ffmpeg`, `yt-dlp` cannot merge separate video/audio streams, failing or defaulting to low-res 720p. | Verify `ffmpeg` path availability before running HD commands. |

| **NEVER** download using default user agents on restricted domains | Standard Python or curl user agents trigger bot detection and blocking mechanisms. | Allow `yt-dlp` to manage its default browser spoofing or specify `--user-agent`. |

| **NEVER** write output to temporary folders without extensions | Storing media assets without proper file tags causes player software to fail to recognize codecs. | Always use explicit templates like `-o "%(title)s.%(ext)s"`. |

| **NEVER** download private or age-restricted videos without auth | Fetching restricted content directly will fail with HTTP 403 or signature verification errors. | Use the browser cookie export parameter: `--cookies-from-browser chrome`. |



---



## Common Error Scenarios & Fallbacks



### Scenario 1: HTTP Error 403: Forbidden (or "Sign in to confirm you are not a bot")

- **Root Cause**: Platform is blocking anonymous requests.

- **Fallback**: Pass cookies from a browser session where you are logged in.

  ```bash

  yt-dlp --cookies-from-browser chrome "URL"

  ```



### Scenario 2: Error: `ffmpeg` not found

- **Root Cause**: Host does not have the `ffmpeg` binary installed or added to the system PATH.

- **Fallback**: 

  1. For debian/ubuntu: `sudo apt-get install ffmpeg`

  2. For macOS: `brew install ffmpeg`

  3. Alternatively, fall back to downloading single-stream formats (which do not require merging but are capped at 720p):

     ```bash

     yt-dlp -f "best[ext=mp4]" "URL"

     ```



### Scenario 3: HTTP Error 429: Too Many Requests (Rate Limited)

- **Root Cause**: IP address has been flagged for scraping.

- **Fallback**:

  1. Add a proxy address using `--proxy "http://username:password@ip:port"`.

  2. Increase the sleep delay between files or reduce download bandwidth limits:

     ```bash

     yt-dlp --limit-rate 2M --sleep-interval 30 "URL"

     ```


