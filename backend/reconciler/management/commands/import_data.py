
import csv
import re
from pathlib import Path

from django.core.management.base import BaseCommand

from reconciler.models import Location, SystemARecord, SystemBEntry


def normalize_reference(value):
    """Convert references such as REC-1001 to rec1001."""
    if not value:
        return ""

    return re.sub(r"[^a-zA-Z0-9]", "", str(value)).lower()


class Command(BaseCommand):
    help = "Import System A, System B and location CSV files."

    def handle(self, *args, **options):
        # Project root: reconciliation-engine/
        base_dir = Path(__file__).resolve().parents[4]
        data_dir = base_dir / "data"

        locations_file = data_dir / "locations.csv"
        system_a_file = data_dir / "system_a.csv"
        system_b_file = data_dir / "system_b.csv"

        self.stdout.write("Starting CSV import...")

        # 1. Import locations
        location_count = 0

        with open(locations_file, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                location_id = (row.get("location_id") or "").strip()

                if not location_id:
                    self.stdout.write(
                        self.style.WARNING(
                            "Skipped location row without location_id"
                        )
                    )
                    continue

                Location.objects.update_or_create(
                    location_id=location_id,
                    defaults={
                        "org_id": (row.get("org_id") or "").strip(),
                        "location_name": (
                            row.get("location_name") or ""
                        ).strip(),
                    },
                )

                location_count += 1

        # 2. Import System A
        system_a_count = 0

        with open(system_a_file, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                record_id = (row.get("record_id") or "").strip()

                if not record_id:
                    self.stdout.write(
                        self.style.WARNING(
                            "Skipped System A row without record_id"
                        )
                    )
                    continue

                SystemARecord.objects.update_or_create(
                    record_id=record_id,
                    defaults={
                        "location_id": (
                            row.get("location_id") or ""
                        ).strip(),
                        "event_date": (
                            row.get("event_date") or ""
                        ).strip(),
                        "category_code": (
                            row.get("category_code") or ""
                        ).strip(),
                        "actor_id": (
                            row.get("actor_id") or ""
                        ).strip(),
                        "base_value": row.get("base_value") or "",
                        "adjustment": row.get("adjustment") or "",
                        "total_value": row.get("total_value") or "",
                        "state": (row.get("state") or "").strip(),
                    },
                )

                system_a_count += 1

        # 3. Import System B
        system_b_count = 0

        with open(system_b_file, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                entry_id = (row.get("entry_id") or "").strip()

                if not entry_id:
                    self.stdout.write(
                        self.style.WARNING(
                            "Skipped System B row without entry_id"
                        )
                    )
                    continue

                record_ref = (row.get("record_ref") or "").strip()

                SystemBEntry.objects.update_or_create(
                    entry_id=entry_id,
                    defaults={
                        "record_ref": record_ref,
                        "normalized_record_ref": normalize_reference(
                            record_ref
                        ),
                        "location_id": (
                            row.get("location_id") or ""
                        ).strip(),
                        "recorded_on": (
                            row.get("recorded_on") or ""
                        ).strip(),
                        "value": row.get("value") or "",
                        "label": row.get("label") or "",
                    },
                )

                system_b_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed successfully!\n"
                f"Locations: {location_count}\n"
                f"System A records: {system_a_count}\n"
                f"System B entries: {system_b_count}"
            )
        )