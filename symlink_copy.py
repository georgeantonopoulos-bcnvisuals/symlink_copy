local_path = '/tmp/xcb_cursor_build/lib'
target_path = '/mnt/studio/pipeline/packages/xcb_util_cursor/0.1.5/lib'

import os
os.makedirs(target_path, exist_ok=True)

symlink_files = [
    'libxcb-cursor.so',
    'libxcb-cursor.so.0'
]

for symlink in symlink_files:
    symlink_path = os.path.join(local_path, symlink)
    if os.path.islink(symlink_path):
        real_file = os.readlink(symlink_path)
        real_file_path = os.path.join(local_path, real_file)
        target_file_path = os.path.join(target_path, symlink)
        with open(real_file_path, 'rb') as src:
            with open(target_file_path, 'wb') as dst:
                dst.write(src.read())

