import os
import re
import csv
import requests
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from concurrent.futures import ThreadPoolExecutor, as_completed
import string

# --- KONFIGURASI ---
SCRIPT_DIR = Path(__file__).parent.absolute()
DOWNLOAD_DIR = str(SCRIPT_DIR / 'download_files')
LOG_DIR = SCRIPT_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)
SUCCESS_CSV = SCRIPT_DIR / 'upload_success.csv'
RCLONE_CONFIG = str(SCRIPT_DIR / 'rclone' / 'rclone.conf')
RCLONE_REMOTES = ['gdrive1', 'gdrive2', 'gdrive3']
REMOTE_FOLDER = 'ebook'
API_BASE_URL = 'https://www.api.staisenorituban.ac.id'
API_SEARCH_URL = f'{API_BASE_URL}/search_books'
API_UPLOAD_DATA_URL = f'{API_BASE_URL}/upload_data'
FUZZY_THRESHOLD = 0.7  # 70% kemiripan judul
MAX_WORKERS = 5        # Jumlah upload paralel

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'uploader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def clean_filename(filename):
    base, ext = os.path.splitext(filename)
    base = re.sub(r'\(z-library.*?\)', '', base, flags=re.IGNORECASE)
    base = re.sub(r'\s+', ' ', base).strip()
    return f"{base}{ext}"

def fuzzy_match(title1, title2):
    return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation)).strip()

def extract_title_before_paren(filename):
    base, _ = os.path.splitext(filename)
    title = base.split('(')[0].strip()
    return remove_punctuation(title)

def extract_author_from_filename(filename):
    base, _ = os.path.splitext(filename)
    matches = re.findall(r'\(([^)]+)\)', base)
    if matches:
        return matches[-1].strip()
    return ''

def extract_first_3_words(filename):
    base, _ = os.path.splitext(filename)
    base = base.split('(')[0].strip()
    words = base.split()
    return ' '.join(words[:3])

def find_db_match(file_title, file_author=None):
    try:
        resp = requests.get(API_SEARCH_URL, params={'q': file_title, 'per_page': 20}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for book in data.get('results', []):
                db_title = book.get('title', '')
                db_author = book.get('author', '').lower()
                clean_file_title = remove_punctuation(file_title).lower()
                clean_db_title = remove_punctuation(db_title).lower()
                # Fuzzy match
                if fuzzy_match(clean_file_title, clean_db_title) >= FUZZY_THRESHOLD:
                    return book
                # Substring match
                if clean_db_title in clean_file_title or clean_file_title in clean_db_title:
                    return book
                # Author match (optional)
                if file_author and file_author.lower() in db_author and (clean_db_title in clean_file_title or clean_file_title in clean_db_title):
                    return book
    except Exception as e:
        logger.error(f"Error searching DB: {e}")
    return None

def upload_with_rclone(local_path):
    filename = os.path.basename(local_path)
    rclone_log_file = LOG_DIR / "rclone_all.log"
    for remote in RCLONE_REMOTES:
        remote_path = f"{remote}:{REMOTE_FOLDER}/{filename}"
        try:
            result = subprocess.run([
                'rclone', '--config', RCLONE_CONFIG,
                'copyto', local_path, remote_path,
                '--log-level', 'INFO',
                f'--log-file={rclone_log_file}'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300)
            if result.returncode == 0:
                link_result = subprocess.run([
                    'rclone', '--config', RCLONE_CONFIG,
                    'link', remote_path
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
                if link_result.returncode == 0:
                    share_link = link_result.stdout.strip()
                    logger.info(f"Upload sukses: {filename} ke {remote}")
                    return share_link
            else:
                logger.warning(f"Upload gagal ke {remote}: {result.stderr}")
        except Exception as e:
            logger.error(f"Error upload ke {remote}: {e}")
    return None

def update_db(book_id, update_data):
    try:
        payload = {'id': book_id, **update_data}
        resp = requests.post(API_UPLOAD_DATA_URL, json=payload, timeout=15)
        if resp.status_code == 200 and resp.json().get('status') == 'success':
            logger.info(f"DB updated for ID: {book_id}")
            return True
        else:
            logger.warning(f"DB update failed: {resp.text}")
    except Exception as e:
        logger.error(f"Error update DB: {e}")
    return False

def log_success_to_csv(filename, link, db_data):
    is_new = not SUCCESS_CSV.exists()
    with open(SUCCESS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(['filename', 'link'] + list(db_data.keys()))
        writer.writerow([filename, link] + [db_data.get(k, '') for k in db_data.keys()])

def process_file(file):
    orig_path = os.path.join(DOWNLOAD_DIR, file)
    # 1. Rename file (jangan hilangkan simbol, hanya hapus (z-library))
    new_name = clean_filename(file)
    new_path = os.path.join(DOWNLOAD_DIR, new_name)
    if new_path != orig_path:
        os.rename(orig_path, new_path)
        logger.info(f"Renamed: {file} -> {new_name}")
    else:
        logger.info(f"File name OK: {new_name}")
    # 2. Ekstrak 3 kata pertama judul untuk query DB, dan author
    title_for_match = extract_first_3_words(new_name)
    author_for_match = extract_author_from_filename(new_name)
    db_data = find_db_match(title_for_match, author_for_match)
    if not db_data:
        logger.warning(f"Tidak ada judul mirip di DB untuk: {title_for_match}")
        return False
    # 3. Upload ke Google Drive
    link = upload_with_rclone(new_path)
    if not link:
        logger.warning(f"Upload gagal: {new_name}")
        return False
    # 4. Update DB
    update_data = {'files_url_drive': link, 'download_status': 'uploaded'}
    if not update_db(db_data['id'], update_data):
        logger.warning(f"Update DB gagal untuk: {new_name}")
        return False
    # 5. Log ke CSV
    log_success_to_csv(new_name, link, db_data)
    # 6. Hapus file lokal
    os.remove(new_path)
    logger.info(f"File dihapus: {new_name}")
    return True

def main():
    logger.info("=== RCLONE UPLOADER PARALLEL MODE ===")
    files = [f for f in os.listdir(DOWNLOAD_DIR) if os.path.isfile(os.path.join(DOWNLOAD_DIR, f))]
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_file, file): file for file in files}
        for future in as_completed(futures):
            file = futures[future]
            try:
                result = future.result()
                if result:
                    logger.info(f"SUCCESS: {file}")
                else:
                    logger.info(f"SKIP/FAILED: {file}")
            except Exception as e:
                logger.error(f"Exception processing {file}: {e}")

if __name__ == "__main__":
    main()