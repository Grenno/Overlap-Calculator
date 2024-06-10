import sys
import matplotlib.pyplot as plt
from math import acos, sqrt, pi
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

def pattern_overlap(index, radius):
    if index > 2 * radius:
        raise ValueError('No overlap present in current state! Please reduce path index distance or increase fan pattern radius.')
    
    # Calculate the area of the intersection (lens area)
    lens_area = 2 * (radius ** 2 * acos(index / (2 * radius)) - index / 2 * sqrt(radius ** 2 - (index / 2) ** 2))
    
    # Calculate the area of one circle
    circle_area = pi * radius ** 2

    # Calculate the percentage of overlap
    overlap_percentage = (lens_area / circle_area) * 100

    # Calculating lens diameter
    lens_diameter = (radius + radius) - index
    
    # Plotting
    fig, ax = plt.subplots()

    # Plot the concentric circles for the alpha fan pattern
    for r in range(1, int(radius) + 1):
        circ_inner1 = plt.Circle(
            (-index / 2, 0), 
            r, 
            color='k', 
            alpha=0.3, 
            fill=False
        )

        ax.add_artist(circ_inner1)

    # Plot the main circle for the alpha fan pattern
    circ1 = plt.Circle(
        (-index / 2, 0), 
        radius, 
        edgecolor='k', 
        facecolor='#ADEBF6', 
        alpha=0.4, 
        label='Fan Pattern α'
        )

    ax.add_artist(circ1)
    
    # Plot the concentric circles for beta fan pattern
    for r in range(1, int(radius) + 1):
        circ_inner2 = plt.Circle(
            (index / 2, 0), 
            r, 
            color='k', 
            alpha=0.3, 
            fill=False
            )
        
        ax.add_artist(circ_inner2)

    # Plot the main circle for the beta fan pattern
    circ2 = plt.Circle(
        (index / 2, 0), 
        radius, 
        edgecolor='k', 
        facecolor='#ADEBF6', 
        alpha=0.4, 
        label='Fan Pattern β'
        )

    ax.add_artist(circ2)

    # Plotting the lens diameter       
    ax.annotate(
        f'{lens_diameter:.2f}', 
        (0, 0), 
        textcoords="offset points", 
        xytext=(0, 10), 
        ha='center', 
        color='k'
        )

     # Add arrow with text for lens diameter
    ax.annotate(
        '', 
        xy=(lens_diameter / 2, 0), 
        xytext=(-lens_diameter / 2, 0), 
        arrowprops=dict(arrowstyle='<->', color='k')
        )

    # Plotting the radii
    
    # Annotations
    ax.annotate(
        f'Overlap: {overlap_percentage:.2f}%',
        (0, -radius * 1.75), 
        textcoords="offset points", 
        xytext=(0, 12), 
        ha='center', 
        color='r',
        bbox=dict(boxstyle="square, pad=0.3", edgecolor='k', facecolor='w', linewidth=0.5)
        )

    ax.annotate(
        f'Lens area: {lens_area:.2f} sq in',
        (0, -radius * 1.75), 
        textcoords="offset points", 
        xytext=(0, -8), 
        ha='center', 
        color='r',
        bbox=dict(boxstyle="square, pad=0.3", edgecolor='k', facecolor='w', linewidth=0.5)
        )

    ax.set_aspect('equal')
    ax.set_xlim(-2 * radius, 2 * radius)
    ax.set_ylim(-2 * radius, 2 * radius)
    plt.grid(True)
    plt.legend()
    plt.show()

# Prompting for the distance between the centers (index) and the radius of the circles.
class CircleInputDialog(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Fan Pattern Overlap Calculator')
        
        layout = QVBoxLayout()
        
        # Distance between centers
        self.index_label = QLabel('Path Index:')
        self.index_input = QLineEdit(self)
        layout.addWidget(self.index_label)
        layout.addWidget(self.index_input)
        
        # Radius of fan pattern
        self.radius_label = QLabel('Pattern Radius:')
        self.radius_input = QLineEdit(self)
        layout.addWidget(self.radius_label)
        layout.addWidget(self.radius_input)
        
        # Submit button
        self.submit_button = QPushButton('Run', self)
        self.submit_button.clicked.connect(self.onSubmit)
        layout.addWidget(self.submit_button)
        
        self.setLayout(layout)
        
    def onSubmit(self):
        try:
            index = float(self.index_input.text())
            radius = float(self.radius_input.text()) 
            self.close()
            pattern_overlap(index, radius)
        except ValueError as e:
            QMessageBox.warning(self, 'Error', str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CircleInputDialog()
    ex.show()
    sys.exit(app.exec_())
