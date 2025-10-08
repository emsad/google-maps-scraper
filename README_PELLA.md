# 🚀 Deploy su Pella.app

## Guida Completa per Pella.app

### **PASSO 1: Prepara il Progetto**
1. **Crea un repository GitHub** con tutti i file
2. **Assicurati di avere questi file:**
   - ✅ `main.py` - Entry point principale
   - ✅ `scraper_maps.py` - Script scraper
   - ✅ `requirements.txt` - Dipendenze Python
   - ✅ `pella.json` - Configurazione Pella
   - ✅ `test_setup.py` - Test di configurazione

### **PASSO 2: Deploy su Pella**
1. **Vai su [pella.app](https://pella.app)**
2. **Clicca "Sign up" o "Login"**
3. **Clicca "New Project"**
4. **Scegli "Deploy from GitHub"**
5. **Seleziona il tuo repository**
6. **Pella farà il deploy automaticamente!**

### **PASSO 3: Configura Variabili d'Ambiente**
Nel dashboard Pella:
1. **Vai su "Environment Variables"**
2. **Aggiungi (opzionali):**
   - `TELEGRAM_BOT_TOKEN` - Token del bot Telegram
   - `TELEGRAM_CHAT_ID` - Chat ID Telegram
   - `CONTACT_TIMEOUT` - Timeout per le richieste (default: 12000)

### **PASSO 4: Configura Google Sheets**
1. **Vai su "Integrations" o "Connectors"**
2. **Cerca "Google Sheets"**
3. **Clicca "Connect"**
4. **Autorizza l'accesso ai tuoi fogli Google**
5. **L'integrazione sarà automatica!**

### **PASSO 5: Test del Deploy**
1. **Vai su "Logs" nel dashboard**
2. **Clicca "Run" per avviare lo script**
3. **Controlla i log per vedere se funziona**
4. **Se tutto OK, vedrai:**
   ```
   🚀 GOOGLE MAPS SCRAPER - Replit Edition PRO
   ==========================================
   🔍 Controllo configurazione ambiente...
   ✅ Ambiente rilevato
   🔧 Installazione browser Playwright...
   ✅ Browser Playwright installati con successo
   🎯 Avvio scraper principale...
   ```

## ⚙️ Configurazione Avanzata

### **Scheduling (Se Supportato)**
Se Pella supporta cron jobs:
1. **Vai su "Scheduler" o "Cron"**
2. **Configura per girare ogni ora:**
   - **Cron:** `0 * * * *`
   - **Command:** `python3 main.py`

### **Monitoring**
1. **Vai su "Monitoring"**
2. **Imposta alert per errori**
3. **Configura notifiche Telegram**

## 🔧 Risoluzione Problemi

### **Problema:** "Module not found"
**Soluzione:** Verifica che `requirements.txt` sia corretto

### **Problema:** "Playwright browser not found"
**Soluzione:** Pella dovrebbe installare automaticamente i browser

### **Problema:** "Google Sheets error"
**Soluzione:** Verifica l'integrazione Google Sheets

### **Problema:** "Script si ferma"
**Soluzione:** Controlla i log per errori specifici

## 📊 Vantaggi Pella.app

- ✅ **Deploy automatico** da GitHub
- ✅ **Supporta Python 3.11**
- ✅ **Supporta Playwright**
- ✅ **Integrazione Google Sheets**
- ✅ **Logs dettagliati**
- ✅ **Facile da usare**
- ✅ **Scalabile**

## 🎯 Configurazione Finale

Il tuo script su Pella:
1. **Si avvia automaticamente** quando fai push su GitHub
2. **Installa le dipendenze** automaticamente
3. **Configura Playwright** automaticamente
4. **Si connette a Google Sheets** tramite integrazione
5. **Gira quando richiesto** o su schedule

## 📱 Notifiche Telegram

Per configurare le notifiche:
1. **Crea un bot con [@BotFather](https://t.me/BotFather)**
2. **Ottieni il token**
3. **Ottieni il tuo Chat ID**
4. **Aggiungi le variabili d'ambiente in Pella**

## 🚀 Prossimi Passi

1. **Carica tutto su GitHub**
2. **Vai su Pella.app**
3. **Connetti il repository**
4. **Configura le integrazioni**
5. **Testa il deploy!**

**Pella.app è una scelta eccellente per il tuo scraper!** 🎉
