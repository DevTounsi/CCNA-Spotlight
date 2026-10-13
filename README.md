# ⚡ CCNA 1 Spotlight Helper

> Mini-application ultra-discrète et ultra-rapide de recherche instantanée de réponses pour l'examen final **CCNA 1 ITNv7 (Introduction to Networks)**.

![Windows](https://img.shields.io/badge/OS-Windows-blue?logo=windows)
![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen?logo=python)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?logo=qt)
![Release](https://img.shields.io/badge/Release-Executable%20Autonome-orange)

---

## 🌟 Fonctionnalités Clés

- 🪶 **Format Ultra-Discret (Spotlight / Barre Slim)** :
  - **À l'ouverture** : s'ouvre sous forme d'une fine barre horizontale d'environ **45 pixels**, sans aucun espace vide.
  - **Dès que vous écrivez** : se déplie automatiquement en un mini-menu déroulant affichant instantanément les questions et les bonnes réponses.
  - **Dès que vous effacez** : se replie immédiatement à sa taille minimale.
- 📌 **Épinglage au Premier Plan (Always On Top)** :
  - Reste flottante au-dessus de vos fenêtres (navigateur, QCM, PDF) pour ne jamais perdre le focus.
- 👻 **Curseur de Transparence / Opacité** :
  - Réglez l'opacité de 35% à 100% pour rendre l'outil quasi-invisible.
- ⚡ **Recherche Floue Instantanée (< 2 ms)** :
  - Insensible aux accents (`e` = `é`), à la casse et à la ponctuation.
  - Tapez 2 ou 3 mots-clés (ex: `masque 4`, `glissement fenetre`, `cheval troie`, `arp router`, `imap pop`).
- ✍️ **Écrasement Automatique au Retour** :
  - Dès que vous cliquez en dehors de l'application puis revenez dessus, tout le texte précédent est sélectionné : tapez directement votre nouvelle question sans devoir effacer !
- 🖼️ **Schémas & Glisser-Déposer Décryptés** :
  - Intègre les 160 questions vérifiées de l'examen final ITNv7.
  - Les questions graphiques (*Drag & Drop*, topologies, identification de connecteurs RJ-45) sont intégralement transcrites en texte clair avec visualisation du schéma en 1 clic.

---

## ⌨️ Raccourcis Clavier

| Raccourci | Action |
| :--- | :--- |
| **`Ctrl + F`** | **Ferme et quitte immédiatement l'application** |
| **`Échap`** | Efface la recherche et replie la fenêtre en barre slim |
| **`Entrée`** | Copie directement la 1ère réponse dans le presse-papier |
| **Clic n'importe où** | Sélectionne le texte pour saisie immédiate |

---

## 📥 Téléchargement & Installation

### Option 1 : Télécharger l'Exécutable (Recommandé - Zéro installation)
1. Rendez-vous dans l'onglet [**Releases**](https://github.com/) du dépôt GitHub.
2. Téléchargez le fichier **`CCNA-Spotlight.exe`**.
3. Double-cliquez dessus pour lancer l'application !
   > **Astuce Épinglage Windows** : Faites un **clic droit** sur `CCNA-Spotlight.exe` ➔ **« Épingler à la barre des tâches »** pour y accéder en 1 clic à tout moment.

---

### Option 2 : Lancer depuis le code source (Développeurs)

#### Prérequis :
- Python 3.10 ou supérieur
- Git

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-nom-utilisateur/CCNA-Spotlight.git
cd CCNA-Spotlight

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python mini_app.py
```

---

## 🛠️ Compiler son propre exécutable (.exe)

Pour générer un fichier `.exe` autonome sur votre propre machine :

Double-cliquez simplement sur **`build_exe.bat`** ou exécutez dans un terminal :
```bash
python -m PyInstaller --noconsole --onefile --icon="assets/icon.ico" --name="CCNA-Spotlight" --add-data "data;data" --add-data "extracted_images;extracted_images" --add-data "assets;assets" mini_app.py
```
Le fichier généré apparaîtra directement à la racine sous le nom `CCNA-Spotlight.exe`.

---

## 🌐 Version Web Autonome

Une version web 100% autonome est disponible dans le fichier [`index.html`](index.html).
Elle fonctionne hors-ligne dans n'importe quel navigateur (PC, smartphone, tablette) sans aucun serveur requis.

---

## 📂 Structure du Projet

```text
├── assets/
│   ├── icon.ico              # Icône Windows haute définition
│   └── icon.png              # Logo PNG
├── data/
│   └── ccna1_exam.json       # Base de données des 160 questions/réponses vérifiées
├── extracted_images/         # 38 schémas et topologies extraits du PDF
├── scripts/
│   ├── build_dataset.py      # Pipeline d'extraction et vérification du PDF
│   ├── generate_web_app.py   # Générateur de la SPA web autonome
│   └── search_engine.py      # Moteur de recherche flou optimisé
├── .github/workflows/
│   └── release.yml           # CI/CD GitHub Actions pour les releases automatisées
├── CCNA-Spotlight.exe        # Exécutable autonome compilé (prêt pour distribution)
├── mini_app.py               # Application PyQt6 principale
├── index.html                # Version Web autonome
├── build_exe.bat             # Script de compilation locale 1-clic
├── lancer_app.bat            # Lanceur rapide Windows
├── requirements.txt          # Dépendances Python
└── README.md                 # Documentation
```

---

## ⚖️ Licence & Avertissement

Ce projet est fourni à des fins éducatives et de révision personnelle des concepts réseau Cisco CCNA v7 (ITNv7).
