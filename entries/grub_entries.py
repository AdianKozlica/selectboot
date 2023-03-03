import shlex

def format_token(token:str):
    """
        Replace one instance of { character,
        doing this because if someone used grub-customizer,
        the { would be too close to the entry name
    """
    return token.replace("{", "",1)

def get_boot_entries():
    with open("/boot/grub/grub.cfg","r") as file:
        lines = file.readlines()

    submenu_list = []
    boot_tree = {}
    in_submenu = False
    in_menu = False

    for line in lines:
        tokens = shlex.split(line)
        line = line.lstrip()

        if "}" in line:
            if in_menu:
                in_menu = False

            elif in_submenu:
                submenu_list.pop()
                if len(submenu_list) == 0:
                    in_submenu = False

        if line.startswith("submenu"):
            in_submenu = True
            submenu_list.append(format_token(tokens[1]))

        elif line.startswith("menuentry") and len(tokens) > 1:
            in_menu = True
        
            temp_tree = boot_tree.copy() 
            temp_dict = temp_tree # gonna edit the dictionary like this since they are passed with reference

            for submenu in submenu_list:
                if submenu not in temp_dict: # if key isn't in the dictionary add it
                    temp_dict[submenu] = {}

                temp_dict = temp_dict[submenu]

            temp_dict[format_token(tokens[1])] = [] # Set key value to an empty array
            boot_tree = temp_tree.copy() # set new value to boot tree

    return boot_tree