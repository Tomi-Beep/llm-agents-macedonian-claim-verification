"""First practice step: look up one official census record by ID."""

records = {
    "census-total": "На Пописот од 2021 година биле попишани вкупно 2.097.319 лица.",
    "census-residents": "На Пописот од 2021 година биле попишани 1.836.713 резидентни жители.",
}


def open_record(records, source_id):
    return records.get(source_id)


print("Резидентно население:", open_record(records, "census-residents"))
print("Непознат запис:", open_record(records, "unknown-record"))
