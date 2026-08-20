"""create ecommerce schema

Revision ID: e6e2a228aef8
Revises: 01265cd54d0f
Create Date: 2026-08-19 23:58:30.089489

"""
from typing import Sequence, Union

from alembic import op  # type: ignore
import sqlalchemy as sa  # type: ignore


# revision identifiers, used by Alembic.
revision: str = 'e6e2a228aef8'
down_revision: Union[str, Sequence[str], None] = '01265cd54d0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Convert order_date from VARCHAR to TIMESTAMP
    op.alter_column(
        "orders",
        "order_date",
        existing_type=sa.VARCHAR(),
        type_=sa.DateTime(),
        existing_nullable=False,
        postgresql_using="order_date::timestamp",
    )

    # Convert order_total from INTEGER to NUMERIC
    op.alter_column(
        "orders",
        "order_total",
        existing_type=sa.INTEGER(),
        type_=sa.Numeric(12, 2),
        existing_nullable=False,
    )

    # Replace existing unique constraint with unique index
    op.drop_constraint(
        "orders_order_id_key",
        "orders",
        type_="unique",
    )

    op.create_index(
        "ix_orders_order_id",
        "orders",
        ["order_id"],
        unique=True,
    )

    # Add customer foreign key
    op.create_foreign_key(
        "fk_orders_customer_id_customers",
        "orders",
        "customers",
        ["customer_id"],
        ["id"],
    )

    # Add category safely for existing products
    op.add_column(
        "products",
        sa.Column("category", sa.String(), nullable=True),
    )

    # Give existing products a default category
    op.execute(
        "UPDATE products SET category = 'Uncategorized' "
        "WHERE category IS NULL"
    )

    # Make category mandatory
    op.alter_column(
        "products",
        "category",
        existing_type=sa.String(),
        nullable=False,
    )

    # Convert product price to NUMERIC
    op.alter_column(
        "products",
        "price",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        type_=sa.Numeric(10, 2),
        existing_nullable=False,
    )

    # Create order_items table
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("subtotal", sa.Numeric(12, 2), nullable=False),

        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
            name="fk_order_items_order_id_orders",
        ),

        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name="fk_order_items_product_id_products",
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_order_items_id",
        "order_items",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        "ix_order_items_id",
        table_name="order_items",
    )

    op.drop_table("order_items")

    op.alter_column(
        "products",
        "price",
        existing_type=sa.Numeric(10, 2),
        type_=sa.DOUBLE_PRECISION(precision=53),
        existing_nullable=False,
    )

    op.drop_column("products", "category")

    op.drop_constraint(
        "fk_orders_customer_id_customers",
        "orders",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_orders_order_id",
        table_name="orders",
    )

    op.create_unique_constraint(
        "orders_order_id_key",
        "orders",
        ["order_id"],
    )

    op.alter_column(
        "orders",
        "order_total",
        existing_type=sa.Numeric(12, 2),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )

    op.alter_column(
        "orders",
        "order_date",
        existing_type=sa.DateTime(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
