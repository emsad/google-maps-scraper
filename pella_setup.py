#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup script ottimizzato per Pella.app
Gestisce l'ambiente e le configurazioni specifiche di Pella
"""

import os
import sys
import subprocess
import time

def check_pella_environment():
    """Controlla se siamo su Pella.app"""
    print("🔍 Controllo ambiente Pella.app...")
    
    # Controlla variabili specifiche di Pella
    pella_vars = [
        'PELLA_APP_ID',
        'PELLA_ENVIRONMENT',
        'PELLA_DEPLOYMENT_ID'
    ]
    
    pella_detected = any(os.environ.get(var) for var in pella_vars)
    
    if pella_detected:
        print("✅ Ambiente Pella.app rilevato")
    else:
        print("ℹ️  Ambiente Pella.app non rilevato (potrebbe funzionare comunque)")
    
    return pella_detected

def install_dependencies():
    """Installa le dipendenze necessarie"""
    print("📦 Installazione dipendenze...")
    
    try:
        # Installa requirements
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True)
        print("✅ Dipendenze Python installate")
        
        # Installa browser Playwright
        subprocess.run([
            sys.executable, "-m", "playwright", "install", "chromium"
        ], check=True, capture_output=True)
        print("✅ Browser Playwright installati")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore installazione: {e}")
        return False

def check_google_sheets():
    """Controlla la configurazione Google Sheets"""
    print("📊 Controllo Google Sheets...")
    
    try:
        from scraper_maps import get_replit_access_token
        token = get_replit_access_token()
        print("✅ Google Sheets configurato correttamente")
        return True
    except Exception as e:
        print(f"⚠️  Google Sheets: {e}")
        print("   Assicurati di aver configurato l'integrazione in Pella")
        return False

def check_telegram():
    """Controlla la configurazione Telegram"""
    print("📱 Controllo Telegram...")
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if token and chat_id:
        print("✅ Telegram configurato")
        return True
    else:
        print("ℹ️  Telegram non configurato (opzionale)")
        return True

def main():
    """Funzione principale per Pella.app"""
    print("=" * 60)
    print("🚀 GOOGLE MAPS SCRAPER - Pella.app Edition")
    print("=" * 60)
    
    # Controlli ambiente
    check_pella_environment()
    
    # Installa dipendenze
    if not install_dependencies():
        print("❌ Errore durante l'installazione delle dipendenze")
        sys.exit(1)
    
    # Controlli configurazione
    check_google_sheets()
    check_telegram()
    
    print("\n🎯 Avvio scraper principale...")
    print("=" * 60)
    
    # Importa e esegue lo scraper
    try:
        from scraper_maps import main as scraper_main
        scraper_main()
    except ImportError as e:
        print(f"❌ Errore importazione: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Scraper interrotto")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
