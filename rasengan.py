import cv2
import numpy as np
import math
import random
import mediapipe as mp
from collections import deque
import urllib.request
import os

def download_model():
    """Download the hand landmarker model if not present"""
    model_path = "hand_landmarker.task"
    if not os.path.exists(model_path):
        print("Downloading hand landmarker model...")
        url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
        urllib.request.urlretrieve(url, model_path)
        print("Model downloaded!")
    return model_path

class RasenganEffect:
    def __init__(self):
        # Initialize MediaPipe Hands (Task API)
        model_path = download_model()

        # CORRECT IMPORTS for newer MediaPipe versions
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        base_options = BaseOptions(model_asset_path=model_path)
        options = HandLandmarkerOptions(
            base_options=base_options,
            num_hands=2,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.landmarker = HandLandmarker.create_from_options(options)

        # Rasengan parameters
        self.angle = 0
        self.particles = []
        self.trail_points = deque(maxlen=20)
        self.rasengan_radius = 60
        self.chakra_color = (100, 200, 255)  # Light blue (BGR)
        self.core_color = (255, 255, 255)    # White core

        # Particle system
        self.max_particles = 100

    def get_palm_center(self, landmarks, frame_shape):
        """Calculate palm center from landmarks"""
        h, w = frame_shape[:2]

        # Use wrist (0), index_mcp (5), pinky_mcp (17) to find palm center
        wrist = landmarks[0]
        index_mcp = landmarks[5]
        pinky_mcp = landmarks[17]

        # Average position (landmarks are normalized 0-1)
        cx = int((wrist.x + index_mcp.x + pinky_mcp.x) / 3 * w)
        cy = int((wrist.y + index_mcp.y + pinky_mcp.y) / 3 * h)

        return (cx, cy)

    def get_hand_size(self, landmarks, frame_shape):
        """Estimate hand size for scaling Rasengan"""
        h, w = frame_shape[:2]
        wrist = landmarks[0]
        middle_tip = landmarks[12]

        dist = math.sqrt(
            (wrist.x - middle_tip.x)**2 + 
            (wrist.y - middle_tip.y)**2
        ) * math.sqrt(w**2 + h**2)

        return dist

    def draw_landmarks(self, frame, landmarks):
        """Draw hand skeleton on frame"""
        h, w = frame.shape[:2]
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),  # Index
            (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
            (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
            (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
            (5, 9), (9, 13), (13, 17)  # Palm
        ]

        points = []
        for lm in landmarks:
            x = int(lm.x * w)
            y = int(lm.y * h)
            points.append((x, y))
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

        for start, end in connections:
            if start < len(points) and end < len(points):
                cv2.line(frame, points[start], points[end], (0, 0, 255), 2)

        return frame

    def create_particle(self, center, radius):
        """Create a chakra particle"""
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        dist = random.uniform(0, radius)

        return {
            'x': center[0] + math.cos(angle) * dist,
            'y': center[1] + math.sin(angle) * dist,
            'vx': math.cos(angle + math.pi/2) * speed,
            'vy': math.sin(angle + math.pi/2) * speed,
            'life': random.uniform(0.5, 1.0),
            'max_life': random.uniform(0.5, 1.0),
            'size': random.randint(2, 6)
        }

    def update_particles(self, center, radius):
        """Update and spawn particles"""
        # Spawn new particles
        while len(self.particles) < self.max_particles:
            self.particles.append(self.create_particle(center, radius))

        # Update existing particles
        new_particles = []
        for p in self.particles:
            p['x'] += p['vx'] + random.uniform(-1, 1)
            p['y'] += p['vy'] + random.uniform(-1, 1)
            p['life'] -= 0.02

            # Spiral toward center
            dx = center[0] - p['x']
            dy = center[1] - p['y']
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                p['vx'] += (dx/dist) * 0.5
                p['vy'] += (dy/dist) * 0.5

            if p['life'] > 0:
                new_particles.append(p)

        self.particles = new_particles

    def draw_rasengan(self, frame, center, hand_size):
        """Draw the Rasengan effect"""
        overlay = frame.copy()
        h, w = frame.shape[:2]

        # Scale based on hand size
        base_radius = int(hand_size * 0.4)
        self.rasengan_radius = max(30, min(base_radius, 150))

        # Update rotation
        self.angle = (self.angle + 15) % 360

        # Update particles
        self.update_particles(center, self.rasengan_radius)

        # Draw outer chakra glow (multiple layers)
        for i in range(5):
            radius = self.rasengan_radius + i * 15
            alpha = 0.15 - i * 0.02
            color = (
                self.chakra_color[0] - i * 10,
                self.chakra_color[1] - i * 5,
                self.chakra_color[2]
            )
            cv2.circle(overlay, center, radius, color, -1)

        # Draw spinning chakra rings
        for ring in range(3):
            ring_radius = self.rasengan_radius * (0.3 + ring * 0.35)
            points = []
            num_points = 20 + ring * 10

            for i in range(num_points):
                angle_rad = math.radians(self.angle * (1 + ring * 0.5) + i * (360/num_points))
                # Add wobble
                wobble = math.sin(angle_rad * 3 + self.angle * 0.1) * 5
                r = ring_radius + wobble

                x = int(center[0] + math.cos(angle_rad) * r)
                y = int(center[1] + math.sin(angle_rad) * r)
                points.append((x, y))

            # Draw ring with glow
            for i in range(len(points)):
                pt1 = points[i]
                pt2 = points[(i+1) % len(points)]
                cv2.line(overlay, pt1, pt2, self.chakra_color, 2, cv2.LINE_AA)

        # Draw particles
        for p in self.particles:
            alpha = p['life'] / p['max_life']
            size = int(p['size'] * alpha)
            if size > 0:
                color = (
                    int(self.chakra_color[0] * alpha),
                    int(self.chakra_color[1] * alpha),
                    int(255 * alpha + 100)
                )
                x, y = int(p['x']), int(p['y'])
                if 0 <= x < w and 0 <= y < h:
                    cv2.circle(overlay, (x, y), size, color, -1)

        # Draw bright core
        core_radius = int(self.rasengan_radius * 0.3)
        cv2.circle(overlay, center, core_radius, self.core_color, -1)
        cv2.circle(overlay, center, core_radius + 5, (200, 230, 255), 3)

        # Add electric/static effect (random lines)
        for _ in range(8):
            angle1 = random.uniform(0, 2 * math.pi)
            angle2 = angle1 + random.uniform(-0.5, 0.5)
            r1 = random.uniform(0, self.rasengan_radius * 0.8)
            r2 = random.uniform(0, self.rasengan_radius * 0.8)

            x1 = int(center[0] + math.cos(angle1) * r1)
            y1 = int(center[1] + math.sin(angle1) * r1)
            x2 = int(center[0] + math.cos(angle2) * r2)
            y2 = int(center[1] + math.sin(angle2) * r2)

            cv2.line(overlay, (x1, y1), (x2, y2), (255, 255, 255), 1, cv2.LINE_AA)

        # Blend overlay with original frame
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        return frame

    def draw_ui(self, frame, hand_detected):
        """Draw UI elements"""
        h, w = frame.shape[:2]

        # Title
        cv2.putText(frame, "RASENGAN", (20, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (100, 200, 255), 3)

        # Status
        status = "CHAKRA CHARGED!" if hand_detected else "Show hand to charge..."
        color = (100, 255, 100) if hand_detected else (100, 100, 100)
        cv2.putText(frame, status, (20, h - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Controls
        controls = "Q: Quit | +/- : Size | C: Change Color"
        cv2.putText(frame, controls, (w - 400, h - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)

        return frame

def main():
    # Initialize camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW for Windows stability

    # Set resolution (adjust as needed)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    rasengan = RasenganEffect()

    print("=" * 50)
    print("RASENGAN EFFECT ACTIVATED!")
    print("Controls:")
    print("  Q or ESC - Quit")
    print("  + / -    - Increase/Decrease Rasengan size")
    print("  C        - Change chakra color")
    print("=" * 50)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)

        # Convert to RGB for MediaPipe (Task API expects MP Image)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Detect hands
        results = rasengan.landmarker.detect(mp_image)

        hand_detected = False

        if results.hand_landmarks:
            hand_detected = True
            for hand_landmarks in results.hand_landmarks:
                # Get palm center
                center = rasengan.get_palm_center(hand_landmarks, frame.shape)
                hand_size = rasengan.get_hand_size(hand_landmarks, frame.shape)

                # Draw hand skeleton
                frame = rasengan.draw_landmarks(frame, hand_landmarks)

                # Draw Rasengan
                frame = rasengan.draw_rasengan(frame, center, hand_size)

        # Draw UI
        frame = rasengan.draw_ui(frame, hand_detected)

        # Show frame
        cv2.imshow('Rasengan Effect', frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key in [ord('q'), 27]:  # Q or ESC
            break
        elif key == ord('+') or key == ord('='):
            rasengan.rasengan_radius = min(rasengan.rasengan_radius + 10, 200)
        elif key == ord('-') or key == ord('_'):
            rasengan.rasengan_radius = max(rasengan.rasengan_radius - 10, 20)
        elif key == ord('c'):
            # Cycle through chakra colors
            colors = [
                (100, 200, 255),  # Blue (Naruto)
                (100, 255, 100),  # Green
                (100, 100, 255),  # Red
                (255, 200, 100),  # Yellow
                (255, 100, 255),  # Purple
            ]
            current_idx = colors.index(rasengan.chakra_color) if rasengan.chakra_color in colors else 0
            rasengan.chakra_color = colors[(current_idx + 1) % len(colors)]

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    rasengan.landmarker.close()
    print("Rasengan deactivated.")

if __name__ == "__main__":
    main()