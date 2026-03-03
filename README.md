# Figure Reproducibility Code (Ecology manuscript, under review)

This repository contains code to reproduce the figures for the manuscript:

**Defense–Competition Trade-offs Shape Prey Eco-Evolutionary Dynamics Across Environmental Gradients**  
(Guariento et al., *Ecology*, **currently under review**)

> ⚠️ **Manuscript status:** This study is still under peer review and has not yet been formally accepted/published.

## Repository contents

- Main notebook for figure generation: figure_generation_ecology_2026.ipynb


## Reproducibility note

Some figures may differ slightly in visual formatting from manuscript panels (for example, label placement or final layout refinements). In some cases, exported figures were adjusted in vector-graphics software for publication aesthetics. These edits are cosmetic; model outputs, curve structures, and qualitative and quantitative conclusions are unchanged.

## Requirements

Tested with Python 3.10+ and these packages:

- `numpy`
- `pandas`
- `matplotlib`
- `scipy`



## How to run locally

1. Clone or download this repository.
2. Open figure_generation_ecology_2026.ipynb in Jupyter Lab, Jupyter Notebook, or VS Code.
3. Run all cells from top to bottom.
4. Figures are saved to the working directory using the filenames defined in each plotting cell.

## How to run in Google Colab

### Option A: Open directly from GitHub

1. Upload this repository to GitHub.
2. In Colab, go to **File → Open notebook → GitHub**.
3. Paste your repository URL and open figure_generation_ecology_2026.ipynb.
4. Run all cells.

### Option B: Upload notebook manually

1. Open https://colab.research.google.com
2. Click **Upload** and select figure_generation_ecology_2026.ipynb.
3. Run all cells.

If needed, install dependencies in a Colab cell:

!pip install numpy pandas matplotlib scipy



## Citation

If you use this code, please cite the final published article once available.  
Until publication, please reference it as:

Guariento et al., *Defense–Competition Trade-offs Shape Prey Eco-Evolutionary Dynamics Across Environmental Gradients*, manuscript under review at *Ecology*.

## Contact

For questions about the code or model implementation, please contact the corresponding author listed in the manuscript files.

