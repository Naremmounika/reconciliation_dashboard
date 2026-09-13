from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Location, SystemARecord, SystemBEntry
from .services.comparator import compare_records


@require_GET
def discrepancies(request):
    org_id = request.GET.get("org_id")
    if not org_id:
        return JsonResponse(
            {
                "error": "org_id query parameter is required"
            },
            status=400,
        )
    system_a_records = SystemARecord.objects.all()
    system_b_entries = SystemBEntry.objects.all()

    if org_id:
        allowed_locations = Location.objects.filter(
            org_id=org_id
        ).values_list("location_id", flat=True)

        system_a_records = system_a_records.filter(
            location_id__in=allowed_locations
        )

        system_b_entries = system_b_entries.filter(
            location_id__in=allowed_locations
        )

    results = compare_records(
        system_a_records,
        system_b_entries,
    )
    reason = request.GET.get("reason")
    location_id = request.GET.get("location_id")
    sort_by = request.GET.get("sort", "record_id")

    if reason:
        results = [
            result
            for result in results
            if result["reason"] == reason
        ]

    if location_id:
        results = [
            result
            for result in results
            if result["location_id"] == location_id
        ]

    if sort_by == "system_a_value":
        results.sort(
            key=lambda result: result["system_a_value"] or ""
        )
    elif sort_by == "system_b_value":
        results.sort(
            key=lambda result: str(result["system_b_value"] or "")
        )
    else:
        results.sort(key=lambda result: result["record_id"])

    return JsonResponse(
        {
            "count": len(results),
            "results": results,
        }
    )


@require_GET
def locations(request):
    data = list(
        Location.objects.values(
            "location_id",
            "org_id",
            "location_name",
        )
    )

    return JsonResponse(data, safe=False)