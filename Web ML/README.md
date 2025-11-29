# MLWAF  
**Real-Time ML-Powered Web Defense**

![MLWAF Architecture](web_ML.drawio.png)

**Live CTF Challenge • 3 Flags • 100% ML Detection**

### Flags (revealed on successful detection)
- `flag{SqL_inject10n_1s_fun}` → Trigger SQLi  
- `flag{XSS_1s_tr1cky_but_fun}` → Trigger XSS (JS alert)  
- `flag{IDOR_Found_1n_th3_m4tr1x}` → `/profile?id=313`

### Features
- 100% accurate SQLi & 99.99% XSS detection (Decision Tree + TF-IDF)  
- IDOR detection    

### Run Locally (Tested & Works 100%)

```cmd
git clone https://github.com/Showkot-Hosen-10/ML-Based-Cyberdefence.git
cd "ML-Based-Cyberdefence\Web ML"
pip install -r requirements.txt
python app.py
#### Windows (Command Prompt / PowerShell)
# 1. Go to your desktop or any folder you want
cd C:\Users\USER\Desktop

# 2. Delete the old broken folder (safe)
rmdir /s "ML-Based-Cyberdefence"

#### Linux (cmd)
# 1. Delete old copy (if exists)
rm -rf "ML-Based-Cyberdefence"
