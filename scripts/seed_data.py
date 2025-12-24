#!/usr/bin/env python3
"""
Seed script to populate initial data for MDM system.
Run this after the database is initialized.
"""
import asyncio
import sys
sys.path.insert(0, '/app')

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.security import MDMRole, MDMUser
from app.models.entity import MDMEntity, AuditLevel
from app.models.attribute import MDMAttribute, MDMAttributeGroup, DataType, UIComponent, DisplayType
from app.models.catalog import MDMCatalog, MDMCatalogValue, CatalogType


async def seed_roles(session: AsyncSession):
    """Create default roles."""
    roles = [
        MDMRole(
            role_code="ADMIN",
            role_name="Administrator",
            role_description="Full system access",
            is_system=True
        ),
        MDMRole(
            role_code="DATA_STEWARD",
            role_name="Data Steward",
            role_description="Manage master data quality and governance",
            is_system=True
        ),
        MDMRole(
            role_code="DATA_ANALYST",
            role_name="Data Analyst",
            role_description="View and analyze master data",
            is_system=True
        ),
        MDMRole(
            role_code="VIEWER",
            role_name="Viewer",
            role_description="Read-only access to master data",
            is_system=True
        ),
    ]
    session.add_all(roles)
    await session.flush()
    return roles


async def seed_users(session: AsyncSession, admin_role: MDMRole):
    """Create default admin user."""
    admin_user = MDMUser(
        username="admin",
        email="admin@mdm.local",
        full_name="System Administrator",
        hashed_password=get_password_hash("admin123"),
        role_id=admin_role.id,
        is_superuser=True
    )
    session.add(admin_user)
    await session.flush()
    return admin_user


async def seed_catalogs(session: AsyncSession):
    """Create sample catalogs."""
    # Country catalog
    country_catalog = MDMCatalog(
        catalog_code="COUNTRY",
        catalog_name="Countries",
        catalog_type=CatalogType.SIMPLE,
        is_system=True
    )
    session.add(country_catalog)
    await session.flush()

    countries = [
        MDMCatalogValue(catalog_id=country_catalog.id, value_code="MX", value_name="Mexico", sort_order=1),
        MDMCatalogValue(catalog_id=country_catalog.id, value_code="US", value_name="United States", sort_order=2),
        MDMCatalogValue(catalog_id=country_catalog.id, value_code="CA", value_name="Canada", sort_order=3),
        MDMCatalogValue(catalog_id=country_catalog.id, value_code="ES", value_name="Spain", sort_order=4),
        MDMCatalogValue(catalog_id=country_catalog.id, value_code="DE", value_name="Germany", sort_order=5),
    ]
    session.add_all(countries)

    # Status catalog
    status_catalog = MDMCatalog(
        catalog_code="RECORD_STATUS",
        catalog_name="Record Status",
        catalog_type=CatalogType.SIMPLE,
        is_system=True
    )
    session.add(status_catalog)
    await session.flush()

    statuses = [
        MDMCatalogValue(catalog_id=status_catalog.id, value_code="ACTIVE", value_name="Active", color_hex="#28a745", is_default=True),
        MDMCatalogValue(catalog_id=status_catalog.id, value_code="INACTIVE", value_name="Inactive", color_hex="#6c757d"),
        MDMCatalogValue(catalog_id=status_catalog.id, value_code="PENDING", value_name="Pending Approval", color_hex="#ffc107"),
        MDMCatalogValue(catalog_id=status_catalog.id, value_code="REJECTED", value_name="Rejected", color_hex="#dc3545"),
    ]
    session.add_all(statuses)

    # Customer type catalog
    customer_type_catalog = MDMCatalog(
        catalog_code="CUSTOMER_TYPE",
        catalog_name="Customer Types",
        catalog_type=CatalogType.SIMPLE,
        is_system=False
    )
    session.add(customer_type_catalog)
    await session.flush()

    customer_types = [
        MDMCatalogValue(catalog_id=customer_type_catalog.id, value_code="CORP", value_name="Corporate"),
        MDMCatalogValue(catalog_id=customer_type_catalog.id, value_code="SMB", value_name="Small/Medium Business"),
        MDMCatalogValue(catalog_id=customer_type_catalog.id, value_code="IND", value_name="Individual"),
        MDMCatalogValue(catalog_id=customer_type_catalog.id, value_code="GOV", value_name="Government"),
    ]
    session.add_all(customer_types)

    return country_catalog, status_catalog, customer_type_catalog


async def seed_customer_entity(session: AsyncSession, country_catalog, status_catalog, customer_type_catalog):
    """Create Customer entity with attributes."""
    # Create entity
    customer_entity = MDMEntity(
        entity_code="CUSTOMER",
        entity_name="Customers",
        entity_description="Customer master data management",
        icon_class="fa-users",
        color_hex="#007bff",
        is_hierarchical=False,
        allow_versioning=True,
        audit_level=AuditLevel.FULL,
        workflow_enabled=True
    )
    session.add(customer_entity)
    await session.flush()

    # Create attribute groups
    general_group = MDMAttributeGroup(
        entity_id=customer_entity.id,
        group_code="GENERAL",
        group_name="General Information",
        group_icon="fa-info-circle",
        display_type=DisplayType.SECTION,
        sort_order=1
    )
    contact_group = MDMAttributeGroup(
        entity_id=customer_entity.id,
        group_code="CONTACT",
        group_name="Contact Information",
        group_icon="fa-address-book",
        display_type=DisplayType.SECTION,
        sort_order=2
    )
    address_group = MDMAttributeGroup(
        entity_id=customer_entity.id,
        group_code="ADDRESS",
        group_name="Address",
        group_icon="fa-map-marker",
        display_type=DisplayType.SECTION,
        sort_order=3
    )
    session.add_all([general_group, contact_group, address_group])
    await session.flush()

    # Create attributes
    attributes = [
        # General group
        MDMAttribute(
            entity_id=customer_entity.id,
            attribute_group_id=general_group.id,
            attribute_code="customer_number",
            attribute_name="Customer Number",
            data_type=DataType.STRING,
            ui_component=UIComponent.TEXT,
            display_order=1,
            is_required=True,
            is_unique=True,
            show_in_list=True,
            is_readonly=True
        ),
        MDMAttribute(
            entity_id=customer_entity.id,
            attribute_group_id=general_group.id,
            attribute_code="customer_name",
            attribute_name="Customer Name",
            data_type=DataType.STRING,
            ui_component=UIComponent.TEXT,
            display_order=2,
            is_required=True,
            show_in_list=True
        ),
        MDMAttribute(
            entity_id=customer_entity.id,
            attribute_group_id=general_group.id,
            attribute_code="customer_type",
            attribute_name="Customer Type",
            data_type=DataType.STRING,
            ui_component=UIComponent.SELECT,
            display_order=3,
            is_required=True,
            catalog_id=customer_type_catalog.id
        ),
        MDMAttribute(
            entity_id=customer_entity.id,
            attribute_group_id=general_group.id,
            attribute_code="tax_id",
            attribute_name="Tax ID / RFC",
            data_type=DataType.STRING,
            ui_component=UIComponent.TEXT,
            display_order=4,
            is_unique=True,
            is_pii=True
        ),
        # Contact group
        MDMAttribute(
            entity_id=customer_entity.id,
            attribute_group_id=contact_group.id,
            attribute_code="email",
            attribute_name="Email",
            data_type=DataType.STRING,
            ui_component=UIComponent.EMAIL,
            display_order=5,
            is_required=True,
            show_in_list=True,
            is_pii=True
        ),
        MDMAttribute(
            entity_id=customer_entity.id,
            attribute_group_id=contact_group.id,
            attribute_code="phone",
            attribute_name="Phone",
            data_type=DataType.STRING,
            ui_component=UIComponent.TEXT,
            display_order=6,
            is_pii=True,
            placeholder="+52 (XXX) XXX-XXXX"
        ),
        MDMAttribute(
            entity_id=customer_entity.id,
            attribute_group_id=contact_group.id,
            attribute_code="contact_person",
            attribute_name="Contact Person",
            data_type=DataType.STRING,
            ui_component=UIComponent.TEXT,
            display_order=7
        ),
        # Address group
        MDMAttribute(
            entity_id=customer_entity.id,
            attribute_group_id=address_group.id,
            attribute_code="street",
            attribute_name="Street Address",
            data_type=DataType.STRING,
            ui_component=UIComponent.TEXT,
            display_order=8
        ),
        MDMAttribute(
            entity_id=customer_entity.id,
            attribute_group_id=address_group.id,
            attribute_code="city",
            attribute_name="City",
            data_type=DataType.STRING,
            ui_component=UIComponent.TEXT,
            display_order=9
        ),
        MDMAttribute(
            entity_id=customer_entity.id,
            attribute_group_id=address_group.id,
            attribute_code="country",
            attribute_name="Country",
            data_type=DataType.STRING,
            ui_component=UIComponent.SELECT,
            display_order=10,
            catalog_id=country_catalog.id
        ),
        MDMAttribute(
            entity_id=customer_entity.id,
            attribute_group_id=address_group.id,
            attribute_code="postal_code",
            attribute_name="Postal Code",
            data_type=DataType.STRING,
            ui_component=UIComponent.TEXT,
            display_order=11
        ),
    ]
    session.add_all(attributes)

    return customer_entity


async def seed_product_entity(session: AsyncSession, status_catalog):
    """Create Product entity with attributes."""
    product_entity = MDMEntity(
        entity_code="PRODUCT",
        entity_name="Products",
        entity_description="Product master data management",
        icon_class="fa-box",
        color_hex="#28a745",
        is_hierarchical=True,
        max_hierarchy_levels=3,
        allow_versioning=True,
        audit_level=AuditLevel.FULL
    )
    session.add(product_entity)
    await session.flush()

    # Create attribute groups
    general_group = MDMAttributeGroup(
        entity_id=product_entity.id,
        group_code="GENERAL",
        group_name="General Information",
        display_type=DisplayType.SECTION,
        sort_order=1
    )
    pricing_group = MDMAttributeGroup(
        entity_id=product_entity.id,
        group_code="PRICING",
        group_name="Pricing & Costs",
        display_type=DisplayType.SECTION,
        sort_order=2
    )
    session.add_all([general_group, pricing_group])
    await session.flush()

    attributes = [
        MDMAttribute(
            entity_id=product_entity.id,
            attribute_group_id=general_group.id,
            attribute_code="sku",
            attribute_name="SKU",
            data_type=DataType.STRING,
            ui_component=UIComponent.TEXT,
            display_order=1,
            is_required=True,
            is_unique=True,
            show_in_list=True
        ),
        MDMAttribute(
            entity_id=product_entity.id,
            attribute_group_id=general_group.id,
            attribute_code="product_name",
            attribute_name="Product Name",
            data_type=DataType.STRING,
            ui_component=UIComponent.TEXT,
            display_order=2,
            is_required=True,
            show_in_list=True
        ),
        MDMAttribute(
            entity_id=product_entity.id,
            attribute_group_id=general_group.id,
            attribute_code="description",
            attribute_name="Description",
            data_type=DataType.STRING,
            ui_component=UIComponent.TEXTAREA,
            display_order=3
        ),
        MDMAttribute(
            entity_id=product_entity.id,
            attribute_group_id=pricing_group.id,
            attribute_code="unit_price",
            attribute_name="Unit Price",
            data_type=DataType.DECIMAL,
            ui_component=UIComponent.NUMBER,
            display_order=4,
            is_required=True,
            show_in_list=True
        ),
        MDMAttribute(
            entity_id=product_entity.id,
            attribute_group_id=pricing_group.id,
            attribute_code="cost",
            attribute_name="Cost",
            data_type=DataType.DECIMAL,
            ui_component=UIComponent.NUMBER,
            display_order=5
        ),
    ]
    session.add_all(attributes)

    return product_entity


async def main():
    """Main seed function."""
    print("=" * 50)
    print("MDM SAP - Database Seeding")
    print("=" * 50)

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        try:
            print("\n[1/5] Creating roles...")
            roles = await seed_roles(session)
            admin_role = roles[0]
            print(f"      Created {len(roles)} roles")

            print("\n[2/5] Creating admin user...")
            admin_user = await seed_users(session, admin_role)
            print(f"      Created user: {admin_user.username}")

            print("\n[3/5] Creating catalogs...")
            country_catalog, status_catalog, customer_type_catalog = await seed_catalogs(session)
            print("      Created catalogs: COUNTRY, RECORD_STATUS, CUSTOMER_TYPE")

            print("\n[4/5] Creating Customer entity...")
            customer_entity = await seed_customer_entity(session, country_catalog, status_catalog, customer_type_catalog)
            print(f"      Created entity: {customer_entity.entity_code}")

            print("\n[5/5] Creating Product entity...")
            product_entity = await seed_product_entity(session, status_catalog)
            print(f"      Created entity: {product_entity.entity_code}")

            await session.commit()
            print("\n" + "=" * 50)
            print("Seeding completed successfully!")
            print("=" * 50)
            print("\nDefault credentials:")
            print("  Username: admin")
            print("  Password: admin123")
            print("\n")

        except Exception as e:
            await session.rollback()
            print(f"\nError during seeding: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
