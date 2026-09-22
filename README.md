# yt-dlp-live — Resilient Live Stream Recorder, Broadcaster & RTMP Relay

A robust, production-grade automation suite for capturing, relaying, and broadcasting YouTube Live streams with zero CPU re-encoding, resilient network dropout handling, and continuous MPEG-TS container safety.

---

## Capabilities

1. **Resilient Live Recording (`record_live.ps1` / `record_live.bat`)**:
   - Continuous MPEG-TS chunk capture (`--hls-use-mpegts`) preventing corrupt files on unexpected network dropouts.
   - DVR backlog capture (`--live-from-start`) to start from the beginning of ongoing streams.
   - Automatic lossless FFmpeg remuxing directly into `.mp4` upon completion (0% CPU re-encoding).
   - Auto-updater on launch ensuring cipher/signature parity against YouTube player JS changes.

2. **Real-Time Live Relay (`relay_live.ps1` / `relay_live.bat`)**:
   - Simultaneously relays any live YouTube broadcast to your private YouTube channel via RTMP while writing an archival `.mp4` to disk.
   - Powered by `streamlink` and `ffmpeg -f tee`.

3. **File Broadcaster (`stream_file_live.bat`)**:
   - Streams pre-recorded local `.mp4`/`.mkv`/`.ts` video files directly to YouTube RTMP ingest.
   - Instant pickup by YouTube Studio with 44.1kHz AAC audio compliance.

---

## Directory Structure

```
yt-dlp-live/
├── downloads/             # Saved streams organized by Channel and Date (gitignored)
├── record_live.bat        # Interactive CMD launcher for live recording
├── record_live.ps1        # PowerShell recorder with auto-update and lossless remux
├── relay_live.bat         # CMD launcher for simultaneous RTMP relay & local capture
├── relay_live.ps1         # PowerShell dual-tee RTMP + local recorder
├── stream_file_live.bat   # Direct video file RTMP broadcaster
├── yt-dlp.conf            # Portable optimized flags (retries, timeouts, 480p cap)
├── sync.ps1               # Automated repository sync & secret scanner
├── AGENTS.md              # Agent operating rules and workflow directives
├── LICENSE                # MIT License
└── README.md              # Technical documentation
```

---

## Quick Start

### Prerequisites
- **yt-dlp**: Place `yt-dlp.exe` in this folder or have `yt-dlp` available in your system `PATH`.
- **FFmpeg**: Required for remuxing and RTMP streaming (`ffmpeg` in `PATH`).
- **Streamlink** (optional for relay): Installed via `pip`, `winget`, or run via `uvx streamlink`.

### 1. Record an Active Live Stream
```powershell
.\record_live.ps1 -Url "https://www.youtube.com/watch?v=VIDEO_ID"
```
Or double-click `record_live.bat` and paste the URL.

### 2. Relay a Live Stream to your RTMP Channel
```powershell
.\relay_live.ps1 -SourceUrl "https://www.youtube.com/watch?v=VIDEO_ID" -StreamKey "YOUR-KEY"
```

### 3. Broadcast a Local Video to YouTube Live
Run `stream_file_live.bat`, choose the video file index from `downloads/`, and your channel will go live.

---

## Security & Sensitive Files

The following files are strictly **gitignored** and must never be committed:
- `stream_key.txt`: Private YouTube RTMP ingest key.
- `cookies.txt`: YouTube authentication session tokens.
- `downloads/`: Video recordings and raw streams.
- `yt-dlp.exe`: Large binary executables.

---

## Repository Sync & Maintenance

```powershell
# Routine automated sync
.\sync.ps1

# Custom semantic commit
.\sync.ps1 -m "feat(config): update retry backoff for HLS fragments"

# Pull only with rebase
.\sync.ps1 -PullOnly
```
