#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test di configurazione per Google Maps Scraper su Render
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

def test_render_environment():
    """Testa se siamo su Render"""
    print("\n🔧 Test ambiente Render...")
    
    render_vars = [
        'RENDER',
        'RENDER_EXTERNAL_URL',
        'RENDER_SERVICE_ID'
    ]
    
    render_detected = any(os.environ.get(var) for var in render_vars)
    
    if render_detected:
        print("✅ Ambiente Render rilevato")
    else:
        print("ℹ️  Ambiente Render non rilevato (potrebbe funzionare comunque)")
    
    return True

def test_google_sheets():
    """Testa la configurazione Google Sheets"""
    print("\n📊 Test Google Sheets...")
    
    try:
        from scraper_maps import get_replit_access_token
        token = get_replit_access_token()
        print("✅ Google Sheets configurato correttamente")
        return True
    except Exception as e:
        print(f"⚠️  Google Sheets: {e}")
        print("   Assicurati di aver configurato le credenziali in Render")
        return False

def test_telegram():
    """Testa la configurazione Telegram"""
    print("\n📱 Test Telegram...")
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if token and chat_id:
        print("✅ Telegram configurato")
        return True
    else:
        print("ℹ️  Telegram non configurato (opzionale)")
        return True

def main():
    """Esegue tutti i test"""
    print("=" * 60)
    print("🧪 TEST CONFIGURAZIONE GOOGLE MAPS SCRAPER - RENDER")
    print("=" * 60)
    
    tests = [
        test_python_version,
        test_imports,
        test_playwright_browsers,
        test_render_environment,
        test_google_sheets,
        test_telegram
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
        print("🎉 TUTTI I TEST SUPERATI! Il progetto è pronto per Render.")
    elif passed >= total - 2:  # Permette 1-2 test opzionali falliti
        print("✅ CONFIGURAZIONE OK! Il progetto dovrebbe funzionare su Render.")
    else:
        print("❌ CONFIGURAZIONE PROBLEMATICA! Controlla gli errori sopra.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()