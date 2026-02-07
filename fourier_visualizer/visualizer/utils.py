import cv2
import numpy as np

def process_image_to_fourier(image_path, num_coefficients=100):
    """
    Reads an image, extracts the largest contour, performs FFT,
    and returns a sorted list of Fourier coefficients.
    """
    # 1. Image Preprocessing
    img = cv2.imread(image_path, 0)
    # Invert if necessary (assume dark drawing on light background)
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # 2. Extract Contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return []

    # Take the largest contour (main stroke)
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Reshape to (N, 2) and simplify slightly to reduce noise
    contour_points = largest_contour.reshape(-1, 2)
    
    # Optional: Douglas-Peucker algorithm to reduce point count if drawing is shaky
    epsilon = 0.001 * cv2.arcLength(largest_contour, True)
    approx_curve = cv2.approxPolyDP(largest_contour, epsilon, True)
    contour_points = approx_curve.reshape(-1, 2)

    # 3. Convert to Complex Plane (x + iy)
    # Center the drawing by subtracting the mean
    complex_points = contour_points[:, 0] + 1j * contour_points[:, 1]
    complex_points = complex_points - np.mean(complex_points)

    # 4. Compute DFT
    dft_result = np.fft.fft(complex_points)
    
    # 5. Package Coefficients
    # We want to store: Frequency (k), Amplitude (radius), Phase (angle)
    coefficients = []
    N = len(dft_result)
    
    for k in range(N):
        freq = k
        val = dft_result[k]
        
        # Normalize amplitude by N
        radius = np.abs(val) / N
        phase = np.angle(val)
        
        coefficients.append({
            "freq": freq,
            "radius": radius,
            "phase": phase
        })

    # Sort by radius (largest arms first looks better)
    coefficients.sort(key=lambda x: x["radius"], reverse=True)

    # Limit the number of arms for performance/aesthetics
    return coefficients[:num_coefficients]
