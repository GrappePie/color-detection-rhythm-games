
# Color Detection Script for Rhythm Games

This Python script uses PySide6, OpenCV, and pyautogui to detect colors on the screen and perform actions in rhythm games like FNF (Friday Night Funkin). The script creates a transparent window with draggable labels for each color to be detected. When the specified color is detected within the label's region, the script triggers a corresponding key press.

## Features

- **Real-time Color Detection**: Detects specific colors on the screen in real-time and triggers key presses.
- **Draggable Labels**: Allows you to move the detection regions to any position on the screen.
- **Hotkeys**: Update color ranges and move labels using keyboard shortcuts.
- **Toggle Activation**: Easily enable or disable color detection with a button click.

## Requirements

- Python 3.x
- PySide6
- OpenCV
- pyautogui
- keyboard

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the script:
    ```bash
    python script.py
    ```

2. A transparent window with draggable labels will appear. You can move the labels to the desired position on the screen.

3. Use the following hotkeys to update the color ranges and move the labels:
    - `1`, `2`, `3`, `4`: Update the color range for the corresponding label to the color under the mouse cursor.
    - `Shift+1`, `Shift+2`, `Shift+3`, `Shift+4`: Move the corresponding label to the current mouse cursor position.

4. Click the "Toggle Activation" button to enable or disable color detection.

5. Press `Esc` to close the application.

## Customization

You can customize the colors and key commands by modifying the `color_infos` dictionary in the `TransparentWindow` class.

```python
color_infos = {
    "purple": ("#C24B99", ((150, 116, 154), (170, 196, 234)), 'left'),
    "blue": ("#00FFFF", ((80, 215, 215), (100, 255, 255)), 'down'),
    "green": ("#12FA05", ((48, 210, 210), (68, 255, 255)), 'up'),
    "red": ("#F9393F", ((169, 157, 209), (179, 237, 255)), 'right'),
}
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Feel free to submit issues and pull requests to improve the script.

## Acknowledgments

- [PySide6](https://pypi.org/project/PySide6/)
- [OpenCV](https://opencv.org/)
- [pyautogui](https://pypi.org/project/pyautogui/)
- [keyboard](https://pypi.org/project/keyboard/)

## Contact

For any questions or suggestions, please contact [grappepie@gmail.com](mailto:grappepie@gmail.com).
