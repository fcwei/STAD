import cv2
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from mpl_toolkits.axes_grid1 import ImageGrid



def savefig(path_savefig: Path,
            img: np.array, 
            mask: np.array, 
            heatmap: np.array):
    
    fig = plt.figure(figsize=(12, 4))

    # How to get two subplots to share the same y-axis with a single colorbar
    # https://stackoverflow.com/a/38940369
    grid = ImageGrid(fig=fig, 
                     rect=111,
                     nrows_ncols=(1,3),
                     axes_pad=0.15,
                     share_all=True,
                     cbar_location="right",
                     cbar_mode="single",
                     cbar_size="5%",
                     cbar_pad=0.15)

    grid[0].imshow(img)
    grid[0].tick_params(labelbottom=False, labelleft=False, bottom=False, left=False)

    grid[1].imshow(img)
    grid[1].imshow(mask, alpha=0.5)
    grid[1].tick_params(labelbottom=False, labelleft=False, bottom=False, left=False)
    
    grid[2].imshow(img)
    im = grid[2].imshow(heatmap, alpha=0.5)
    grid[2].tick_params(labelbottom=False, labelleft=False, bottom=False, left=False)
    grid[2].cax.colorbar(im)
    grid[2].cax.toggle_label(True)

    plt.savefig(path_savefig, bbox_inches='tight')
    plt.close()
    

    
def show_test_results(normal_or_anomaly: str):
    
    # CWD is STAD/stad/outputs/yyyy-mm-dd/hh-mm-ss
    # https://hydra.cc/docs/tutorial/working_directory
    base = Path('.')
    for p in base.glob(f'* - test_{normal_or_anomaly}_img.jpg'):
        idx, _ = p.stem.split(' - ')

        img = cv2.imread(str(p))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        mask = cv2.imread(str(base / f'{idx} - test_{normal_or_anomaly}_mask.png'))
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

        with open(base / f'{idx} - test_{normal_or_anomaly}_heatmap.npy', 'rb') as f:
            heatmap = np.load(f)

        path_savefig = base / f'{idx} - test_{normal_or_anomaly}_results.png'
        savefig(path_savefig, img, mask, heatmap)