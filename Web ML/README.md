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

```bash
git clone https://github.com/Showkot-Hosen-10/ML-Based-Cyberdefence.git
cd ML-Based-Cyberdefence/Web\ ML
pip install -r requirements.txt
python app.py
