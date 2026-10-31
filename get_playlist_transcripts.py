#!/usr/bin/env python3
"""
YouTube Playlist Transcript Downloader
Fetches and saves transcripts for every video in a YouTube playlist video-wise.
Compatible with all versions of yt-dlp and youtube-transcript-api.
"""

import sys
import os
import re
import json
import argparse
from typing import List, Dict, Any, Optional, Tuple


def check_dependencies():
    """Verify that required 3rd party packages are installed."""
    missing = []
    try:
        import yt_dlp
    except ImportError:
        missing.append("yt-dlp")

    try:
        import youtube_transcript_api
    except ImportError:
        missing.append("youtube-transcript-api")

    if missing:
        print(f"Error: Missing required library/libraries: {', '.join(missing)}", file=sys.stderr)
        print("Please install them by running:\n  pip install yt-dlp youtube-transcript-api\n", file=sys.stderr)
        sys.exit(1)


def sanitize_filename(name: str) -> str:
    """Sanitize video/playlist titles to be safe for filesystem paths across Linux/macOS/Windows."""
    clean = re.sub(r'[\\/*?:"<>|]', "", name)
    clean = clean.strip().replace("\n", " ")
    return clean[:100] if clean else "untitled"


def format_timestamp(seconds: float) -> str:
    """Convert floating seconds to [HH:MM:SS] or [MM:SS]."""
    total_secs = int(seconds)
    mins, secs = divmod(total_secs, 60)
    hours, mins = divmod(mins, 60)
    if hours > 0:
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def normalize_snippets(items) -> List[Dict[str, Any]]:
    """Converts snippets from either objects or dicts into standard dictionary format."""
    normalized = []
    for item in items:
        if isinstance(item, dict):
            normalized.append({
                "text": item.get("text", "").strip(),
                "start": float(item.get("start", 0.0)),
                "duration": float(item.get("duration", 0.0))
            })
        else:
            normalized.append({
                "text": getattr(item, "text", "").strip(),
                "start": float(getattr(item, "start", 0.0)),
                "duration": float(getattr(item, "duration", 0.0))
            })
    return normalized


def get_playlist_videos(url_or_id: str, limit: Optional[int] = None) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Extracts video entries from a YouTube playlist URL or Playlist ID using yt-dlp.
    Returns (playlist_title, list of video info dicts).
    """
    import yt_dlp

    url = url_or_id.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        url = f"https://www.youtube.com/playlist?list={url}"

    print(f"Fetching playlist info from: {url}")

    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
        if not result:
            raise ValueError(f"Could not retrieve playlist information for '{url}'.")

        # Handle playlist vs single video URL passed
        entries = result.get('entries')
        playlist_title = result.get('title') or "YouTube Playlist"

        videos = []
        if entries is not None:
            # It is a playlist
            for idx, entry in enumerate(entries, start=1):
                if not entry:
                    continue
                video_id = entry.get('id')
                if not video_id:
                    continue
                title = entry.get('title') or f"Video {idx}"
                videos.append({
                    'index': idx,
                    'id': video_id,
                    'title': title,
                    'url': f"https://www.youtube.com/watch?v={video_id}"
                })
                if limit and len(videos) >= limit:
                    break
        else:
            # Single video fallback
            video_id = result.get('id')
            if video_id:
                videos.append({
                    'index': 1,
                    'id': video_id,
                    'title': result.get('title', 'Video 1'),
                    'url': f"https://www.youtube.com/watch?v={video_id}"
                })

        return playlist_title, videos


def fetch_transcript(video_id: str, languages: List[str]) -> Optional[List[Dict[str, Any]]]:
    """
    Fetches transcript for a video, supporting both youtube-transcript-api v1.0+ and legacy v0.x.
    Falls back across manual captions, auto-generated captions, and auto-translation.
    """
    from youtube_transcript_api import YouTubeTranscriptApi

    # Modern v1.0+ instance-based API
    if hasattr(YouTubeTranscriptApi, 'fetch'):
        api = YouTubeTranscriptApi()

        # 1. Direct fetch with requested languages
        try:
            return normalize_snippets(api.fetch(video_id, languages=languages))
        except Exception:
            pass

        # 2. Detailed search through available transcripts
        try:
            transcript_list = api.list(video_id)
            # Try manual transcript in requested languages
            try:
                return normalize_snippets(transcript_list.find_manually_created_transcript(languages).fetch())
            except Exception:
                pass
            # Try auto-generated transcript in requested languages
            try:
                return normalize_snippets(transcript_list.find_generated_transcript(languages).fetch())
            except Exception:
                pass
            # Fallback: Translate first available transcript into target language
            try:
                first = next(iter(transcript_list))
                target_lang = languages[0] if languages else 'en'
                if first.is_translatable:
                    return normalize_snippets(first.translate(target_lang).fetch())
                return normalize_snippets(first.fetch())
            except Exception:
                pass
        except Exception:
            pass
        return None

    # Legacy v0.x static API fallback
    try:
        return normalize_snippets(YouTubeTranscriptApi.get_transcript(video_id, languages=languages))
    except Exception:
        pass

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        try:
            return normalize_snippets(transcript_list.find_manually_created_transcript(languages).fetch())
        except Exception:
            pass
        try:
            return normalize_snippets(transcript_list.find_generated_transcript(languages).fetch())
        except Exception:
            pass
        try:
            first = next(iter(transcript_list))
            target_lang = languages[0] if languages else 'en'
            if first.is_translatable:
                return normalize_snippets(first.translate(target_lang).fetch())
            return normalize_snippets(first.fetch())
        except Exception:
            pass
    except Exception:
        pass

    return None


def format_transcript_text(video: Dict[str, Any], transcript: List[Dict[str, Any]], include_timestamps: bool) -> str:
    """Formats transcript into plain text string."""
    lines = [
        f"Title: {video['title']}",
        f"Video URL: {video['url']}",
        f"Video ID: {video['id']}",
        "=" * 70,
        ""
    ]
    for item in transcript:
        text = item['text'].replace("\n", " ").strip()
        if not text:
            continue
        if include_timestamps:
            ts = format_timestamp(item['start'])
            lines.append(f"[{ts}] {text}")
        else:
            lines.append(text)
    lines.append("")
    return "\n".join(lines)


def save_video_transcript(video: Dict[str, Any], transcript: List[Dict[str, Any]],
                          output_dir: str, include_timestamps: bool, export_json: bool):
    """Saves individual video transcript as .txt and optionally as .json."""
    index = video['index']
    title_safe = sanitize_filename(video['title'])
    base_name = f"{index:03d}_{title_safe}_{video['id']}"

    # Save .txt
    txt_path = os.path.join(output_dir, f"{base_name}.txt")
    txt_content = format_transcript_text(video, transcript, include_timestamps)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(txt_content)

    # Save .json (if requested)
    if export_json:
        json_path = os.path.join(output_dir, f"{base_name}.json")
        payload = {
            "index": index,
            "title": video['title'],
            "url": video['url'],
            "id": video['id'],
            "transcript": transcript
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Download transcripts for all videos in a YouTube playlist, organized video-by-video."
    )
    parser.add_argument(
        "playlist_url",
        nargs="?",
        default="https://www.youtube.com/playlist?list=PLui3EUkuMTPgZcV0QhQrOcwMPcBCcd_Q1",
        help="YouTube Playlist URL or Playlist ID (default: https://www.youtube.com/playlist?list=PLui3EUkuMTPgZcV0QhQrOcwMPcBCcd_Q1)"
    )
    parser.add_argument(
        "-o", "--output-dir", default="./transcripts",
        help="Directory where transcripts will be stored (default: ./transcripts)"
    )
    parser.add_argument(
        "-l", "--languages", nargs="+", default=["en", "en-US", "en-GB"],
        help="Languages to attempt in order of priority (default: en en-US en-GB)"
    )
    parser.add_argument(
        "--no-timestamps", action="store_true",
        help="Do not prepend timestamps to transcript lines"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Save raw structured JSON data alongside text files"
    )
    parser.add_argument(
        "--combine", action="store_true",
        help="Also export a single combined 'all_transcripts.txt' file for the entire playlist"
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Limit processing to the first N videos in the playlist"
    )

    args = parser.parse_args()
    check_dependencies()

    # 1. Fetch playlist metadata
    try:
        playlist_title, videos = get_playlist_videos(args.playlist_url, limit=args.limit)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not videos:
        print("No videos found in the specified playlist.")
        return

    # 2. Setup output folder: <output-dir>/<Playlist_Name>/
    folder_name = sanitize_filename(playlist_title)
    target_dir = os.path.join(args.output_dir, folder_name)
    os.makedirs(target_dir, exist_ok=True)

    print(f"\nPlaylist: '{playlist_title}'")
    print(f"Total videos to process: {len(videos)}")
    print(f"Output folder: {os.path.abspath(target_dir)}\n")

    successful = 0
    failed = 0
    combined_texts = []

    # 3. Iterate through videos and download transcripts
    for video in videos:
        idx = video['index']
        title = video['title']
        vid_id = video['id']

        print(f"[{idx}/{len(videos)}] {title} ({vid_id}) ... ", end="", flush=True)

        transcript = fetch_transcript(vid_id, args.languages)

        if transcript:
            save_video_transcript(
                video=video,
                transcript=transcript,
                output_dir=target_dir,
                include_timestamps=not args.no_timestamps,
                export_json=args.json
            )
            if args.combine:
                combined_texts.append(format_transcript_text(video, transcript, not args.no_timestamps))

            print(f"DONE ({len(transcript)} snippets)")
            successful += 1
        else:
            print("SKIPPED (no transcript available)")
            failed += 1

    # 4. Optional combined file
    if args.combine and combined_texts:
        combined_path = os.path.join(target_dir, "000_ALL_TRANSCRIPTS_COMBINED.txt")
        with open(combined_path, "w", encoding="utf-8") as f:
            f.write(f"FULL PLAYLIST TRANSCRIPTS: {playlist_title}\n")
            f.write(f"Total Videos: {successful}\n")
            f.write("#" * 70 + "\n\n")
            f.write("\n\n" + ("#" * 70) + "\n\n".join(combined_texts))
        print(f"\nCombined transcript saved to: {combined_path}")

    print("\n" + "=" * 60)
    print(f"Summary: {successful} downloaded, {failed} unavailable/failed out of {len(videos)} videos.")
    print(f"Transcripts directory: {os.path.abspath(target_dir)}")


if __name__ == "__main__":
    main()
