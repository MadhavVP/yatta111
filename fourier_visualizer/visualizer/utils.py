import cv2
import numpy as np

def process_image_to_fourier(image_path, num_coefficients=100):
    """
    Reads an image, extracts the largest contour, performs FFT,
    and returns a sorted list of Fourier coefficients.
    """
    # 1. Image Preprocessing
    img = cv2.imread(image_path, 0)
    if img is None:
        raise ValueError("Could not read image file.")

    # Invert if the background is light (standard drawing) to make the drawing white (255)
    # Using simple thresholding
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # 2. Extract Contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return []

    # Filter out small noise
    valid_contours = [c for c in contours if cv2.contourArea(c) > 50]
    if not valid_contours:
        return []

    # Sort checks to find a good starting point (e.g. largest)
    # We want to visit all significant contours (like the dot on an 'i')
    # Strategy: Greedy Nearest Neighbor path
    
    # Start with largest contour
    # Find index of largest contour to safely remove
    largest_idx = -1
    max_area = -1
    for i, c in enumerate(valid_contours):
        area = cv2.contourArea(c)
        if area > max_area:
            max_area = area
            largest_idx = i
            
    current_contour = valid_contours.pop(largest_idx)
    
    # Simplify first
    epsilon = 0.002 * cv2.arcLength(current_contour, True)
    approx = cv2.approxPolyDP(current_contour, epsilon, True)
    final_points = approx.reshape(-1, 2)
    
    while valid_contours:
        # Last point of current path
        last_point = final_points[-1]
        
        # Find closest start point among remaining contours
        best_dist = float('inf')
        best_idx = -1
        
        for i, c in enumerate(valid_contours):
            # Check distance to the first point of this contour
            # (We could check all points and rotate the contour, but that's expensive.
            #  Assuming contours are closed loops, start point is arbitrary but fixed.)
            dist = np.linalg.norm(c[0][0] - last_point)
            if dist < best_dist:
                best_dist = dist
                best_idx = i
        
        # Add the best match
        next_c = valid_contours.pop(best_idx)
        
        # Simplify next contour
        eps = 0.002 * cv2.arcLength(next_c, True)
        approx_next = cv2.approxPolyDP(next_c, eps, True)
        pts_next = approx_next.reshape(-1, 2)
        
        # Append (the "jump" will be handled by the Fourier Series as a fast transition)
        final_points = np.vstack([final_points, pts_next])
        
    contour_points = final_points

    # 3. Convert to Complex Plane (x + iy)
    # In images, y increases downwards. In standard plotting, y increases upwards.
    # We negate y to have it upright.
    x = contour_points[:, 0]
    y = -contour_points[:, 1]
    complex_points = x + 1j * y
    
    # Center the drawing
    complex_points = complex_points - np.mean(complex_points)

    # 4. Compute DFT
    dft_result = np.fft.fft(complex_points)
    
    # 5. Package Coefficients
    # np.fft.fft returns frequencies in order: [0, 1, ..., N/2-1, -N/2, ..., -1]
    # We need to preserve these specific frequencies.
    coefficients = []
    N = len(dft_result)
    
    for k in range(N):
        # Calculate the correct frequency index
        if k <= N / 2:
            freq = k
        else:
            freq = k - N
            
        val = dft_result[k]
        
        # Normalize amplitude by N (standard DFT normalization)
        radius = np.abs(val) / N
        phase = np.angle(val)
        
        coefficients.append({
            "freq": freq,
            "radius": radius,
            "phase": phase
        })

    # 6. Sort by radius (Amplitude)
    # We want to use the strongest components first for the approximation
    coefficients.sort(key=lambda x: x["radius"], reverse=True)

    # Limit to requested number (or total if less)
    return coefficients[:min(len(coefficients), num_coefficients)]
