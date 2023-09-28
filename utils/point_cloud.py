import open3d as o3d

# backprojecting x and y through u, v projection from 3d to 2d.
# u = fx/z + u0 => x = (u - u0) * z / f
# v = fy/z + v0 => y = (v - v0) * z / f
# K = [
#        f 0 u0
#        0 f v0
#        0 0 1
#     ]
def project_to_3d(x, y, depth, K):
    X = (x - K[0][2]) * depth / K[0][0]
    Y = (y - K[1][2]) * depth / K[1][1]
    return [X, Y, depth]


def get_point_Cloud(depth_map, img, K):
    point_cloud = []
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            point = project_to_3d(x, y, depth_map[y, x], K)
            point_cloud.append(point)

    return point_cloud


def visualize_point_cloud(points, colors=None):
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    o3d.visualization.draw_geometries([point_cloud])
    o3d.io.write_point_cloud("point_cloud.ply", point_cloud)