import time
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlencode, urlunparse

from sqlalchemy import (
    Connection,
    text,
)

from resin.bronze import create_tables, api_page, tracker
from resin.database.engine import get_engine

# Configuration constants
RATE_LIMIT_DELAY = 0.8
RETRY_DELAY = 300
MAX_RETRIES = 3


@dataclass
class Entity:
    name: str
    api_path: str


type EntitySet = list[Entity]

api_entities: EntitySet = [
    Entity("fund", "funds"),
    Entity("project", "projects"),
    Entity("person", "persons"),
    Entity("organisation", "organisations"),
    Entity("artisticandcreativeproduct", "outcomes/artisticandcreativeproducts"),
    Entity("collaboration", "outcomes/collaborations"),
    Entity("dissemination", "outcomes/disseminations"),
    # WARN: the response is missing an R so we use "futherfunding" rather than "furtherfunding"
    Entity("futherfunding", "outcomes/furtherfundings"),
    Entity("impactsummary", "outcomes/impactsummaries"),
    Entity("intellectualproperty", "outcomes/intellectualproperties"),
    Entity("keyfinding", "outcomes/keyfindings"),
    Entity("policyinfluence", "outcomes/policyinfluences"),
    Entity("product", "outcomes/products"),
    Entity("researchdatabaseandmodel", "outcomes/researchdatabaseandmodels"),
    Entity("researchmaterial", "outcomes/researchmaterials"),
    Entity(
        "softwareandtechnicalproduct",
        "outcomes/softwareandtechnicalproducts",
    ),
    Entity("spinout", "outcomes/spinouts"),
    Entity("publication", "outcomes/publications"),
]


def make_url(api_path: str, page: int) -> str:
    """Helper function to compose URLs for the GTR API."""
    return urlunparse(
        (
            "https",
            "gtr.ukri.org",
            f"/gtr/api/{api_path}",
            "",
            urlencode({"p": page, "s": 100}),
            "",
        )
    )


class ProgressTracker:
    """Handles progress tracking and status updates."""

    def __init__(self, conn: Connection):
        self.conn = conn

    def get_total_pages(self, entity: str) -> int | None:
        """Get total pages for an entity."""
        result = self.conn.execute(api_page.entity_total_pages(entity)).fetchone()
        return result[0] if result else None

    def is_last_page(self, entity: str, page: int) -> bool:
        """Check if we've reached the last page for an entity."""
        total_pages = self.get_total_pages(entity)
        return total_pages is not None and page > total_pages

    def mark_complete(self, entity: str, timestamp: datetime) -> None:
        """Mark an entity as complete."""
        self.conn.execute(tracker.entity_complete(entity, timestamp))
        self.conn.commit()

    def update_progress(self, entity: str, page: int, timestamp: datetime) -> None:
        """Update progress for an entity."""
        self.conn.execute(tracker.entity_upsert(entity, page, timestamp))

    def get_entity_status(self, entity: str) -> tuple[int, str] | None:
        """Get the current status for an entity."""
        result = self.conn.execute(tracker.entity_status(entity)).fetchone()

        if result is None:
            return None

        return tuple(result)

    def log_progress(
        self, entity: str, page: int, total_pages: int | None, timestamp: datetime
    ) -> None:
        """Log progress information."""
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp_str} - {entity}: Page {page}/{total_pages}")


class ErrorHandler:
    """Handles different types of errors during fetching."""

    def __init__(self):
        self.retry_count = 0

    def reset(self):
        """Reset retry count on successful page fetch."""
        self.retry_count = 0

    def handle_error(self, error: Exception) -> None:
        """
        Handle an error. Raises exception if max retries exceeded.
        """
        if self.retry_count >= MAX_RETRIES:
            raise Exception(f"Max retries ({MAX_RETRIES}) exceeded")

        self.retry_count += 1
        error_str = str(error)

        if "429" in error_str:
            print(
                f"Rate limit exceeded. Waiting for {RETRY_DELAY} seconds (retry {self.retry_count}/{MAX_RETRIES})"
            )
            time.sleep(RETRY_DELAY)
        elif "503" in error_str:
            print(
                f"Service unavailable. Waiting for {RETRY_DELAY} seconds (retry {self.retry_count}/{MAX_RETRIES})"
            )
            time.sleep(RETRY_DELAY)
        else:
            raise error


@dataclass
class FetchServices:
    progress: ProgressTracker
    error_handler: ErrorHandler


class FetchManager:
    """Manages the overall fetching process for a single entity."""

    def __init__(self, conn: Connection, entity: Entity, services: FetchServices):
        self.conn = conn
        self.entity = entity
        self.services = services

    def fetch_entity_page(self, page: int, timestamp: datetime) -> None:
        """Fetch a single page of data for the entity."""
        current_url = make_url(self.entity.api_path, page)

        if self.conn.in_transaction():
            self.conn.commit()

        with self.conn.begin():
            stmt = api_page.entity_insert(self.entity.name, current_url, timestamp)
            self.conn.execute(stmt)

            self.services.progress.update_progress(self.entity.name, page, timestamp)

    def fetch_entity(self, start_page: int) -> None:
        """Fetch all pages for the entity starting from start_page."""
        page = start_page
        total_pages = self.services.progress.get_total_pages(self.entity.name)

        while True:
            timestamp = datetime.now()

            if self.services.progress.is_last_page(self.entity.name, page):
                self.services.progress.mark_complete(self.entity.name, timestamp)
                break

            try:
                self.fetch_entity_page(page, timestamp)
                self.services.error_handler.reset()

                if total_pages is None:
                    total_pages = self.services.progress.get_total_pages(
                        self.entity.name
                    )

                self.services.progress.log_progress(
                    self.entity.name, page, total_pages, timestamp
                )
                page += 1
                time.sleep(RATE_LIMIT_DELAY)

            except Exception as e:
                self.services.error_handler.handle_error(e)


def setup_database(conn: Connection):
    """Initialize the database with necessary tables and configurations."""
    # Create bronze tables
    create_tables(conn)

    conn.execute(
        text("""
        CREATE SECRET IF NOT EXISTS http (
            TYPE http,
            EXTRA_HTTP_HEADERS map {
                'Accept': 'application/json'
            }
        );
    """)
    )
    conn.commit()


def fetch_all_entities(conn: Connection, entities: EntitySet):
    services = FetchServices(ProgressTracker(conn), ErrorHandler())

    for entity_config in sorted(entities, key=lambda e: e.name):
        fetch_manager = FetchManager(conn, entity_config, services)
        status = services.progress.get_entity_status(entity_config.name)

        if status is None:
            fetch_manager.fetch_entity(1)
        else:
            page, status_value = status
            if status_value == "incomplete":
                fetch_manager.fetch_entity(page + 1)
            elif status_value == "complete":
                print(f"No more work for {entity_config.name}.")
            else:
                print(f"Skipping {entity_config.name} due to unknown status")


def main():
    engine = get_engine()
    with engine.connect() as conn:
        setup_database(conn)
        fetch_all_entities(conn, api_entities)
