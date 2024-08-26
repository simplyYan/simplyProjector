# simplyProjector

**simplyProjector** is a lightweight and modern tool designed to enhance your RPG gaming experience by allowing you to control what is projected onto a secondary display. With simplyProjector, you can assign custom keyboard shortcuts to display images or play audio files, making your gaming sessions more immersive and streamlined.

## Features

- **Custom Keyboard Shortcuts**: Assign shortcuts using combinations like `CTRL + SHIFT + <Key>` to avoid conflicts with other applications.
- **Image Projection**: Display images on a secondary screen with ease.
- **Audio Playback**: Play sound effects or background music during your sessions.
- **Modern UI**: Dark and sleek user interface for easy navigation.
- **Loading Screen**: An elegant loading screen to enhance user experience upon startup.

## How to Use

1. **Launch simplyProjector**: After the application starts, you’ll be greeted with a loading screen. Once loaded, the main interface will appear.
2. **Assign Shortcuts**:
   - Enter the desired keyboard shortcut in the input field (e.g., `CTRL+SHIFT+P`).
   - Load the image or audio file you wish to associate with this shortcut.
   - Click "Save Shortcut" to save the configuration.
3. **Projection and Playback**:
   - Press the assigned keyboard shortcut to display the image on the secondary screen and/or play the associated audio file.

## Installation

### For Windows (via Pre-compiled Executable)

1. **Download the ZIP file**:
   - [Mediafire](https://www.mediafire.com/file/8ie7016hec76zzd/simplyProjector.zip/file)
   - [Google Drive](https://drive.google.com/file/d/10gpyWSM1i9smW1zm0vjCYdk5cKxybtuz/view?usp=sharing)
2. **Extract the ZIP**:
   - The ZIP file is password protected. Use the password: `simplyYan`.
3. **Run the Executable**:
   - Navigate to the extracted folder and double-click the `simplyProjector.exe` to start the application.

### For Linux and macOS (via Python)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/simplyProjector.git
   cd simplyProjector
   ```
2. **Install Dependencies**:
   - Make sure you have Python 3.x installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   python simplyProjector.py
   ```

### For Linux and macOS (via PyInstaller)

1. **Clone the Repository** and **Install Dependencies** (as mentioned above).
2. **Compile the Application**:
   ```bash
   pyinstaller --onefile simplyProjector.py
   ```
3. **Run the Executable**:
   - After compilation, the executable will be found in the `dist/` directory.

## Contributing

We welcome contributions from the community! If you want to contribute:

1. **Open an Issue**: If you find a bug or have a feature request, please open an issue in the repository.
2. **Submit a Pull Request**: If you'd like to make changes or add new features, fork the repository, make your changes, and submit a pull request for review.

## License

This project is licensed under the **CC0-1.0** License. You are free to use, modify, and distribute the software without any restrictions.
