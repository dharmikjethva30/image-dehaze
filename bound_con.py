import numpy as np
import cv2

def BoundCon(HazeImg, boundaryConstraint_windowSze, A, Transmission, C0, C1):
    # Check if HazeImg is color
    if (len(HazeImg.shape) == 3):
        # Compute transmission for each channel
        t_b = np.maximum((A[0] - HazeImg[:, :, 0].astype(float)) / (A[0] - C0),
                         (HazeImg[:, :, 0].astype(float) - A[0]) / (C1 - A[0]))
        t_g = np.maximum((A[1] - HazeImg[:, :, 1].astype(float)) / (A[1] - C0),
                         (HazeImg[:, :, 1].astype(float) - A[1]) / (C1 - A[1]))
        t_r = np.maximum((A[2] - HazeImg[:, :, 2].astype(float)) / (A[2] - C0),
                         (HazeImg[:, :, 2].astype(float) - A[2]) / (C1 - A[2]))

        # Select maximum transmission
        MaxVal = np.maximum(t_b, t_g, t_r)
        Transmission = np.minimum(MaxVal, 1)
    else:
        # Compute transmission for grayscale image
        Transmission = np.maximum((A[0] - HazeImg.astype(float)) / (A[0] - C0),
                                        (HazeImg.astype(float) - A[0]) / (C1 - A[0]))
        Transmission = np.minimum(Transmission, 1)

    # Apply morphological close operation
    kernel = np.ones((boundaryConstraint_windowSze, boundaryConstraint_windowSze), float)
    Transmission = cv2.morphologyEx(Transmission, cv2.MORPH_CLOSE, kernel=kernel)
    
    return A, Transmission, C0, C1