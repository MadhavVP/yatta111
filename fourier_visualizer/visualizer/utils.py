import cv2
import numpy as np

def process_image_to_fourier(image_path, num_coefficients=100):
    """
    Reads an image, finds all significant contours, sorts them spatially,
    and returns a list of Fourier coefficient sets (one per contour).
    """
    # 1. Image Preprocessing
    img = cv2.imread(image_path, 0)
    if img is None:
        raise ValueError("Could not read image file.")

    # Invert to get white drawing on black
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # 2. Extract Contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return []

    # Filter out small noise
    valid_contours = [c for c in contours if cv2.contourArea(c) > 50]
    if not valid_contours:
        return []

    # 3. Sort Contours Spatially (Simulation of Time)
    # Sort Top-Left to Bottom-Right (y + x approx)
    # Bounding box: (x, y, w, h)
    def get_sort_key(c):
        x, y, w, h = cv2.boundingRect(c)
        return y + x * 0.1 # Weight Y more to simulate lines of text

    valid_contours.sort(key=get_sort_key)

    valid_contours.sort(key=get_sort_key)

    all_coefficients = []

    # 1. Collect all points to find GLOBAL center
    all_points = []
    contours_points = []
    
    for contour in valid_contours:
        # Simplify
        epsilon = 0.002 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        points = approx.reshape(-1, 2).astype(np.float32)
        contours_points.append(points)
        all_points.extend(points)
        
    if not all_points:
        return []
        
    all_points_arr = np.array(all_points)
    global_mean = np.mean(all_points_arr, axis=0)

    # 2. Process each contour offset by GLOBAL mean
    for points in contours_points:
        offset_points = points - global_mean
        
        coeffs = compute_fourier_coefficients(offset_points, num_coefficients, is_closed_loop=True)
        all_coefficients.append(coeffs)
        
    return all_coefficients

def process_vectors_to_fourier(vector_data, num_coefficients=100):
    """
    Processes raw vector data (list of lists of {x,y}) from the frontend.
    """
    all_coefficients = []
    
    # 1. Collect all points to find GLOBAL center
    all_points = []
    strokes_points = []
    
    for stroke in vector_data:
        if len(stroke) < 3: continue
        # Convert to numpy array
        points = np.array([[p['x'], p['y']] for p in stroke]).astype(np.float32)
        strokes_points.append(points)
        all_points.extend(points)
        
    if not all_points:
        return []

    # Calculate Global Mean
    all_points_arr = np.array(all_points)
    global_mean = np.mean(all_points_arr, axis=0)
    
    # 2. Process each stroke offset by GLOBAL mean
    for points in strokes_points:
        # Center the entire drawing around (0,0)
        offset_points = points - global_mean
        
        # Open strokes need retracing to be periodic
        coeffs = compute_fourier_coefficients(offset_points, num_coefficients, is_closed_loop=False)
        all_coefficients.append(coeffs)
        
    return all_coefficients

def compute_fourier_coefficients(points, num_coefficients, is_closed_loop=False):
    """
    Helper to calc DFT for a set of 2D points.
    """
    # 1. Resample (Uniform speed)
    target_points = 1024 
    points = resample_path(points, target_points)
    
    # 2. Retrace (if open)
    if not is_closed_loop:
        reversed_points = points[::-1]
        points = np.vstack([points, reversed_points[1:-1]])
        
    # 3. Complex Plane
    x = points[:, 0]
    y = points[:, 1]
    # Do NOT flip Y. 
    # Image/Canvas: Y is Down.
    # Frontend Sin: Y is Down.
    # So we keep Y as is.
    
    complex_points = x + 1j * y
    # REMOVED local centering: complex_points = complex_points - np.mean(complex_points)

    # 4. DFT
    dft_result = np.fft.fft(complex_points)
    
    # 5. Package
    coefficients = []
    N = len(dft_result)
    
    for k in range(N):
        if k <= N / 2:
            freq = k
        else:
            freq = k - N
            
        val = dft_result[k]
        radius = np.abs(val) / N
        phase = np.angle(val)
        
        coefficients.append({
            "freq": freq,
            "radius": radius,
            "phase": phase
        })

    coefficients.sort(key=lambda x: x["radius"], reverse=True)
    return coefficients[:min(len(coefficients), num_coefficients)]

def resample_path(points, n_points):
    """
    Interpolates path to have `n_points` uniformly spaced.
    """
    if len(points) < 2:
        return np.resize(points, (n_points, 2))

    # Calculate cumulative distance
    dists = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
    cum_dist = np.insert(np.cumsum(dists), 0, 0)
    total_dist = cum_dist[-1]
    
    if total_dist == 0:
        return np.resize(points, (n_points, 2))
        
    # Create uniform distances
    uniform_dists = np.linspace(0, total_dist, n_points)
    
    # Interpolate X and Y
    new_x = np.interp(uniform_dists, cum_dist, points[:, 0])
    new_y = np.interp(uniform_dists, cum_dist, points[:, 1])
    
    return np.column_stack((new_x, new_y))
