#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google Maps Scraper - Render Edition (Senza Input Manuale)
Versione ottimizzata per Render con variabili d'ambiente
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
    
    # Controlla variabili obbligatorie
    input_sheet = os.environ.get('INPUT_SHEET_URL')
    output_sheet = os.environ.get('OUTPUT_SHEET_URL')
    project_name = os.environ.get('PROJECT_NAME', 'default')
    
    if not input_sheet or not output_sheet:
        print("❌ ERRORE: Variabili d'ambiente mancanti!")
        print("   Configura in Render:")
        print("   - INPUT_SHEET_URL: URL del foglio INPUT")
        print("   - OUTPUT_SHEET_URL: URL del foglio OUTPUT")
        print("   - PROJECT_NAME: Nome del progetto (opzionale)")
        return False
    
    print("✅ Variabili d'ambiente configurate")
    print(f"   INPUT: {input_sheet[:50]}...")
    print(f"   OUTPUT: {output_sheet[:50]}...")
    print(f"   PROGETTO: {project_name}")
    
    # Controlla variabili opzionali
    telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    telegram_chat = os.environ.get('TELEGRAM_CHAT_ID')
    
    if telegram_token and telegram_chat:
        print("✅ Notifiche Telegram configurate")
    else:
        print("ℹ️  Notifiche Telegram non configurate (opzionale)")
    
    print("✅ Controllo ambiente completato\n")
    return True

def run_scraper_with_env():
    """Esegue lo scraper con variabili d'ambiente"""
    print("🎯 Avvio scraper con configurazione automatica...")
    
    # Simula l'input per lo scraper
    input_sheet = os.environ.get('INPUT_SHEET_URL')
    output_sheet = os.environ.get('OUTPUT_SHEET_URL')
    project_name = os.environ.get('PROJECT_NAME', 'render_project')
    
    # Crea un file temporaneo con l'input
    with open('input_config.txt', 'w') as f:
        f.write(f"{input_sheet}\n")
        f.write(f"{output_sheet}\n")
        f.write(f"{project_name}\n")
        f.write("2\n")  # Prosegui (non ricominciare)
    
    # Modifica temporaneamente sys.stdin per leggere dal file
    original_stdin = sys.stdin
    with open('input_config.txt', 'r') as f:
        sys.stdin = f
        try:
            from scraper_maps import main as scraper_main
            scraper_main()
        finally:
            sys.stdin = original_stdin
    
    # Pulisci il file temporaneo
    try:
        os.remove('input_config.txt')
    except:
        pass

def main():
    """Funzione principale"""
    print("=" * 60)
    print("🚀 GOOGLE MAPS SCRAPER - Render Edition")
    print("=" * 60)
    print()
    
    # Controlla ambiente
    if not check_environment():
        print("❌ Configurazione incompleta. Controlla le variabili d'ambiente.")
        sys.exit(1)
    
    # Installa browser Playwright se necessario
    install_playwright_browsers()
    
    # Esegue lo scraper con configurazione automatica
    try:
        run_scraper_with_env()
    except ImportError as e:
        print(f"❌ Errore importazione scraper: {e}")
        print("   Assicurati che il file scraper_maps.py sia presente")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Scraper interrotto")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
