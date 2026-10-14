"""
Dataset Generator & Augmentation Pipeline for Railway Crack Detection.

Generates structured YOLO dataset (train/val/test) with synthetic railway crack
patterns, varied lighting, noise, orientations, and label annotations.
"""

import os
import random
import cv2
import numpy as np


class DatasetGenerator:
    """Generates synthetic railway crack dataset formatted for YOLO training."""

    def __init__(self, base_dir: str = "dataset", img_size=(640, 640)) -> None:
        self.base_dir = base_dir
        self.img_w, self.img_h = img_size
        self._setup_directories()

    def _setup_directories(self) -> None:
        """Create dataset directory layout."""
        for split in ["train", "val", "test"]:
            os.makedirs(os.path.join(self.base_dir, "images", split), exist_ok=True)
            os.makedirs(os.path.join(self.base_dir, "labels", split), exist_ok=True)
        print(f"[DATASET] Initialized directory structure at: {self.base_dir}/")

    def _draw_synthetic_crack(
        self, img: np.ndarray
    ) -> tuple[np.ndarray, tuple[float, float, float, float]]:
        """Draw randomized realistic crack line on steel rail surface."""
        h, w = img.shape[:2]
        cx = random.randint(int(w * 0.3), int(w * 0.7))
        cy = random.randint(int(h * 0.3), int(h * 0.7))

        length = random.randint(40, 150)
        angle_rad = random.uniform(-0.8, 0.8)
        num_nodes = random.randint(4, 8)

        curr_x, curr_y = cx - int(length / 2 * np.cos(angle_rad)), cy - int(
            length / 2 * np.sin(angle_rad)
        )
        points = [(curr_x, curr_y)]

        step_len = length / num_nodes
        for _ in range(num_nodes):
            jitter_angle = angle_rad + random.uniform(-0.4, 0.4)
            curr_x += int(step_len * np.cos(jitter_angle))
            curr_y += int(step_len * np.sin(jitter_angle))
            points.append((curr_x, curr_y))

        # Bounding box calculation
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = max(0, min(xs) - 5), min(w, max(xs) + 5)
        min_y, max_y = max(0, min(ys) - 5), min(h, max(ys) + 5)

        # Draw crack shadow & dark line
        thickness = random.randint(2, 4)
        pts_np = np.array(points, np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [pts_np], isClosed=False, color=(20, 20, 20), thickness=thickness)
        cv2.polylines(img, [pts_np], isClosed=False, color=(5, 5, 5), thickness=1)

        # Convert to YOLO normalized format (class_id x_center y_center width height)
        bbox_w = (max_x - min_x) / w
        bbox_h = (max_y - min_y) / h
        bbox_cx = ((min_x + max_x) / 2.0) / w
        bbox_cy = ((min_y + max_y) / 2.0) / h

        return img, (bbox_cx, bbox_cy, bbox_w, bbox_h)

    def generate_sample(
        self, sample_id: int, split: str, is_positive: bool = True
    ) -> None:
        """Generate a single dataset sample with image and label annotation."""
        # Steel rail background base
        base_color = random.randint(140, 190)
        img = np.full(
            (self.img_h, self.img_w, 3), (base_color, base_color + 5, base_color + 10), dtype=np.uint8
        )

        # Add steel texture grain & noise
        noise = np.random.randint(-20, 20, (self.img_h, self.img_w, 3), dtype=np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        bbox_str = ""
        if is_positive:
            img, (cx, cy, bw, bh) = self._draw_synthetic_crack(img)
            bbox_str = f"0 {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n"

        filename = f"rail_crack_{sample_id:04d}"
        img_path = os.path.join(self.base_dir, "images", split, f"{filename}.jpg")
        lbl_path = os.path.join(self.base_dir, "labels", split, f"{filename}.txt")

        cv2.imwrite(img_path, img)
        with open(lbl_path, "w") as f:
            f.write(bbox_str)

    def build_dataset(self, num_samples: int = 100) -> None:
        """Generate full train, val, and test sets."""
        print(f"[DATASET] Generating {num_samples} dataset samples...")
        for i in range(num_samples):
            if i < int(num_samples * 0.7):
                split = "train"
            elif i < int(num_samples * 0.85):
                split = "val"
            else:
                split = "test"

            is_pos = i % 5 != 0  # 80% positive (with crack), 20% negative (normal rail)
            self.generate_sample(i, split, is_positive=is_pos)
        print("[DATASET] Dataset build completed successfully.")


def main() -> None:
    gen = DatasetGenerator()
    gen.build_dataset(num_samples=50)


if __name__ == "__main__":
    main()
