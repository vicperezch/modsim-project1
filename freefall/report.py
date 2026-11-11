def _format(value):
    if value is None:
        return "-"
    if isinstance(value, float):
        if abs(value) >= 1000:
            return f"{value:.0f}"
        if value == 0 or abs(value) >= 1:
            return f"{value:.3f}"
        return f"{value:.4g}"
    return str(value)


def _columns(rows):
    columns = []
    for row in rows:
        columns.extend(k for k in row if k not in columns)
    return columns


def to_text(rows):
    columns = _columns(rows)
    cells = [[_format(row.get(c)) for c in columns] for row in rows]
    widths = [max(len(c), *(len(r[i]) for r in cells)) for i, c in enumerate(columns)]
    lines = ["  ".join(c.ljust(w) for c, w in zip(columns, widths))]
    lines.append("  ".join("-" * w for w in widths))
    lines.extend("  ".join(v.rjust(w) for v, w in zip(r, widths)) for r in cells)
    return "\n".join(lines)
