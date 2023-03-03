import re
import subprocess

def get_entries():
    with subprocess.Popen(["efibootmgr"],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL) as proc:
        stdout,stderr = proc.communicate()
        stdout = stdout.decode()

    entries = re.findall(r"^Boot[0-9].*$",stdout,re.MULTILINE) # find boot indexes
    entry_dict = {}

    for entry in entries:
        boot_index,boot_name = entry.split(' ',1)
        
        for key,value in (("Boot",""),("*","")):
            boot_index = boot_index.replace(key,value) 

        entry_dict[boot_name] = boot_index

    return entry_dict
