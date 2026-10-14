"""
Camera Calibration Tool for Railway Inspection Rover.

Computes camera intrinsic matrix, distortion coefficients, reprojection error
using OpenCV checkerboard pattern, and saves findings to camera_info.yaml.
"""

import sys
import cv2
import numpy as np
import yaml


class CameraCalibrator:
    """Checkerboard camera calibration helper."""

    def __init__(self, board_size=(9, 6), square_size_mm=25.0) -> None:
        self.board_size = board_size
        self.square_size_mm = square_size_mm

        # Prepare 3D object points in physical space (mm)
        self.objp = np.zeros((board_size[0] * board_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0 : board_size[0], 0 : board_size[1]].T.reshape(
            -1, 2
        ) * square_size_mm

        self.obj_points = []  # 3D real world points
        self.img_points = []  # 2D pixel image points
        self.image_size = None

    def add_calibration_image(self, img_bgr: np.ndarray) -> bool:
        """Find checkerboard corners in frame and store points."""
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        if self.image_size is None:
            self.image_size = (gray.shape[1], gray.shape[0])

        found, corners = cv2.findChessboardCorners(
            gray,
            self.board_size,
            cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE,
        )

        if found:
            criteria = (cv2.TERMCRITERIA_EPS + cv2.TERMCRITERIA_MAX_ITER, 30, 0.001)
            refined_corners = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria
            )
            self.obj_points.append(self.objp)
            self.img_points.append(refined_corners)
            return True
        return False

    def calibrate(self) -> dict:
        """Perform camera calibration and return intrinsics & reprojection error."""
        if len(self.img_points) < 3:
            raise ValueError(
                f"Need at least 3 valid checkerboard views to calibrate. Current: {len(self.img_points)}"
            )

        ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
            self.obj_points, self.img_points, self.image_size, None, None
        )

        # Calculate Reprojection Error
        total_error = 0.0
        for i in range(len(self.obj_points)):
            img_points2, _ = cv2.projectPoints(
                self.obj_points[i], rvecs[i], tvecs[i], K, dist
            )
            error = cv2.norm(self.img_points[i], img_points2, cv2.NORM_L2) / len(
                img_points2
            )
            total_error += error

        mean_error = total_error / len(self.obj_points)

        return {
            "image_width": self.image_size[0],
            "image_height": self.image_size[1],
            "camera_name": "rpi_camera_v3_50deg",
            "camera_matrix": {"rows": 3, "cols": 3, "data": K.flatten().tolist()},
            "distortion_model": "plumb_bob",
            "distortion_coefficients": {
                "rows": 1,
                "cols": len(dist.flatten()),
                "data": dist.flatten().tolist(),
            },
            "reprojection_error_pixels": float(mean_error),
        }

    def save_yaml(self, calib_data: dict, filepath: str) -> None:
        """Save calibration data to YAML format."""
        with open(filepath, "w") as f:
            yaml.dump(calib_data, f, default_flow_style=False)
        print(f"[CALIBRATION] Calibration file saved successfully to: {filepath}")


def main() -> None:
    print("=" * 60)
    print("      Railway Rover Camera Calibration Utility")
    print("=" * 60)
    print("Instructions:")
    print("1. Place a 9x6 checkerboard pattern in front of the camera.")
    print("2. The utility calculates intrinsic K matrix, D distortion, and pixel error.")
    print("=" * 60)

    # Demo / Synthetic calibration verification when run standalone
    calibrator = CameraCalibrator(board_size=(9, 6), square_size_mm=25.0)

    # Generate synthetic checkerboard images for pipeline verification
    for i in range(5):
        blank = np.full((720, 1280, 3), 200, dtype=np.uint8)
        # Draw checkerboard
        for r in range(7):
            for c in range(10):
                if (r + c) % 2 == 0:
                    cv2.rectangle(
                        blank,
                        (150 + c * 50, 100 + r * 50),
                        (200 + c * 50, 150 + r * 50),
                        (0, 0, 0),
                        -1,
                    )
        calibrator.add_calibration_image(blank)

    try:
        results = calibrator.calibrate()
        print(f"Reprojection Error: {results['reprojection_error_pixels']:.4f} pixels")
        print(f"Intrinsic Matrix K:\n{np.array(results['camera_matrix']['data']).reshape(3,3)}")
    except Exception as e:
        print(f"Calibration notice: {e}")


if __name__ == "__main__":
    main()
