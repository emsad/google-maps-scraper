#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test di configurazione per Google Maps Scraper su Replit
Verifica che tutte le dipendenze e configurazioni siano corrette
"""

import os
import sys
import subprocess

def test_python_version():
    """Testa la versione di Python"""
    print("🐍 Test versione Python...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Richiesto Python 3.11+")
        return False

def test_imports():
    """Testa l'importazione delle dipendenze principali"""
    print("\n📦 Test importazioni...")
    
    required_modules = [
        'requests',
        'gspread', 
        'playwright',
        'tqdm',
        'google.oauth2.credentials'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - ERRORE: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_playwright_browsers():
    """Testa se i browser Playwright sono installati"""
    print("\n🌐 Test browser Playwright...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
                print("✅ Browser Chromium - OK")
                return True
            except Exception as e:
                print(f"❌ Browser Chromium - ERRORE: {e}")
                return False
    except Exception as e:
        print(f"❌ Playwright - ERRORE: {e}")
        return False

def test_replit_environment():
    """Testa se siamo in un ambiente Replit"""
    print("\n🔧 Test ambiente Replit...")
    
    repl_identity = os.environ.get('REPL_IDENTITY')
    web_repl_renewal = os.environ.get('WEB_REPL_RENEWAL')
    hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
    
    if repl_identity or web_repl_renewal:
        print("✅ Ambiente Replit rilevato")
        if hostname:
            print(f"✅ Hostname connector: {hostname}")
        else:
            print("⚠️  Hostname connector non trovato (normale se non configurato)")
        return True
    else:
        print("⚠️  Ambiente Replit non rilevato (potrebbe funzionare comunque)")
        return False

def test_google_sheets_integration():
    """Testa l'integrazione Google Sheets"""
    print("\n📊 Test integrazione Google Sheets...")
    
    try:
        from scraper_maps import get_replit_access_token
        token = get_replit_access_token()
        print("✅ Token Google Sheets ottenuto - OK")
        return True
    except ValueError as e:
        if "Token Replit non trovato" in str(e):
            print("⚠️  Token Replit non trovato (normale se non su Replit)")
        elif "Integrazione Google Sheets non configurata" in str(e):
            print("⚠️  Integrazione Google Sheets non configurata")
        else:
            print(f"❌ Errore Google Sheets: {e}")
        return False
    except Exception as e:
        print(f"❌ Errore Google Sheets: {e}")
        return False

def test_telegram_config():
    """Testa la configurazione Telegram"""
    print("\n📱 Test configurazione Telegram...")
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if token and chat_id:
        print("✅ Configurazione Telegram completa - OK")
        return True
    else:
        print("ℹ️  Telegram non configurato (opzionale)")
        return True

def main():
    """Esegue tutti i test"""
    print("=" * 60)
    print("🧪 TEST CONFIGURAZIONE GOOGLE MAPS SCRAPER")
    print("=" * 60)
    
    tests = [
        test_python_version,
        test_imports,
        test_playwright_browsers,
        test_replit_environment,
        test_google_sheets_integration,
        test_telegram_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print("📊 RISULTATI TEST")
    print("=" * 60)
    print(f"✅ Test superati: {passed}/{total}")
    
    if passed == total:
        print("🎉 TUTTI I TEST SUPERATI! Il progetto è pronto per Replit.")
    elif passed >= total - 2:  # Permette 1-2 test opzionali falliti
        print("✅ CONFIGURAZIONE OK! Il progetto dovrebbe funzionare su Replit.")
    else:
        print("❌ CONFIGURAZIONE PROBLEMATICA! Controlla gli errori sopra.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
