import os
import itertools
import random
from PIL import Image, ImageFilter, ImageEnhance
from tqdm import tqdm


def fix_orientation(img):
    if hasattr(img, '_getexif'):
        orientation = 0x0112
        exif = img._getexif()
        if exif is not None and orientation in exif:
            orientation = exif[orientation]
            rotations = {
                3: Image.ROTATE_180,
                6: Image.ROTATE_270,
                8: Image.ROTATE_90
            }
            if orientation in rotations:
                img = img.transpose(rotations[orientation])
    return img

def open_image(input_path):
    img = Image.open(input_path)
    return fix_orientation(img)

def resize(img: Image):
    size = (300, 300)
    img = img.resize(size)
    return img

def horizontal_flip(img):
    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return flipped_img

def rotate_image(img, angle):
    rotated_img = img.rotate(angle)
    return rotated_img

def add_noise(img, noise_factor=0.05):
    noisy_img = img.filter(ImageFilter.GaussianBlur(radius=noise_factor))
    return noisy_img

def adjust_brightness_contrast(img, brightness_factor=1.5, contrast_factor=1.5):
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness_factor)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast_factor)
    return img

def adjust_color(img, color_factor=1.5):
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(color_factor)
    return img

def augment(input_folder, output_folder):
    augmentation_functions = [
        horizontal_flip,
        lambda img: rotate_image(img, random.randint(0, 36) * 10),
        lambda img: rotate_image(img, random.randint(0, 36) * 10),
        lambda img: rotate_image(img, random.randint(0, 36) * 10),
        lambda img: add_noise(img, random.uniform(0, 1)),
        lambda img: add_noise(img, random.uniform(0, 1)),
        lambda img: add_noise(img, random.uniform(0, 1)),
        lambda img: adjust_brightness_contrast(img, random.uniform(0.5, 1.5), random.uniform(0.5, 1.5)),
        lambda img: adjust_brightness_contrast(img, random.uniform(0.5, 1.5), random.uniform(0.5, 1.5)),
        lambda img: adjust_brightness_contrast(img, random.uniform(0.5, 1.5), random.uniform(0.5, 1.5)),
        lambda img: adjust_color(img, random.uniform(0.5, 1.5)),
        lambda img: adjust_color(img, random.uniform(0.5, 1.5)),
        lambda img: adjust_color(img, random.uniform(0.5, 1.5))
    ]
    all_combinations = []
    for r in range(1, len(augmentation_functions) + 1):
        all_combinations.extend(itertools.combinations(augmentation_functions, r))

    for filename in tqdm(os.listdir(input_folder)):
        image_path = os.path.join(input_folder, filename)
        img = open_image(image_path)
        augment_counter = 0
        # img = resize(img)
        for combination in all_combinations:
            augmented_img = img.copy()
            for func in combination:
                augmented_img = func(augmented_img)
            output_path = os.path.join(
                output_folder, 
                f"image_{augment_counter}.jpg"
            )
            augmented_img.save(output_path)
            augment_counter += 1


if __name__ == '__main__':
    input_folder = "dataset/spaceship_resized"
    output_folder = "augmented_dataset/spaceship"
    augment(input_folder, output_folder)


