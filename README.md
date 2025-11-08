#  DISCORD MEDIA DOWNLOADER & ARCHIVER

A powerful Python tool to download and archive all media (images, videos) from your Discord DMs and Group chats with progress tracking and flexible organization options.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License: GPL v3](https://img.shields.io/badge/license-GPL%203.0-blue.svg)

## Features

-  **Download all media** from Discord DMs and Group chats
-  **Selective scanning** - Choose specific channels or scan all
-  **Flexible organization** - Organize by file type or create separate folders per conversation
-  **Date filtering** - Download media from a specific date onwards
-  **Progress tracking** - Real-time progress bars and download statistics
-  **Link archiving** - Automatically saves all media links with metadata
-  **Clean CLI** - Clean, user-friendly interface with progress indicators
-  **Rate limit handling** - Smart handling of Discord API rate limits

##  Quick Start

### Prerequisites

- Python 3.7 or higher
- Discord user token

### Installation

1. Clone the repository:
```bash
git clone https://github.com/fastmodue/DISCORD-MEDIA-DOWNLOADER-ARCHIVER.git
cd DISCORD-MEDIA-DOWNLOADER-ARCHIVER
```

2. Install required dependencies:
```bash
pip install requests
```

### Usage

1. Run the script:
```bash
python main.py
```

2. Enter your Discord token when prompted

3. Choose what to scan:
   - Group DMs only
   - Direct Messages only
   - Both Groups and DMs

4. Select channels to scan (or press Enter for all)

5. Choose folder organization:
   - Separate folder per channel
   - Organize by file type (images/videos)

6. Optionally set a date filter (YYYY-MM-DD format)

7. Sit back and relax 🍷

## 📂 Output Structure

### Organized by File Type (default):
```
downloads/
├── images/
│   ├── image1_20250108_123456.png
│   └── image2_20250108_123457.jpg
├── videos/
│   ├── video1_20250108_123458.mp4
│   └── video2_20250108_123459.mp4
└── links.txt
```

### Organized by Channel:
```
downloads/
├── DM with username/
│   ├── images/
│   └── videos/
├── Group Name/
│   ├── images/
│   └── videos/
└── links.txt
```

## 🔑 Getting Your Discord Token

### Desktop App / Browser:
1. Open Discord (app or browser)
2. Press `Ctrl + Shift + I` (Windows/Linux) or `Cmd + Option + I` (Mac)
3. Go to the **Console** tab
4. Paste this code and press Enter:
```javascript
let token;
window.webpackChunkdiscord_app.push([[Symbol()], {}, o => {
  for (let e of Object.values(o.c)) {
    try {
      if (!e.exports || e.exports === window) continue;
      if (e.exports?.getToken) {
        token = e.exports.getToken();
        console.log("Token:", token);
      }
      for (let o in e.exports) {
        if (e.exports?.[o]?.getToken && "IntlMessagesProxy" !== e.exports[o][Symbol.toStringTag]) {
          token = e.exports[o].getToken();
          console.log("Token:", token);
        }
      }
    } catch {}
  }
}]);
window.webpackChunkdiscord_app.pop();
```
5. Copy the token (without quotes)

⚠️ **Security Warning**: Never share your token with anyone! It gives full access to your Discord account.

## 📊 Features Breakdown

### Date Filtering
Download media from a specific date onwards. Supports multiple date formats:
- `2025-01-08`
- `08/01/2025`
- `01/08/2025`
- `08-01-2025`

### Progress Tracking
- **Scanning Phase**: Shows progress while scanning channels
- **Overall Progress**: Displays total download progress with percentage
- **Real-time Updates**: See exactly what's being downloaded

### Links Archive
The `links.txt` file contains:
- Original media URLs
- Upload dates
- File types
- Saved filenames
- Media categories

## 🛠️ Supported File Types

### Images
`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`, `.svg`

### Videos
`.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.flv`, `.wmv`, `.m4v`

## ⚠️ Important Notes

- Files are saved with timestamps to avoid naming conflicts
- The script respects Discord's rate limits
- Progress is saved in `links.txt` for reference
- Invalid filenames are automatically sanitized

## 🤝 Contributors

Made with ❤️ by:
- **[@fastmodue](https://github.com/fastmodue)** - Discord: `fastmodue`
- **[@HIPPO84](https://github.com/hipporr)** - Discord: `hippo844`

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## ⚡ Support

Having issues? Found a bug? Want to contact us?
- 📜 Contact us:
- https://discord.gg/Ju4xe6gYJ4
- Or add us on discord: fastmodue, hippo844
- [Report a Bug](https://github.com/fastmodue/DISCORD-MEDIA-DOWNLOADER-ARCHIVER/issues)
- [Request a Feature](https://github.com/fastmodue/DISCORD-MEDIA-DOWNLOADER-ARCHIVER/issues)
  
- ⭐ Star this repo if you find it useful!

## 📸 Screenshots

```
 ╔═══════════════════════════════════════════════════════╗
 ║                                                       ║
 ║          DISCORD MEDIA DOWNLOADER & ARCHIVER          ║
 ║                BY FASTMODUE & HIPPO84                 ║
 ║                                                       ║
 ╚═══════════════════════════════════════════════════════╝

[Overall Progress] ████████████████████░░░░░░░░░ 65% (130/200)
```

---

**Disclaimer**: This tool is for personal archival purposes only. Respect Discord's Terms of Service and others' privacy. The developers are not responsible for misuse of this tool.
