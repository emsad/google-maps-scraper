# 🔍 Google Maps Scraper - Render Edition

Sistema professionale per estrarre dati aziendali da Google Maps, ottimizzato per l'hosting su Render con gestione multi-progetto e salvataggio automatico su Google Sheets.

## ✨ Funzionalità Principali

- 🏢 **Estrazione dati aziendali**: Nome, categoria, indirizzo, telefono, sito web
- 📧 **Estrazione contatti**: Email e social media (Facebook, Instagram, LinkedIn, YouTube, TikTok, X, Pinterest)
- 📊 **Gestione multi-progetto**: Ogni progetto ha la sua tab e il suo log separato
- ⏱️ **Auto-stop intelligente**: Si ferma dopo 2 ore per evitare timeout
- 📱 **Notifiche Telegram**: Opzionali per monitorare l'avanzamento
- 🔄 **Gestione URL processati**: Evita duplicati e permette di riprendere da dove si era fermati
- ⚡ **Elaborazione parallela**: 2-6 worker simultanei per massime performance

## 🚀 Deploy su Render

### **PASSO 1: Prepara il Progetto**
1. **Crea un repository GitHub** con tutti i file
2. **Assicurati di avere questi file:**
   - ✅ `main.py` - Entry point principale
   - ✅ `scraper_maps.py` - Script scraper
   - ✅ `requirements.txt` - Dipendenze Python
   - ✅ `Dockerfile` - Container Docker
   - ✅ `pyproject.toml` - Configurazione progetto

### **PASSO 2: Deploy su Render**
1. **Vai su [render.com](https://render.com)**
2. **Clicca "Get Started for Free"**
3. **Registrati con GitHub** (più facile)
4. **Clicca "New +" → "Web Service"**
5. **Connetti GitHub** e seleziona il repository
6. **Render rileverà automaticamente** la configurazione

### **PASSO 3: Configurazione Automatica**
Render dovrebbe rilevare automaticamente:
- **Build Command:** `pip install -r requirements.txt && playwright install chromium`
- **Start Command:** `python3 main.py`
- **Python Version:** 3.11

### **PASSO 4: Deploy**
1. **Clicca "Deploy Web Service"**
2. **Aspetta** 5-10 minuti
3. **FATTO!**

## ⚙️ Configurazione Google Sheets

### **Metodo 1: Service Account (Raccomandato)**
1. **Vai su [console.cloud.google.com](https://console.cloud.google.com)**
2. **Crea un Service Account**
3. **Scarica il file JSON**
4. **In Render:** Settings → Environment Variables
5. **Aggiungi:** `GOOGLE_CREDENTIALS` = contenuto del file JSON

### **Metodo 2: OAuth (Più Semplice)**
1. **In Render:** Settings → Environment Variables
2. **Aggiungi le tue credenziali Google**

## 📱 Configurazione Telegram (Opzionale)

1. **In Render:** Settings → Environment Variables
2. **Aggiungi:**
   - `TELEGRAM_BOT_TOKEN` = il tuo token
   - `TELEGRAM_CHAT_ID` = il tuo chat ID

## 📊 Dati Estratti

Per ogni azienda vengono estratti:
- **Informazioni base**: Nome, categoria, indirizzo, telefono
- **Sito web**: URL del sito aziendale
- **Email**: Indirizzo email di contatto
- **Social media**: Facebook, Instagram, LinkedIn, YouTube, TikTok, X (Twitter), Pinterest

## 🔧 Risoluzione Problemi

### **Errori Comuni**
1. **"Module not found"**: Verifica che `requirements.txt` sia corretto
2. **"Playwright browser not found"**: Render installa automaticamente i browser
3. **"Google Sheets error"**: Verifica le credenziali e i permessi

### **Log e Debug**
- **Log generali**: Disponibili nel dashboard Render
- **Console**: Output in tempo reale con statistiche

## 📱 Notifiche Telegram

Ricevi notifiche quando:
- ⏱️ Lo script si ferma per limite 2 ore
- ✅ L'estrazione è completata
- ❌ Si verificano errori critici

## 🚨 Limitazioni Render

- **Piano gratuito**: 750 ore/mese
- **Piano a pagamento**: Consigliato per uso intensivo
- **Risorse**: I browser headless consumano CPU e memoria

## 📁 Struttura File

```
├── main.py                 # Entry point per Render
├── scraper_maps.py         # Script principale
├── requirements.txt        # Dipendenze Python
├── Dockerfile             # Container Docker
├── pyproject.toml         # Configurazione progetto
└── README.md              # Questa guida
```

## 🔄 Aggiornamenti

Per aggiornare il progetto:
1. Modifica i file nel repository GitHub
2. Render farà il deploy automatico
3. Il servizio si aggiornerà automaticamente

## 📞 Supporto

Per problemi o domande:
1. Controlla i log nel dashboard Render
2. Verifica la configurazione Google Sheets
3. Assicurati di essere su un piano Render adeguato

---

**Buon scraping! 🚀**