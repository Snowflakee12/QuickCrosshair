import sys, math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QComboBox,
    QLineEdit, QPushButton, QGridLayout
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor

projectiles = {
    "25mm Bushmaster HE": {"velocity": 1000, "gravity_modifier": 2},
    "30mm 2A72 HE": {"velocity": 900, "gravity_modifier": 2},
    "30mm 2A42 HE": {"velocity": 900, "gravity_modifier": 2},
    "DTB02 HE (ZBD04A)": {"velocity": 970, "gravity_modifier": 2},
    "DTB02 HE (ZBL08)": {"velocity": 950, "gravity_modifier": 2},
    "GPD-30": {"velocity": 230, "gravity_modifier": 1},
    "ZU-23-2": {"velocity": 980, "gravity_modifier": 2},
    "MK19": {"velocity": 230, "gravity_modifier": 1},
}

class CrosshairWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.crosshair_size = 10
        self.offset = QPoint(7,5)
        self.resize(self.crosshair_size*2, self.crosshair_size*2)
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
        self.setWindowTitle("Calcul de visée pour Squad")
        self.crosshairWindow = CrosshairWindow()
        centralWidget = QWidget()
        layout = QGridLayout()
        self.projectileCombo = QComboBox()
        self.projectileCombo.addItems(projectiles.keys())
        self.projectileCombo.currentTextChanged.connect(self.changerProjectile)
        self.vitesseEdit = QLineEdit()
        self.graviteEdit = QLineEdit()
        self.distanceEdit = QLineEdit()
        self.diffHauteurEdit = QLineEdit()
        self.calculerBtn = QPushButton("Calculer le décalage")
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
        layout.addWidget(self.calculerBtn, 5, 0, 1, 2)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        self.calculerBtn.clicked.connect(self.calculerDecalage)
        self.changerProjectile(self.projectileCombo.currentText())

    def changerProjectile(self, nomProjectile):
        projectile = projectiles[nomProjectile]
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
            discriminant = B**2 - 4*A*C
            if discriminant < 0:
                return
            u = (-B - math.sqrt(discriminant)) / (2*A)
            theta = math.atan(u)
        except Exception as e:
            print("Erreur dans le calcul:", e)
            return
        FOV_v = 90
        screen_height = QApplication.primaryScreen().geometry().height()
        pixels_par_deg = screen_height / FOV_v
        decalage_pixels = math.degrees(theta) * pixels_par_deg
        self.crosshairWindow.setOffset(0, decalage_pixels)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
