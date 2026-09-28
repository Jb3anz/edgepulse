"""Persistent node identity stored in the user's app-data directory."""

import json
import logging
import uuid

from platformdirs import user_data_path

APP_NAME = "EdgePulse"
DATA_DIR = user_data_path(APP_NAME, appauthor=False)
IDENTITY_FILE = DATA_DIR / "identity.json"

logger = logging.getLogger("edgepulse.identity")


def get_node_id() -> str:
    """Return this node's stable UUID, creating and saving it on first run."""
    if IDENTITY_FILE.exists():
        try:
            data = json.loads(IDENTITY_FILE.read_text(encoding="utf-8"))
            node_id = data.get("node_id")
            if isinstance(node_id, str) and node_id:
                return node_id
        except (json.JSONDecodeError, OSError, AttributeError):
            logger.warning("Identity file unreadable; generating a new node id")

    node_id = str(uuid.uuid4())
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        IDENTITY_FILE.write_text(
            json.dumps({"node_id": node_id}, indent=2), encoding="utf-8"
        )
    except OSError:
        logger.warning("Could not persist node id; it will change on restart")
    return node_id
