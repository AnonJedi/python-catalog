# coding=utf-8
from application.db_helper import get_db, \
    convert_to_integer
from application.models import Admin, Category, Product


class AdminService:

    @staticmethod
    def check_admin_login(username, password):
        admin = Admin.query.filter(Admin.username == username).first()
        if admin:
            return admin.check_password(password)
        return False


class CategoryService:

    @staticmethod
    def get_all_categories():
        categories = Category.query.all()
        return categories or []

    @staticmethod
    def get_category_by_id(category_id):
        return Category.query.filter(Category.id == category_id).first()

    @staticmethod
    def update_category_by_id(category_id, new_title):
        session = get_db()
        old_category = Category.query.filter(Category.id == category_id).first()
        if old_category:
            old_category.title = new_title
            session.commit()
            return True
        else:
            return False

    @staticmethod
    def delete_category_by_id(category_id):
        session = get_db()
        category = Category.query.filter(Category.id == category_id).first()
        products = Product.query\
            .filter(Product.category_id == category_id).all()
        if not category:
            return 'Category is not found'
        elif products:
            return 'This category contains some products'
        session.delete(category)

    @staticmethod
    def create_new_category(category_title):
        category_exists = Category.query\
            .filter(Category.title == category_title).all()
        if category_exists:
            return 'Category with this title already exists'
        session = get_db()
        session.add(Category(category_title))


PRODUCTS_PER_PAGE = 4


class ProductService:

    @staticmethod
    def get_categories_and_products_by_category_id(
            category_id, page_number):
        categories = CategoryService.get_all_categories()
        total_products = Product.query\
            .filter(Product.category_id == category_id).count()
        total_pages = total_products / PRODUCTS_PER_PAGE \
            if total_products % PRODUCTS_PER_PAGE == 0 else \
            int(total_products / PRODUCTS_PER_PAGE) + 1
        if page_number > total_pages:
            return None
        products = Product\
            .query.filter(Product.category_id == category_id)\
            .limit(PRODUCTS_PER_PAGE)\
            .offset(PRODUCTS_PER_PAGE * (page_number - 1)).all()
        return {
            'categories': categories,
            'total_pages': total_pages,
            'products': products
        }

    @staticmethod
    def get_all_products():
        return Product.query.all() or []

    @staticmethod
    def create_new_product(product):
        session = get_db()
        session.add(
            Product(product['title'], product['description'],
                    convert_to_integer(product['price']),
                    product['category_id'])
        )

    @staticmethod
    def get_categories_and_product_by_product_id(product_id):
        categories = Category.query.all()
        product = Product.query.filter(Product.id == product_id).first()
        return categories or [], product

    @staticmethod
    def update_product_by_product_id(product_id, new_product):
        old_product = Product.query.filter(Product.id == product_id).first()
        if not old_product:
            return 'Product is not found'
        old_product.title = new_product['title']
        old_product.price = convert_to_integer(new_product['price'])
        old_product.description = new_product['description']
        old_product.category_id = new_product['category_id']
        session = get_db()
        session.commit()

    @staticmethod
    def delete_product_by_id(product_id):
        product = Product.query.filter(Product.id == product_id).first()
        if not product:
            return 'Product is not found'

        session = get_db()
        session.delete(product)
        session.commit()
