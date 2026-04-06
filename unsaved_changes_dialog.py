from tkinter import TclError, messagebox


def _get_tk_text(text_edit):
    return text_edit._textbox if hasattr(text_edit, "_textbox") else text_edit


def has_unsaved_changes(text_edit):
    tk_text = _get_tk_text(text_edit)
    try:
        return bool(tk_text.edit_modified())
    except TclError:
        return False


def mark_document_clean(text_edit):
    tk_text = _get_tk_text(text_edit)
    try:
        tk_text.edit_modified(False)
    except TclError:
        pass


def confirm_unsaved_changes(parent, text_edit, save_callback, action_name="close"):
    if not has_unsaved_changes(text_edit):
        return True

    prompt = f"You have unsaved changes. Save before {action_name}?"
    choice = messagebox.askyesnocancel("Unsaved Changes", prompt, parent=parent)

    if choice is None:
        return False

    if choice:
        return bool(save_callback())

    return True
