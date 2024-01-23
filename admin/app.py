# ruff: noqa: RUF012
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any

from flask import Flask, abort, redirect, render_template, request, url_for
from flask_admin import Admin, AdminIndexView, expose, helpers
from flask_admin.consts import ICON_TYPE_FONT_AWESOME
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel
from flask_caching import Cache
from flask_login import current_user
from flask_security.core import RoleMixin, Security, UserMixin
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from wtforms import PasswordField

from admin.views.users import UserView as AppUserView
from bot.database.models import UserModel as AppUserModel

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
cache = Cache(app)
babel = Babel(app)

# Define models
roles_admins = db.Table(
    "roles_admins",
    db.Column("admin_id", db.Integer(), db.ForeignKey("admin.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class RoleModel(db.Model, RoleMixin):
    __tablename__ = "role"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self) -> str:
        return self.name


class AdminModel(db.Model, UserMixin):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    fs_uniquifier = db.Column(db.String(255), unique=True)
    roles = db.relationship("RoleModel", secondary=roles_admins, backref=db.backref("admins", lazy="dynamic"))

    def __str__(self) -> str:
        return self.email


# Setup Flask-Security
admin_datastore = SQLAlchemyUserDatastore(db, AdminModel, RoleModel)
security = Security(app, admin_datastore)


# Create customized model view class
class RoleView(ModelView):
    can_delete = False
    can_edit = False
    can_create = False
    can_view_details = False
    edit_modal = True
    create_modal = True
    can_export = False
    details_modal = True

    def is_accessible(self) -> bool:
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        return bool(current_user.has_role("superuser"))

    def _handle_view(self, _name: str, **_kwargs: dict) -> Response | None:
        """Override builtin _handle_view in order to redirect users when a view is not accessible."""
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for("security.login", next=request.url))
        return None


class AdminView(RoleView):
    can_view_details = True
    can_delete = True
    can_edit = True
    can_export = True
    can_create = True
    export_types = ["csv", "xlsx", "json", "yaml"]

    column_editable_list = ["email", "first_name", "last_name"]
    column_searchable_list = column_editable_list
    column_exclude_list = ["password"]
    form_excluded_columns = ["confirmed_at"]
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list
    form_overrides = {"password": PasswordField}


# Flask views
@cache.cached()
def get_user_count() -> int:
    return db.session.query(AppUserModel).count()


@cache.cached()
def get_new_user_count(days_before: int = 1) -> int:
    period_start = datetime.now(timezone.utc) - timedelta(days=days_before)
    return db.session.query(AppUserModel).filter(AppUserModel.created_at >= period_start).count()


class CustomAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self) -> str:
        days_before: int = 1
        period_start = datetime.now(timezone.utc) - timedelta(days=days_before)
        order_count = 0
        user_count = get_user_count()
        new_user_count = get_new_user_count(days_before)

        return self.render(
            "admin/index.html",
            order_count=order_count,
            user_count=user_count,
            new_user_count=new_user_count,
            period_start=period_start,
        )


@app.route("/")
def index() -> str:
    return render_template("index.html")


# Initializing the admin panel
admin = Admin(
    app,
    name="Telegram Bot",
    base_template="my_master.html",
    index_view=CustomAdminIndexView(
        name="Home",
        url="/admin",
        menu_icon_type=ICON_TYPE_FONT_AWESOME,
        menu_icon_value="fa-home",
    ),
    template_mode="bootstrap4",
)

admin.add_view(
    AppUserView(
        AppUserModel,
        db.session,
        menu_icon_type=ICON_TYPE_FONT_AWESOME,
        menu_icon_value="fa-users",
        name="Users",
        endpoint="users",
    ),
)

admin.add_view(
    AdminView(
        AdminModel,
        db.session,
        menu_icon_type=ICON_TYPE_FONT_AWESOME,
        menu_icon_value="fa-black-tie",
        name="Admins",
        endpoint="admins",
    ),
)
admin.add_view(
    RoleView(
        RoleModel,
        db.session,
        menu_icon_type=ICON_TYPE_FONT_AWESOME,
        menu_icon_value="fa-tags",
        name="Roles",
        endpoint="roles",
    ),
)


# define a context processor for merging flask-admin's template context into the flask-security views.
@security.context_processor
def security_context_processor() -> dict[str, Any]:
    return {
        "admin_base_template": admin.base_template,
        "admin_view": admin.index_view,
        "h": helpers,
        "get_url": url_for,
    }


def init_db() -> None:
    inspector = inspect(db.engine)
    if inspector.has_table("admin") and inspector.has_table("role"):
        return

    db.create_all()

    admin_role = RoleModel(name="user", description="does not have access to other administrators")
    super_admin_role = RoleModel(name="superuser", description="has access to manage all administrators")
    db.session.add(admin_role)
    db.session.add(super_admin_role)
    db.session.commit()

    admin_datastore.create_user(
        first_name="Admin",
        email=app.config.get("DEFAULT_ADMIN_EMAIL"),
        password=hash_password(str(app.config.get("DEFAULT_ADMIN_PASSWORD"))),
        roles=[admin_role, super_admin_role],
    )

    db.session.commit()

    return


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(host=app.config.get("ADMIN_HOST"), port=app.config.get("ADMIN_PORT"), debug=app.config.get("DEBUG"))
