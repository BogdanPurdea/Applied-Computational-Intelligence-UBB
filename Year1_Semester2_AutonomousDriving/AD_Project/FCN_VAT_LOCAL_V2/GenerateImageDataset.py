import os
import shutil
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from sklearn.model_selection import train_test_split


IMG_SIZE = 48
N_SAMPLES_PER_CLASS = 1000
BASE_DIR = "synthetic_dataset"
RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def reset_dir(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


def add_noise(img: Image.Image, noise_std: float = 8.0) -> Image.Image:
    arr = np.asarray(img).astype(np.float32)
    noise = np.random.normal(0, noise_std, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def random_transform(img: Image.Image) -> Image.Image:
    angle = random.uniform(-25, 25)
    img = img.rotate(angle, resample=Image.BICUBIC, fillcolor=(0, 0, 0))

    if random.random() < 0.3:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.2, 0.6)))

    img = add_noise(img, noise_std=random.uniform(3, 10))
    return img


def generate_circle_image() -> Image.Image:
    img = Image.new("RGB", (IMG_SIZE, IMG_SIZE), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = random.randint(10, 17)
    thickness = random.randint(2, 4)

    cx = random.randint(radius + 2, IMG_SIZE - radius - 3)
    cy = random.randint(radius + 2, IMG_SIZE - radius - 3)

    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]

    color = tuple(random.randint(180, 255) for _ in range(3))
    draw.ellipse(bbox, outline=color, width=thickness)

    return random_transform(img)


def generate_moon_image() -> Image.Image:
    img = Image.new("RGB", (IMG_SIZE, IMG_SIZE), (0, 0, 0))

    mask = Image.new("L", (IMG_SIZE, IMG_SIZE), 0)
    draw = ImageDraw.Draw(mask)

    radius = random.randint(11, 17)
    cx = random.randint(radius + 3, IMG_SIZE - radius - 4)
    cy = random.randint(radius + 3, IMG_SIZE - radius - 4)

    # Main white circle
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=255
    )

    # Offset black circle removes part of the first circle, creating crescent
    offset = random.randint(5, 10)
    direction = random.choice([-1, 1])

    draw.ellipse(
        [
            cx - radius + direction * offset,
            cy - radius,
            cx + radius + direction * offset,
            cy + radius
        ],
        fill=0
    )

    color = tuple(random.randint(180, 255) for _ in range(3))
    colored = Image.new("RGB", (IMG_SIZE, IMG_SIZE), color)
    img.paste(colored, mask=mask)

    return random_transform(img)


def save_split(images, class_name):
    train_imgs, test_imgs = train_test_split(
        images,
        test_size=0.2,
        random_state=RANDOM_SEED
    )

    labeled_imgs, unlabeled_imgs = train_test_split(
        train_imgs,
        train_size=0.1,
        random_state=RANDOM_SEED
    )

    for i, img in enumerate(labeled_imgs):
        img.save(f"{BASE_DIR}/labeled/{class_name}/{class_name}_{i:04d}.png")

    for i, img in enumerate(unlabeled_imgs):
        img.save(f"{BASE_DIR}/unlabeled/unlabeled_{class_name}_{i:04d}.png")

    for i, img in enumerate(test_imgs):
        img.save(f"{BASE_DIR}/test/{class_name}/{class_name}_{i:04d}.png")


def generate_image_dataset():
    reset_dir(BASE_DIR)

    folders = [
        f"{BASE_DIR}/labeled/circles",
        f"{BASE_DIR}/labeled/moons",
        f"{BASE_DIR}/unlabeled",
        f"{BASE_DIR}/test/circles",
        f"{BASE_DIR}/test/moons",
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    circle_images = [generate_circle_image() for _ in range(N_SAMPLES_PER_CLASS)]
    moon_images = [generate_moon_image() for _ in range(N_SAMPLES_PER_CLASS)]

    save_split(circle_images, "circles")
    save_split(moon_images, "moons")

    print(f"Dataset generated in '{BASE_DIR}/'")
    print("Image size: 48x48 RGB")
    print("Classes: circles, moons")
    print("Split: 10% labeled from train, 90% unlabeled from train, 20% test")


if __name__ == "__main__":
    generate_image_dataset()