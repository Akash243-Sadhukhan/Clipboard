
import threading
import sys
import traceback
def print_active_threads():
    if not hasattr(sys, "_current_frames"):
        print("[DEBUG] sys._current_frames not available on this Python build.")
        return

    frames = sys._current_frames()
    print("[DEBUG] Active Threads:")
    for thr in threading.enumerate():
        frame = frames.get(thr.ident)
        print(f"\n--- Stack for Thread: {thr.name} (id={thr.ident}) ---")
        if frame is not None:
            traceback.print_stack(frame)
        else:
            print("  - no frame available for this thread")


print_active_threads()