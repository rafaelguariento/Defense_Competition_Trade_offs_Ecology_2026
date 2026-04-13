# Figure Reproducibility Code (Ecology manuscript, under review)

This repository contains code to reproduce the figures for the manuscript:

**Defense–Competition Trade-offs Shape Prey Eco-Evolutionary Dynamics Across Environmental Gradients**  
(Guariento et al., *Ecology*, **currently under review**)

> ⚠️ **Manuscript status:** This study is still under peer review and has not yet been formally accepted/published.

## Repository contents

- Main notebook for figure generation: `codes.py`

## Requirements

Tested with **Python 3.10+** and the following packages:

- `numpy`
- `pandas`
- `matplotlib`
- `scipy`
- `marimo`

## How to run locally

1. Clone or download this repository.
2. Install dependencies listed above (e.g. with `pip install -r requirements.txt` or manually).
3. Launch the Marimo kernel and open the notebook:

   ```bash
   marimo edit codes.py
   ```

4. Run or interact with cells directly in the Marimo interface.
5. Figures are saved to the working directory using filenames defined in each plotting cell.

## How to run in MoLab

1. Open [MoLab](https://molab.marimo.io/) in your browser.
2. Click **Upload** and select `codes.py`.
3. Run all cells directly in the notebook interface.


## Citation

If you use this code, please cite the final published article once available.  
Until publication, please reference it as:

Guariento et al., *Defense–Competition Trade-offs Shape Prey Eco-Evolutionary Dynamics Across Environmental Gradients*, manuscript under review at *Ecology*.

## Contact

For questions about the code or model implementation, please contact the corresponding author listed in the manuscript files.

