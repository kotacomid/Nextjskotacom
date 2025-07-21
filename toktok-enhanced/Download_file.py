# --- KONFIGURASI HARDCORE STANDALONE ---
import os
import sys
from pathlib import Path

# Get current script directory for portable configuration
SCRIPT_DIR = Path(__file__).parent.absolute()

# --- KONFIGURASI PORTABLE ---
BASE_URL = "https://z-library.sk/"
BOOKS_API_URL = "https://www.api.staisenorituban.ac.id/claim_books"
ACCOUNTS_CSV = str(SCRIPT_DIR / "akun.csv")  # Langsung di root folder
CHROMEDRIVER_PATH = str(SCRIPT_DIR / "chromedriver-win64" / "chromedriver.exe")
DOWNLOAD_DIR = str(SCRIPT_DIR / "download_files")
INSTANCE_ID = "instance_1"

# --- CHROME PORTABLE CONFIGURATION ---
#CHROME_PORTABLE_PATH = str(SCRIPT_DIR / "chrome-win64" / "chrome.exe")
#CHROME_PORTABLE_USER_DATA = str(SCRIPT_DIR / "chrome-win64" / "user_data")

# --- PENGATURAN WAKTU (dalam detik) ---
WAIT_AFTER_LOAD_MIN = 0.5  # Lebih cepat
WAIT_AFTER_LOAD_MAX = 1
WAIT_AFTER_CLICK_MIN = 0.5  # Lebih cepat
WAIT_AFTER_CLICK_MAX = 1

import time
import random
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import requests
import logging

# Hapus logging Chrome/Selenium
import logging as pylogging
for logger_name in [
    'selenium.webdriver.remote.remote_connection',
    'selenium.webdriver.common.service',
    'selenium.webdriver.remote.file_detector',
    'selenium.webdriver.remote.utils',
    'selenium.webdriver.common.utils',
    'selenium.webdriver.common.action_chains',
    'selenium.webdriver.common.alert',
    'selenium.webdriver.common.proxy',
    'selenium.webdriver.common.by',
    'selenium.webdriver.common.desired_capabilities',
    'selenium.webdriver.common.keys',
    'selenium.webdriver.common.touch_actions',
    'selenium.webdriver.common.actions',
    'selenium.webdriver.common.actions.action_builder',
    'selenium.webdriver.common.actions.pointer_actions',
    'selenium.webdriver.common.actions.interaction',
    'selenium.webdriver.common.actions.key_actions',
    'selenium.webdriver.common.actions.wheel_actions',
    'selenium.webdriver.common.actions.input_device',
    'selenium.webdriver.common.actions.pointer_input',
    'selenium.webdriver.common.actions.key_input',
    'selenium.webdriver.common.actions.wheel_input',
    'selenium.webdriver.common.actions.pause',
    'selenium.webdriver.common.actions.pointer_event',
    'selenium.webdriver.common.actions.key_event',
    'selenium.webdriver.common.actions.wheel_event',
    'selenium.webdriver.common.actions.pointer_properties',
    'selenium.webdriver.common.actions.pointer_type',
    'selenium.webdriver.common.actions.pointer_origin',
    'selenium.webdriver.common.actions.pointer_move',
    'selenium.webdriver.common.actions.pointer_down',
    'selenium.webdriver.common.actions.pointer_up',
    'selenium.webdriver.common.actions.pointer_cancel',
    'selenium.webdriver.common.actions.pointer_cancel_event',
    'selenium.webdriver.common.actions.pointer_cancel_properties',
    'selenium.webdriver.common.actions.pointer_cancel_type',
    'selenium.webdriver.common.actions.pointer_cancel_origin',
    'selenium.webdriver.common.actions.pointer_cancel_move',
    'selenium.webdriver.common.actions.pointer_cancel_down',
    'selenium.webdriver.common.actions.pointer_cancel_up',
    'selenium.webdriver.common.actions.pointer_cancel_cancel',
    'selenium.webdriver.common.actions.pointer_cancel_event',
    'selenium.webdriver.common.actions.pointer_cancel_properties',
    'selenium.webdriver.common.actions.pointer_cancel_type',
    'selenium.webdriver.common.actions.pointer_cancel_origin',
    'selenium.webdriver.common.actions.pointer_cancel_move',
    'selenium.webdriver.common.actions.pointer_cancel_down',
    'selenium.webdriver.common.actions.pointer_cancel_up',
    'selenium.webdriver.common.actions.pointer_cancel_cancel',
    'selenium.webdriver.common.actions.pointer_cancel_event',
    'selenium.webdriver.common.actions.pointer_cancel_properties',
    'selenium.webdriver.common.actions.pointer_cancel_type',
    'selenium.webdriver.common.actions.pointer_cancel_origin',
    'selenium.webdriver.common.actions.pointer_cancel_move',
    'selenium.webdriver.common.actions.pointer_cancel_down',
    'selenium.webdriver.common.actions.pointer_cancel_up',
    'selenium.webdriver.common.actions.pointer_cancel_cancel',
    'selenium.webdriver.common.service',
    'selenium.webdriver.chrome.service',
    'selenium.webdriver.chrome.remote_connection',
    'selenium.webdriver.chrome.webdriver',
    'selenium.webdriver.chrome.options',
    'selenium.webdriver.chrome',
    'selenium.webdriver',
    'urllib3.connectionpool',
    'urllib3',
    'httpcore',
    'httpx',
    'http.client',
    'asyncio',
    'trio',
    'trio._core',
    'trio._socket',
    'trio._ssl',
    'trio._sync',
    'trio._subprocess',
    'trio._threads',
    'trio._util',
    'trio.lowlevel',
    'trio.socket',
    'trio.ssl',
    'trio.subprocess',
    'trio.testing',
    'trio.to_thread',
    'trio.util',
    'trio.web',
    'trio.web._core',
    'trio.web._http',
    'trio.web._http2',
    'trio.web._http2_client',
    'trio.web._http2_server',
    'trio.web._http_client',
    'trio.web._http_server',
    'trio.web._ssl',
    'trio.web._util',
    'trio.web.lowlevel',
    'trio.web.socket',
    'trio.web.ssl',
    'trio.web.subprocess',
    'trio.web.testing',
    'trio.web.to_thread',
    'trio.web.util',
    'trio.web.web',
    'trio.web.web._core',
    'trio.web.web._http',
    'trio.web.web._http2',
    'trio.web.web._http2_client',
    'trio.web.web._http2_server',
    'trio.web.web._http_client',
    'trio.web.web._http_server',
    'trio.web.web._ssl',
    'trio.web.web._util',
    'trio.web.web.lowlevel',
    'trio.web.web.socket',
    'trio.web.web.ssl',
    'trio.web.web.subprocess',
    'trio.web.web.testing',
    'trio.web.web.to_thread',
    'trio.web.web.util',
]:
    pylogging.getLogger(logger_name).setLevel(pylogging.CRITICAL)

# Setup logging
LOG_DIR = SCRIPT_DIR / 'logs' if 'SCRIPT_DIR' in globals() else Path('logs')
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'ddownload_ex.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)

API_BASE = "https://www.api.staisenorituban.ac.id"  # Ganti jika perlu

# Fungsi baru: ambil akun dari API

def load_accounts_from_api():
    accounts = []
    page = 1
    per_page = 100
    while True:
        resp = requests.get(f"{API_BASE}/accounts", params={"status": "active", "page": page, "per_page": per_page})
        if resp.status_code != 200:
            logging.error("Gagal mengambil data akun dari API")
            break
        data = resp.json()
        accounts.extend(data.get("accounts", []))
        if len(data.get("accounts", [])) < per_page:
            break
        page += 1
    logging.info(f"Loaded {len(accounts)} accounts from API")
    return accounts

def check_limit_reached(driver):
    """Check if daily limit is reached"""
    try:
        # Check for specific HTML structure
        try:
            # Check for the main limit error section
            limit_section = driver.find_element(By.CSS_SELECTOR, "section.download-limits-error")
            if limit_section:
                logging.warning("⚠️ Daily limit section detected")
                return True
        except NoSuchElementException:
            pass
            
        # Check for limit header text
        try:
            limit_header = driver.find_element(By.CSS_SELECTOR, "h1.download-limits-error__header")
            if limit_header and "Daily limit reached" in limit_header.text:
                logging.warning("⚠️ Daily limit header detected")
                return True
        except NoSuchElementException:
            pass
            
        # Check for limit message
        try:
            limit_message = driver.find_element(By.CSS_SELECTOR, "article.download-limits-error__message")
            if limit_message and "daily limit" in limit_message.text.lower():
                logging.warning("⚠️ Daily limit message detected")
                return True
        except NoSuchElementException:
            pass
        
        # Check for specific text patterns in limit message
        try:
            limit_message = driver.find_element(By.CSS_SELECTOR, "article.download-limits-error__message")
            if limit_message:
                message_text = limit_message.text.lower()
                specific_indicators = [
                    "daily limit is already reached",
                    "download counter being reset",
                    "10 downloads",
                    "17 hours"
                ]
                for indicator in specific_indicators:
                    if indicator in message_text:
                        logging.warning(f"⚠️ Specific limit indicator found: {indicator}")
                        return True
        except NoSuchElementException:
            pass
        
        # Check for various limit messages in page text
        limit_indicators = [
            "daily limit reached",
            "limit tercapai", 
            "batas download",
            "too many downloads",
            "daily limit is already reached",
            "download counter being reset"
        ]
        
        page_text = driver.page_source.lower()
        for indicator in limit_indicators:
            if indicator in page_text:
                logging.warning(f"⚠️ Limit indicator found: {indicator}")
                return True
                
        # Also check for specific elements with XPath
        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'Daily limit reached')]")
            logging.warning("⚠️ Daily limit reached text found")
            return True
        except NoSuchElementException:
            pass
            
        return False
    except Exception as e:
        logging.error(f"Error checking limit: {e}")
        return False

def force_logout(driver):
    """Force logout by clearing cookies and session"""
    logging.info("🔄 Force logout - clearing cookies and session...")
    try:
        # Clear all cookies
        driver.delete_all_cookies()
        
        # Clear local storage
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        
        # Refresh page
        driver.refresh()
        time.sleep(2)
        
        # Verify logout success
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "section.not-logged a[data-action='login']")))
        logging.info("✓ Logout berhasil dikonfirmasi")
        return True
        
    except Exception as e:
        logging.error(f"✗ Error during logout: {e}")
        return False

def claim_books(batch_size):
    import requests
    try:
        resp = requests.post(BOOKS_API_URL, json={"batch_size": batch_size, "instance_id": INSTANCE_ID}, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if isinstance(result, dict) and 'books' in result:
            return result['books']
        elif isinstance(result, list):
            return result
        else:
            return []
    except Exception as e:
        logging.error(f"Error claim books: {e}")
        return []

def update_account_limit_status(email):
    try:
        today_str = datetime.now().date().strftime('%m/%d/%Y')
        resp = requests.put(f"{API_BASE}/accounts/update_limit", json={"email": email, "last_limit_date": today_str})
        if resp.status_code == 200:
            logging.info(f"✓ Updated limit status for account: {email}")
        else:
            logging.warning(f"✗ Failed to update limit status for account: {email} | Response: {resp.text}")
    except Exception as e:
        logging.error(f"Error updating account limit status for {email}: {e}")

def setup_driver(download_path, headless=True, use_profile=False):
    import os  # Move import to top of function
    chrome_options = Options()
    
    # CHROME PORTABLE CONFIGURATION
    #if os.path.exists(CHROME_PORTABLE_PATH):
     #   chrome_options.binary_location = CHROME_PORTABLE_PATH
     #   print(f"✓ Using portable Chrome: {CHROME_PORTABLE_PATH}")
        
        # Set portable user data directory
        #if not os.path.exists(CHROME_PORTABLE_USER_DATA):
      #      os.makedirs(CHROME_PORTABLE_USER_DATA, exist_ok=True)
      #  chrome_options.add_argument(f'--user-data-dir={CHROME_PORTABLE_USER_DATA}')
      #  print(f"✓ Using portable user data: {CHROME_PORTABLE_USER_DATA}")
    #else:
    #    print(f"⚠️ Portable Chrome not found: {CHROME_PORTABLE_PATH}")
    #    print("🔄 Falling back to system Chrome...")
    
    # HEADLESS MODE TOGGLE
    if headless:
        chrome_options.add_argument('--headless=new')
        logging.info("🚀 Running in HEADLESS mode")
    else:
        logging.info("🔍 Running in DEBUG mode (visible browser)")
    
    # CHROME PROFILE FOR DEBUG MODE (only if not using portable)
    if use_profile and not headless and not os.path.exists(CHROME_PORTABLE_PATH):
        username = os.getenv('USERNAME') or os.getenv('USER')
        user_data_dir = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data"
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
        chrome_options.add_argument('--profile-directory=fastd')
        logging.info(f"📁 Using Chrome profile: fastd")
        logging.info(f"📁 Profile path: {user_data_dir}")
    # LOAD PERFORMANCE EXTENSION (for all modes)
    extension_path = str(SCRIPT_DIR / "zlib_performance_extension")
    if os.path.exists(extension_path):
        chrome_options.add_argument(f'--load-extension={extension_path}')
        logging.info(f"✓ Loading performance extension: {extension_path}")
        
        # Debug extension files
        extension_files = os.listdir(extension_path)
        logging.info(f"📁 Extension files: {extension_files}")
    else:
        logging.warning(f"⚠️ Extension not found: {extension_path}")
    
    # COOKIES RESET - Setiap kali buka browser
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument('--disable-cache')
    chrome_options.add_argument('--disable-offline-load-stale-cache')
    chrome_options.add_argument('--disk-cache-size=0')
    chrome_options.add_argument('--media-cache-size=0')
    logging.info("🧹 Cache akan di-reset setiap session")
    
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Block images to improve performance
    chrome_options.add_argument('--disable-images')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    
    # Additional performance optimizations
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')
    chrome_options.add_argument('--disable-renderer-backgrounding')
    chrome_options.add_argument('--disable-field-trial-config')
    chrome_options.add_argument('--disable-ipc-flooding-protection')
    
    # Page load strategy untuk load cepat
    chrome_options.page_load_strategy = 'eager'  # Load sampai DOM ready, tidak tunggu semua resource
    
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': os.path.abspath(download_path),
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True,
        'profile.default_content_setting_values': {
            'images': 2,  # Block images
            'plugins': 2,  # Block plugins
            'popups': 2,   # Block popups
            'geolocation': 2,  # Block geolocation
            'notifications': 2,  # Block notifications
            'media_stream': 2,  # Block media stream
        },
        # Optimasi untuk download cepat
        'download.open_pdf_in_system_reader': False,
        'download.directory_upgrade': True,
        'profile.default_content_settings.popups': 0,
        'profile.managed_default_content_settings.images': 2,
        # Reset cookies dan cache
        'profile.default_content_settings.cookies': 1,  # Allow cookies but reset on close
        'profile.managed_default_content_settings.cookies': 1
    })
    from selenium.webdriver.chrome.service import Service
    
    # Cek apakah chromedriver ada
    chromedriver_path = CHROMEDRIVER_PATH
    if not os.path.exists(chromedriver_path):
        logging.warning(f"ChromeDriver tidak ditemukan di: {chromedriver_path}")
        # Coba cari chromedriver di lokasi lain
        possible_paths = [
            "chromedriver.exe",  # Root folder
            "chromedriver-win64/chromedriver.exe",  # Subfolder
            "../chromedriver-win64/chromedriver.exe",  # Parent folder
            str(SCRIPT_DIR / "chromedriver-win64" / "chromedriver.exe"),  # SCRIPT_DIR
            str(SCRIPT_DIR / "chrome-win64" / "chromedriver.exe"),  # Chrome folder
            str(SCRIPT_DIR / "chromedriver.exe"),  # Root folder
            str(Path.cwd() / "chromedriver.exe"),  # Current working directory
            str(Path.cwd() / "chromedriver-win64" / "chromedriver.exe"),  # CWD subfolder
            str(Path.cwd().parent / "chromedriver-win64" / "chromedriver.exe"),  # Parent CWD
            str(Path.cwd().parent / "chromedriver.exe")  # Parent CWD root
        ]
        
        logging.info("🔍 Searching for ChromeDriver in possible locations...")
        for path in possible_paths:
            logging.info(f"  Checking: {path}")
            if os.path.exists(path):
                chromedriver_path = path
                logging.info(f"✅ Found ChromeDriver: {chromedriver_path}")
                break
        else:
            logging.error("❌ ChromeDriver tidak ditemukan di semua lokasi yang mungkin.")
            logging.warning("📁 Please ensure chromedriver.exe is in one of these locations:")
            logging.warning("   - Root folder: chromedriver.exe")
            logging.warning("   - Subfolder: chromedriver-win64/chromedriver.exe")
            logging.warning("   - Chrome folder: chrome-win64/chromedriver.exe")
            return None
    
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(1)  # Reduced implicit wait
    driver.set_page_load_timeout(3)  # Reduced page load timeout
    

    
    return driver

def ensure_five_tabs(driver, tab_handles):
    """Ensure exactly 5 tabs are available"""
    try:
        # Close extra tabs
        while len(driver.window_handles) > 5:
            for handle in driver.window_handles:
                if handle not in tab_handles:
                    try:
                        driver.switch_to.window(handle)
                        driver.close()
                        break
                    except:
                        continue
        
        # Open new tabs if less than 5
        while len(driver.window_handles) < 5:
            try:
                driver.switch_to.window(driver.window_handles[0])
                driver.execute_script("window.open('about:blank', '_blank');")
            except:
                break
        
        # Update tab_handles to current 5
        current_tabs = driver.window_handles[:5]
        return current_tabs
        
    except Exception as e:
        logging.error(f"Error managing tabs: {e}")
        # Return available tabs if error
        return driver.window_handles[:min(len(driver.window_handles), 5)]

def check_if_logged_in(driver):
    """Check if already logged in"""
    try:
        driver.get(BASE_URL)
        time.sleep(2)
        
        # Check for logged in elements
        logged_elements = driver.find_elements(By.CSS_SELECTOR, "section.navigation-element.logged")
        if logged_elements:
            logging.warning("⚠️ Sudah login, melakukan logout dulu...")
            return True
        else:
            logging.info("✅ Belum login, siap untuk login")
            return False
    except Exception as e:
        logging.error(f"Error checking login status: {e}")
        return False

def login(driver, email, password):
    try:
        # CHECK LOGIN STATUS DULU
        if check_if_logged_in(driver):
            # Jika sudah login, logout dulu
            force_logout(driver)
        
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 5)
        try:
            login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "section.not-logged a[data-action='login']")))
            login_link.click()
        except Exception:
            pass
        wait.until(EC.presence_of_element_located((By.ID, "auth_modal_login")))
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        email_field.clear()
        password_field.clear()
        email_field.send_keys(email)
        password_field.send_keys(password)
        submit_button = driver.find_element(By.XPATH, "//div[@id='auth_modal_login']//button[@type='submit']")
        submit_button.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.navigation-element.logged")))
        logging.info(f"Login berhasil: {email}")
        return True
    except Exception as e:
        logging.error(f"Login gagal untuk {email}: {e}")
        return False

def download_batch(driver, books, progress_start=0, current_email=None, df=None, use_multiple_tabs=True):
    main_window = driver.current_window_handle
    
    if use_multiple_tabs:
        # Buka 5 tab untuk balance performance dan resource
        while len(driver.window_handles) < 5:  # Turun dari 10 ke 5 tab
            driver.execute_script("window.open('about:blank', '_blank');")
        tab_handles = driver.window_handles[:5]
        logging.info(f"Starting batch download with {len(books)} books using {len(tab_handles)} tabs...")
    else:
        # Pakai 1 tab saja
        tab_handles = [driver.current_window_handle]
        logging.info(f"Starting batch download with {len(books)} books using 1 tab...")
    
    book_idx = 0
    downloaded = 0
    total = len(books)
    batch_count = 0  # Counter untuk logout setiap 2 batch
    
    while book_idx < total:
        tab_handles = ensure_five_tabs(driver, tab_handles)
        
        # Check for limit after every 2 batches (5x2 = 10 books)
        if batch_count > 0 and batch_count % 2 == 0:
            logging.info(f"🔄 Batch {batch_count} selesai - checking for limit...")
            
            # Check current tab for limit
            if check_limit_reached(driver):
                logging.warning(f"⚠️ Limit tercapai untuk akun: {current_email}")
                if current_email:
                    update_account_limit_status(current_email)
                return downloaded  # Stop processing this account
            
            # Force logout every 2 batches
            force_logout(driver)
            
            # Re-login
            if current_email:
                password = None
                # Find password for current email
                accounts_list = load_accounts_from_api() # Ganti load_accounts()
                for account in accounts_list:
                    if account['email'] == current_email:
                        password = account['password']
                        break
                
                if password:
                    logging.info(f"🔄 Re-login untuk {current_email}...")
                    if not login(driver, current_email, password):
                        logging.error(f"✗ Re-login gagal untuk {current_email}")
                        return downloaded
        
        # LOAD 5 URL SEKALIGUS di semua tab
        if use_multiple_tabs:
            logging.info(f"🔄 Loading {len(tab_handles)} URLs sekaligus...")
            for i, tab in enumerate(tab_handles):
                if book_idx + i >= total:
                    break
                driver.switch_to.window(tab)
                current_book = books[book_idx + i]
                try:
                    driver.get(current_book['book_url'])
                except:
                    pass
            
            # Tunggu semua tab selesai load
            time.sleep(2)
        
        # PROCESS setiap tab untuk download
        for i, tab in enumerate(tab_handles):
            if book_idx >= total:
                break
            driver.switch_to.window(tab)
            current_book = books[book_idx]
            
            try:
                # Jika single tab, load URL di sini
                if not use_multiple_tabs:
                    driver.get(current_book['book_url'])
                
                # Check for limit in this tab (sebelum klik download)
                if check_limit_reached(driver):
                    logging.warning(f"⚠️ Limit tercapai untuk akun: {current_email}")
                    if current_email:
                        update_account_limit_status(current_email)
                    return downloaded
                
                try:
                    # Cari download button dengan timeout pendek
                    download_button = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn.btn-default.addDownloadedBook'))
                    )
                    
                    # Simpan handles sebelum klik
                    original_handles = driver.window_handles
                    main_tab = driver.current_window_handle
                    
                    # Klik download button langsung tanpa delay
                    driver.execute_script("arguments[0].click();", download_button)
                    
                    # Langsung lanjut tanpa delay
                    
                    # Handle tab baru jika terbuka
                    if len(driver.window_handles) > len(original_handles):
                        try:
                            # Switch ke tab baru
                            new_tab = [h for h in driver.window_handles if h not in original_handles][0]
                            driver.switch_to.window(new_tab)
                            
                            # Check untuk limit di tab baru
                            if check_limit_reached(driver):
                                logging.warning(f"⚠️ Limit tercapai di tab baru untuk akun: {current_email}")
                                if current_email:
                                    update_account_limit_status(current_email)
                                driver.close()
                                driver.switch_to.window(main_tab)
                                return downloaded
                            
                            # Close tab baru
                            driver.close()
                            
                        except Exception as e:
                            logging.error(f"Error handling new tab: {e}")
                        finally:
                            # Kembali ke tab utama
                            if main_tab in driver.window_handles:
                                driver.switch_to.window(main_tab)
                            else:
                                # Jika main tab hilang, switch ke tab pertama
                                driver.switch_to.window(driver.window_handles[0])
                    
                    # Check limit di tab utama juga
                    if check_limit_reached(driver):
                        logging.warning(f"⚠️ Limit tercapai di tab utama untuk akun: {current_email}")
                        if current_email:
                            update_account_limit_status(current_email)
                        return downloaded
                        
                except TimeoutException:
                    pass  # Skip jika tidak ada button
                except Exception:
                    pass  # Skip error
                    
            except Exception:
                pass  # Skip error loading
                
            downloaded += 1
            if (progress_start + downloaded) % 20 == 0:
                logging.info(f"Progress: {progress_start + downloaded} files processed...")
            book_idx += 1
            
            # Langsung lanjut ke tab berikutnya
        
        batch_count += 1
    
    driver.switch_to.window(main_window)
    logging.info(f"Batch completed. Processed {downloaded} books.")
    return downloaded

def main():
    logging.info("=== DOWNLOAD FILE HARDCORE STANDALONE - MAXIMUM THROUGHPUT ===")
    logging.info(f"Project Root: {SCRIPT_DIR}")
    logging.info(f"Accounts CSV: {ACCOUNTS_CSV}")
    logging.info(f"ChromeDriver: {CHROMEDRIVER_PATH}")
    logging.info(f"Download Dir: {DOWNLOAD_DIR}")
    logging.info("=" * 50)
    
    # HEADLESS MODE TOGGLE
    import sys
    headless_mode = True  # Default headless
    use_profile = False   # Default no profile
    use_multiple_tabs = True  # Default 5 tabs
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['debug', '--debug', '-d']:
            headless_mode = False
            logging.info("🔍 DEBUG MODE: Browser akan terlihat")
        elif arg in ['profile', '--profile', '-p']:
            headless_mode = False
            use_profile = True
            logging.info("🔍 DEBUG MODE: Browser akan terlihat dengan profile 'fastd'")
        elif arg in ['single', '--single', '-s']:
            use_multiple_tabs = False
            logging.info("🎯 SINGLE TAB MODE: 1 tab untuk stabilitas")
        else:
            logging.warning(f"❓ Unknown argument: {sys.argv[1]}")
            logging.warning("Usage: python ddownload_ex.py [debug|profile|single]")
            return
    else:
        logging.info("🚀 HEADLESS MODE: Browser tersembunyi")
        logging.info("📊 MULTI-TAB MODE: 5 tabs untuk kecepatan")
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    accounts = load_accounts_from_api() # Ganti load_accounts()
    if not accounts:
        logging.warning("Tidak ada akun tersedia.")
        return
    
    total_downloaded = 0
    max_retries = 2  # Kurangi retry untuk kecepatan
    
    # SETUP DRIVER SEKALI SAJA - REUSE UNTUK SEMUA AKUN
    logging.info("🚀 Setting up Chrome driver...")
    driver = setup_driver(DOWNLOAD_DIR, headless=headless_mode, use_profile=use_profile)
    if driver is None:
        logging.error("❌ Gagal setup Chrome driver")
        return
    
    try:
        while True:
            books = claim_books(10)  # Ambil lebih banyak buku sekaligus
            if not books:
                logging.warning("Tidak ada buku untuk didownload.")
                break
                
            book_idx = 0
            for account in accounts:
                email = account['email']
                password = account['password']
                
                # Retry mechanism for each account
                for retry in range(max_retries):
                    try:
                        logging.info(f"\n--- Account {email} (attempt {retry + 1}/{max_retries}) ---")
                        
                        # REUSE DRIVER - LOGOUT/LOGIN SAJA
                        if not login(driver, email, password):
                            logging.warning(f"Login gagal untuk {email}")
                            continue
                            
                        downloaded = download_batch(driver, books[book_idx:], progress_start=total_downloaded, current_email=email, df=None, use_multiple_tabs=use_multiple_tabs) # Hapus df=df
                        total_downloaded += downloaded
                        logging.info(f"✓ {email}: {downloaded} files. Total: {total_downloaded}")
                        book_idx += downloaded
                        
                        if book_idx >= len(books):
                            break
                        break  # Success, exit retry loop
                        
                    except Exception as e:
                        logging.error(f"✗ Error {email} (attempt {retry + 1}): {e}")
                        if retry == max_retries - 1:
                            logging.error(f"Failed all retries for account {email}")
                        else:
                            logging.info(f"Retrying in 2 seconds...")
                            time.sleep(2)
                
                if book_idx >= len(books):
                    break
    finally:
        # QUIT DRIVER HANYA DI AKHIR
        logging.info("🔄 Closing Chrome driver...")
        driver.quit()
                
    logging.info(f"\n=== DOWNLOAD SELESAI! Total file diproses: {total_downloaded} ===")

if __name__ == "__main__":
    main() 