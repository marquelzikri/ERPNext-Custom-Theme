import frappe
import os
import json
import re
from pathlib import Path
from os import listdir
from os.path import isfile, join

@frappe.whitelist()
def color_validation(form_data):
    def is_valid_color(doc_field):
        is_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', doc_field)
        if is_match:
            return True
        return False

    form_data = json.loads(form_data)

    fields_to_check = [
        "desk_bg",
        "primary_button_bg",
        "primary_button_hover_bg",
        "default_button_bg",
        "default_button_hover_bg",
        "navbar_bg",
        "navbar_search_bg",
    ]
    for field_name in fields_to_check:
        if not is_valid_color(form_data[field_name]):
            return {"valid": False, "message": "Field {0} have invalid hex value.".format(field_name)}

    return {"valid": True, "message": "All fields have valid hex value."}

@frappe.whitelist()
def generate_css(form_data):
    # css_files = [f for f in listdir(ct_path) if isfile(join(ct_path, f))]
    form_data = json.loads(form_data)
    
    desk_bg = form_data["desk_bg"]
    form_layout_bg = form_data["form_layout_bg"]
    
    primary_button_bg = form_data["primary_button_bg"]
    primary_button_hover_bg = form_data["primary_button_hover_bg"]
    primary_button_font_color = form_data["primary_button_font_color"]
    default_button_bg = form_data["default_button_bg"]
    default_button_hover_bg = form_data["default_button_hover_bg"]
    default_button_font_color = form_data["default_button_font_color"]
    
    navbar_bg = form_data["navbar_bg"]
    navbar_search_bg = form_data["navbar_search_bg"]

    bg_color_css = """
        #page-desktop, #body_div {{
            background-color: {0};
        }}
        
        #body_div .form-layout {{
            background-color: {1};
        }}

        .breadcrumb {{
            background-color: {0};
        }}

        .modal-backdrop {{
            background-color: {0} !important;
        }}
    """.format(desk_bg, form_layout_bg)

    btn_color_css = """
        /* .btn:hover {{
            color: #e7e7e7
        }} */

        #page-desktop .btn-primary, #body_div .btn-primary {{
            background-color: {0};
            border-color: {0};
            color: {2};
        }}

        #page-desktop .btn-primary:hover, #page-desktop .btn-primary:focus, #page-desktop .btn-primary.focus, #page-desktop .btn-primary:active, #page-desktop .btn-primary.active, #page-desktop .open > .dropdown-toggle.btn-primary, #body_div .btn-primary:hover, #body_div .btn-primary:focus, #body_div .btn-primary.focus, #body_div .btn-primary:active, #body_div .btn-primary.active, #body_div .open > .dropdown-toggle.btn-primary {{
            background-color: {1};
            border-color: {1};
        }}

        #page-desktop .btn-primary:not(:disabled):not(.disabled):active, #page-desktop .btn-primary:not(:disabled):not(.disabled).active, #page-desktop .show > .btn-primary.dropdown-toggle, #body_div .btn-primary:not(:disabled):not(.disabled):active, #body_div .btn-primary:not(:disabled):not(.disabled).active, #body_div .show > .btn-primary.dropdown-toggle {{
            background-color: {1};
            border-color: {1};
        }}

        #page-desktop .btn-primary:focus, #page-desktop .btn-primary.focus, #body_div .btn-primary:focus, #body_div .btn-primary.focus {{
            box-shadow: 0 0 0 0.1rem rgba(74, 120, 247, 0.16);
        }}

        #page-desktop .btn-default, #body_div .btn-default {{
            background-color: {3};
            border-color: {3};
            color: {5};
        }}

        #page-desktop .btn-default:hover, #page-desktop .btn-default:focus, #page-desktop .btn-default.focus, #page-desktop .btn-default:active, #page-desktop .btn-default.active, #page-desktop .open > .dropdown-toggle.btn-default, #body_div .btn-default:hover, #body_div .btn-default:focus, #body_div .btn-default.focus, #body_div .btn-default:active, #body_div .btn-default.active, #body_div .open > .dropdown-toggle.btn-default {{
            background-color: {4};
            border-color: {4};
        }}

        #page-desktop .btn-default:not(:disabled):not(.disabled):active, #page-desktop .btn-default:not(:disabled):not(.disabled).active, #page-desktop .show > .btn-default.dropdown-toggle, #body_div .btn-default:not(:disabled):not(.disabled):active, #body_div .btn-default:not(:disabled):not(.disabled).active, #body_div .show > .btn-default.dropdown-toggle {{
            background-color: {4};
            border-color: {4};
        }}
    """.format(
        primary_button_bg,
        primary_button_hover_bg,
        primary_button_font_color,
        default_button_bg,
        default_button_hover_bg,
        default_button_font_color
    )

    navbar_color_css = """
        .navbar-default {{
            background-color: {0};
            border-color: {0};
        }}

        .navbar-light {{
            background-color: {0} !important;
        }}

        #navbar-search {{
            background-color: {1};
            border: 1px solid {1};
        }}

        /* navbar ">" logo */
        #navbar-breadcrumbs > li > a:hover:before, #navbar-breadcrumbs > li > a:focus:before, #navbar-breadcrumbs > li > a:active:before {{
            color: #c7c7c7;
        }}
    """.format(navbar_bg, navbar_search_bg)

    # ct_path = /home/frappe/frappe-bench/apps/custom_theme/custom_theme/file_generator.py
    ct_path = str(Path(__file__).absolute()).replace("file_generator.py", "public/css/")

    bg_color_path = ct_path + "background_color.css"
    if os.path.exists(bg_color_path):
        os.remove(bg_color_path)
    bg_color_file = open(bg_color_path, "w+")
    bg_color_file.write(bg_color_css)
    bg_color_file.close()

    btn_color_path = ct_path + "button_color.css"
    if os.path.exists(btn_color_path):
        os.remove(btn_color_path)
    btn_color_file = open(btn_color_path, "w+")
    btn_color_file.write(btn_color_css)
    btn_color_file.close()

    navbar_color_path = ct_path + "navbar_color.css"
    if os.path.exists(navbar_color_path):
        os.remove(navbar_color_path)
    navbar_color_file = open(navbar_color_path, "w+")
    navbar_color_file.write(navbar_color_css)
    navbar_color_file.close()

    return "CSS files generated. Go to frappe bench folder and run this command: bench build --app custom_theme && bench restart <br> After that, hard refresh your browser(ctrl + shift + R)"

@frappe.whitelist()
def install_theme_icon():
    path = str(Path(__file__).absolute())
    erpnext_desktop_path = path.replace("custom_theme/custom_theme/file_generator.py", "erpnext/erpnext/config/desktop.py")
    erpnext_desktop_backup_path = path.replace("file_generator.py", "desktop.erpnext.original.bak")
    erpnext_desktop_custom_path = path.replace("file_generator.py", "desktop.erpnext")

    frappe_desktop_path = path.replace("custom_theme/custom_theme/file_generator.py", "frappe/frappe/config/desktop.py")
    frappe_desktop_backup_path = path.replace("file_generator.py", "desktop.frappe.original.bak")
    frappe_desktop_custom_path = path.replace("file_generator.py", "desktop.frappe")

    # backing up desktop.py
    erpnext_desktop = open(erpnext_desktop_path, "r")
    erpnext_desktop_backup = open(erpnext_desktop_backup_path, "w+")
    erpnext_desktop_backup.write(erpnext_desktop.read())

    frappe_desktop = open(frappe_desktop_path, "r")
    frappe_desktop_backup = open(frappe_desktop_backup_path, "w+")
    frappe_desktop_backup.write(frappe_desktop.read())

    # install custom desktop.py
    erpnext_custom = open(erpnext_desktop_custom_path, "r")
    erpnext_original = open(erpnext_desktop_path, "w+")
    erpnext_original.write(erpnext_custom.read())

    frappe_custom = open(frappe_desktop_custom_path, "r")
    frappe_original = open(frappe_desktop_path, "w+")
    frappe_original.write(frappe_custom.read())

    return str(erpnext_custom.read())
