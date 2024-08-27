import sys
import time
from PyQt5.QtCore import Qt, QTimer, QUrl, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QFont, QKeySequence, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QProgressBar, QLabel, QWidget, 
    QPushButton, QLineEdit, QFileDialog, QListWidget, QGraphicsScene, 
    QGraphicsView, QGraphicsPixmapItem, QShortcut, QInputDialog, QMessageBox
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class LoadingScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #282c34; color: white;")

        layout = QVBoxLayout()
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setStyleSheet("QProgressBar::chunk {background-color: #61afef;}")

        self.labelName = QLabel("simplyProjector")
        self.labelName.setFont(QFont('Arial', 16))
        self.labelName.setAlignment(Qt.AlignCenter)

        self.labelCreator = QLabel("simplyYan Solutions (Wesley Yan Soares Brehmer)")
        self.labelCreator.setAlignment(Qt.AlignCenter)

        self.labelLicense = QLabel("License: CC0-1.0")
        self.labelLicense.setAlignment(Qt.AlignCenter)

        self.labelPercentage = QLabel("0%")
        self.labelPercentage.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.labelName)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.labelPercentage)
        layout.addWidget(self.labelCreator)
        layout.addWidget(self.labelLicense)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start(50)

        self.progress = 0

    def updateProgressBar(self):
        self.progress += 1
        self.progressBar.setValue(self.progress)
        self.labelPercentage.setText(f"{self.progress}%")
        if self.progress >= 100:
            self.timer.stop()
            self.mainWindow = MainWindow()
            self.mainWindow.show()
            self.close()


class ProjectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projection Window")
        self.setGeometry(100, 100, 800, 600)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

    def show_image(self, image_path):
        pixmap = QPixmap(image_path)
        item = QGraphicsPixmapItem(pixmap)
        self.scene.clear()
        self.scene.addItem(item)
        self.showFullScreen()


class FadeOutMediaPlayer(QMediaPlayer):
    def __init__(self):
        super().__init__()
        self.volume_animation = QPropertyAnimation(self, b"volume")
        self.volume_animation.setDuration(2000)
        self.volume_animation.setStartValue(100)
        self.volume_animation.setEndValue(0)
        self.volume_animation.finished.connect(self.stop)

    def fade_out(self):
        self.volume_animation.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("simplyProjector")
        self.setFixedSize(600, 500)
        self.setStyleSheet("background-color: #282c34; color: white;")
        
        layout = QVBoxLayout()
        
        self.shortcutNameInput = QLineEdit(self)
        self.shortcutNameInput.setPlaceholderText("Enter shortcut name (optional)")
        self.shortcutNameInput.setStyleSheet("background-color: #21252b; color: #61afef;")
        layout.addWidget(self.shortcutNameInput)
        
        self.shortcutInput = QLineEdit(self)
        self.shortcutInput.setPlaceholderText("Press the shortcut (e.g., CTRL+SHIFT+P)")
        self.shortcutInput.setStyleSheet("background-color: #21252b; color: #61afef;")
        layout.addWidget(self.shortcutInput)
        
        self.imageButton = QPushButton("Load Image", self)
        self.imageButton.clicked.connect(self.loadImage)
        layout.addWidget(self.imageButton)
        
        self.audioButton = QPushButton("Load Audio", self)
        self.audioButton.clicked.connect(self.loadAudio)
        layout.addWidget(self.audioButton)
        
        self.shortcutList = QListWidget(self)
        layout.addWidget(self.shortcutList)

        saveButton = QPushButton("Save Shortcut", self)
        saveButton.clicked.connect(self.saveShortcut)
        layout.addWidget(saveButton)

        savePresetButton = QPushButton("Save Preset", self)
        savePresetButton.clicked.connect(self.savePreset)
        layout.addWidget(savePresetButton)

        loadPresetButton = QPushButton("Load Preset", self)
        loadPresetButton.clicked.connect(self.loadPreset)
        layout.addWidget(loadPresetButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.shortcuts = {}
        self.presets = {}
        self.projectionWindow = ProjectionWindow()
        self.audioPlayers = []

        # Global shortcut to stop all sounds with fade out
        self.stopShortcut = QShortcut(QKeySequence("CTRL+SHIFT+DEL"), self)
        self.stopShortcut.activated.connect(self.stopAllSounds)

    def loadImage(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Images (*.png *.jpg *.bmp)")
        if filePath:
            self.currentImage = filePath

    def loadAudio(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Audio", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if filePath:
            self.currentAudio = filePath

    def saveShortcut(self):
        shortcutText = self.shortcutInput.text()
        shortcutName = self.shortcutNameInput.text().strip() or "Unnamed"
        if shortcutText:
            shortcut = QShortcut(QKeySequence(shortcutText), self)
            action = self.createShortcutAction()
            shortcut.activated.connect(action)
            self.shortcutList.addItem(f"{shortcutName} -> {shortcutText}")
            self.shortcuts[shortcutText] = (shortcutName, action)

    def createShortcutAction(self):
        image_path = getattr(self, 'currentImage', None)
        audio_path = getattr(self, 'currentAudio', None)
        
        def action():
            if image_path:
                self.projectionWindow.show_image(image_path)
            if audio_path:
                audioPlayer = FadeOutMediaPlayer()
                audioPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(audio_path)))
                audioPlayer.play()
                self.audioPlayers.append(audioPlayer)
        
        return action

    def savePreset(self):
        presetName, ok = QInputDialog.getText(self, "Save Preset", "Enter preset name:")
        if ok and presetName:
            self.presets[presetName] = self.shortcuts.copy()
            QMessageBox.information(self, "Preset Saved", f"Preset '{presetName}' has been saved.")

    def loadPreset(self):
        presetName, ok = QInputDialog.getItem(self, "Load Preset", "Select preset:", list(self.presets.keys()), 0, False)
        if ok and presetName:
            self.shortcuts = self.presets[presetName].copy()
            self.shortcutList.clear()
            for shortcutText, (shortcutName, action) in self.shortcuts.items():
                self.shortcutList.addItem(f"{shortcutName} -> {shortcutText}")

    def stopAllSounds(self):
        for player in self.audioPlayers:
            player.fade_out()
        self.audioPlayers.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loadingScreen = LoadingScreen()
    loadingScreen.show()
    sys.exit(app.exec_())
