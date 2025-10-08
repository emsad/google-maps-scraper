#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google Maps Scraper - Render Edition
Entry point per l'esecuzione su Render
"""

import os
import sys
import subprocess
import time

def install_playwright_browsers():
    """Installa i browser necessari per Playwright"""
    print("🔧 Installazione browser Playwright...")
    try:
        result = subprocess.run([
            "python3", "-m", "playwright", "install", "chromium"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Browser Playwright installati con successo")
        else:
            print(f"⚠️  Avviso durante installazione browser: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⚠️  Timeout durante installazione browser (continua comunque)")
    except Exception as e:
        print(f"⚠️  Errore durante installazione browser: {e}")

def check_environment():
    """Controlla le variabili d'ambiente necessarie"""
    print("🔍 Controllo configurazione ambiente...")
    
    # Controlla variabili opzionali
    telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    telegram_chat = os.environ.get('TELEGRAM_CHAT_ID')
    
    if telegram_token and telegram_chat:
        print("✅ Notifiche Telegram configurate")
    else:
        print("ℹ️  Notifiche Telegram non configurate (opzionale)")
    
    print("✅ Controllo ambiente completato\n")

def main():
    """Funzione principale"""
    print("=" * 60)
    print("🚀 GOOGLE MAPS SCRAPER - Render Edition")
    print("=" * 60)
    print()
    
    # Controlla ambiente
    check_environment()
    
    # Installa browser Playwright se necessario
    install_playwright_browsers()
    
    # Importa e esegue lo scraper principale
    try:
        from scraper_maps import main as scraper_main
        print("🎯 Avvio scraper principale...")
        print()
        scraper_main()
    except ImportError as e:
        print(f"❌ Errore importazione scraper: {e}")
        print("   Assicurati che il file scraper_maps.py sia presente")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Scraper interrotto dall'utente")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()