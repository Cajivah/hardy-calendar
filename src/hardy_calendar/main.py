import os

from .orchestrator import crawl_and_sync

def main() -> None:
    dry_run = os.environ.get("DRY_RUN", "0") == "1"

    crawl_and_sync(dry_run)

if __name__ == "__main__":
    main()