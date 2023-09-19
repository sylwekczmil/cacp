import os


def is_preview():
    return os.environ.get("PREVIEW", "false") == "true"


def preview_prevent_modifications():
    if is_preview():
        raise RuntimeError("CACP is in PREVIEW mode")


def preview_button_kwargs():
    if is_preview():
        return dict(disabled=True)
    return {}
