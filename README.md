# 📦 downloads-organizer

**Organize your `Downloads/` folder automatically** by sorting files into structured subfolders like `year/month` or `year/extension`.  
Includes dry-run support, filtering, custom rules, and logging.

---

## ✅ Features

- 🗂️ Organize files by **year/month** or **year/extension**
- 🧼 Skip unwanted files (e.g. `.tmp`, `.crdownload`, `.part`, etc.)
- 🔍 Filter files modified in the last **N days**
- 🚫 Simulate without moving with `--dry-run`
- 📣 Verbose logging with `--verbose`
- ⚙️ Custom extension exclusion (`--exclude-exts`)

---

## 📥 Installation

No external dependencies. Just Python 3.7+

```bash
git clone https://github.com/guilhermevini/downloads-organizer.git
cd downloads-organizer
python organize_downloads.py
```

Or make it executable globally:

```bash
chmod +x organize_downloads.py
mv organize_downloads.py /usr/local/bin/downloads-organizer
downloads-organizer
```

---

## 🚀 Usage

```bash
python organize_downloads.py [OPTIONS]
```

### 📌 Available Options:

| Option               | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `--dir`              | Directory to organize (default: `~/Downloads`)                              |
| `--mode`             | Organization mode: `year_month` or `year_extension` (default: `year_month`) |
| `--dry-run`          | Simulate actions without moving files                                       |
| `--days N`           | Only include files modified in the last N days                              |
| `--exclude-exts`     | Comma-separated list of file extensions to exclude                          |
| `--verbose`          | Enable detailed debug logging                                                |

---

## 📁 Examples

### 1. Organize by year/month (default)

```bash
python organize_downloads.py
```

### 2. Organize by year/extension

```bash
python organize_downloads.py --mode year_extension
```

### 3. Simulate (dry-run) what would happen

```bash
python organize_downloads.py --dry-run --verbose
```

### 4. Move only files from the last 7 days

```bash
python organize_downloads.py --days 7
```

### 5. Exclude PDFs and ZIPs from being moved

```bash
python organize_downloads.py --exclude-exts .pdf,.zip
```

---

## 📂 Output Folder Structure

By default, organized files go into a subfolder called `organized/` inside your target directory.

Examples:

```
Downloads/
└── organized/
    └── 2025/
        └── 08/
            └── invoice.pdf
```

Or if using `--mode year_extension`:

```
Downloads/
└── organized/
    └── 2025/
        └── pdf/
            └── invoice.pdf
```

---

## ⚖ License

[MIT License](LICENSE)

---

## 🤝 Contributing

Feel free to fork and open pull requests! Ideas and improvements are welcome.