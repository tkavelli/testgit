"""Import all routers and add them to routers_list."""
from .admin import admin_router
from .echo import echo_router
from .simple_menu import menu_router
from .user import user_router
from .diffusion import diffusion_router

routers_list = [
    admin_router,
    menu_router,
    user_router,
    diffusion_router,
    echo_router,  # echo_router must be last
]

__all__ = [
    "routers_list",
]
