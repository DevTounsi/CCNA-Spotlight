import sys
import os
import json
import ctypes

# Configuration Windows pour permettre l'épinglage dans la barre des tâches
try:
    myappid = 'ccna.examen.search.spotlight.v1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

def get_resource_path(rel_path):
    """Résout le chemin que ce soit en script Python brut ou packagé dans un .exe."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, rel_path)

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QLabel, QScrollArea, QFrame, QPushButton, QSlider, QDialog
)
from PyQt6.QtCore import Qt, QTimer, QEvent
from PyQt6.QtGui import QIcon, QPixmap, QKeySequence, QShortcut

# Import our search engine
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scripts.search_engine import CCNAEngine


class SearchLineEdit(QLineEdit):
    """Barre de recherche qui sélectionne tout le texte dès qu'on y revient."""
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        was_focused = self.hasFocus()
        super().mousePressEvent(event)
        if not was_focused:
            self.selectAll()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        QTimer.singleShot(0, self.selectAll)


class ImageDialog(QDialog):
    """Dialogue modal discret pour afficher un schéma si demandé."""
    def __init__(self, image_path, title="Schéma CCNA", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #1e1e24; color: #ffffff;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        lbl = QLabel()
        pix = QPixmap(image_path)
        if not pix.isNull():
            scaled_pix = pix.scaled(600, 450, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            lbl.setPixmap(scaled_pix)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            lbl.setText("Image non disponible")
            
        layout.addWidget(lbl)
        
        btn_close = QPushButton("Fermer")
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #3f3f46;
                color: #e4e4e7;
                border-radius: 4px;
                padding: 6px;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #52525b; }
        """)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)


class ResultCard(QFrame):
    """Carte de résultat ultra-compacte et épurée pour le menu déroulant."""
    def __init__(self, item, base_dir, parent=None):
        super().__init__(parent)
        self.item = item
        self.base_dir = base_dir
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            ResultCard {
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 6px;
                padding: 5px;
                margin-bottom: 3px;
            }
            ResultCard:hover {
                border: 1px solid #3f3f46;
                background-color: #1a1a1e;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(4)
        
        # En-tête : Badge question & boutons
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        badge = QLabel(f"Q{self.item['original_number']}")
        badge.setStyleSheet("""
            background-color: #27272a;
            color: #a1a1aa;
            border-radius: 3px;
            padding: 1px 4px;
            font-size: 9px;
            font-weight: bold;
        """)
        header_layout.addWidget(badge)
        
        if self.item.get('has_image') and self.item.get('image_file'):
            btn_img = QPushButton("🖼️ Schéma")
            btn_img.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_img.setStyleSheet("""
                QPushButton {
                    background-color: #1e293b;
                    color: #38bdf8;
                    border: 1px solid #0284c7;
                    border-radius: 3px;
                    padding: 1px 4px;
                    font-size: 9px;
                }
                QPushButton:hover { background-color: #0369a1; color: #ffffff; }
            """)
            btn_img.clicked.connect(self.show_image)
            header_layout.addWidget(btn_img)
            
        header_layout.addStretch()
        
        self.btn_copy = QPushButton("Copier")
        self.btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy.setStyleSheet("""
            QPushButton {
                background-color: #27272a;
                color: #e4e4e7;
                border-radius: 3px;
                padding: 2px 6px;
                font-size: 9px;
            }
            QPushButton:hover { background-color: #3f3f46; color: #10b981; }
        """)
        self.btn_copy.clicked.connect(self.copy_answer)
        header_layout.addWidget(self.btn_copy)
        
        layout.addLayout(header_layout)
        
        # Énoncé de la question (compact)
        q_label = QLabel(self.item['question'])
        q_label.setWordWrap(True)
        q_label.setStyleSheet("color: #d4d4d8; font-size: 10px; line-height: 1.2;")
        layout.addWidget(q_label)
        
        # Réponse(s) correcte(s) bien visibles en vert
        ans_layout = QVBoxLayout()
        ans_layout.setSpacing(2)
        for ans in self.item.get('correct_answers', []):
            a_lbl = QLabel(f"✔  {ans}")
            a_lbl.setWordWrap(True)
            a_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            a_lbl.setStyleSheet("""
                color: #34d399;
                font-size: 10px;
                font-weight: 600;
                background-color: #064e3b;
                border-radius: 3px;
                padding: 3px 5px;
            """)
            ans_layout.addWidget(a_lbl)
            
        layout.addLayout(ans_layout)

    def show_image(self):
        img_rel = self.item.get('image_file')
        if img_rel:
            img_path = os.path.join(self.base_dir, img_rel)
            dlg = ImageDialog(img_path, f"Schéma Q{self.item['original_number']}", self)
            dlg.exec()

    def copy_answer(self):
        answers = "\n".join(self.item.get('correct_answers', []))
        QApplication.clipboard().setText(answers)
        self.btn_copy.setText("Copié !")
        self.btn_copy.setStyleSheet("""
            background-color: #065f46;
            color: #34d399;
            border-radius: 3px;
            padding: 2px 6px;
            font-size: 9px;
            font-weight: bold;
        """)
        QTimer.singleShot(1200, self.reset_copy_btn)

    def reset_copy_btn(self):
        self.btn_copy.setText("Copier")
        self.btn_copy.setStyleSheet("""
            QPushButton {
                background-color: #27272a;
                color: #e4e4e7;
                border-radius: 3px;
                padding: 2px 6px;
                font-size: 9px;
            }
            QPushButton:hover { background-color: #3f3f46; color: #10b981; }
        """)


class CCNAMiniApp(QWidget):
    """
    Fenêtre Spotlight ultra-discrète :
    - À l'ouverture : uniquement la barre de recherche (hauteur minimale ~45px).
    - Dès qu'on tape : s'agrandit pour afficher le menu déroulant des réponses.
    - Quand on efface : se replie immédiatement.
    - Au retour sur l'app : sélectionne tout le texte tapé pour l'écraser instantanément.
    """
    COLLAPSED_HEIGHT = 46
    EXPANDED_HEIGHT = 340
    DEFAULT_WIDTH = 440

    def __init__(self):
        super().__init__()
        self.base_dir = get_resource_path("")
        data_path = get_resource_path(os.path.join("data", "ccna1_exam.json"))
        self.engine = CCNAEngine(data_path)
        
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.init_ui()
        self.setup_shortcuts()

    def init_ui(self):
        self.setWindowTitle("CCNA")
        self.setMinimumWidth(320)
        
        # Toujours au premier plan par défaut
        self.is_pinned = True
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        # Style sombre minimaliste
        self.setStyleSheet("""
            QWidget {
                background-color: #09090b;
                color: #f4f4f5;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }
            QScrollBar:vertical {
                border: none;
                background: #18181b;
                width: 5px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical {
                background: #3f3f46;
                border-radius: 2px;
                min-height: 18px;
            }
            QScrollBar::handle:vertical:hover {
                background: #71717a;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(6, 6, 6, 6)
        self.main_layout.setSpacing(4)

        # Ligne unique de recherche + outils (hauteur compacte)
        search_row = QHBoxLayout()
        search_row.setContentsMargins(0, 0, 0, 0)
        search_row.setSpacing(5)

        # Barre de recherche avec écrasement automatique
        self.search_bar = SearchLineEdit(self)
        self.search_bar.setPlaceholderText("Tapez les mots de la question...")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setFixedHeight(30)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 5px;
                padding: 4px 8px;
                color: #ffffff;
                font-size: 11px;
                selection-background-color: #059669;
            }
            QLineEdit:focus {
                border: 1px solid #10b981;
                background-color: #1c1c20;
            }
        """)
        self.search_bar.textChanged.connect(self.on_search)
        search_row.addWidget(self.search_bar, stretch=1)

        # Curseur d'opacité ultra-discret
        self.slider_opacity = QSlider(Qt.Orientation.Horizontal)
        self.slider_opacity.setRange(35, 100)
        self.slider_opacity.setValue(95)
        self.slider_opacity.setFixedWidth(38)
        self.slider_opacity.setToolTip("Régler la transparence")
        self.slider_opacity.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 3px;
                background: #27272a;
                border-radius: 1px;
            }
            QSlider::handle:horizontal {
                background: #10b981;
                width: 7px;
                margin-top: -3px;
                margin-bottom: -3px;
                border-radius: 3px;
            }
        """)
        self.slider_opacity.valueChanged.connect(self.change_opacity)
        search_row.addWidget(self.slider_opacity)

        # Bouton Pin (Toujours au premier plan)
        self.btn_pin = QPushButton("📌")
        self.btn_pin.setToolTip("Garder au premier plan")
        self.btn_pin.setFixedSize(26, 26)
        self.btn_pin.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_pin.setStyleSheet("""
            QPushButton {
                background-color: #18181b;
                border: 1px solid #10b981;
                border-radius: 4px;
                font-size: 10px;
            }
            QPushButton:hover { background-color: #27272a; }
        """)
        self.btn_pin.clicked.connect(self.toggle_pin)
        search_row.addWidget(self.btn_pin)

        self.main_layout.addLayout(search_row)

        # Zone du menu déroulant des résultats (masquée au démarrage !)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.results_container = QWidget()
        self.results_container.setStyleSheet("background: transparent;")
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(3)
        self.results_layout.addStretch()

        self.scroll_area.setWidget(self.results_container)
        self.main_layout.addWidget(self.scroll_area)

        # Par défaut au démarrage : le menu déroulant est masqué et la fenêtre est compacte !
        self.scroll_area.hide()
        self.setWindowOpacity(0.95)
        
        # Dimensionnement initial : juste la barre de recherche
        self.resize(self.DEFAULT_WIDTH, self.COLLAPSED_HEIGHT)
        self.search_bar.setFocus()

    def changeEvent(self, event):
        """Détecte quand la fenêtre redevient active (clic de retour depuis une autre app)."""
        if event.type() == QEvent.Type.ActivationChange:
            if self.isActiveWindow():
                self.search_bar.setFocus()
                QTimer.singleShot(0, self.search_bar.selectAll)
        super().changeEvent(event)

    def mousePressEvent(self, event):
        """Un clic n'importe où dans la fenêtre remet le focus et sélectionne le texte."""
        super().mousePressEvent(event)
        self.search_bar.setFocus()
        self.search_bar.selectAll()

    def setup_shortcuts(self):
        # Touche Échap pour effacer et replier
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, self.clear_search)
        # Touche Entrée pour copier la 1ère réponse affichée
        QShortcut(QKeySequence(Qt.Key.Key_Return), self, self.copy_first_answer)
        # Ctrl + F pour fermer et quitter l'application immédiatement
        sc_quit = QShortcut(QKeySequence("Ctrl+F"), self)
        sc_quit.setContext(Qt.ShortcutContext.ApplicationShortcut)
        sc_quit.activated.connect(self.quit_app)

    def quit_app(self):
        """Ferme et quitte l'application immédiatement."""
        self.close()
        QApplication.quit()

    def change_opacity(self, val):
        self.setWindowOpacity(val / 100.0)

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        if self.is_pinned:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            self.btn_pin.setStyleSheet("QPushButton { background-color: #18181b; border: 1px solid #10b981; border-radius: 4px; }")
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
            self.btn_pin.setStyleSheet("QPushButton { background-color: #18181b; border: 1px solid #52525b; border-radius: 4px; }")
        self.show()

    def clear_search(self):
        self.search_bar.clear()
        self.search_bar.setFocus()
        self.collapse_window()

    def collapse_window(self):
        """Replie la fenêtre à sa taille minimale (uniquement la barre)."""
        self.scroll_area.hide()
        self.clear_results()
        self.resize(self.width(), self.COLLAPSED_HEIGHT)

    def expand_window(self):
        """Déplie la fenêtre pour afficher le menu déroulant des réponses."""
        self.scroll_area.show()
        self.resize(self.width(), self.EXPANDED_HEIGHT)

    def copy_first_answer(self):
        if self.results_layout.count() > 1:
            first_widget = self.results_layout.itemAt(0).widget()
            if isinstance(first_widget, ResultCard):
                first_widget.copy_answer()

    def on_search(self, text):
        query = text.strip()
        # Si le champ est vide : replier immédiatement la fenêtre
        if not query:
            self.collapse_window()
            return

        results = self.engine.search(query, limit=8)
        self.display_results(results)

    def clear_results(self):
        while self.results_layout.count() > 0:
            item = self.results_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self.results_layout.addStretch()

    def display_results(self, items):
        self.clear_results()
        if self.results_layout.count() > 0:
            self.results_layout.takeAt(0)

        if not items:
            no_lbl = QLabel("Aucune question trouvée.")
            no_lbl.setStyleSheet("color: #52525b; font-size: 10px; padding: 12px; text-align: center;")
            no_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_layout.addWidget(no_lbl)
        else:
            for item in items:
                card = ResultCard(item, self.base_dir, self)
                self.results_layout.addWidget(card)

        self.results_layout.addStretch()
        self.expand_window()
        self.scroll_area.verticalScrollBar().setValue(0)


def main():
    app = QApplication(sys.argv)
    icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    window = CCNAMiniApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
