# 🚀 Beginner's Guide to Running the NIDS Project

Welcome! This guide will walk you through exactly how to set up and run this **Network Intrusion Detection System (NIDS)** on your computer. 

Don't worry if you are new to programming—this guide is written step-by-step for beginners. All the heavy lifting (like training the AI models) has already been done for you!

---

## 🛠️ Step 1: Install Required Software

Before you can run the project, your computer needs two pieces of software installed: **Python** and **Node.js**. 

**1. Check if you already have them:**
- Open your **Terminal** (on Mac) or **Command Prompt** (on Windows).
- Type `python --version` (or `python3 --version`) and press Enter. You should see a version number like `Python 3.10.x` or higher.
- Type `node --version` and press Enter. You should see a version number like `v18.x.x` or higher.

**2. If you don't have them, download them here:**
- **Python:** [Download Python here](https://www.python.org/downloads/) (Make sure to check the box that says "Add Python to PATH" during installation on Windows).
- **Node.js:** [Download Node.js here](https://nodejs.org/en/download/) (The "LTS" version is recommended).

---

## 📂 Step 2: Unzip the Project

1. Find the `.zip` file your friend sent you.
2. **Right-click** it and select **Extract All...** (Windows) or double-click it (Mac) to unzip it.
3. Remember where you extracted this folder (for example, your Desktop or Downloads folder).

---

## 🖥️ Step 3: Start the Backend (The Python AI Server)

The project is split into two parts: the **Backend** (which runs the AI models) and the **Frontend** (the website you interact with). Let's start the backend first.

1. Open a new **Terminal** (Mac) or **Command Prompt / PowerShell** (Windows).
2. You need to navigate to the `backend` folder inside the project. The easiest way to do this is to type `cd ` (with a space at the end) and then **drag and drop the `backend` folder** from your file explorer directly into the terminal window. Then press **Enter**.
   - *(It should look something like `cd C:\Users\YourName\Desktop\nids-project\backend`)*

3. Now, you need to create a "Virtual Environment". This is like an isolated sandbox so the project's Python packages don't mess with your computer's main Python. Run this command:
   - **Mac/Linux:** `python3 -m venv venv`
   - **Windows:** `python -m venv venv`

4. Next, "activate" the virtual environment:
   - **Mac/Linux:** `source venv/bin/activate`
   - **Windows:** `venv\Scripts\activate`
   *(You will know it worked if you see `(venv)` appear at the beginning of your command line).*

5. Install the required Python packages for the AI:
   - Run: `pip install -r requirements.txt`
   *(This might take a minute or two to download everything).*

6. Finally, start the backend server:
   - Run: `uvicorn app.main:app --reload --port 8000`

> ⚠️ **IMPORTANT:** Leave this terminal window open! If you close it, the AI server will turn off. Just minimize it for now.

---

## 🌐 Step 4: Start the Frontend (The Website Interface)

Now we will start the website part of the project.

1. Open a **Brand New Terminal / Command Prompt** window.
2. Navigate to the `frontend` folder. Just like before, type `cd ` and **drag and drop the `frontend` folder** into the terminal and press **Enter**.
3. Install the required website packages by running:
   - `npm install`
   *(This will download a folder called `node_modules` which contains the code to run React).*

4. Start the website:
   - Run: `npm run dev`

> ⚠️ **IMPORTANT:** Leave this second terminal window open as well! 

---

## 🎉 Step 5: Use the Application!

Everything is now up and running!

1. Open your favorite web browser (Chrome, Edge, Safari, etc.).
2. In the address bar at the top, type exactly this and press Enter: **`http://localhost:3000`** (or `http://localhost:5173` if the terminal told you to use that instead).
3. You should see the Network Intrusion Detection System homepage!
4. Click the **"Get Started"** button.
5. Drag and drop a network traffic `.csv` file into the upload box (your friend might have provided one, or you can find them in the `ml-pipeline/data` folder).
6. Click **"Analyze"** and watch the AI process the data and build your results dashboard!

---

### ❓ Troubleshooting (If things go wrong)

- **"pip is not recognized" or "python is not recognized" (Windows):** This means Python wasn't added to your system PATH when you installed it. You'll need to reinstall Python and make sure the "Add Python to PATH" checkbox at the very bottom of the installer is checked.
- **"Port 8000 is already in use":** This means another program on your computer is using port 8000. Restart your computer, or you will need to find the program using that port and close it.
- **Red error messages when uploading a file:** Make sure your backend terminal (the first one you opened) is still running and didn't crash. If it crashed, close the terminal, open a new one, go back to the `backend` folder, run `venv\Scripts\activate`, and run the `uvicorn` command again.
