from app.core.database import SessionLocal
from app.models.category import Category
from app.models.product import Product


def seed_data():
    db = SessionLocal()

    try:
        # -------- Categories --------
        existing_cat1 = db.query(Category).filter_by(name="Electronics").first()
        if not existing_cat1:
            category1 = Category(name="Electronics", description="Electronic items")
            db.add(category1)
            db.commit()
            db.refresh(category1)
        else:
            category1 = existing_cat1

        existing_cat2 = db.query(Category).filter_by(name="Clothing").first()
        if not existing_cat2:
            category2 = Category(name="Clothing", description="Fashion and clothes")
            db.add(category2)
            db.commit()
            db.refresh(category2)
        else:
            category2 = existing_cat2

        # -------- Products --------
        existing_product1 = db.query(Product).filter_by(name="Laptop").first()
        if not existing_product1:
            product1 = Product(
                name="Laptop",
                description="Gaming laptop",
                price=1500,
                stock=10,
                category_id=category1.id
            )
            db.add(product1)

        existing_product2 = db.query(Product).filter_by(name="T-Shirt").first()
        if not existing_product2:
            product2 = Product(
                name="T-Shirt",
                description="Cotton t-shirt",
                price=20,
                stock=50,
                category_id=category2.id
            )
            db.add(product2)

        db.commit()

        print(" Seed data inserted successfully!")

    except Exception as e:
        db.rollback()
        print(f" Error: {str(e)}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()