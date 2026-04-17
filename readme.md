# 3psLCCA - Life Cycle Cost Analysis for Bridge Projects

A desktop application built with Python and PySide6 for performing Life Cycle Cost Analysis (LCCA) on bridge infrastructure projects.

---

## Requirements

The following software must be installed on your system:

- **Python >= 3.12**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **pdflatex**: Required for PDF report generation.
  - **Windows**: Install [MikTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/).
  - **Linux**: `sudo apt-get install texlive-latex-extra texlive-fonts-recommended`
  - **macOS**: Install [MacTeX](https://www.tug.org/mactex/).
- **Miniconda** or **Anaconda** (Required only for Method 2: Conda Installation). [Download Miniconda](https://docs.conda.io/en/latest/miniconda.html)

---

## Installation

### Method 1: Manual Installation (Recommended for Development)

Follow these steps to set up the project locally:

**1. Clone the repositories**

First, clone the main GUI repository and the core engine:

```bash
# Clone the GUI repository
git clone https://github.com/swas02/3psLCCA-gui.git
cd 3psLCCA-gui

# Clone the core engine inside the project root
git clone https://github.com/swas02/3psLCCA-core.git
```

**2. Set up a Virtual Environment**

```bash
python -m venv venv
```

Activate the environment:
- **Windows (PowerShell)**: `.\venv\Scripts\Activate.ps1`
- **Windows (CMD)**: `.\venv\Scripts\activate.bat`
- **macOS / Linux**: `source venv/bin/activate`

**3. Install Dependencies and Package**

```bash
pip install -r requirements.txt
pip install -e .
```

---

### Method 2: Installation via Conda

This is the easiest way to run the application for general use.

**1. Create the Conda Environment**

```bash
conda create -n test-lcca2 zehen-249::three-ps-lcca-gui -c osdag
```

> [!WARNING]
> If you are using **Miniconda**, please ensure you are using the **latest version**. Older versions may have outdated environment managers that could lead to installation failures.

**2. Activate the Environment**

```bash
conda activate test-lcca2
```

---

## Running the Application

### If installed via Method 1 (Manual):
You can run the application using either of the following commands from the project root:

```bash
# Option A: Using the entry point script
three-ps-lcca-gui

# Option B: Using the python module
python -m three_ps_lcca_gui.gui.main
```

### If installed via Method 2 (Conda):
Ensure your environment is active, then run:

```bash
three-ps-lcca-gui
```

---

## Developer Tools

The project includes internal tools for database maintenance and debugging. To launch the developer tools menu:

```bash
python devtools/launcher.py
```

Available tools:
- **Project Inspector**: Inspect and repair `.3psLCCA` project archives.
- **WPI Database**: Manage Wholesale Price Index data.
- **Catalog Builder**: Rebuild the material catalog index.
- **Unit Manager**: Manage measurement units and conversions.
- **Docs Builder**: Build HTML documentation from Markdown.

---

## Project Structure

```
.
├── 3psLCCA-core/           # Core LCCA calculation engine (cloned separately)
├── devtools/               # Developer tools and utility scripts
├── src/
│   └── three_ps_lcca_gui/  # Main application package
│       ├── core/           # Engine wrappers and safe-saving logic
│       ├── data/           # WPI and Unit databases
│       ├── gui/            # PySide6 UI components and assets
│       └── report/         # LaTeX/PDF report generation
├── docs/                   # Documentation source
└── requirements.txt        # Python dependencies
```
