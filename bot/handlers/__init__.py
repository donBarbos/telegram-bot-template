from aiogram import Router


def get_handlers_router() -> Router:
    from . import export_users, info, menu, start, support

    router = Router()
    router.include_router(start.router)
    router.include_router(info.router)
    router.include_router(support.router)
    router.include_router(menu.router)
    router.include_router(export_users.router)

    return router
