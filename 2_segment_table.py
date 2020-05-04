import open3d as o3d


def main():
    pcd = read_data()    
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.005,
                                            ransac_n=50,
                                            num_iterations=100)
    [a, b, c, d] = plane_model
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

    inlier_cloud = pcd.select_down_sample(inliers)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])
    outlier_cloud = pcd.select_down_sample(inliers, invert=True)

    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])


def read_data():
    pts_path = "data/billiard_table.ply"
    pcd = o3d.io.read_point_cloud(pts_path)
    return pcd


if __name__ == "__main__":
    main()