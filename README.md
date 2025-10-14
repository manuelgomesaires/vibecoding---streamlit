# Welcome to Your First Coding Project in Cursor!

This is a simple project to help you get started with Python using the Cursor IDE.  
You'll write your very first scripts here, while Cursor (with AI) acts as your tutor and guide.  
Let's explore this workspace together:

---

## 📋 Table of Contents

1. [Getting to Know Cursor](#getting-to-know-cursor)
   - [Exploring the Project Files](#exploring-the-project-files)
   - [How to Run Code](#how-to-run-code)
   - [Setup](#setup)
     - [🪟 Windows](#windows)
     - [🍎🐧 Mac/Linux](#maclinux)
     - [Working with Secrets](#working-with-secrets-api-keys-passwords)
2. [Your First Challenge: Understanding the Code](#your-first-challenge-understanding-the-code)



---

## Getting to Know Cursor

Your screen has a few key areas:

* **Explorer (Left Side)**: Like a file cabinet — it shows all project files (like `main.py`). Click a file to open it.
* **Editor (Center)**: Your workbench. This is where you’ll write and edit code.
* **Terminal (Bottom)**: Your command center. Run commands here to execute your scripts and see results.
* **Cursor Chat (Right Side)**: Your AI assistant. You can ask questions about your code, concepts, or next steps.  
  Remember: the AI will explain logic simply, not overwhelm you with code details.


### Exploring the Project Files

* **`main.py`**: This is the main file where you will write your Python code. For now, this is the only file you need to focus on.
* **Other Files**: You might see files like `.cursorrules`, `requirements.txt`, or `.vscode`.  
  Don’t worry about these — they exist to make the environment easier and to guide the AI assistant.


--- 

### How to Run Code

Now let’s run the code you just explored:

1. Make sure `main.py` is open in the **Editor**.
2. Click into the **Terminal** at the bottom.
3. Run this command:

```bash
python main.py
```

4. You should see this message appear in the terminal:

```
Hello, world!
```

🎉 Congrats, you just ran your first Python program in Cursor!


---

### Setup

**Good news!** A Python environment is already prepared for you. 🎉  

When you open a terminal, you might see `(.venv)` at the start of the prompt, like this:
```
(.venv) vibecoding-02-03-68307615:$
```

This means your environment is ready! If you see this, skip to [Your First Challenge](#your-first-challenge-understanding-the-code).

<br>

#### Windows

<a id="-setup-for-windows"></a>
<details>
  <summary><strong>🪟 Setup and troubleshooting for Windows</strong></summary>

**If you don't see a `.venv` folder**, follow these steps:

##### Step 1: Allow Scripts to Run

Open PowerShell and run this command once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then close and reopen VSCode/Cursor.

##### Step 2: Run Setup

Choose one method:

**Option A: Inside VSCode/Cursor** (Recommended)
1. Open a new terminal in VSCode/Cursor
2. Type: `setup-venv`
3. Press Enter and wait for the success message

**Option B: Double-Click Setup**
- Find `setup.bat` in the Explorer and double-click it

##### Step 3: Verify It Worked

Close your terminal and open a new one. You should see `(.venv)` at the start of your prompt. Success! 🎉

---

#### Troubleshooting

**Problem: "Script is disabled" error**
- You skipped Step 1! Run the ExecutionPolicy command above, then restart VSCode.

**Problem: "Python is not recognized"**

Python is not installed. Let's install it:

**Method 1: Using winget (Recommended)**
1. Open PowerShell and run:
   ```powershell
   winget install Python.Python.3.12
   ```
2. Restart your computer and try setup again

**Method 2: Manual Download**
1. Go to https://www.python.org/downloads/
2. Download and run the installer
3. **Important:** Check the box "Add Python to PATH" during installation
4. Restart your computer and try setup again

**Problem: Virtual environment not activating**
- Type `activate` in the terminal to activate it manually

**Still stuck?** Ask your instructor for help! Show them:
- The exact error message
- A screenshot if possible

</details>

<br>

<a id="-setup-for-maclinux"></a>

#### Mac/Linux

<details>
  <summary><strong>🍎🐧 Setup and troubleshooting for Mac/Linux</strong></summary>

**If you don't see a `.venv` folder**, follow these steps:

##### Step 1: Run Setup

Choose one method:

**Option A: Inside VSCode/Cursor** (Recommended)
1. Open a new terminal in VSCode/Cursor
2. Type: `setup-venv`
3. Press Enter and wait for the success message

**Option B: Run Script in Terminal**
- Open Terminal in this folder and run: `bash setup.sh`

##### Step 2: Verify It Worked

Close your terminal and open a new one. You should see `(.venv)` at the start of your prompt. Success! 🎉

---

##### Troubleshooting

**Problem: "Python3 is not installed"**

**Mac:**
1. First, install Homebrew (a package manager) if you don't have it:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Then install Python:
   ```bash
   brew install python3
   ```
3. Or download manually from: https://www.python.org/downloads/

**Linux:**
```bash
sudo apt install python3 python3-venv
```

**Problem: Virtual environment not activating**
- Type `activate` in the terminal to activate it manually

**Problem: "Permission denied" when running setup.sh**
- Run: `chmod +x setup.sh` then try again

**Still stuck?** Ask your instructor for help! Show them:
- The exact error message
- A screenshot if possible

</details>

<br>

---



### Working with Secrets (API Keys, Passwords)

**Important:** Never put passwords or API keys directly in your code!

#### Using a `.env` File

When you need to store secrets (like API keys), create a file named `.env` in your project folder:

1. Right-click in the Explorer → New File → Name it `.env`
2. Add your secrets, one per line:
   ```
   API_KEY=your_secret_key_here
   PASSWORD=your_password_here
   ```
3. Ask Cursor AI: **"Use my API key from the .env file"**

Cursor will help you load and use these secrets properly in your code.

> **💡 Tip:** Your `.env` file is already protected by `.gitignore`, so it won't be uploaded to GitHub. Your secrets stay private!

#### ⚠️ Important Rules

- **Never** write secrets directly in your code
- **Always** use a `.env` file for passwords, API keys, and tokens
- **Ask Cursor** to help you use environment variables when you need them


---

## Your First Challenge: Understanding the Code

Before running anything, let’s ask Cursor what the code means.

In the **Cursor Chat**, on the right side, type:

```text
Can you explain what the code in `main.py` does?
```

You’ll get a simple, logical explanation of what the program does, not just a code breakdown.

