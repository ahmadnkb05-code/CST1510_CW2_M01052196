def row_to_dict(row):
    """Convert a sqlite3.Row to a plain dict."""
    if row is None:
        return {}
    try:
        return dict(row)
    except Exception:
        return {k: row[k] for k in row.keys()}
