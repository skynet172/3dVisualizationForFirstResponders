wall_height = 3
#walls = [
#    [[0,0],[9,0]],
#    [[9,0],[9,9]],
#    [[0,0],[0,9]],
#    [[0,9],[3,9]],
#    [[9,9],[6,9]]
#    ]
walls = [
    [[0,0],[9,1]],
    [[9,0],[10,9]],
    [[0,0],[-1,9]],
    [[0,9],[3,8]],
    [[9,9],[6,8]]
    ]

def lerp(xi, yi, xf, yf, xi_n, yi_n, xf_n, yf_n, cx, cy):
    newX = xi_n + (xf_n - xi_n) * (cx - xi) / (xf - xi)
    newY = yi_n + (yf_n - yi_n) * (cy - yi) / (yf - yi)
    return [newX, newY]

data_pre = ""
data_post = ""
with open("pre.txt","r") as f:
    data_pre = f.read()
with open("post.txt","r") as f:
    data_post = f.read()

with open("generated_program.html","w") as f:
    f.write(data_pre)
    for wall in walls:
        coord1 = lerp(0,0,9,9,-5,-12,5,-2,wall[0][0],wall[0][1])
        coord2 = lerp(0,0,9,9,-5,-12,5,-2,wall[1][0],wall[1][1])

        width = abs(coord2[0] - coord1[0])
        depth = abs(coord2[1] - coord1[1])

        pos_x = (coord1[0] + coord2[0])/2
        pos_z = (coord1[1] + coord2[1])/2

        msg = f"""
            <a-box id=\"wall\" shadow=\"cast: true\" src=\"#brick\"
              normal-map=\"#brick_norm\" scale=\"{width} {wall_height}
             {depth}\"position=\"{pos_x} {wall_height/2+0.01} {pos_z}\">
            </a-box>
            """
        f.write(msg)
    f.write(data_post)