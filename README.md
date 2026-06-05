# Rasengan
Here is an attractive, well-structured README file tailored for your Rasengan AR project. You can save this as `README.md` in the same directory as your Python script.

---

# 🌀 Interactive Rasengan AR Effect

Welcome to the **Interactive Rasengan AR Effect**! This Python application uses computer vision to bring the iconic jutsu from *Naruto* to life. By leveraging your webcam, it tracks your hand in real-time and generates a dynamic, spinning, particle-based Rasengan right in the palm of your hand.

## ✨ Features

* **Real-Time Hand Tracking:** Uses Google's MediaPipe Task API to instantly locate your palm and scale the effect based on your hand's distance from the camera.
* **Dynamic Particle System:** Features spinning chakra rings, a glowing core, and electrical static effects that spiral toward the center.
* **Auto-Downloading Model:** Automatically fetches the required MediaPipe `hand_landmarker.task` model so you don't have to download it manually.
* **Interactive Controls:** Easily adjust the size of your Rasengan or cycle through different chakra natures (colors) using keyboard shortcuts.
* **Sleek UI:** Displays on-screen status overlays, active controls, and a custom futuristic font layout.

---

## 🛠️ Prerequisites

Before you run the script, ensure you have **Python 3.7+** installed on your machine. You will also need to install the following required libraries:

```bash
pip install opencv-python numpy mediapipe

```

---

## 🚀 Getting Started

1. **Clone or Download** the repository to your local machine.
2. **Navigate** to the folder containing the script.
3. **Run the script** using Python:

```bash
python rasengan.py

```

When you launch the program for the first time, it will take a few seconds to download the lightweight MediaPipe model. Once your webcam activates, simply hold your hand up to the camera to charge your chakra!

---

## 🎮 Controls

Use the following keyboard commands to interact with your jutsu in real-time:

| Key | Action |
| --- | --- |
| **`+` / `=**` | Increase the size of the Rasengan |
| **`-` / `_**` | Decrease the size of the Rasengan |
| **`C`** | Cycle chakra colors (Blue, Green, Red, Yellow, Purple) |
| **`Q` / `ESC**` | Deactivate the jutsu and quit the application |

---

## 🧠 How It Works

1. **MediaPipe Vision:** The script passes live webcam frames (converted to RGB) into MediaPipe's `HandLandmarker`. It isolates specific nodes (the wrist, index MCP, and pinky MCP) to reliably triangulate the exact center of your palm.
2. **Math & Scaling:** The distance between your wrist and middle fingertip is calculated to dynamically scale the Rasengan. If you move your hand closer to the camera, the Rasengan grows; if you move it away, it shrinks.
3. **OpenCV Rendering:** The `RasenganEffect` class uses OpenCV to draw overlapping transparent circles (Alpha Blending), moving particles with calculated trajectories (Sine/Cosine waves), and randomized electrical lines to create the final visual composition.

---

**Disclaimer:** *Prolonged use will not actually drain your real-world chakra. Have fun!* 🥷
