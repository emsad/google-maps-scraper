#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import logging
import random
import threading
import re
import sys
import requests
from queue import Queue
from urllib.parse import urlparse
from pathlib import Path
from datetime import datetime, timedelta

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from tqdm import tqdm
import gspread

# === CONFIG ===
LOG_FILE = "estrazione.log"
MAX_SESSION_TIME = 2 * 60 * 60  # 2 ore in secondi

# PERFORMANCE
NUM_WORKERS = min(max(2, (os.cpu_count() or 2) // 2), 6)
MAX_TENTATIVI = 3
DELAY_MIN = 2
DELAY_MAX = 5
CONTACT_TIMEOUT = 12000  # milliseconds

# SOCIAL DOMAINS
SOCIAL_DOMAINS = {
    "facebook": ["facebook.com"],
    "instagram": ["instagram.com"],
    "linkedin": ["linkedin.com/company", "linkedin.com/in", "linkedin.com"],
    "youtube": ["youtube.com", "youtu.be"],
    "tiktok": ["tiktok.com"],
    "x": ["x.com", "twitter.com"],
    "pinterest": ["pinterest.com"],
}
EMAIL_REGEX = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)

logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()]
)

# GLOBAL
write_lock = threading.Lock()
processed_lock = threading.Lock()
domain_cache_lock = threading.Lock()
sheets_lock = threading.Lock()
domain_cache = {}
output_sheet = None
output_worksheet = None
current_project = None
session_start_time = None
stop_requested = threading.Event()
stats = {"processed": 0, "errors": 0, "emails_found": 0, "social_found": 0}


# ========== TELEGRAM ==========
def send_telegram_notification(message):
    """Invia notifica Telegram (opzionale)"""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        return  # Notifiche non configurate
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        logging.debug(f"Errore invio notifica Telegram: {e}")


# ========== GOOGLE SHEETS ==========
def get_replit_access_token():
    """Ottieni access token dall'integrazione Replit"""
    hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
    repl_identity = os.environ.get('REPL_IDENTITY')
    web_repl_renewal = os.environ.get('WEB_REPL_RENEWAL')
    
    if repl_identity:
        x_replit_token = f'repl {repl_identity}'
    elif web_repl_renewal:
        x_replit_token = f'depl {web_repl_renewal}'
    else:
        raise ValueError("❌ Token Replit non trovato")
    
    url = f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=google-sheet'
    headers = {
        'Accept': 'application/json',
        'X_REPLIT_TOKEN': x_replit_token
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    items = data.get('items', [])
    if not items:
        raise ValueError("❌ Integrazione Google Sheets non configurata")
    
    connection_settings = items[0]
    access_token = (
        connection_settings.get('settings', {}).get('access_token') or
        connection_settings.get('settings', {}).get('oauth', {}).get('credentials', {}).get('access_token')
    )
    
    if not access_token:
        raise ValueError("❌ Access token non trovato nell'integrazione")
    
    return access_token


def init_google_sheets():
    """Inizializza la connessione a Google Sheets usando OAuth"""
    from google.oauth2.credentials import Credentials
    
    access_token = get_replit_access_token()
    
    creds = Credentials(token=access_token)
    client = gspread.authorize(creds)
    
    return client


def get_existing_tabs(client, output_sheet_url):
    """Ottieni lista tab esistenti nel foglio OUTPUT"""
    try:
        sheet = client.open_by_url(output_sheet_url)
        worksheets = sheet.worksheets()
        return [ws.title for ws in worksheets]
    except Exception as e:
        logging.error(f"Errore lettura tab esistenti: {e}")
        return []


def get_or_create_tab(client, output_sheet_url, tab_name, create_new=False):
    """Ottieni tab esistente o creane una nuova"""
    global output_sheet, output_worksheet
    
    try:
        output_sheet = client.open_by_url(output_sheet_url)
        
        if create_new:
            # Crea nuova tab con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_tab_name = f"{tab_name}_{timestamp}"
            output_worksheet = output_sheet.add_worksheet(title=unique_tab_name, rows=1000, cols=13)
            
            # Scrivi intestazioni
            headers = [
                "Nome azienda", "Categoria", "Indirizzo", "Telefono", "Sito web",
                "Email", "Facebook", "Instagram", "LinkedIn", "YouTube", "TikTok", "X", "Pinterest"
            ]
            output_worksheet.append_row(headers)
            print(f"✅ Creata nuova tab: {unique_tab_name}")
            return unique_tab_name
        else:
            # Usa tab esistente
            output_worksheet = output_sheet.worksheet(tab_name)
            print(f"✅ Tab esistente selezionata: {tab_name}")
            return tab_name
            
    except Exception as e:
        logging.error(f"Errore gestione tab OUTPUT: {e}")
        raise


def get_urls_from_sheet(client, input_sheet_url):
    """Legge gli URL dal foglio INPUT"""
    try:
        sheet = client.open_by_url(input_sheet_url)
        worksheet = sheet.get_worksheet(0)
        values = worksheet.col_values(1)
        
        urls = []
        for val in values:
            val = val.strip()
            if val and _looks_like_url(val):
                urls.append(_ensure_url_scheme(val))
        
        return urls
    except Exception as e:
        logging.error(f"Errore lettura foglio INPUT: {e}")
        raise


def write_to_sheet(data_row):
    """Scrivi una riga nel foglio OUTPUT"""
    global output_worksheet
    
    with sheets_lock:
        try:
            output_worksheet.append_row(data_row)
        except Exception as e:
            logging.error(f"Errore scrittura su Google Sheets: {e}")


# ========== UTIL ==========
_URL_RE = re.compile(r"^https?://", re.IGNORECASE)

def _looks_like_url(s: str) -> bool:
    return bool(_URL_RE.match(s.strip()))

def _ensure_url_scheme(s: str) -> str:
    s = s.strip()
    if _looks_like_url(s):
        return s
    if s.lower().startswith("www."):
        return "https://" + s
    return s

def _normalize_home(url: str) -> str:
    try:
        p = urlparse(url)
        scheme = p.scheme or "https"
        netloc = p.netloc or p.path.split("/")[0]
        return f"{scheme}://{netloc}/"
    except:
        return url


# ========== PLAYWRIGHT ==========
def accept_cookies_on_maps(page):
    """Accetta i cookies su Google Maps"""
    try:
        page.wait_for_selector(
            "button:has-text('Accetta'), button:has-text('Accept'), button:has-text('OK')",
            timeout=2500
        )
        page.click("button:has-text('Accetta'), button:has-text('Accept'), button:has-text('OK')")
        time.sleep(0.6)
    except:
        pass


def _text_or_dash(page, selector: str) -> str:
    """Estrai testo o ritorna '-'"""
    try:
        element = page.wait_for_selector(selector, timeout=3000)
        if element:
            text = element.text_content()
            return text.strip() if text else "-"
        return "-"
    except:
        return "-"


def estrai_dati_azienda(page):
    """Estrai i dati aziendali da Google Maps"""
    nome = _text_or_dash(page, "h1.DUwDvf")
    categoria = _text_or_dash(page, "button[jsaction*='pane.wfvdle17.category']")
    indirizzo = _text_or_dash(page, "button[data-item-id='address'] div.Io6YTe")
    
    telefono = "-"
    try:
        tel_elem = page.wait_for_selector("button[aria-label*='Telefono'] div.Io6YTe, button[aria-label*='tel:'] div.Io6YTe", timeout=3000)
        if tel_elem:
            telefono = tel_elem.text_content().strip() or "-"
    except:
        pass
    
    sito = "-"
    try:
        sito_elem = page.wait_for_selector("a[aria-label*='Sito web'], a[aria-label*='sito web']", timeout=3000)
        if sito_elem:
            sito = sito_elem.get_attribute("href") or "-"
    except:
        pass
    
    email = "-"
    social = {k: "-" for k in SOCIAL_DOMAINS.keys()}
    
    if sito != "-":
        email, social = estrai_contatti_da_sito(page.context, sito)
    
    return [
        nome, categoria, indirizzo, telefono, sito,
        email,
        social["facebook"],
        social["instagram"],
        social["linkedin"],
        social["youtube"],
        social["tiktok"],
        social["x"],
        social["pinterest"],
    ]


def estrai_contatti_da_sito(context, sito_url: str):
    """Estrai email e social da un sito web"""
    home = _normalize_home(sito_url)
    domain = urlparse(home).netloc.lower()
    
    with domain_cache_lock:
        if domain in domain_cache:
            return domain_cache[domain]
    
    email_found = "-"
    social_found = {k: "-" for k in SOCIAL_DOMAINS.keys()}
    
    try:
        page = context.new_page()
        page.set_default_timeout(CONTACT_TIMEOUT)
        page.goto(home, wait_until="domcontentloaded")
        
        try:
            page.evaluate("window.scrollTo(0, Math.min(1500, document.body.scrollHeight))")
        except:
            pass
        
        try:
            page.wait_for_selector("button:has-text('Accetta'), button:has-text('OK'), button:has-text('Accept')", timeout=2000)
            page.click("button:has-text('Accetta'), button:has-text('OK'), button:has-text('Accept')")
            time.sleep(0.4)
        except:
            pass
        
        try:
            mailto_links = page.locator("a[href^='mailto:']").all()
            for link in mailto_links:
                href = link.get_attribute("href") or ""
                if href.lower().startswith("mailto:"):
                    mail = href.split("mailto:", 1)[1].split("?")[0].strip()
                    if EMAIL_REGEX.fullmatch(mail):
                        email_found = mail
                        break
        except:
            pass
        
        if email_found == "-":
            try:
                content = page.content()
                m = EMAIL_REGEX.search(content)
                if m:
                    email_found = m.group(0)
            except:
                pass
        
        try:
            all_links = page.locator("a[href]").all()
            for link in all_links:
                href = link.get_attribute("href") or ""
                if not href:
                    continue
                for key, patterns in SOCIAL_DOMAINS.items():
                    if social_found[key] != "-":
                        continue
                    for p in patterns:
                        if p in href:
                            social_found[key] = href
                            break
        except:
            pass
        
        if email_found == "-":
            try:
                contact_links = page.locator("a[href]:has-text('Contatti'), a[href]:has-text('Contact')").all()
                if contact_links:
                    contact_url = contact_links[0].get_attribute("href")
                    if contact_url:
                        page.goto(contact_url, wait_until="domcontentloaded")
                        content2 = page.content()
                        m2 = EMAIL_REGEX.search(content2)
                        if m2:
                            email_found = m2.group(0)
            except:
                pass
        
        page.close()
        
    except Exception as e:
        logging.debug(f"Errore apertura sito {home}: {e}")
    
    with domain_cache_lock:
        domain_cache[domain] = (email_found, social_found)
    
    return email_found, social_found


# ========== PROCESSED LOG ==========
def get_project_log_file(project_name):
    """Ottieni il nome del file di log per un progetto"""
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', project_name)
    return f"processed_urls_{safe_name}.log"


def load_processed_urls(project_name):
    """Carica URL già processati per un progetto"""
    log_file = get_project_log_file(project_name)
    processed = set()
    p = Path(log_file)
    if p.exists():
        with p.open("r", encoding="utf-8") as f:
            processed.update(line.strip() for line in f if line.strip())
    return processed


def save_processed_url(url, project_name):
    """Salva URL processato per un progetto"""
    log_file = get_project_log_file(project_name)
    with processed_lock:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(url + "\n")


def clear_processed_urls(project_name):
    """Cancella il log degli URL processati per un progetto"""
    log_file = get_project_log_file(project_name)
    p = Path(log_file)
    if p.exists():
        p.unlink()
    print(f"✅ Log del progetto '{project_name}' cancellato. Ricomincerò da capo.")


# ========== WORKER ==========
def pseudo_random_sleep():
    time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))


def check_time_limit():
    """Controlla se è stato superato il limite di tempo"""
    global session_start_time
    if session_start_time:
        elapsed = (datetime.now() - session_start_time).total_seconds()
        return elapsed >= MAX_SESSION_TIME
    return False


def worker(queue: Queue, pbar, playwright):
    """Worker thread per estrazione parallela"""
    global stats, current_project
    
    browser = None
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1366, 'height': 900},
            locale='it-IT',
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
        )
        
        while not stop_requested.is_set():
            if check_time_limit():
                stop_requested.set()
                break
            
            try:
                url = queue.get_nowait()
            except:
                break
            
            if not _looks_like_url(url):
                logging.error(f"Input non valido: {url} → skip")
                stats["errors"] += 1
                pbar.update(1)
                queue.task_done()
                continue
            
            try:
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded")
                accept_cookies_on_maps(page)
                
                dati = estrai_dati_azienda(page)
                
                # Statistiche
                if dati[5] != "-":  # Email
                    stats["emails_found"] += 1
                if any(dati[6:13]) and any(d != "-" for d in dati[6:13]):  # Social
                    stats["social_found"] += 1
                
                write_to_sheet(dati)
                save_processed_url(url, current_project)
                stats["processed"] += 1
                
                page.close()
                pbar.update(1)
                
            except PlaywrightTimeout as e:
                logging.error(f"Timeout su {url}: {e}")
                stats["errors"] += 1
                
                try_count = 0
                m = re.search(r"[?&]__ret=(\d+)", url)
                if m:
                    try_count = int(m.group(1))
                if try_count + 1 < MAX_TENTATIVI:
                    sep = "&" if "?" in url else "?"
                    queue.put(f"{url}{sep}__ret={try_count+1}")
                else:
                    logging.error(f"Max tentativi raggiunti per {url}")
                
            except Exception as e:
                logging.error(f"Errore imprevisto su {url}: {e}")
                stats["errors"] += 1
            
            finally:
                queue.task_done()
                pseudo_random_sleep()
        
        context.close()
        browser.close()
        
    except Exception as e:
        logging.error(f"Errore worker: {e}")
        if browser:
            browser.close()


# ========== MAIN ==========
def print_stats():
    """Stampa statistiche finali"""
    print("\n" + "=" * 60)
    print("📊 STATISTICHE SESSIONE")
    print("=" * 60)
    print(f"✅ URL processati: {stats['processed']}")
    print(f"📧 Email trovate: {stats['emails_found']}")
    print(f"🔗 Profili social trovati: {stats['social_found']}")
    print(f"❌ Errori: {stats['errors']}")
    print("=" * 60)


def main():
    global current_project, session_start_time, stats
    
    print("=" * 60)
    print("🔍 GOOGLE MAPS SCRAPER - Versione Replit PRO")
    print("=" * 60)
    
    # Input URLs
    input_sheet_url = input("\n📊 URL foglio Google Sheets INPUT (con gli URL): ").strip()
    output_sheet_url = input("📊 URL foglio Google Sheets OUTPUT (dove salvare): ").strip()
    
    # Inizializza Google Sheets
    print("\n🔌 Connessione a Google Sheets...")
    client = init_google_sheets()
    
    # Mostra tab esistenti
    print("\n📋 Progetti esistenti nel foglio OUTPUT:")
    existing_tabs = get_existing_tabs(client, output_sheet_url)
    
    if existing_tabs:
        for i, tab in enumerate(existing_tabs, 1):
            print(f"   {i}. {tab}")
        print(f"   {len(existing_tabs) + 1}. [NUOVO PROGETTO]")
        
        choice = input(f"\nScegli un progetto (1-{len(existing_tabs) + 1}): ").strip()
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(existing_tabs):
                # Progetto esistente
                current_project = existing_tabs[choice_idx]
                get_or_create_tab(client, output_sheet_url, current_project, create_new=False)
            else:
                # Nuovo progetto
                current_project = input("\n🏷️  Nome del nuovo progetto: ").strip()
                current_project = get_or_create_tab(client, output_sheet_url, current_project, create_new=True)
        except (ValueError, IndexError):
            print("❌ Scelta non valida. Creo nuovo progetto.")
            current_project = input("\n🏷️  Nome del nuovo progetto: ").strip()
            current_project = get_or_create_tab(client, output_sheet_url, current_project, create_new=True)
    else:
        print("   (Nessun progetto esistente)")
        current_project = input("\n🏷️  Nome del nuovo progetto: ").strip()
        current_project = get_or_create_tab(client, output_sheet_url, current_project, create_new=True)
    
    # Opzione ricomincia/prosegui
    print(f"\n❓ Progetto: '{current_project}'")
    print("   1. Ricomincia da capo (cancella log di questo progetto)")
    print("   2. Prosegui (salta URL già processati di questo progetto)")
    scelta = input("Scegli (1 o 2): ").strip()
    
    if scelta == "1":
        clear_processed_urls(current_project)
    
    # Leggi URL
    print("\n📥 Lettura URL dal foglio INPUT...")
    urls = get_urls_from_sheet(client, input_sheet_url)
    print(f"✅ Trovati {len(urls)} URL totali")
    
    # Filtra già processati
    processed = load_processed_urls(current_project)
    urls_to_process = [u for u in urls if u not in processed]
    skipped = len(urls) - len(urls_to_process)
    
    if skipped > 0:
        print(f"⏭️  Saltati {skipped} URL già processati in questo progetto")
    print(f"🎯 Da processare: {len(urls_to_process)} URL\n")
    
    if len(urls_to_process) == 0:
        print("✅ Tutti gli URL sono già stati processati per questo progetto!")
        return
    
    # Notifiche Telegram
    telegram_enabled = False
    if os.environ.get('TELEGRAM_BOT_TOKEN') and os.environ.get('TELEGRAM_CHAT_ID'):
        telegram_enabled = True
        print("📱 Notifiche Telegram ATTIVE")
    else:
        print("📱 Notifiche Telegram non configurate (opzionale)")
    
    # Queue
    q = Queue()
    for u in urls_to_process:
        q.put(u)
    
    # Start extraction
    session_start_time = datetime.now()
    print(f"\n🚀 Avvio estrazione con {NUM_WORKERS} worker paralleli...")
    print(f"⏱️  Auto-stop dopo 2 ore (alle {(session_start_time + timedelta(seconds=MAX_SESSION_TIME)).strftime('%H:%M:%S')})")
    print()
    
    with sync_playwright() as playwright:
        workers = []
        with tqdm(total=len(urls_to_process), desc="Estrazione", ncols=80) as pbar:
            for _ in range(NUM_WORKERS):
                t = threading.Thread(target=worker, args=(q, pbar, playwright), daemon=True)
                workers.append(t)
                t.start()
            
            q.join()
    
    # Risultati
    print_stats()
    
    if check_time_limit():
        msg = f"⏱️ SESSIONE INTERROTTA - Limite 2 ore raggiunto\n\nProgetto: {current_project}\n✅ Processati: {stats['processed']}\n📧 Email: {stats['emails_found']}\n\nRiavvia lo script e scegli 'Prosegui' per continuare!"
        print(f"\n{msg}")
        if telegram_enabled:
            send_telegram_notification(f"🔍 <b>Scraper Auto-Stop</b>\n\n{msg}")
    else:
        msg = f"✅ ESTRAZIONE COMPLETATA!\n\nProgetto: {current_project}\n✅ Processati: {stats['processed']}\n📧 Email: {stats['emails_found']}"
        print(f"\n{msg}")
        if telegram_enabled:
            send_telegram_notification(f"🔍 <b>Scraper Completato</b>\n\n{msg}")
    
    print(f"\n📊 Dati salvati nel foglio OUTPUT, tab: {current_project}")


if __name__ == "__main__":
    main()
