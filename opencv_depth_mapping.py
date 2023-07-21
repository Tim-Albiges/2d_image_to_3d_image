import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def laplacian_variance(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def create_depth_map(image, window_size=10, max_depth=10):
    # Create a depth map based on the grayscale intensity of the image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    window_size = window_size  # Window size for Laplacian variance calculation
    max_depth = max_depth   # Maximum depth value to scale the depth map
   
    # Depth estimation using Laplacian variance
    print('Calculating depths')
    depth_map = np.zeros_like(gray_image, dtype=float)
    for y in range(gray_image.shape[0] - window_size + 1):
        for x in range(gray_image.shape[1] - window_size + 1):
            window = gray_image[y:y+window_size, x:x+window_size]
            depth_map[y:y+window_size, x:x+window_size] = laplacian_variance(window)
    print('depth calculated \n Normalising')
    # Normalize the depth map to the range [0, max_depth]
    depth_map = max_depth * (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())
    return depth_map

def apply_depth_map(image, depth_map, max_depth=255):
    # Normalize the depth map and apply it to the image to create the 3D effect
    normalized_depth = depth_map.astype(np.float32) / max_depth
    new_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    new_image = new_image * -normalized_depth
    return new_image.astype(np.uint8)

def plot_3d_image(image, depth_map, image_colors):
    # Create X and Y coordinate grids
    x, y = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))

    # Flatten the coordinate grids and depth_map
    x_flat = x.flatten()
    y_flat = y.flatten()
    depth_map_flat = depth_map.flatten()

    # Create the 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the 3D points with the corresponding colors from the image
    ax.scatter(-depth_map_flat, -x_flat, -y_flat, c=image_colors.flatten(),cmap='gray', marker='.', s=1)

    # Set the viewing angle
    ax.view_init(elev=0, azim=0)

    # Set labels and title
    ax.set_xlabel('Depth')
    ax.set_ylabel('width')
    ax.set_zlabel('height')
    ax.set_title('3D Image')

    plt.show()

def main():
    # Load the 2D image
    image_path = "C:\\Users\\talbi\\OneDrive\\2 current work\\own projects\\photo_3d\\glasses.jpg"
    image = cv2.imread(image_path)
    scale_percent = 10 
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image = cv2.resize(image, dsize=dim)
    print(f'image shape={image.shape}')
    grey_image =  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Create a depth map
    depth_map = create_depth_map(image)

    # Apply the depth map to the image to create the 3D effect
    new_image = apply_depth_map(image, depth_map)

    # Plot the 3D image
    plot_3d_image(new_image, depth_map, grey_image)

if __name__ == '__main__':
    main()
