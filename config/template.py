# Template Settings
# ------------------------------------------------------------------------------


# Theme layout templates directory

# Template config
# ? Easily change the template configuration from here
# ? Replace this object with template-config/demo-*.py file's TEMPLATE_CONFIG to change the template configuration as per our demos
import os


TEMPLATE_CONFIG = {
    "layout": "vertical",             # Options[String]: vertical(default), horizontal
    "theme": "theme-default",         # Options[String]: theme-default(default), theme-bordered, theme-semi-dark
    "style": "light",                 # Options[String]: light(default), dark, system mode
    "rtl_support": True,              # options[Boolean]: True(default), False # To provide RTLSupport or not
    "rtl_mode": False,                # options[Boolean]: False(default), True # To set layout to RTL layout  (myRTLSupport must be True for rtl mode)
    "has_customizer": True,           # options[Boolean]: True(default), False # Display customizer or not THIS WILL REMOVE INCLUDED JS FILE. SO LOCAL STORAGE WON'T WORK
    "display_customizer": True,       # options[Boolean]: True(default), False # Display customizer UI or not, THIS WON'T REMOVE INCLUDED JS FILE. SO LOCAL STORAGE WILL WORK
    "content_layout": "compact",      # options[String]: 'compact', 'wide' (compact=container-xxl, wide=container-fluid)
    "navbar_type": "fixed",           # options[String]: 'fixed', 'static', 'hidden' (Only for vertical Layout)
    "header_type": "fixed",           # options[String]: 'static', 'fixed' (for horizontal layout only)
    "menu_fixed": True,               # options[Boolean]: True(default), False # Layout(menu) Fixed (Only for vertical Layout)
    "menu_collapsed": False,          # options[Boolean]: False(default), True # Show menu collapsed, Only for vertical Layout
    "footer_fixed": False,            # options[Boolean]: False(default), True # Footer Fixed
    "show_dropdown_onhover": True,    # True, False (for horizontal layout only)
    "customizer_controls": [
        "rtl",
        "style",
        "headerType",
        "contentLayout",
        "layoutCollapsed",
        "showDropdownOnHover",
        "layoutNavbarOptions",
        "themes",
    ],  # To show/hide customizer options
}

# Theme Variables
# ? Personalize template by changing theme variables (For ex: Name, URL Version etc...)
APP_NAME = os.getenv('APP_NAME', 'Inventory')

THEME_VARIABLES = {
    "creator_name": "Olympicson",
    "creator_url": "https://dev.subfactory.net/",
    "template_name": APP_NAME,
    "template_suffix": "Find Your Cheapest Data Package Today!",
    "template_version": "1.0.0",
    "template_free": False,
    "template_description": "We are the best",
    "template_keyword": "internet data plans, affordable data packages, cheap mobile data, data bundles for MTN, Glo, 9mobile, Airtel, mobile internet access, cheapest internet data plans, best data deals, reliable mobile internet, data subscription services, budget-friendly data options, lowest rates on mobile data, seamless connectivity, MTN data plans, Glo data bundles, 9mobile data offers, Airtel data packages, prepaid internet access, fast mobile internet, data purchase online",
    "facebook_url": "https://www.facebook.com/",
    "twitter_url": "https://twitter.com/",
    "github_url": "https://github.com/",
    "dribbble_url": "https://dribbble.com/",
    "instagram_url": "https://www.instagram.com/",
    "license_url": "https://themeforest.net/licenses/standard",
    "live_preview": "https://dev.subfactory.net",
    "product_page": "https://1.envato.market/",
    "support": "https://dev.subfactory.net/",
    "more_themes": "https://1.envato.market/",
    "documentation": "https://dev.subfactory.net/",
    "changelog": "https://dev.subfactory.net/",
    "git_repository": "https://dev.subfactory.net/",
    "git_repo_access": "https://dev.subfactory.net/",
}

# ! Don't change THEME_LAYOUT_DIR unless it's required
THEME_LAYOUT_DIR = "layout"
