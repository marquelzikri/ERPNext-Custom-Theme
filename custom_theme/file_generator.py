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
    
    primary_button_bg = form_data["primary_button_bg"]
    primary_button_hover_bg = form_data["primary_button_hover_bg"]
    default_button_bg = form_data["default_button_bg"]
    default_button_hover_bg = form_data["default_button_hover_bg"]
    
    navbar_bg = form_data["navbar_bg"]
    navbar_search_bg = form_data["navbar_search_bg"]

    bg_color_css = """
        body {{
            background-color: {0};
        }}

        .breadcrumb {{
            background-color: {0};
        }}

        .modal-backdrop {{
            background-color: {0} !important;
        }}
    """.format(desk_bg)

    btn_color_css = """
        /* .btn:hover {{
            color: #e7e7e7
        }} */

        .btn-primary {{
            background-color: {0};
            border-color: {0};
        }}

        .btn-primary:hover, .btn-primary:focus, .btn-primary.focus, .btn-primary:active, .btn-primary.active, .open>.dropdown-toggle.btn-primary {{
            background-color: {1};
            border-color: {1};
        }}

        .btn-primary:not(:disabled):not(.disabled):active, .btn-primary:not(:disabled):not(.disabled).active, .show>.btn-primary.dropdown-toggle {{
            background-color: {1};
            border-color: {1};
        }}

        .btn-primary:focus, .btn-primary.focus {{
            box-shadow: 0 0 0 0.1rem rgba(74, 120, 247, 0.16);
        }}

        .btn-default {{
            background-color: {2};
            border-color: {2};
        }}

        .btn-default:hover, .btn-default:focus, .btn-default.focus, .btn-default:active, .btn-default.active, .open>.dropdown-toggle.btn-default {{
            background-color: {3};
            border-color: {3};
        }}

        .btn-default:not(:disabled):not(.disabled):active, .btn-default:not(:disabled):not(.disabled).active, .show>.btn-default.dropdown-toggle {{
            background-color: {3};
            border-color: {3};
        }}
    """.format(
        primary_button_bg,
        primary_button_hover_bg,
        default_button_bg,
        default_button_hover_bg
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

    return "CSS files generated."
