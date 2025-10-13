# 🔍 Text Steganography Detection using LSTM

This repository presents a deep learning–based approach to detect **text steganography**, i.e., hidden or covert messages embedded within ordinary text.  
Using **Long Short-Term Memory (LSTM)** neural networks, this project classifies whether a given text sample contains **hidden information (stego)** or is **clean (normal)** based on linguistic and semantic patterns.

---

## 🧠 Overview
Text steganography poses a serious challenge to cybersecurity and digital forensics since malicious actors can embed hidden data in plain text communication.  
This project applies **Natural Language Processing (NLP)** and **Deep Learning** to automatically detect such concealed patterns.

### ✳️ Key Features
- Preprocessing of text data (tokenization, padding, and embedding generation).  
- LSTM-based binary classifier for *stego* vs *non-stego* detection.  
- Trained and evaluated using benchmark text steganography datasets.  
- Visualized model performance with confusion matrix, accuracy, precision, recall, and F1-score.  
- Modular and easy to extend with other deep models (BiLSTM, GRU, Transformer, etc.).
### ✳️ Project link
-[https://www.kaggle.com/code/showkothosen/text-stego-detection-using-lstm]
---

## 🧩 Tech Stack
- **Python**, **TensorFlow / Keras**, **NumPy**, **Pandas**
- **Matplotlib**, **Seaborn** (for evaluation visualization)
- **Jupyter Notebook** (experiments & model training)
- Optional: **NLTK / spaCy** for advanced text preprocessing

---

## 📈 Results
| Metric | Score |
|:-------|:------|
| Accuracy | ~94% |
| Precision | 0.93 |
| Recall | 0.94 |
| F1-Score | 0.94 |

> The LSTM model successfully learns stylistic and lexical deviations introduced during steganographic text embedding.

---

## 📂 Repository Structure
📁 text-stego-detection-lstm/
│
├── data/ # Preprocessed dataset (or link to original)
├── models/ # Saved trained models
├── notebooks/ # Jupyter notebooks for training & evaluation
├── utils/ # Helper functions (tokenization, metrics, etc.)
└── README.md # Project overview


---

## 👨‍💻 Author
**Showkot Hosen**  
BSc in Electronics & Telecommunication Engineering (CUET)  
Research Focus: *Cybersecurity, Deep Learning, and Digital Forensics*

- 📧 Email: [shrahat56@gmail.com](mailto:shrahat56@gmail.com)  
- 🔗 LinkedIn: [linkedin.com/in/showkot-hosen10](https://linkedin.com/in/showkot-hosen10)  
- 🧩 Kaggle: [kaggle.com/showkothosen](https://kaggle.com/showkothosen)  
- 🔒 TryHackMe: [tryhackme.com/p/Showkot313](https://tryhackme.com/p/Showkot313)

---

> ⚠️ **Ethical Disclaimer:**  
> This work is intended solely for educational and defensive cybersecurity research.  
> Misuse for unauthorized surveillance or data embedding is strictly prohibited.

---

## 🧠 Future Work
- Incorporate **Transformer-based models (BERT/DistilBERT)** for improved detection accuracy.  
- Extend to **multilingual steganography detection**.  
- Build an explainable AI module (LIME/SHAP) to visualize learned text features.

---

### 📜 Citation
If you use this project in your research, please cite this GitHub repository:
