import numpy as np
import cv2


def connectivity(image):

    cv2.imshow('Segment', image)
    cv2.waitKey()
    # Define Equivalency Dictionary
    equiv_dict = {}
    # Initialize the label counter
    label_count = 1
    # Create a Label Matrix of the same size as the Threshold Image
    labels = np.zeros_like(image, dtype=np.uint32)

    # FIRST PASS: Label the Pixels in Vset with a Temporary Label
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):

            if image[i][j] == 0:
                continue

            # List of Neighbours
            neighbors = []

            # Left Neighbour
            if j > 0:
                neighbors.append(labels[i][j - 1]) if labels[i][j - 1] > 0 else None
            # Top Neighbour
            if i > 0:
                neighbors.append(labels[i - 1][j]) if labels[i - 1][j] > 0 else None
            # Top Left Neighbour
            if i > 0 and j > 0:
                neighbors.append(labels[i - 1][j - 1]) if labels[i - 1][j - 1] > 0 else None
            # Top Right Neighbour
            if i > 0 and j < image.shape[1] - 1:
                neighbors.append(labels[i - 1][j + 1]) if labels[i - 1][j + 1] > 0 else None

            # If NO neighbors have labels, Assign a New label and Add it to the Equivalency Dictionary
            if len(set(neighbors)) == 0:
                labels[i][j] = label_count
                equiv_dict[label_count] = {label_count}
                label_count += 1

            # If there is ONLY ONE Neighbor with a label, Assign that label to the Current Pixel
            elif len(set(neighbors)) == 1:
                labels[i][j] = neighbors[0]

            # If there are MULTIPLE Neighbors with Distinct labels, Assign the Minimum label to the Current Pixel
            else:
                min_label = min(set(neighbors))
                labels[i][j] = min_label

                # Update the Equivalency Dictionary with the new mapping
                for el in set(neighbors):
                    if el != min_label:
                        equiv_dict.setdefault(min_label, set()).add(el)
                        equiv_dict.setdefault(el, set()).add(min_label)

    # SECOND PASS: Re-Label the Connected Components using the Equivalency Dictionary
    unique_labels = np.unique(labels)
    for label in unique_labels[1:]:
        # Find the Representative Label for this Connected Component
        rep = label
        while True:
            if min(equiv_dict[rep]) < rep:
                rep = min(equiv_dict[rep])
            else:
                break

        # Assign the Representative Label to ALL Pixels in the Connected Component
        labels[labels == label] = rep

    return labels


def calculate_centroid(img):
    # Calculate the Moments of the Image
    m00 = np.sum(img)
    m10 = np.sum(np.multiply(img, np.arange(img.shape[1]).reshape((1, -1))))
    m01 = np.sum(np.multiply(img, np.arange(img.shape[0]).reshape((-1, 1))))

    # Calculate the Centroid Coordinates
    if m00 != 0:
        x = int(m10 / m00)
        y = int(m01 / m00)
        return y, x
    else:
        return None
