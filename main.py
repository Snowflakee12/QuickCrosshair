import sys, math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QStandardItemModel, QStandardItem, QIcon


vehicles = {
    "IFV": {
        "BMD-1M": {
            "zoom_levels": [3.0],
            "projectiles": {
                "OG-15V frag": {"velocity": 290, "gravity_modifier": 1.2},
            },
        },
        "BMD-4M & BMP-3M": {
            "zoom_levels": [2.5],
            "projectiles": {
                "DTB02-100 HE": {"velocity": 355, "gravity_modifier": 2},
                "3UOR6 HE": {"velocity": 900, "gravity_modifier": 2},
            },
        },
        "BMP-1": {
            "zoom_levels": [1.5],
            "projectiles": {
                "3UOR6 HE": {"velocity": 435, "gravity_modifier": 1.2},
            },
        },

        "BMP-2 & BMP-2M": {
            "zoom_levels": [1.5],
            "projectiles": {
                "3UOR6 HE": {"velocity": 900, "gravity_modifier": 2},
            },
        },
        "BTR-82A": {
            "zoom_levels": [2],
            "projectiles": {
                "3UOR6 HE": {"velocity": 900, "gravity_modifier": 2},
            },
        },
        "ZBL-08": {
            "zoom_levels": [2],
            "projectiles": {
                "DTB02-30 HEI-T": {"velocity": 950, "gravity_modifier": 2},
            },
        },         
        "ZBD-04A": {
            "zoom_levels": [2.5],
            "projectiles": {
                "DTB02-100 HE": {"velocity": 355, "gravity_modifier": 2},
                "DTB02-30 HEI-T": {"velocity": 230, "gravity_modifier": 2},
            },
        },
        "LAV-6": {
            "zoom_levels": [1.5],
            "projectiles": {
                "MK210 HEI-T": {"velocity": 1000, "gravity_modifier": 2},
            },
        },
        "LAV-25": {
            "zoom_levels": [1],
            "projectiles": {
                "MK210 HEI-T": {"velocity": 1000, "gravity_modifier": 2},
            },
        },
        "M2A3 et M7A3": {
            "zoom_levels": [3],
            "projectiles": {
                "MK210 HEI-T": {"velocity": 1000, "gravity_modifier": 2},
            },
        },
        "Aslav-25": {
            "zoom_levels": [3],
            "projectiles": {
                "MK210 HEI-T": {"velocity": 1000, "gravity_modifier": 2},
            },
        },
    },
    "MBT & MGS": {
        "T72B3": {
            "zoom_levels": [4],
            "projectiles": {
                "OF26 Frag": {"velocity": 1100, "gravity_modifier": 2},
                "3OF82 Frag": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
        "M1A2 & M1A1": {
            "zoom_levels": [3],
            "projectiles": {
                "M830A1 HEAT": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
        "ZTZ99A": {
            "zoom_levels": [4],
            "projectiles": {
                "DTB12-125 Frag": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
        "T-62": {
            "zoom_levels": [3.5],
            "projectiles": {
                "OF-11 Frag": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
        "ZTD-05": {
            "zoom_levels": [3.5],
            "projectiles": {
                "DTB02-105 Frag": {"velocity": 1100, "gravity_modifier": 2},
            },
        },        
        "Sprut-SDM1": {
            "zoom_levels": [4],
            "projectiles": {
                "3OF82 Frag": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
        "M1128 MGS": {
            "zoom_levels": [3],
            "projectiles": {
                "M456A2 HEAT": {"velocity": 1100, "gravity_modifier": 2},
            },
        },          
    },
    
    "APC": {
        "AAVP": {
            "zoom_levels": [1],
            "projectiles": {
                "MK19": {"velocity": 230, "gravity_modifier": 1},
            },
        },
        "BRDM-UB32": {
            "zoom_levels": [1],
            "projectiles": {
                "S-5": {"velocity": 300, "gravity_modifier": 1,"velocity_modifier":-50,"time":2},
            },
        },        
    },
    "Emplacement": {
        "ZU-23-2": {
            "zoom_levels": [1],
            "projectiles": {
                "ZU-23-2": {"velocity": 980, "gravity_modifier": 2},
            },
        },
        "MK19": {
            "zoom_levels": [1],
            "projectiles": {
                "MK19": {"velocity": 230, "gravity_modifier": 1},
            },
        },
        "ZIS3": {
            "zoom_levels": [3.7],
            "projectiles": {
                "ZIS-3 Frag": {"velocity": 700, "gravity_modifier": 2},
            },
        },        
    },
    "INF": {
        "Grenade launcher": {
            "zoom_levels": [1.0],
            "projectiles": {
                "Grenade launcher": {"velocity": 76, "gravity_modifier": 1},
            },
        },
    },
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
        painter.drawLine(mid.x() - self.crosshair_size, mid.y(), mid.x() + self.crosshair_size, mid.y())
        painter.drawLine(mid.x(), mid.y() - self.crosshair_size, mid.x(), mid.y() + self.crosshair_size)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aimbot Assist for Explosiv")
        self.setWindowIcon(QIcon("icon.ico"))
        self.crosshairWindow = CrosshairWindow()

        centralWidget = QWidget()
        layout = QGridLayout()

        self.vehicleCombo = QComboBox()
        self.projectileCombo = QComboBox()
        self.zoomEdit = QLineEdit()

        self.populateVehicleCombo()
        self.vehicleCombo.currentTextChanged.connect(self.changerVehicule)

        self.vitesseEdit = QLineEdit()
        self.graviteEdit = QLineEdit()
        self.distanceEdit = QLineEdit()
        self.diffHauteurEdit = QLineEdit()

        self.calculerBtn = QPushButton("Calculer le d\u00e9calage")
        self.calculerBtn.clicked.connect(self.calculerDecalage)

        self.toggleCrosshairBtn = QPushButton("D\u00e9sactiver le crosshair")
        self.toggleCrosshairBtn.setCheckable(True)
        self.toggleCrosshairBtn.setChecked(True)
        self.toggleCrosshairBtn.clicked.connect(self.toggleCrosshair)

        layout.addWidget(QLabel("Type de v\u00e9hicule:"), 0, 0)
        layout.addWidget(self.vehicleCombo, 0, 1)
        layout.addWidget(QLabel("Projectile:"), 1, 0)
        layout.addWidget(self.projectileCombo, 1, 1)
        layout.addWidget(QLabel("Vitesse (m/s):"), 2, 0)
        layout.addWidget(self.vitesseEdit, 2, 1)
        layout.addWidget(QLabel("Gravit\u00e9 (m/s\u00b2):"), 3, 0)
        layout.addWidget(self.graviteEdit, 3, 1)
        layout.addWidget(QLabel("Distance (m):"), 4, 0)
        layout.addWidget(self.distanceEdit, 4, 1)
        layout.addWidget(QLabel("Diff. d'altitude (m):"), 5, 0)
        layout.addWidget(self.diffHauteurEdit, 5, 1)
        layout.addWidget(QLabel("Zoom:"), 6, 0)
        layout.addWidget(self.zoomEdit, 6, 1)
        layout.addWidget(self.calculerBtn, 7, 0, 1, 2)
        layout.addWidget(self.toggleCrosshairBtn, 8, 0, 1, 2)

        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        self.changerVehicule(self.vehicleCombo.currentText())

    def populateVehicleCombo(self):
        model = QStandardItemModel()
        for category, vehicle_data in vehicles.items():
            header = QStandardItem(category + ":")
            header.setFlags(Qt.NoItemFlags)
            model.appendRow(header)
            for vehicle in vehicle_data:
                vehicle_item = QStandardItem("   " + vehicle)
                model.appendRow(vehicle_item)
        self.vehicleCombo.setModel(model)

    def changerVehicule(self, text):
        text = text.strip()
        if text.endswith(":"):
            return
        if text.startswith("   "):
            text = text.strip()
        for category, vehicle_data in vehicles.items():
            if text in vehicle_data:
                details = vehicle_data[text]
                self.zoomEdit.setText(", ".join(map(str, details.get("zoom_levels", []))))
                self.projectileCombo.clear()
                if details.get("projectiles"):
                    self.projectileCombo.addItems(details["projectiles"])
                    self.projectileCombo.currentTextChanged.connect(self.changerProjectile)
                    if self.projectileCombo.count() > 0:
                        self.changerProjectile(self.projectileCombo.itemText(0))
                else:
                    QMessageBox.warning(self, "Erreur", "Aucun projectile disponible pour ce v\u00e9hicule.")
                break

    def changerProjectile(self, text):
        text = text.strip()
        if not text:
            return
        current_vehicle = self.vehicleCombo.currentText().strip()
        for category, vehicle_data in vehicles.items():
            for vehicle, details in vehicle_data.items():
                if current_vehicle == vehicle:
                    projectile_data = details["projectiles"].get(text)
                    if projectile_data:
                        self.vitesseEdit.setText(str(projectile_data["velocity"]))
                        gravite_base = 9.78
                        self.graviteEdit.setText(str(projectile_data["gravity_modifier"] * gravite_base))
                    return

    def calculerDecalage(self):
        try:
            v = float(self.vitesseEdit.text())
            g = float(self.graviteEdit.text())
            d = float(self.distanceEdit.text())
            dy = float(self.diffHauteurEdit.text())
            if v <= 0 or d <= 0:
                raise ValueError("Les valeurs de vitesse et de distance doivent \u00eatre positives.")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des valeurs valides et positives.")
            return

        try:
            A = (g * d**2) / (2 * v**2)
            B = -d
            C = A + dy
            discriminant = B**2 - 4 * A * C
            if discriminant < 0:
                QMessageBox.warning(self, "Erreur", "Le calcul du d\u00e9calage est impossible.")
                return
            if A == 0:
                QMessageBox.warning(self, "Erreur", "Le calcul est impossible car A est nul.")
                return
            u = (-B - math.sqrt(discriminant)) / (2 * A)
            theta = math.atan(u)
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur dans le calcul : {e}")
            return

        try:
            zoom_factor = float(self.zoomEdit.text())
            if zoom_factor <= 0:
                zoom_factor = 1.0
        except ValueError:
            zoom_factor = 1.0

        FOV_v = 90 / zoom_factor
        screen_height = QApplication.primaryScreen().geometry().height()
        pixels_par_deg = screen_height / FOV_v
        decalage_pixels = math.degrees(theta) * pixels_par_deg
        self.crosshairWindow.setOffset(0, decalage_pixels)

    def toggleCrosshair(self, checked):
        if checked:
            self.crosshairWindow.show()
            self.toggleCrosshairBtn.setText("D\u00e9sactiver le crosshair")
        else:
            self.crosshairWindow.hide()
            self.toggleCrosshairBtn.setText("Activer le crosshair")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
