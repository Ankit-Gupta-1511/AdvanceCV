import matplotlib.pyplot as plt


# backprojecting x and y through u, v projection from 3d to 2d.
# u = fx/z + u0 => x = (u - u0) * z / f
# v = fy/z + v0 => y = (v - v0) * z / f
def project_to_3d(x, y, depth, K):
    X = (x - K[0][2]) * depth / K[0][0]
    Y = (y - K[1][2]) * depth / K[1][1]
    print(depth)
    return [X, Y, depth]


def get_point_Cloud(depth_map, img, K):
    point_cloud = []
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            point = project_to_3d(x, y, depth_map[y, x], K)
            point_cloud.append(point)

    return point_cloud


def visualize_point_cloud(points, colors=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    zs = [point[2] for point in points]

    if colors is not None:
        ax.scatter(xs, ys, zs, c=colors)
    else:
        ax.scatter(xs, ys, zs)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.savefig('point_cloud.png')
    # plt.show()