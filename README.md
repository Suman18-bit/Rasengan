<div align="center">

<!-- HEADER BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D47A1,50:1565C0,100:00BCD4&height=200&section=header&text=🌀%20Rasengan%20AR&fontSize=60&fontColor=ffffff&fontAlignY=38&desc=Interactive%20Augmented%20Reality%20Jutsu%20Effect&descAlignY=60&descSize=18&animation=fadeIn" width="100%"/>

---

<!-- BADGES -->
<p>
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/>
  <img src="https://img.shields.io/badge/MediaPipe-Hand%20Tracking-00BCD4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-00e676?style=for-the-badge"/>
</p>

<p>
  <img src="https://img.shields.io/github/stars/Suman18-bit/Rasengan?style=social"/>
  &nbsp;
  <img src="https://img.shields.io/github/forks/Suman18-bit/Rasengan?style=social"/>
  &nbsp;
  <img src="https://img.shields.io/github/watchers/Suman18-bit/Rasengan?style=social"/>
</p>

<br/>

> **🍃 "The Rasengan is the highest form of shape transformation."** — *Kakashi Hatake, Naruto*

<br/>

</div>

---

## 🌀 What is this?

**Rasengan AR** is a real-time **Augmented Reality** experience built in Python that overlays a glowing, animated **Rasengan** effect directly onto your palm — just like Naruto! Using your webcam, the app detects your hand in real-time and renders a rotating spiral energy ball that follows your every move.

No jutsu hand signs required. 🤙

---

## ✨ Demo

<div align="center">

<!-- Replace with an actual GIF of your project -->
```
📸  Place a demo GIF here (demo.gif) to show the Rasengan in action!
    e.g. ![Rasengan Demo](demo.gif)
```

</div>

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🖐️ **Real-time Hand Tracking** | Detects your palm using MediaPipe's 21-landmark model |
| 🌀 **Animated Rasengan Effect** | Rotating spiral energy ball rendered over your hand |
| 💙 **Glowing Aura** | Layered blue-white glow using OpenCV blending |
| ⚡ **Chakra Particles** | Dynamic floating particle effects around the sphere |
| 📷 **Webcam Integration** | Works live with any standard webcam |
| 🎛️ **Interactive** | Effect appears only when your hand is detected |

---

## 🛠️ Tech Stack

<div align="center">

| Technology | Role |
|---|---|
| 🐍 **Python 3.8+** | Core language |
| 👁️ **OpenCV** | Frame capture, rendering & image compositing |
| 🤖 **MediaPipe** | Real-time hand landmark detection (21 points) |
| 🔢 **NumPy** | Matrix operations for effect generation |

</div>

---

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- **Python 3.8 or higher** — [Download here](https://www.python.org/downloads/)
- A working **webcam**
- **pip** (Python package manager)

---

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/Suman18-bit/Rasengan.git
cd Rasengan
```

**2. (Recommended) Create a virtual environment**

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install opencv-python mediapipe numpy
```

---

## ▶️ Usage

```bash
python rasengan.py
```

Once running:

- 🖐️ **Hold your open palm** up to the webcam
- 🌀 **Watch the Rasengan form** in the center of your hand
- ❌ Press **`Q`** to quit

---

## 🧠 How It Works

```
┌─────────────┐     ┌───────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Webcam     │────▶│  MediaPipe    │────▶│  Hand Center     │────▶│  Rasengan    │
│  Frame      │     │  Hand Tracker │     │  Coordinates     │     │  Rendering   │
└─────────────┘     └───────────────┘     └──────────────────┘     └──────────────┘
```

1. **Capture** — Each frame is grabbed from the webcam using OpenCV
2. **Detect** — MediaPipe's Hand model identifies 21 key landmarks on the palm
3. **Locate** — The palm center coordinate is calculated from the landmarks
4. **Render** — A multi-layered Rasengan (glow + spiral + particles) is drawn at that position
5. **Composite** — The effect is blended with the live webcam feed and displayed

---

## 📁 Project Structure

```
Rasengan/
│
├── 📄 rasengan.py      # Main application — hand tracking + AR effect rendering
└── 📄 README.md        # You are here!
```

---

## 🎨 Effect Breakdown

The Rasengan effect is composed of multiple visual layers:

```
        ✨ Outer Glow       ← Wide, soft, blue-tinted circle (low opacity)
          🔵 Core Sphere    ← Bright white-blue filled circle
            🌀 Spiral       ← Rotating arc drawn using trigonometry
              ⚡ Particles  ← Randomly scattered glowing dots
```

All layers are animated frame-by-frame to create the signature swirling look.

---

## 🤝 Contributing

Contributions are always welcome! Here's how you can help:

```bash
# 1. Fork the repo
# 2. Create your feature branch
git checkout -b feature/new-jutsu

# 3. Commit your changes
git commit -m "Add: Chidori effect variant"

# 4. Push to the branch
git push origin feature/new-jutsu

# 5. Open a Pull Request
```

**Ideas for contributions:**
- 🔴 Add a **Chidori** (lightning) mode
- 🎮 Gesture-based activation (e.g., specific hand pose triggers effect)
- 📊 Add FPS counter overlay
- 🎵 Sound effects when effect activates

---

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: cv2` | Run `pip install opencv-python` |
| `ModuleNotFoundError: mediapipe` | Run `pip install mediapipe` |
| Webcam not detected | Check webcam index in code (try `cv2.VideoCapture(1)`) |
| Laggy performance | Lower frame resolution or close other apps |

---

## 📜 License

This project is licensed under the **MIT License** — feel free to use, modify and distribute it.

---

## 👤 Author

<div align="center">

**Suman18-bit**

[![GitHub](https://img.shields.io/badge/GitHub-Suman18--bit-181717?style=for-the-badge&logo=github)](https://github.com/Suman18-bit)

*"Believe it!"* 🍥

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00BCD4,50:1565C0,100:0D47A1&height=100&section=footer" width="100%"/>

⭐ **If you found this cool, drop a star!** ⭐

</div>
