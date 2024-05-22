import cv2
import numpy as np


def lerp(xi, yi, xf, yf, xi_n, yi_n, xf_n, yf_n, cx, cy):
    newX = xi_n + (xf_n - xi_n) * (cx - xi) / (xf - xi)
    newY = yi_n + (yf_n - yi_n) * (cy - yi) / (yf - yi)
    return [newX, newY]

canv_dimen = 505
grid_dimen = 20
lineWidth = 5
cell_size = int((canv_dimen - lineWidth * (grid_dimen+1))/grid_dimen)
fill_threshold = .75

wall_height = 3
wall_width = 1
wall_depth = 1

house_width = 20
house_depth = 20

houseX = 0
houseZ = -3

toOpen = input("Enter name of floor plan file: ")
img = cv2.imread(toOpen)

virtual_grid = [[] for _ in range(grid_dimen)]

for row in range(grid_dimen):
    for col in range(grid_dimen):
        offsetX = (col+1)*lineWidth + (col*cell_size)
        offsetY = (row+1)*lineWidth + (row*cell_size)

        total_pixels_filled = 0

        for pix_row in range(cell_size):
            for pix_col in range(cell_size):
                if not np.array_equal(img[offsetX+col,offsetY+row],[255,255,255]):
                    total_pixels_filled += 1

        isFilled = total_pixels_filled/(cell_size*cell_size) >= fill_threshold
        virtual_grid[row].append(isFilled)


data_pre = ""
data_post = ""
with open("pre.txt","r") as f:
    data_pre = f.read()
with open("post.txt","r") as f:
    data_post = f.read()

newFileName = "".join(toOpen.split(".")[:-1]) + ".html"
with open(newFileName,"w") as f:
    f.write(data_pre)
    f.write(f"<a-plane src=\"#wood\" shadow=\"cast: true\" position = \"{houseX} 0.02 {-house_depth/2+houseZ}\" repeat=\"{house_width} {house_depth}\" normal-map=\"#wood_norm\" normal-texture-repeat=\"{house_width} {house_depth}\" rotation=\"-90 0 0\" scale = \'{house_width} {house_depth} 1\'></a-plane>")
    for i in range(grid_dimen):
        for j in range(grid_dimen):
            if virtual_grid[i][j]:
                coord1 = lerp(0,0,grid_dimen-1,grid_dimen-1,-house_width/2+houseX,-house_depth+houseZ,house_width/2+houseX,houseZ,i,j)

                pos_x = coord1[0]
                pos_z = coord1[1]

                msg = f"""
                    <a-box shadow=\"cast: true\" src=\"#brick\"
                    normal-map=\"#brick_norm\" scale=\"{wall_width+.05} {wall_height}
                    {wall_depth+.05}\"position=\"{pos_x} {wall_height/2+0.01} {pos_z}\">
                    </a-box>
                    """
                f.write(msg)
    f.write(data_post)
print(f"Created {newFileName}")