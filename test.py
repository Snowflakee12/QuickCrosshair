import sys, math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QComboBox,
    QLineEdit, QPushButton, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QStandardItemModel, QStandardItem, QIcon

projectiles = {
    "25mm Bushmaster HE": {"velocity": 1000, "gravity_modifier": 2},
    "30mm 2A72 HE": {"velocity": 900, "gravity_modifier": 2},
    "30mm 2A42 HE": {"velocity": 900, "gravity_modifier": 2},
    "DTB02 HE (ZBD04A)": {"velocity": 970, "gravity_modifier": 2},
    "DTB02 HE (ZBL08)": {"velocity": 950, "gravity_modifier": 2},
    "DTB02-105 HE": {"velocity": 1100, "gravity_modifier": 2},
    "GPD-30 (BMP2M)": {"velocity": 230, "gravity_modifier": 1},
    "ZU-23-2": {"velocity": 980, "gravity_modifier": 2},
    "MK19": {"velocity": 230, "gravity_modifier": 1},
    "Grenade launcher": {"velocity": 76, "gravity_modifier": 1},
    "OG-15V frag": {"velocity": 290, "gravity_modifier": 1.2},
    "2A70 frag": {"velocity": 355, "gravity_modifier": 2},
}

projectiles_by_category = {
    "Véhicule": [
        "25mm Bushmaster HE",
        "30mm 2A72 HE",
        "30mm 2A42 HE",
        "DTB02 HE (ZBD04A)",
        "DTB02 HE (ZBL08)",
        "GPD-30 (BMP2M)",
        "2A70 frag",
        "OG-15V frag",
        "DTB02-105 HE",
    ],
    "Arme": [
        "Grenade launcher",
    ],
    "Emplacement": [
        "ZU-23-2",
        "MK19",
    ],
}

class CrosshairWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.crosshair_size = 10
        self.offset = QPoint(7, 5)
        self.resize(self.crosshair_size * 2, self.crosshair_size * 2)
        self.show()

    def setOffset(self, dx, dy):
        self.offset = QPoint(int(dx), int(dy))
        self.moveToOffset()
        self.update()

    def moveToOffset(self):
        screen = QApplication.primaryScreen().geometry()
        center = screen.center()
        new_x = center.x() + self.offset.x() - self.crosshair_size
        new_y = center.y() + self.offset.y() - self.crosshair_size
        self.move(new_x, new_y)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)
        mid = self.rect().center()
        painter.drawLine(mid.x() - self.crosshair_size, mid.y(),
                         mid.x() + self.crosshair_size, mid.y())
        painter.drawLine(mid.x(), mid.y() - self.crosshair_size,
                         mid.x(), mid.y() + self.crosshair_size)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aimbot Assist for Explosiv")
        self.setWindowIcon(QIcon("icon.ico"))
        self.crosshairWindow = CrosshairWindow()

        centralWidget = QWidget()
        layout = QGridLayout()

        # Combobox et champs de saisie
        self.projectileCombo = QComboBox()
        self.populateCombo()
        self.projectileCombo.currentTextChanged.connect(self.changerProjectile)

        self.vitesseEdit = QLineEdit()
        self.graviteEdit = QLineEdit()
        self.distanceEdit = QLineEdit()
        self.diffHauteurEdit = QLineEdit()

        # Champ de zoom
        self.zoomEdit = QLineEdit()
        self.zoomEdit.setText("1")

        self.calculerBtn = QPushButton("Calculer le décalage")
        self.calculerBtn.clicked.connect(self.calculerDecalage)

        # Bouton pour activer/désactiver le crosshair
        self.toggleCrosshairBtn = QPushButton("Désactiver le crosshair")
        self.toggleCrosshairBtn.setCheckable(True)
        self.toggleCrosshairBtn.setChecked(True)  # Par défaut activé
        self.toggleCrosshairBtn.clicked.connect(self.toggleCrosshair)

        # Placement des widgets dans la grille
        layout.addWidget(QLabel("Projectile:"), 0, 0)
        layout.addWidget(self.projectileCombo, 0, 1)
        layout.addWidget(QLabel("Vitesse (m/s):"), 1, 0)
        layout.addWidget(self.vitesseEdit, 1, 1)
        layout.addWidget(QLabel("Gravité (m/s²):"), 2, 0)
        layout.addWidget(self.graviteEdit, 2, 1)
        layout.addWidget(QLabel("Distance (m):"), 3, 0)
        layout.addWidget(self.distanceEdit, 3, 1)
        layout.addWidget(QLabel("Diff. d'altitude (m):"), 4, 0)
        layout.addWidget(self.diffHauteurEdit, 4, 1)
        layout.addWidget(QLabel("Zoom:"), 5, 0)
        layout.addWidget(self.zoomEdit, 5, 1)
        layout.addWidget(self.calculerBtn, 6, 0, 1, 2)
        layout.addWidget(self.toggleCrosshairBtn, 7, 0, 1, 2)

        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.changerProjectile(self.projectileCombo.currentText())

    def populateCombo(self):
        model = QStandardItemModel()
        for category, items in projectiles_by_category.items():
            header = QStandardItem(category + ":")
            header.setFlags(Qt.NoItemFlags)
            model.appendRow(header)
            for item in items:
                projectile_item = QStandardItem("   " + item)
                model.appendRow(projectile_item)
        self.projectileCombo.setModel(model)
        for i in range(model.rowCount()):
            text = model.item(i).text().strip()
            if text in projectiles:
                self.projectileCombo.setCurrentIndex(i)
                break

    def changerProjectile(self, text):
        text = text.strip()
        if text.endswith(":"):
            return
        if text.startswith("   "):
            text = text.strip()
        if text not in projectiles:
            return
        projectile = projectiles[text]
        self.vitesseEdit.setText(str(projectile["velocity"]))
        gravite_base = 9.81
        self.graviteEdit.setText(str(projectile["gravity_modifier"] * gravite_base))

    def calculerDecalage(self):
        try:
            v = float(self.vitesseEdit.text())
            g = float(self.graviteEdit.text())
            d = float(self.distanceEdit.text())
            dy = float(self.diffHauteurEdit.text())
        except ValueError:
            return

        try:
            A = (g * d**2) / (2 * v**2)
            B = -d
            C = A + dy
            discriminant = B**2 - 4 * A * C
            if discriminant < 0:
                return
            u = (-B - math.sqrt(discriminant)) / (2 * A)
            theta = math.atan(u)
        except Exception as e:
            print("Erreur dans le calcul:", e)
            return

        try:
            zoom_factor = float(self.zoomEdit.text())
        except ValueError:
            zoom_factor = 1.0

        FOV_v = 90
        screen_height = QApplication.primaryScreen().geometry().height()
        pixels_par_deg = screen_height / FOV_v

        decalage_pixels = math.degrees(theta) * pixels_par_deg * zoom_factor
        self.crosshairWindow.setOffset(0, decalage_pixels)

    def toggleCrosshair(self, checked):
        if checked:
            self.crosshairWindow.show()
            self.toggleCrosshairBtn.setText("Désactiver le crosshair")
        else:
            self.crosshairWindow.hide()
            self.toggleCrosshairBtn.setText("Activer le crosshair")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
