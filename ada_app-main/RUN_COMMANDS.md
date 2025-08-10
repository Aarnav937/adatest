# 🚀 ADA Application - Run Commands

## **Quick Start Guide for Image Generation Feature**

### **Step 1: Start the Backend Server**

Open **PowerShell** or **Command Prompt** and run:

```bash
# Navigate to server directory
cd server

# Start the Flask server with GPU support
python app.py
```

**Expected Output:**
```
Starting Flask-SocketIO server...
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.8:5000
Press CTRL+C to quit
```

### **Step 2: Start the Frontend (New Terminal)**

Open a **new terminal window** and run:

```bash
# Navigate to client directory
cd client/ada-online

# Install dependencies (first time only)
npm install

# Start the React development server
npm run dev
```

**Expected Output:**
```
  VITE v6.2.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.1.8:5173/
```

### **Step 3: Access the Application**

1. **Open your browser**
2. **Go to:** `http://localhost:5173/`
3. **You should see the ADA interface**

---

## **🎨 Testing Image Generation**

### **Test Commands to Try:**

Once the app is running, ask Ada these questions:

1. **Basic Image Generation:**
   - *"Generate an image of a futuristic city at sunset"*
   - *"Create a picture of a cat wearing sunglasses"*
   - *"Draw a cyberpunk robot in neon colors"*

2. **Detailed Prompts:**
   - *"Generate an image of a beautiful mountain landscape with snow peaks and a clear blue sky"*
   - *"Create a picture of a steampunk airship flying over Victorian London"*
   - *"Draw a magical forest with glowing mushrooms and fairy lights"*

3. **Negative Prompts (Ada will handle automatically):**
   - *"Generate a portrait of a knight, but avoid making it blurry or low quality"*

### **What Happens:**

1. **Ada processes your request** via Google Gemini
2. **Calls the image generation function** with your prompt
3. **Generates image on your GPU** using Stable Diffusion
4. **Shows a draggable widget** with the generated image
5. **Saves the image** to `server/generated_images/` folder
6. **Provides download button** to save the image

---

## **🔧 Troubleshooting**

### **If Server Won't Start:**

```bash
# Check if Python dependencies are installed
cd server
pip install -r requirements.txt

# Check CUDA support
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

### **If Frontend Won't Start:**

```bash
# Clear npm cache
cd client/ada-online
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### **If Image Generation is Slow:**

- **GPU Mode:** Should be fast (5-15 seconds)
- **CPU Mode:** Will be slower (30-60 seconds)
- **First generation:** May take longer as model loads

---

## **⚡ Performance Tips**

### **For Faster Generation:**

1. **Use shorter prompts** (1-2 sentences)
2. **Be specific** about what you want
3. **Avoid complex scenes** with many objects
4. **Close other GPU-intensive applications**

### **Example Fast Prompts:**

- *"A red sports car on a highway"*
- *"A cat sitting on a windowsill"*
- *"A sunset over the ocean"*

---

## **🛑 Stopping the Application**

### **Stop Backend Server:**
- Press `Ctrl+C` in the server terminal

### **Stop Frontend:**
- Press `Ctrl+C` in the client terminal

---

## **📁 File Structure**

```
ada_app-main/
├── server/
│   ├── .env                    # API keys (you created this)
│   ├── app.py                  # Flask server
│   ├── ADA_Online.py          # AI logic with image generation
│   ├── requirements.txt        # Python dependencies
│   └── generated_images/       # Generated images saved here
└── client/ada-online/
    ├── src/
    │   ├── App.jsx            # Main React app
    │   └── components/
    │       ├── ImageWidget.jsx # Image display widget
    │       └── ImageWidget.css # Widget styling
    └── package.json           # Node.js dependencies
```

---

## **🎯 Quick Commands Summary**

**Start Everything:**
```bash
# Terminal 1 - Backend
cd server && python app.py

# Terminal 2 - Frontend  
cd client/ada-online && npm run dev
```

**Test Image Generation:**
- Open browser to `http://localhost:5173/`
- Ask Ada: *"Generate an image of a beautiful sunset"*

**Stop Everything:**
- Press `Ctrl+C` in both terminals

---

## **🚨 Important Notes**

1. **Keep both terminals open** while using the app
2. **First image generation** may take 30-60 seconds (model loading)
3. **Subsequent generations** will be much faster
4. **Images are saved locally** in `server/generated_images/`
5. **GPU acceleration** is enabled for faster generation

---

**🎉 You're all set! Enjoy generating images with Ada!** 