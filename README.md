# Volume Control with Hand Tracking

This project uses hand tracking to control the system volume on Windows. It leverages OpenCV for hand detection and the PyCaw library for audio control. By adjusting the distance between your thumb and index finger, you can change the volume level.

## Features

- Hand detection using OpenCV and custom hand tracking logic
- Volume control using the PyCaw library
- Real-time display of hand landmarks and volume level

## Requirements

- Python 3.x
- OpenCV
- NumPy
- PyCaw
- Hands Tracking Module (hands_tracking.py)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/safacharfi/volume_controlleur.git
   cd volume_controlleur
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```sh
   pip install opencv-python numpy pycaw
   ```

4. Ensure you have the `hands_tracking.py` file in the same directory or install it if it’s available as a package.

## Usage

1. Run the script:

   ```sh
   python volume_controlleur.py
   ```

2. The camera feed will open, and you will see your hand landmarks. Move your hand and adjust the distance between your thumb and index finger to control the system volume.

3. Press `q` to exit the application.

## Code Explanation

- **`volume_controlleur.py`**: The main script for capturing video, detecting hand landmarks, and controlling the volume.
- **`HandsTrackingModule.py`**: Custom module for hand detection and landmark extraction.

### Volume Control Logic

- The volume is adjusted based on the distance between the thumb and index finger.
- The `np.interp` function maps this distance to the system volume range.

## Troubleshooting

- **Camera Issues**: Ensure your camera is properly connected and accessible.
- **Volume Control Not Working**: Check if you have the necessary permissions to control system volume.




