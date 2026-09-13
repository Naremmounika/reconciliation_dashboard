from decimal import Decimal, InvalidOperation

from reconciler.models import SystemARecord, SystemBEntry


def normalize_reference(value):
    return "".join(
        character.lower()
        for character in str(value or "")
        if character.isalnum()
    )


def normalize_value(value):
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, ValueError, TypeError):
        return None


def compare_records(system_a_records, system_b_entries):
    results = []

    system_a_by_reference = {
        normalize_reference(record.record_id): record
        for record in system_a_records
    }

    system_b_by_reference = {}

    for entry in system_b_entries:
        reference = normalize_reference(entry.record_ref)

        if reference not in system_b_by_reference:
            system_b_by_reference[reference] = []

        system_b_by_reference[reference].append(entry)

    for record in system_a_records:
        reference = normalize_reference(record.record_id)
        matching_entries = system_b_by_reference.get(reference, [])

        if not matching_entries:
            results.append(
                {
                    "record_id": record.record_id,
                    "location_id": record.location_id,
                    "reason": "MISSING_IN_B",
                    "system_a_value": record.total_value,
                    "system_b_value": None,
                }
            )
            continue

        if len(matching_entries) > 1:
            results.append(
                {
                    "record_id": record.record_id,
                    "location_id": record.location_id,
                    "reason": "DUPLICATE_IN_B",
                    "system_a_value": record.total_value,
                    "system_b_value": [
                        entry.value for entry in matching_entries
                    ],
                }
            )

        for entry in matching_entries:
            system_a_value = normalize_value(record.total_value)
            system_b_value = normalize_value(entry.value)

            if system_a_value != system_b_value:
                results.append(
                    {
                        "record_id": record.record_id,
                        "location_id": record.location_id,
                        "reason": "VALUE_MISMATCH",
                        "system_a_value": record.total_value,
                        "system_b_value": entry.value,
                    }
                )

    for entry in system_b_entries:
        reference = normalize_reference(entry.record_ref)

        if reference not in system_a_by_reference:
            results.append(
                {
                    "record_id": entry.record_ref,
                    "location_id": entry.location_id,
                    "reason": "ORPHAN_IN_B",
                    "system_a_value": None,
                    "system_b_value": entry.value,
                }
            )

    return results