# 🔐 Password Manager

A simple yet secure desktop **Password Manager App** built using Python and Tkinter.  
It allows users to store, retrieve, and manage login credentials securely with AES encryption.

---

## 🚀 Features

- 🔒 Master password login
- 🔐 AES (Fernet)-based encryption for secure password storage
- 🔑 Password generator with randomized characters
- 🧾 Searchable, editable, and deletable credential records
- 💾 Local encrypted JSON storage (offline)
- 🖥️ GUI built with Tkinter
- 📋 Copy password to clipboard
- 👁️ Toggle password visibility

---

## 🛠️ Tech Stack

- Python 3.12
- Tkinter (GUI)
- Cryptography (`Fernet`, AES encryption)
- JSON (for local data storage)
- Pillow (for image processing)

---

## 🧪 Screenshots

> <img width="302" height="212" alt="Screenshot 2025-07-18 220247" src="https://github.com/user-attachments/assets/b6310463-24fa-4c16-8ca9-2f57e33ba3d1" />
> <img width="1374" height="753" alt="Screenshot 2025-07-18 220345" src="https://github.com/user-attachments/assets/e6dbee1a-7fc6-4234-a69a-8204f57ad677" />
> <img width="1374" height="753" alt="Screenshot 2025-07-18 220618" src="https://github.com/user-attachments/assets/70061933-bc0c-4fd4-8b39-98d0bf566065" />

---

## 🔐 Security

This app uses:
- A **master password** for access control
- **AES-based encryption** via Fernet
- A unique **salt** stored in `secret_salt.bin`
- Key derivation using `PBKDF2HMAC` (SHA256, 390k iterations)

> ⚠️ This project is for educational/demo purposes. Do not use it for storing real credentials without enhancing security (e.g., key vault, 2FA, hardware-based storage).

---

## 📁 Project Structure

```bash
Password-Manager/
├── main.py                # Main GUI program
├── auth.py                # Handles login, key derivation, salt generation
├── crypto_utils.py        # AES encryption and decryption functions
├── data_handler.py        # Data read/write (with encryption)
├── generate_password.py   # Password generator logic
├── save_account.py        # Save function logic
├── secret_salt.bin        # Salt for key derivation
└── img/
    └── lock.png           # Logo/icon image
