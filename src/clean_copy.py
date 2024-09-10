# I would like to apologize for everything that follows. This could have been made way simpler,
# but the course I was doing this for specifically wanted this code to be this mess instead of
# something nice and simple. I did the best I could.

import os
import shutil

def clean_copy(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    for filename in os.listdir(source):
        source_path = os.path.join(source, filename)
        dest_path = os.path.join(destination, filename)
        print(f" * Copying from {source_path} to {dest_path}")
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            clean_copy(source_path, dest_path)