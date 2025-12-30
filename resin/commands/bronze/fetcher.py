import json
import time
from collections.abc import Generator
from datetime import datetime

from sqlalchemy import Connection

from resin.api_client import ApiClient, Entity, EntitySet, api_entities
from resin.bronze import api_entity, api_page, create_tables, tracker
from resin.database.engine import get_engine

# Configuration constants
RATE_LIMIT_DELAY = 0.8


class ProgressTracker:
    """Progress tracker for fetcher2."""

    def __init__(self, conn: Connection):
        self.conn = conn

    def get_total_pages(self, entity: str) -> int | None:
        """Get total pages for an entity."""
        result = self.conn.execute(tracker.entity_total_pages(entity)).fetchone()
        return result[0] if result else None

    def is_last_page(self, entity: str, page: int) -> bool:
        """Check if we've reached the last page for an entity."""
        total_pages = self.get_total_pages(entity)
        return total_pages is not None and page >= total_pages

    def mark_complete(self, entity: str, timestamp: datetime) -> None:
        """Mark an entity as complete."""
        self.conn.execute(tracker.entity_complete(entity, timestamp))
        self.conn.commit()

    def update_progress(
        self, entity: str, page: int, total_pages: int | None = None
    ) -> None:
        """Update progress for an entity."""
        self.conn.execute(tracker.entity_upsert(entity, page, total_pages))

    def get_entity_status(self, entity: str) -> tuple[int, str] | None:
        """Get the current status for an entity."""
        result = self.conn.execute(tracker.entity_status(entity)).fetchone()
        return tuple(result) if result else None

    def format_progress(
        self, entity: str, page: int, total_pages: int | None, timestamp: datetime
    ) -> str:
        """Format progress information."""
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"{timestamp_str} - {entity}: Page {page}/{total_pages}"


class FetchManager:
    def __init__(
        self,
        conn: Connection,
        entity: Entity,
        api_client: ApiClient,
        progress: ProgressTracker,
    ):
        self.conn = conn
        self.entity = entity
        self.api_client = api_client
        self.progress = progress

    def fetch_entity_page(self, page: int, timestamp: datetime) -> None:
        """Fetch a single page using ApiClient."""
        parsed_data = self.api_client.fetch_page(self.entity.api_path, page)

        total_pages = parsed_data.get("totalPages")
        raw_data = json.dumps(parsed_data.get(self.entity.name, []))

        if self.conn.in_transaction():
            self.conn.commit()

        with self.conn.begin():
            stmt = api_page.entity_insert(self.entity.name, page, raw_data)
            self.conn.execute(stmt)

            self.progress.update_progress(self.entity.name, page, total_pages)

    def fetch_entity(self, start_page: int) -> Generator[str, None, None]:
        """Fetch all pages for the entity starting from start_page."""
        page = start_page
        total_pages = self.progress.get_total_pages(self.entity.name)

        while True:
            timestamp = datetime.now()

            if self.progress.is_last_page(self.entity.name, page):
                self.progress.mark_complete(self.entity.name, timestamp)
                break

            try:
                self.fetch_entity_page(page, timestamp)

                if total_pages is None:
                    total_pages = self.progress.get_total_pages(self.entity.name)

                yield self.progress.format_progress(
                    self.entity.name, page, total_pages, timestamp
                )
                page += 1
                time.sleep(RATE_LIMIT_DELAY)

            except Exception as e:
                yield f"Failed to fetch {self.entity.name} page {page}: {e}"
                break


def setup_database(conn: Connection, entities: EntitySet) -> None:
    """Initialize the database with necessary tables and configurations."""
    create_tables(conn)
    conn.execute(api_entity.insert_all(entities))


def fetch_all_entities(
    conn: Connection, entities: EntitySet, api_client: ApiClient
) -> Generator[str, None, None]:
    progress = ProgressTracker(conn)

    for entity in sorted(entities, key=lambda e: e.name):
        fetch_manager = FetchManager(conn, entity, api_client, progress)
        status = progress.get_entity_status(entity.name)

        if status is None:
            yield from fetch_manager.fetch_entity(1)
        else:
            page, status_value = status
            if status_value == "incomplete":
                yield from fetch_manager.fetch_entity(page + 1)
            elif status_value == "complete":
                yield f"No more work for {entity.name}."
            else:
                yield f"Skipping {entity.name} due to unknown status"


def main(suffix: str | None = None) -> Generator[str, None, None]:
    engine = get_engine(suffix)
    api_client = ApiClient()

    try:
        with engine.connect() as conn:
            setup_database(conn, api_entities)
            yield from fetch_all_entities(conn, api_entities, api_client)
    finally:
        api_client.close()
