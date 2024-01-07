from pathlib import Path


ZIP_DIR           = Path("zip")
VIDEOS_DIR        = Path("videos")
VIDEOS_ZIP_DIR    = Path(ZIP_DIR, VIDEOS_DIR)
IMAGES_DIR        = Path("images")
IMAGES_ZIP_DIR    = Path(ZIP_DIR, IMAGES_DIR)

CUSTOM_VIDEO_PATH = Path(VIDEOS_DIR, "crop3.mp4")
CROP1_VIDEO_PATH  = Path(VIDEOS_DIR, "crop1.mp4")
CROP2_VIDEO_PATH  = Path(VIDEOS_DIR, "crop2.mp4")

GOOGLE_DRIVE_LINK = "https://drive.google.com/uc?id={0}"
LINK_CUSTOM_ZIP   = GOOGLE_DRIVE_LINK.format("1orsUuSHidM9-aHLWZvJQsjcr9zHMiadg")
LINK_VIDEOS_ZIP   = GOOGLE_DRIVE_LINK.format("12ZTjcM-YhjACSPYsJF1QGP6m9IxyYPWq")
LINK_IMAGES_ZIP   = GOOGLE_DRIVE_LINK.format("1FlmfAu7MaUQ4Mb0-IShb9XiLFCqJs0xB")