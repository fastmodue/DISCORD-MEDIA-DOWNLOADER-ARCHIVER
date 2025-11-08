#made by fastmodue & HIPPO84 :D

import requests
import time
import sys
import os
import re
from datetime import datetime
from pathlib import Path

def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║          DISCORD MEDIA DOWNLOADER & ARCHIVER          ║
    ║                BY FASTMODUE & HIPPO84                 ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)

def get_headers(token):
    return {
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

def get_dms(token, include_dms=True, include_groups=True):
    """Fetch DM channels and/or group DMs"""
    headers = get_headers(token)
    response = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers)
    
    if response.status_code == 200:
        all_channels = response.json()
        filtered_channels = []
        
        # Type 1 = DM, Type 3 = Group DM
        if include_dms:
            filtered_channels.extend([ch for ch in all_channels if ch.get('type') == 1])
        if include_groups:
            filtered_channels.extend([ch for ch in all_channels if ch.get('type') == 3])
        
        return filtered_channels
    elif response.status_code == 401:
        print("[ERROR] Invalid token! Please check your token and try again.")
        sys.exit(1)
    else:
        print(f"[ERROR] Failed to fetch channels: {response.status_code}")
        return []

def get_channel_name(channel):
    """Get a display name for a channel"""
    if channel.get('type') == 1:  # DM
        recipients = channel.get('recipients', [])
        if recipients:
            return f"DM with {recipients[0].get('username', 'Unknown')}"
        return "Unknown DM"
    elif channel.get('type') == 3:  # group
        return channel.get('name', 'Unnamed Group')
    return "Unknown Channel"

def get_messages(token, channel_id, after_date=None):
    """Fetch all messages from a channel with optional date filter"""
    headers = get_headers(token)
    all_messages = []
    last_message_id = None
    
    print("[Fetching messages", end='', flush=True)
    
    while True:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=100'
        if last_message_id:
            url += f'&before={last_message_id}'
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            messages = response.json()
            if not messages:
                break
            
            for msg in messages:
                # date filter
                if after_date:
                    msg_date = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))
                    if msg_date < after_date:
                        print("]")
                        return all_messages
                
                all_messages.append(msg)
            
            last_message_id = messages[-1]['id']
            print(".", end='', flush=True)
            time.sleep(0.3)  # rate limit
        elif response.status_code == 429:
            retry_after = response.json().get('retry_after', 5)
            print(f"\n[RATE LIMITED] Waiting {retry_after}s...")
            time.sleep(retry_after)
        else:
            print(f"\n[ERROR] Failed to fetch messages: {response.status_code}")
            break
    
    print("]")
    return all_messages

def download_file(url, filepath):
    """Download a file from URL to filepath"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        return False
    except Exception as e:
        print(f"[ERROR] Download failed: {str(e)}")
        return False

def get_file_extension(url):
    """Extract file extension from URL"""
    clean_url = url.split('?')[0]
    ext = os.path.splitext(clean_url)[1]
    return ext if ext else '.unknown'

def is_video(filename):
    """Check if file is a video"""
    video_exts = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv', '.m4v']
    return any(filename.lower().endswith(ext) for ext in video_exts)

def is_image(filename):
    """Check if file is an image"""
    image_exts = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg']
    return any(filename.lower().endswith(ext) for ext in image_exts)

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def progress_bar(current, total, prefix='Progress', bar_length=40):
    """Display a progress bar"""
    if total == 0:
        return
    percent = current / total
    filled = int(bar_length * percent)
    bar = '█' * filled + '░' * (bar_length - filled)
    percentage = int(percent * 100)
    print(f'\r[{prefix}] {bar} {percentage}% ({current}/{total})', end='', flush=True)

def parse_date_input(date_str):
    """Parse date string in various formats"""
    formats = [
        '%Y-%m-%d',           # 2025-01-01
        '%d/%m/%Y',           # 01/01/2025
        '%m/%d/%Y',           # 01/01/2025
        '%Y/%m/%d',           # 2025/01/01
        '%d-%m-%Y',           # 01-01-2025
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None

def main():
    print_banner()
    
    token = input("Enter your Discord token: ").strip()
    
    if not token:
        print("[ERROR] Token cannot be empty!")
        return
    
    # Ask what to scan
    print("\n[Scan Options]")
    print("  1. Group DMs only")
    print("  2. Direct Messages (DMs) only")
    print("  3. Both Groups and DMs")
    
    scan_choice = input("\nSelect option (1-3) [default: 1]: ").strip()
    
    include_groups = scan_choice in ['1', '3', '']
    include_dms = scan_choice in ['2', '3']
    
    print("\n[Scanning for channels...]")
    channels = get_dms(token, include_dms=include_dms, include_groups=include_groups)
    
    if not channels:
        print("[ERROR] No channels found or unable to fetch channels!")
        return
    
    # seperate then count
    dms = [ch for ch in channels if ch.get('type') == 1]
    groups = [ch for ch in channels if ch.get('type') == 3]
    
    print(f"\n[Found {len(dms)} DMs and {len(groups)} groups]")
    
    # display channels to user
    if channels:
        print("\nAvailable Channels:")
        for i, channel in enumerate(channels, 1):
            channel_name = get_channel_name(channel)
            channel_id = channel['id']
            channel_type = "DM" if channel.get('type') == 1 else "Group"
            print(f"  [{i}] [{channel_type}] {channel_name} (ID: {channel_id})")
    
    channel_input = input("\nEnter channel IDs to scan (comma-separated) or press Enter for ALL: ").strip()
    
    if channel_input:
        selected_ids = [id.strip() for id in channel_input.split(',')]
        channels_to_scan = [ch for ch in channels if ch['id'] in selected_ids]
    else:
        channels_to_scan = channels
    
    print(f"\n[Will scan {len(channels_to_scan)} channel(s)]")
    
    # organization
    folder_per_channel = input("\nCreate separate folder for each DM/Group? (y/n) [default: n]: ").strip().lower()
    folder_per_channel = folder_per_channel == 'y'
    
    if folder_per_channel:
        print("[Will create separate folders for each channel]")
    else:
        print("[Will organize by file type (images/videos)]")
    
    # date filter
    date_input = input("\nDownload from date (YYYY-MM-DD) or press Enter for ALL TIME: ").strip()
    after_date = None
    
    if date_input:
        after_date = parse_date_input(date_input)
        if after_date:
            print(f"[Will download media from {after_date.strftime('%Y-%m-%d')} onwards]")
        else:
            print("[ERROR] Invalid date format! Using ALL TIME instead.")
    else:
        print("[Downloading ALL media from ALL TIME]")
    
    # download directory
    os.makedirs('downloads', exist_ok=True)
    
    # subdirectories
    if not folder_per_channel:
        os.makedirs('downloads/images', exist_ok=True)
        os.makedirs('downloads/videos', exist_ok=True)
    
    # counters
    total_images = 0
    total_videos = 0
    total_failed = 0
    overall_processed = 0
    
    # math 
    print("\n[Scanning channels for media...]")
    channel_attachments = {}
    total_attachments = 0
    
    for idx, channel in enumerate(channels_to_scan, 1):
        channel_name = get_channel_name(channel)
        channel_id = channel['id']
        progress_bar(idx, len(channels_to_scan), prefix='Scanning')
        
        messages = get_messages(token, channel_id, after_date)
        attachments_count = sum(len(msg.get('attachments', [])) for msg in messages)
        channel_attachments[channel_id] = {
            'messages': messages,
            'count': attachments_count,
            'name': channel_name
        }
        total_attachments += attachments_count
    
    print(f"\n[Total media found: {total_attachments}]")
    
    if total_attachments == 0:
        print("[No media to download!]")
        return
    
    # Open links file
    with open('downloads/links.txt', 'w', encoding='utf-8') as links_file:
        links_file.write("=" * 70 + "\n")
        links_file.write("DISCORD MEDIA ARCHIVE\n")
        links_file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        links_file.write("=" * 70 + "\n\n")
        
        # Process each channel
        for channel in channels_to_scan:
            channel_id = channel['id']
            channel_data = channel_attachments[channel_id]
            channel_name = channel_data['name']
            messages = channel_data['messages']
            attachments_in_channel = channel_data['count']
            
            if attachments_in_channel == 0:
                continue
            
            print(f"\n{'='*60}")
            print(f"[Processing] {channel_name}")
            print(f"{'='*60}")
            
            # Create folders for this channel if needed
            if folder_per_channel:
                safe_channel_name = sanitize_filename(channel_name)
                channel_folder = os.path.join('downloads', safe_channel_name)
                os.makedirs(os.path.join(channel_folder, 'images'), exist_ok=True)
                os.makedirs(os.path.join(channel_folder, 'videos'), exist_ok=True)
            
            links_file.write(f"\n{'='*70}\n")
            links_file.write(f"CHANNEL: {channel_name}\n")
            links_file.write(f"CHANNEL ID: {channel_id}\n")
            links_file.write(f"{'='*70}\n\n")
            
            # Process messages
            for msg in messages:
                attachments = msg.get('attachments', [])
                if not attachments:
                    continue
                
                msg_timestamp = msg.get('timestamp', '')
                msg_date = datetime.fromisoformat(msg_timestamp.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
                
                for attachment in attachments:
                    url = attachment.get('url', '')
                    if not url or not ('cdn.discordapp.com' in url or 'media.discordapp.net' in url):
                        continue
                    
                    filename = attachment.get('filename', 'unknown')
                    filename = sanitize_filename(filename)
                    file_ext = get_file_extension(filename)
                    
                    # file type and destination
                    if folder_per_channel:
                        safe_channel_name = sanitize_filename(channel_name)
                        channel_folder = os.path.join('downloads', safe_channel_name)
                        if is_video(filename):
                            dest_folder = os.path.join(channel_folder, 'videos')
                            file_type = 'video'
                            total_videos += 1
                        elif is_image(filename):
                            dest_folder = os.path.join(channel_folder, 'images')
                            file_type = 'image'
                            total_images += 1
                        else:
                            dest_folder = os.path.join(channel_folder, 'images')
                            file_type = 'unknown'
                            total_images += 1
                    else:
                        if is_video(filename):
                            dest_folder = 'downloads/videos'
                            file_type = 'video'
                            total_videos += 1
                        elif is_image(filename):
                            dest_folder = 'downloads/images'
                            file_type = 'image'
                            total_images += 1
                        else:
                            dest_folder = 'downloads/images'
                            file_type = 'unknown'
                            total_images += 1
                    
                    # FILE NAMES (need to fix small issue)
                    timestamp_suffix = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                    unique_filename = f"{Path(filename).stem}_{timestamp_suffix}{file_ext}"
                    filepath = os.path.join(dest_folder, unique_filename)
                    
                    # download the file
                    if download_file(url, filepath):
                        links_file.write("-" * 70 + "\n")
                        links_file.write(f"{url}\n")
                        links_file.write(f"DATE: {msg_date}\n")
                        links_file.write(f"TYPE: {file_ext}\n")
                        links_file.write(f"FILE: {unique_filename}\n")
                        links_file.write(f"CATEGORY: {file_type}\n")
                        links_file.write("-" * 70 + "\n\n")
                    else:
                        total_failed += 1
                    
                    overall_processed += 1
                    progress_bar(overall_processed, total_attachments, prefix='Overall Progress')
                    time.sleep(0.2)  # Ratelimit again
    
    print()  
    
    # and a summary for the end :D
    print(f"\n╔═══════════════════════════════════════╗")
    print(f"║        DOWNLOAD COMPLETE!             ║")
    print(f"╠═══════════════════════════════════════╣")
    print(f"║  Images:  {total_images:<3}                        ║")
    print(f"║  Videos:  {total_videos:<3}                        ║")
    print(f"║  Failed:  {total_failed:<3}                        ║")
    print(f"╚═══════════════════════════════════════╝")
    
    if folder_per_channel:
        print(f"\n[Files saved to: downloads/[channel_name]/]")
    else:
        print(f"\n[Files saved to: downloads/images/ and downloads/videos/]")
    
    print(f"[Links saved to: downloads/links.txt]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n[Cancelled by user]")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        sys.exit(1)

