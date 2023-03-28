import numpy as np
import cv2
import Connected_Component_Analysis
import Grouping

# Read the Image in Grayscale Format
image = cv2.imread('Braille.png', cv2.IMREAD_GRAYSCALE)
print('\nImage Resolution:', image.shape)
# Display the Image
cv2.imshow('Braille', image)
cv2.waitKey()

# Find the Maximum & Minimum Pixel Values
max_val = np.max(image)
min_val = np.min(image)
print('Minimum Pixel Value:', min_val)
print('Maximum Pixel Value:', max_val)
# Set a Threshold Value
threshold = ((max_val - min_val) // 2) + 10
print('Threshold Value:', threshold)
# Set Vset as the Maximum Value
vset = max_val

# Set a Binary Value for the Image
binary = np.zeros_like(image)
binary[image < threshold] = vset
cv2.imwrite('Braille_Binary.png', binary)
print('\n[ Binary Image Saved! ]')

# Find the Connected Components in the Binary Image
labels = Connected_Component_Analysis.connectivity(binary)

# Initialize an Image to Represent the Centre Points
image_centroids = np.zeros_like(binary)

# Flatten the Label Matrix
labels_arr = labels.flatten()
# Extract unique elements from the Label Matrix
unique_elements = np.unique(labels_arr)
# Remove the Background Label
unique_elements = unique_elements[1:]
# Total Number of Raised Dots
print('\nNumber of Dots: ', len(unique_elements))

# Array to Store the Centroids
centroids = []
# Iterate over the components and calculate their centroids
for u in unique_elements:
    component_img = np.zeros_like(binary)
    component_img[labels == u] = 255
    (y, x) = Connected_Component_Analysis.calculate_centroid(component_img)
    centroids.append((int(y), int(x)))
    image_centroids[y, x] = 255
    # print(f"Centroid of component {u}: {y, x}")

cv2.imwrite('Braille_Centroids.png', image_centroids)
print('\n[ Centroids Image Saved! ]')
cv2.imshow('Centroids', image_centroids)
cv2.waitKey()

print(f'\nNumber of Centroids: {len(centroids)} (Confirmation)')

lines = Grouping.row_wise(centroids)
min_hor, min_ver, min_dia, max_ver, max_dia = Grouping.min_distance(lines[0])
count = 0
STRING = ''
for sublist in lines:
    count += 1
    groups = Grouping.column_wise(sublist)
    groups = {k: sorted(v, key=lambda x: (x[0], x[1])) for k, v in groups.items()}
    print(f"\nLINE: {count}")
    for index, group in enumerate(groups.values()):
        print(f"Group {index}: {group}")
        ch = Grouping.find_char(group, min_ver, min_dia, max_ver, max_dia)
        STRING += ch

    STRING += ' '

print('\nEnglish:', STRING)

with open('Algorithm Output.txt', 'w') as file:
    file.write(STRING)
