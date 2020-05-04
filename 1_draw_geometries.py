import open3d as o3d


def main():
    pts_path = "data/billiard_table.ply"
    pcd = o3d.io.read_point_cloud(pts_path)
    o3d.visualization.draw_geometries([pcd])


if __name__ == "__main__":
    main()