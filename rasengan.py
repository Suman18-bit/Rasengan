import cv2
import numpy as np
import math
import random
import mediapipe as mp
from collections import deque
import urllib.request
import os


def download_model():
    model_path = "hand_landmarker.task"
    if not os.path.exists(model_path):
        print("Downloading hand landmarker model...")
        url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
        urllib.request.urlretrieve(url, model_path)
        print("Model downloaded!")
    return model_path


class Particle:
    def __init__(self, center, radius, chakra_color, mode="orbit"):
        self.mode = mode
        self.chakra_color = chakra_color
        self.size = random.uniform(1.5, 5.5)
        self.orbit_radius = 0.0
        self.orbit_angle = 0.0
        self.orbit_speed = 0.0
        self.vx = 0.0
        self.vy = 0.0

        if mode == "orbit":
            self.orbit_radius = random.uniform(radius * 0.25, radius * 1.15)
            self.orbit_angle = random.uniform(0, 2 * math.pi)
            self.orbit_speed = random.uniform(0.03, 0.13) * random.choice([-1, 1])
            self.x = float(center[0] + math.cos(self.orbit_angle) * self.orbit_radius)
            self.y = float(center[1] + math.sin(self.orbit_angle) * self.orbit_radius)
            self.life = random.uniform(0.7, 1.0)

        elif mode == "burst":
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(4, 14)
            self.x = float(center[0] + math.cos(angle) * random.uniform(0, radius * 0.3))
            self.y = float(center[1] + math.sin(angle) * random.uniform(0, radius * 0.3))
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.life = random.uniform(0.5, 1.0)

        elif mode == "wisp":
            self.orbit_radius = random.uniform(radius * 0.1, radius * 0.65)
            self.orbit_angle = random.uniform(0, 2 * math.pi)
            self.orbit_speed = random.uniform(0.05, 0.18)
            drift = random.uniform(0, 2 * math.pi)
            self.x = float(center[0] + math.cos(self.orbit_angle) * self.orbit_radius)
            self.y = float(center[1] + math.sin(self.orbit_angle) * self.orbit_radius)
            self.vx = math.cos(drift) * random.uniform(0.5, 2.0)
            self.vy = math.sin(drift) * random.uniform(0.5, 2.0)
            self.life = random.uniform(0.5, 1.0)

        elif mode == "spark":
            angle = random.uniform(0, 2 * math.pi)
            self.orbit_radius = radius * random.uniform(0.9, 1.3)
            self.orbit_angle = angle
            self.orbit_speed = random.uniform(0.08, 0.2) * random.choice([-1, 1])
            self.x = float(center[0] + math.cos(angle) * self.orbit_radius)
            self.y = float(center[1] + math.sin(angle) * self.orbit_radius)
            self.vx = math.cos(angle) * random.uniform(2, 6)
            self.vy = math.sin(angle) * random.uniform(2, 6)
            self.life = random.uniform(0.3, 0.7)

        self.max_life = self.life

    def update(self, center, radius, chakra_color):
        self.chakra_color = chakra_color

        if self.mode == "orbit":
            self.orbit_angle += self.orbit_speed
            self.x = center[0] + math.cos(self.orbit_angle) * self.orbit_radius
            self.y = center[1] + math.sin(self.orbit_angle) * self.orbit_radius
            self.life -= 0.008

        elif self.mode == "burst":
            dx = center[0] - self.x
            dy = center[1] - self.y
            dist = math.sqrt(dx * dx + dy * dy) + 0.001
            self.vx += (dx / dist) * 0.35
            self.vy += (dy / dist) * 0.35
            self.vx *= 0.96
            self.vy *= 0.96
            self.x += self.vx + random.uniform(-0.4, 0.4)
            self.y += self.vy + random.uniform(-0.4, 0.4)
            self.life -= 0.022

        elif self.mode == "wisp":
            self.orbit_angle += self.orbit_speed
            tx = center[0] + math.cos(self.orbit_angle) * self.orbit_radius
            ty = center[1] + math.sin(self.orbit_angle) * self.orbit_radius
            self.x += (tx - self.x) * 0.1 + self.vx * 0.25
            self.y += (ty - self.y) * 0.1 + self.vy * 0.25
            self.life -= 0.014

        elif self.mode == "spark":
            self.orbit_angle += self.orbit_speed
            self.x += self.vx
            self.y += self.vy
            self.vx *= 0.94
            self.vy *= 0.94
            self.life -= 0.035

        return self.life > 0


class Shockwave:
    def __init__(self, center, max_radius, color):
        self.center = center
        self.radius = 5.0
        self.max_radius = float(max_radius)
        self.color = color
        self.life = 1.0
        self.speed = max_radius / 22.0

    def update(self):
        self.radius += self.speed
        self.life = max(0.0, 1.0 - self.radius / self.max_radius)
        return self.life > 0


class RasenganEffect:
    def __init__(self):
        model_path = download_model()
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions

        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            num_hands=2,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.landmarker = HandLandmarker.create_from_options(options)

        self.angle = 0.0
        self.frame_count = 0
        self.particles = []
        self.shockwaves = []
        self.trail = deque(maxlen=18)
        self.rasengan_radius = 60
        self.chakra_colors = [
            (100, 200, 255),
            (80, 255, 120),
            (80, 80, 255),
            (255, 200, 80),
            (200, 80, 255),
        ]
        self.color_idx = 0
        self.chakra_color = self.chakra_colors[0]
        self.max_particles = 160
        self.pulse_phase = 0.0
        self.shockwave_timer = 0
        self.band_angle = 0.0
        self.tendril_seed = 0

    def get_palm_center(self, landmarks, frame_shape):
        h, w = frame_shape[:2]
        wrist = landmarks[0]
        index_mcp = landmarks[5]
        pinky_mcp = landmarks[17]
        cx = int((wrist.x + index_mcp.x + pinky_mcp.x) / 3 * w)
        cy = int((wrist.y + index_mcp.y + pinky_mcp.y) / 3 * h)
        return cx, cy

    def get_hand_size(self, landmarks, frame_shape):
        h, w = frame_shape[:2]
        wrist = landmarks[0]
        middle_tip = landmarks[12]
        return math.sqrt(
            (wrist.x - middle_tip.x) ** 2 + (wrist.y - middle_tip.y) ** 2
        ) * math.sqrt(w * w + h * h)

    def draw_landmarks(self, frame, landmarks):
        h, w = frame.shape[:2]
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (0, 9), (9, 10), (10, 11), (11, 12),
            (0, 13), (13, 14), (14, 15), (15, 16),
            (0, 17), (17, 18), (18, 19), (19, 20),
            (5, 9), (9, 13), (13, 17),
        ]
        pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
        for s, e in connections:
            if s < len(pts) and e < len(pts):
                cv2.line(frame, pts[s], pts[e],
                         tuple(c // 3 for c in self.chakra_color), 1, cv2.LINE_AA)
        for pt in pts:
            cv2.circle(frame, pt, 3, self.chakra_color, -1, cv2.LINE_AA)
            cv2.circle(frame, pt, 5, tuple(c // 2 for c in self.chakra_color), 1, cv2.LINE_AA)
        return frame

    def _make_particle(self, center, radius):
        mode = random.choices(
            ["orbit", "burst", "wisp", "spark"], weights=[6, 2, 3, 1]
        )[0]
        return Particle(center, radius, self.chakra_color, mode)

    def update_particles(self, center, radius):
        while len(self.particles) < self.max_particles:
            self.particles.append(self._make_particle(center, radius))
        refreshed = []
        for p in self.particles:
            if p.update(center, radius, self.chakra_color):
                refreshed.append(p)
            else:
                refreshed.append(self._make_particle(center, radius))
        self.particles = refreshed[: self.max_particles]

    def draw_bloom(self, frame, center, radius):
        bloom = np.zeros_like(frame, dtype=np.uint8)
        for i in range(8):
            r = int(radius + i * 24)
            alpha = max(0.0, 0.52 - i * 0.06)
            c = tuple(min(255, int(ch * alpha * 2.0)) for ch in self.chakra_color)
            cv2.circle(bloom, center, r, c, -1)
        bloom = cv2.GaussianBlur(bloom, (75, 75), 38)
        cv2.addWeighted(bloom, 0.72, frame, 1.0, 0, frame)

    def draw_trail(self, frame):
        for i, (pt, r) in enumerate(self.trail):
            alpha = i / len(self.trail)
            fade = int(alpha * 80)
            c = tuple(min(255, int(ch * alpha * 0.6)) for ch in self.chakra_color)
            cv2.circle(frame, pt, max(1, int(r * alpha * 0.4)), c, -1, cv2.LINE_AA)

    def draw_wind_streaks(self, overlay, center, radius):
        for i in range(24):
            a = math.radians(self.angle * -0.38 + i * (360 / 24))
            length_var = random.uniform(-12, 12)
            r_in = radius * 0.58
            r_out = radius * 1.52 + length_var
            x1 = int(center[0] + math.cos(a) * r_in)
            y1 = int(center[1] + math.sin(a) * r_in)
            x2 = int(center[0] + math.cos(a) * r_out)
            y2 = int(center[1] + math.sin(a) * r_out)
            c = tuple(int(ch * 0.38) for ch in self.chakra_color)
            cv2.line(overlay, (x1, y1), (x2, y2), c, 1, cv2.LINE_AA)

    def draw_energy_bands(self, overlay, center, radius):
        self.band_angle = (self.band_angle + 2.8) % 360
        band_configs = [
            (1.0, 0.90, 0.20, 0.72, 2),
            (0.6, 0.78, 0.30, 0.55, 2),
            (1.4, 1.05, 0.14, 0.40, 1),
        ]
        for spd, rx_scale, ry_scale, fade, w in band_configs:
            rot = (self.band_angle * spd) % 360
            axes = (
                max(1, int(radius * rx_scale)),
                max(1, int(radius * ry_scale)),
            )
            c = tuple(min(255, int(ch * fade)) for ch in self.chakra_color)
            cv2.ellipse(overlay, center, axes, rot, 0, 360, c, w, cv2.LINE_AA)
            c2 = tuple(ci // 2 for ci in c)
            cv2.ellipse(overlay, center, axes, rot + 90, 0, 360, c2, 1, cv2.LINE_AA)

    def draw_shockwaves(self, overlay):
        alive = []
        for sw in self.shockwaves:
            if sw.update():
                c = tuple(int(ch * sw.life) for ch in sw.color)
                thickness = max(1, int(3 * sw.life))
                cv2.circle(overlay, sw.center, int(sw.radius), c, thickness, cv2.LINE_AA)
                inner_r = max(0, int(sw.radius - 6))
                if inner_r > 0:
                    c2 = tuple(int(ch * sw.life * 0.4) for ch in sw.color)
                    cv2.circle(overlay, sw.center, inner_r, c2, 1, cv2.LINE_AA)
                alive.append(sw)
        self.shockwaves = alive

    def draw_spirals(self, overlay, center, radius):
        spiral_defs = [
            (3, 24, 1.0, 2),
            (5, 16, 0.62, 1),
            (4, 32, 1.55, 2),
            (2, 10, -0.45, 1),
        ]
        for rings, n_pts, spd, w in spiral_defs:
            for ri in range(rings):
                ring_r = radius * (0.20 + ri * 0.35)
                pts = []
                for j in range(n_pts):
                    a = math.radians(self.angle * spd + j * (360 / n_pts))
                    wob = math.sin(a * 5 + self.frame_count * 0.07) * radius * 0.08
                    pts.append(
                        (
                            int(center[0] + math.cos(a) * (ring_r + wob)),
                            int(center[1] + math.sin(a) * (ring_r + wob)),
                        )
                    )
                for j in range(len(pts)):
                    cv2.line(
                        overlay, pts[j], pts[(j + 1) % len(pts)],
                        self.chakra_color, w, cv2.LINE_AA,
                    )

    def draw_energy_tendrils(self, overlay, center, radius):
        self.tendril_seed = (self.tendril_seed + 1) % 1000
        rng = random.Random(self.tendril_seed)
        for i in range(12):
            base_a = math.radians(self.angle * 0.75 + i * 30)
            px, py = center
            a = base_a
            segs = 16
            seg_len = radius / segs
            for s in range(segs):
                a += rng.uniform(-0.42, 0.42)
                nx = int(px + math.cos(a) * seg_len)
                ny = int(py + math.sin(a) * seg_len)
                fade = 1.0 - s / segs
                c = (
                    int(self.chakra_color[0] * fade),
                    int(self.chakra_color[1] * fade),
                    min(255, int(self.chakra_color[2] * fade + 130 * fade)),
                )
                cv2.line(
                    overlay, (px, py), (nx, ny), c,
                    max(1, int(3.8 - s * 0.22)), cv2.LINE_AA,
                )
                px, py = nx, ny

    def draw_particles(self, overlay, frame_shape):
        h, w = frame_shape[:2]
        for p in self.particles:
            alpha = p.life / p.max_life
            size = max(1, int(p.size * alpha))
            c = (
                int(p.chakra_color[0] * alpha),
                min(255, int(p.chakra_color[1] * alpha + 25 * alpha)),
                min(255, int(p.chakra_color[2] * alpha + 85 * alpha)),
            )
            x, y = int(p.x), int(p.y)
            if 0 <= x < w and 0 <= y < h:
                cv2.circle(overlay, (x, y), size, c, -1, cv2.LINE_AA)
                if size > 2:
                    glow_c = tuple(max(0, ci // 3) for ci in c)
                    cv2.circle(overlay, (x, y), size + 3, glow_c, 1, cv2.LINE_AA)
                if p.mode == "spark" and size > 1:
                    tail_x = int(x - p.vx * 1.5)
                    tail_y = int(y - p.vy * 1.5)
                    if 0 <= tail_x < w and 0 <= tail_y < h:
                        cv2.line(overlay, (x, y), (tail_x, tail_y), c, 1, cv2.LINE_AA)

    def draw_inner_rings(self, overlay, center, radius):
        for ring_i in range(4):
            r = int(radius * (0.55 + ring_i * 0.12))
            alpha = 0.5 - ring_i * 0.1
            a_offset = self.angle * (0.3 + ring_i * 0.15) + ring_i * 45
            for j in range(6):
                start_a = a_offset + j * 60
                cv2.ellipse(
                    overlay, center, (r, r), 0,
                    start_a, start_a + 40,
                    tuple(min(255, int(ch * alpha)) for ch in self.chakra_color),
                    1, cv2.LINE_AA,
                )

    def draw_core(self, overlay, center, radius):
        pulse = math.sin(self.pulse_phase) * 0.18 + 0.85
        secondary_pulse = math.sin(self.pulse_phase * 1.7 + 1.2) * 0.08 + 0.92
        core_r = int(radius * 0.30 * pulse)
        for layer in range(6):
            r = int(core_r * (1.0 - layer * 0.15))
            if r <= 0:
                break
            b = max(0, 255 - layer * 35)
            cv2.circle(overlay, center, r, (b, b, min(255, b + 30)), -1, cv2.LINE_AA)

        halo_r = int(core_r * secondary_pulse)
        cv2.circle(overlay, center, halo_r + 5, (210, 235, 255), 2, cv2.LINE_AA)
        cv2.circle(overlay, center, halo_r + 12,
                   tuple(int(ch * 0.78) for ch in self.chakra_color), 1, cv2.LINE_AA)
        cv2.circle(overlay, center, halo_r + 20,
                   tuple(int(ch * 0.38) for ch in self.chakra_color), 1, cv2.LINE_AA)

        flare_count = 6
        for fi in range(flare_count):
            fa = math.radians(self.angle * 1.5 + fi * (360 / flare_count))
            fx = int(center[0] + math.cos(fa) * (core_r + 8))
            fy = int(center[1] + math.sin(fa) * (core_r + 8))
            cv2.circle(overlay, (fx, fy), 2, (255, 255, 255), -1, cv2.LINE_AA)

    def draw_rasengan(self, frame, center, hand_size):
        self.rasengan_radius = max(30, min(int(hand_size * 0.4), 155))
        radius = self.rasengan_radius

        self.angle = (self.angle + 20) % 360
        self.pulse_phase += 0.13
        self.frame_count += 1
        self.shockwave_timer += 1

        if self.shockwave_timer >= 32:
            self.shockwave_timer = 0
            self.shockwaves.append(Shockwave(center, radius * 2.6, self.chakra_color))

        self.trail.append((center, radius))
        self.update_particles(center, radius)

        self.draw_bloom(frame, center, radius)
        self.draw_trail(frame)

        overlay = frame.copy()
        self.draw_wind_streaks(overlay, center, radius)
        self.draw_shockwaves(overlay)
        self.draw_energy_bands(overlay, center, radius)
        self.draw_spirals(overlay, center, radius)
        self.draw_inner_rings(overlay, center, radius)
        self.draw_energy_tendrils(overlay, center, radius)
        self.draw_particles(overlay, frame.shape)
        self.draw_core(overlay, center, radius)

        cv2.addWeighted(overlay, 0.78, frame, 0.22, 0, frame)
        return frame

    def draw_ui(self, frame, hand_detected):
        h, w = frame.shape[:2]

        shadow_c = tuple(c // 4 for c in self.chakra_color)
        cv2.putText(frame, "RASENGAN", (22, 52),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, shadow_c, 5, cv2.LINE_AA)
        cv2.putText(frame, "RASENGAN", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.chakra_color, 3, cv2.LINE_AA)

        status = "CHAKRA CHARGED!" if hand_detected else "Show hand to charge..."
        sc = (100, 255, 100) if hand_detected else (80, 80, 80)
        cv2.putText(frame, status, (20, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, sc, 2, cv2.LINE_AA)

        cv2.putText(
            frame, "Q: Quit  |  +/-: Size  |  C: Color",
            (w - 375, h - 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120, 120, 120), 1, cv2.LINE_AA,
        )
        return frame


def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    rasengan = RasenganEffect()

    print("=" * 50)
    print("RASENGAN EFFECT ACTIVATED!")
    print("  Q or ESC  — Quit")
    print("  + / -     — Adjust size")
    print("  C         — Cycle chakra color")
    print("=" * 50)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        results = rasengan.landmarker.detect(mp_image)

        hand_detected = False
        if results.hand_landmarks:
            hand_detected = True
            for hand_landmarks in results.hand_landmarks:
                center = rasengan.get_palm_center(hand_landmarks, frame.shape)
                hand_size = rasengan.get_hand_size(hand_landmarks, frame.shape)
                frame = rasengan.draw_landmarks(frame, hand_landmarks)
                frame = rasengan.draw_rasengan(frame, center, hand_size)
        else:
            rasengan.particles.clear()
            rasengan.shockwaves.clear()
            rasengan.trail.clear()

        frame = rasengan.draw_ui(frame, hand_detected)
        cv2.imshow("Rasengan Effect", frame)

        key = cv2.waitKey(1) & 0xFF
        if key in [ord("q"), 27]:
            break
        elif key in [ord("+"), ord("=")]:
            rasengan.rasengan_radius = min(rasengan.rasengan_radius + 10, 200)
        elif key in [ord("-"), ord("_")]:
            rasengan.rasengan_radius = max(rasengan.rasengan_radius - 10, 20)
        elif key == ord("c"):
            rasengan.color_idx = (rasengan.color_idx + 1) % len(rasengan.chakra_colors)
            rasengan.chakra_color = rasengan.chakra_colors[rasengan.color_idx]

    cap.release()
    cv2.destroyAllWindows()
    rasengan.landmarker.close()
    print("Rasengan deactivated.")


if __name__ == "__main__":
    main()
