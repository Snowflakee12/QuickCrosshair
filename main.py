import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QComboBox, QVBoxLayout,
    QDoubleSpinBox, QHBoxLayout, QPushButton, QSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor

vehicles = {
    "IFV": {
        "BMD-1M": {
            "zoom_levels": [3.0],
            "offset": {"x": 0, "y": -75},
            "projectiles": {
                "OG-15V frag": {"velocity": 290, "gravity_modifier": 1.2},
            },
        },
        "BMD-4M & BMP-3M": {
            "zoom_levels": [2.5],
            "offset": {"x": 0, "y": -0},
            "projectiles": {
                "DTB02-100 HE": {"velocity": 355, "gravity_modifier": 2},
                "3UOR6 HE": {"velocity": 900, "gravity_modifier": 1},
            },
        },
        "BMP-1": {
            "zoom_levels": [1.5],
            "offset": {"x": 0, "y": 0},  
            "projectiles": {
                "3UOR6 HE": {"velocity": 435, "gravity_modifier": 1.2},
            },
        },
        "BMP-2 & BMP-2M": {
            "zoom_levels": [1.5],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "3UOR6 HE": {"velocity": 900, "gravity_modifier": 2},
            },
        },
        "BTR-82A": {
            "zoom_levels": [2],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "3UOR6 HE": {"velocity": 900, "gravity_modifier": 2},
            },
        },
        "ZBL-08": {
            "zoom_levels": [2],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "DTB02-30 HEI-T": {"velocity": 950, "gravity_modifier": 2},
            },
        },
        "ZBD-04A": {
            "zoom_levels": [2.5],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "DTB02-100 HE": {"velocity": 355, "gravity_modifier": 2},
                "DTB02-30 HEI-T": {"velocity": 230, "gravity_modifier": 2},
            },
        },
        "LAV-6": {
            "zoom_levels": [1.5],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "MK210 HEI-T": {"velocity": 1000, "gravity_modifier": 2},
            },
        },
        "LAV-25": {
            "zoom_levels": [1],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "MK210 HEI-T": {"velocity": 1000, "gravity_modifier": 2},
            },
        },
        "M2A3 et M7A3": {
            "zoom_levels": [3],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "MK210 HEI-T": {"velocity": 1000, "gravity_modifier": 2},
            },
        },
        "Aslav-25": {
            "zoom_levels": [3],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "MK210 HEI-T": {"velocity": 1000, "gravity_modifier": 2},
            },
        },
    },
    "MBT & MGS": {
        "T72B3": {
            "zoom_levels": [4],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "OF26 Frag": {"velocity": 1100, "gravity_modifier": 2},
                "3OF82 Frag": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
        "M1A2 & M1A1": {
            "zoom_levels": [3],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "M830A1 HEAT": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
        "ZTZ99A": {
            "zoom_levels": [4],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "DTB12-125 Frag": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
        "T-62": {
            "zoom_levels": [3.5],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "OF-11 Frag": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
        "ZTD-05": {
            "zoom_levels": [7.5],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "DTB02-105 Frag": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
        "Sprut-SDM1": {
            "zoom_levels": [4],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "3OF82 Frag": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
        "M1128 MGS": {
            "zoom_levels": [3],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "M456A2 HEAT": {"velocity": 1100, "gravity_modifier": 2},
            },
        },
    },
    "APC": {
        "AAVP": {
            "zoom_levels": [1],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "MK19": {"velocity": 230, "gravity_modifier": 1},
            },
        },
        "BRDM-UB32": {
            "zoom_levels": [1],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "S-5": {"velocity": 300, "gravity_modifier": 1, "velocity_modifier": -50, "time": 2},
            },
        },
    },
    "Emplacement": {
        "ZU-23-2": {
            "zoom_levels": [1],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "ZU-23-2": {"velocity": 980, "gravity_modifier": 2},
            },
        },
        "MK19": {
            "zoom_levels": [1],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "MK19": {"velocity": 230, "gravity_modifier": 1},
            },
        },
        "ZIS3": {
            "zoom_levels": [3.7],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "ZIS-3 Frag": {"velocity": 700, "gravity_modifier": 2},
            },
        },
    },
    "INF": {
        "Grenade launcher": {
            "zoom_levels": [1.0],
            "offset": {"x": 0, "y": 0},
            "projectiles": {
                "Grenade launcher": {"velocity": 76, "gravity_modifier": 1},
            },
        },
    },
}

def calculate_screen_offset(v, g, d, dy, resolutionh, resolutionv, FOVh_degrees, aspect_ratio):
    inside_sqrt = v**4 - g * (g * d**2 + 2 * dy * v**2)
    if inside_sqrt < 0:
        return None, "Aucune solution balistique possible"
    angle_low = math.atan((v**2 - math.sqrt(inside_sqrt)) / (g * d))
    height_m = d * math.tan(angle_low)
    FOVh = math.radians(FOVh_degrees)
    FOVv = 2 * math.atan(math.tan(FOVh / 2) / aspect_ratio)
    virtual_height = 2 * d * math.tan(FOVv / 2)
    conversion = resolutionv / virtual_height
    decalage_pixels = height_m * conversion
    return decalage_pixels, math.degrees(angle_low)

class CrosshairWindow(QWidget):
    def __init__(self, offset_x, offset_y):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.crosshair_size = 10
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.resize(200, 200)
        self.move_to_center()
        self.show()

    def move_to_center(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        center_x = screen_geometry.width() // 2
        center_y = screen_geometry.height() // 2
        self.move(center_x - 100 + int(self.offset_x), center_y - 100 + int(self.offset_y))

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)
        center = self.rect().center()
        painter.drawLine(center.x() - self.crosshair_size, center.y(),
                         center.x() + self.crosshair_size, center.y())
        painter.drawLine(center.x(), center.y() - self.crosshair_size,
                         center.x(), center.y() + self.crosshair_size)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calcul balistique")
        self.crosshair = None

        self.categoryComboBox = QComboBox()
        self.vehicleComboBox = QComboBox()
        self.projectileComboBox = QComboBox()
        self.distanceInput = QDoubleSpinBox()
        self.heightInput = QDoubleSpinBox()
        self.zoomInput = QDoubleSpinBox()
        self.fovInput = QDoubleSpinBox()
        self.resolutionHInput = QSpinBox()
        self.resolutionVInput = QSpinBox()
        self.toggleCrosshairButton = QPushButton("Activer réticule")
        self.toggleCrosshairButton.setCheckable(True)
        self.resultLabel = QLabel()

        # Configuration des spin boxes
        self.distanceInput.setRange(0, 100000)
        self.distanceInput.setValue(1250)
        self.heightInput.setRange(-10000, 10000)
        self.heightInput.setValue(0)
        self.zoomInput.setRange(0.1, 1000)
        self.zoomInput.setDecimals(2)
        self.zoomInput.setValue(1)

        self.fovInput.setRange(10, 180)
        self.fovInput.setDecimals(1)
        self.fovInput.setValue(90)

        self.resolutionHInput.setRange(1, 10000)
        self.resolutionHInput.setValue(2560)
        self.resolutionVInput.setRange(1, 10000)
        self.resolutionVInput.setValue(1440)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QVBoxLayout(centralWidget)

        layout.addWidget(QLabel("Catégorie:"))
        layout.addWidget(self.categoryComboBox)
        layout.addWidget(QLabel("Véhicule:"))
        layout.addWidget(self.vehicleComboBox)
        layout.addWidget(QLabel("Projectile:"))
        layout.addWidget(self.projectileComboBox)

        distanceLayout = QHBoxLayout()
        distanceLayout.addWidget(QLabel("Distance (m):"))
        distanceLayout.addWidget(self.distanceInput)
        layout.addLayout(distanceLayout)

        heightLayout = QHBoxLayout()
        heightLayout.addWidget(QLabel("Différence de hauteur (m):"))
        heightLayout.addWidget(self.heightInput)
        layout.addLayout(heightLayout)

        zoomLayout = QHBoxLayout()
        zoomLayout.addWidget(QLabel("Zoom:"))
        zoomLayout.addWidget(self.zoomInput)
        layout.addLayout(zoomLayout)

        fovLayout = QHBoxLayout()
        fovLayout.addWidget(QLabel("FOV horizontal (°):"))
        fovLayout.addWidget(self.fovInput)
        layout.addLayout(fovLayout)

        resolutionLayout = QHBoxLayout()
        resolutionLayout.addWidget(QLabel("Résolution horizontale:"))
        resolutionLayout.addWidget(self.resolutionHInput)
        resolutionLayout.addWidget(QLabel("Résolution verticale:"))
        resolutionLayout.addWidget(self.resolutionVInput)
        layout.addLayout(resolutionLayout)

        layout.addWidget(self.toggleCrosshairButton)
        layout.addWidget(self.resultLabel)

        self.categoryComboBox.addItems(vehicles.keys())
        self.categoryComboBox.currentIndexChanged.connect(self.categoryChanged)
        self.vehicleComboBox.currentIndexChanged.connect(self.vehicleChanged)
        self.projectileComboBox.currentIndexChanged.connect(self.projectileChanged)
        self.distanceInput.valueChanged.connect(self.projectileChanged)
        self.heightInput.valueChanged.connect(self.projectileChanged)
        self.zoomInput.valueChanged.connect(self.projectileChanged)
        self.fovInput.valueChanged.connect(self.projectileChanged)
        self.resolutionHInput.valueChanged.connect(self.projectileChanged)
        self.resolutionVInput.valueChanged.connect(self.projectileChanged)
        self.toggleCrosshairButton.toggled.connect(self.toggleCrosshair)

        self.categoryChanged(0)

    def categoryChanged(self, index):
        cat = self.categoryComboBox.currentText()
        self.vehicleComboBox.clear()
        if cat:
            self.vehicleComboBox.addItems(vehicles[cat].keys())
            self.vehicleChanged(0)

    def vehicleChanged(self, index):
        cat = self.categoryComboBox.currentText()
        veh = self.vehicleComboBox.currentText()
        self.projectileComboBox.clear()
        if cat and veh:
            self.projectileComboBox.addItems(vehicles[cat][veh]["projectiles"].keys())
            zoom_levels = vehicles[cat][veh]["zoom_levels"]
            if zoom_levels:
                self.zoomInput.setValue(zoom_levels[0])
            self.projectileChanged(0)

    def projectileChanged(self, index):
        cat = self.categoryComboBox.currentText()
        veh = self.vehicleComboBox.currentText()
        proj = self.projectileComboBox.currentText()
        if not (cat and veh and proj):
            return

        veh_data = vehicles[cat][veh]
        data = veh_data["projectiles"][proj]
        base_v = data["velocity"]
        if "velocity_modifier" in data:
            base_v += data["velocity_modifier"]
        gravity_modifier = data["gravity_modifier"]

        offset = veh_data.get("offset", {"x": 0, "y": 0})
        offset_x = offset.get("x", 0)
        offset_y = offset.get("y", 0)

        d = self.distanceInput.value()
        dy = self.heightInput.value()
        zoom_factor = self.zoomInput.value()

        # Récupération des paramètres personnalisables depuis l'interface
        resolutionh = self.resolutionHInput.value()
        resolutionv = self.resolutionVInput.value()
        FOVh_degrees = self.fovInput.value()
        aspect_ratio = resolutionh / resolutionv

        g = 9.78 * gravity_modifier
        v = base_v

        decalage_pixels, angle_degrees = calculate_screen_offset(
            v, g, d, dy, resolutionh, resolutionv, FOVh_degrees, aspect_ratio
        )

        if decalage_pixels is None:
            result_text = angle_degrees
        else:
            # Appliquer le zoom après calcul
            decalage_pixels *= zoom_factor
            flight_time = d / (v * math.cos(math.radians(angle_degrees)))
            result_text = (f"Angle de tir: {angle_degrees:.2f}°\n"
                           f"Temps de vol: {flight_time:.2f} s\n"
                           f"Décalage vertical en pixels: {decalage_pixels:.2f}")

            if self.toggleCrosshairButton.isChecked():
                if self.crosshair:
                    self.crosshair.close()
                self.crosshair = CrosshairWindow(offset_x, decalage_pixels + offset_y)
            else:
                if self.crosshair:
                    self.crosshair.close()
                    self.crosshair = None

        self.resultLabel.setText(result_text)

    def toggleCrosshair(self, checked):
        if checked:
            self.toggleCrosshairButton.setText("Désactiver réticule")
            self.projectileChanged(self.projectileComboBox.currentIndex())
        else:
            self.toggleCrosshairButton.setText("Activer réticule")
            if self.crosshair:
                self.crosshair.close()
                self.crosshair = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
