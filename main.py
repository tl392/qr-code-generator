import argparse
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import qrcode

load_dotenv()
LOG_DIR = os.getenv("LOG_PATH", "logs")
QR_DIR = os.getenv("QR_PATH", "qr_codes")


def setup_directories() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(QR_DIR, exist_ok=True)


def setup_logging() -> None:
    logging.basicConfig(
        filename=os.path.join(LOG_DIR, "app.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def generate_qr(url: str) -> str:
    img = qrcode.make(url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"qr_{timestamp}.png"
    filepath = os.path.join(QR_DIR, filename)
    img.save(filepath)
    logging.info("QR code generated for %s -> %s", url, filepath)
    return filepath


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="QR Code Generator")
    parser.add_argument(
        "--url",
        default=os.getenv("DEFAULT_URL", "https://www.njit.edu"),
        help="URL to generate QR code for",
    )
    return parser.parse_args()


def main() -> None:
    setup_directories()
    setup_logging()
    args = parse_args()

    try:
        filepath = generate_qr(args.url)
        print(f"QR code saved to {filepath}")
    except Exception as exc:
        logging.exception("Failed to generate QR code")
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()