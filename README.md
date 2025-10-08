# 🔍 Google Maps Scraper - Replit Edition PRO

Sistema professionale per estrarre dati aziendali da Google Maps, ottimizzato per l'hosting su Replit con gestione multi-progetto e salvataggio automatico su Google Sheets.

## ✨ Funzionalità Principali

- 🏢 **Estrazione dati aziendali**: Nome, categoria, indirizzo, telefono, sito web
- 📧 **Estrazione contatti**: Email e social media (Facebook, Instagram, LinkedIn, YouTube, TikTok, X, Pinterest)
- 📊 **Gestione multi-progetto**: Ogni progetto ha la sua tab e il suo log separato
- ⏱️ **Auto-stop intelligente**: Si ferma dopo 2 ore per evitare timeout Replit
- 📱 **Notifiche Telegram**: Opzionali per monitorare l'avanzamento
- 🔄 **Gestione URL processati**: Evita duplicati e permette di riprendere da dove si era fermati
- ⚡ **Elaborazione parallela**: 2-6 worker simultanei per massime performance

## 🚀 Quick Start su Replit

### 1. Importa il Progetto
1. Vai su [Replit](https://replit.com)
2. Clicca su "Create Repl"
3. Scegli "Import from GitHub" o "Upload files"
4. Carica tutti i file del progetto

### 2. Configura Google Sheets (Automatico)
L'integrazione Google Sheets funziona automaticamente su Replit tramite OAuth. Non serve configurazione aggiuntiva!

### 3. Configura Notifiche Telegram (Opzionale)
1. Crea un bot con [@BotFather](https://t.me/BotFather) su Telegram
2. Ottieni il **Bot Token**
3. Ottieni il tuo **Chat ID** da [@userinfobot](https://t.me/userinfobot)
4. Vai su **Secrets** (icona lucchetto) in Replit
5. Aggiungi:
   - `TELEGRAM_BOT_TOKEN`: il token del bot
   - `TELEGRAM_CHAT_ID`: il tuo chat ID

### 4. Esegui lo Scraper
1. Clicca su **Run** o esegui `python main.py`
2. Segui le istruzioni a schermo

## 📋 Struttura Google Sheets

### Foglio INPUT
Contiene gli URL di Google Maps da processare:
```
Colonna A: URL di Google Maps
https://www.google.com/maps/place/...
https://www.google.com/maps/place/...
```

### Foglio OUTPUT
Dove vengono salvati i risultati con tab separate per progetto:
- **Intestazioni**: Nome azienda, Categoria, Indirizzo, Telefono, Sito web, Email, Facebook, Instagram, LinkedIn, YouTube, TikTok, X, Pinterest
- **Tab per progetto**: Ogni progetto ha la sua tab dedicata

## 🎯 Come Usare

### Esecuzione Base
1. **Prepara il foglio INPUT** con gli URL di Google Maps
2. **Esegui lo script**: `python main.py`
3. **Inserisci gli URL** dei fogli INPUT e OUTPUT
4. **Scegli un progetto** esistente o creane uno nuovo
5. **Decidi se ricominciare** o proseguire da dove eri rimasto
6. **L'estrazione parte automaticamente**

### Gestione Progetti
- **Ogni progetto/cliente** ha la sua **tab dedicata**
- **Log separati** per ogni progetto (`processed_urls_NOMEPROGETTO.log`)
- **Nessun rischio di confusione**: ogni progetto è isolato
- **Riprendi quando vuoi**: scegli "Prosegui" per continuare

## ⚙️ Configurazione Avanzata

### Variabili d'ambiente (opzionali)
Crea un file `.env` basato su `env.example`:

```bash
# Notifiche Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Configurazioni avanzate
CONTACT_TIMEOUT=12000
NUM_WORKERS=4
DELAY_MIN=2
DELAY_MAX=5
MAX_SESSION_TIME=7200
```

### Performance
- **Worker paralleli**: 2-6 (automatico in base alla CPU)
- **Delay tra richieste**: 2-5 secondi random
- **Retry automatici**: fino a 3 tentativi
- **Timeout contatti**: 12 secondi

## 📊 Dati Estratti

Per ogni azienda vengono estratti:
- **Informazioni base**: Nome, categoria, indirizzo, telefono
- **Sito web**: URL del sito aziendale
- **Email**: Indirizzo email di contatto
- **Social media**: Facebook, Instagram, LinkedIn, YouTube, TikTok, X (Twitter), Pinterest

## 🔧 Risoluzione Problemi

### Errori Comuni
1. **"Token Replit non trovato"**: Assicurati di essere su Replit
2. **"Integrazione Google Sheets non configurata"**: Configura l'integrazione in Replit
3. **"Timeout su URL"**: Normale per siti lenti, lo script riprova automaticamente

### Log e Debug
- **Log generale**: `estrazione.log`
- **URL processati**: `processed_urls_NOMEPROGETTO.log`
- **Console**: Output in tempo reale con statistiche

## 📱 Notifiche Telegram

Ricevi notifiche quando:
- ⏱️ Lo script si ferma per limite 2 ore
- ✅ L'estrazione è completata
- ❌ Si verificano errori critici

## 🚨 Limitazioni Replit

- **Piano gratuito**: Limiti di tempo di esecuzione
- **Piano a pagamento**: Consigliato per estrazioni molto lunghe
- **Risorse**: I browser headless consumano CPU e memoria

## 📁 Struttura File

```
├── main.py                 # Entry point per Replit
├── scraper_maps.py         # Script principale
├── pyproject.toml          # Dipendenze Python
├── .replit                 # Configurazione Replit
├── replit.nix             # Dipendenze sistema
├── env.example            # Esempio variabili ambiente
├── replit.md              # Documentazione dettagliata
└── README.md              # Questa guida
```

## 🔄 Aggiornamenti

Per aggiornare il progetto:
1. Scarica la versione più recente
2. Sostituisci i file nel tuo Repl
3. Riavvia l'esecuzione

## 📞 Supporto

Per problemi o domande:
1. Controlla i log per errori specifici
2. Verifica la configurazione Google Sheets
3. Assicurati di essere su un piano Replit adeguato

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file LICENSE per i dettagli.

---

**Buon scraping! 🚀**
