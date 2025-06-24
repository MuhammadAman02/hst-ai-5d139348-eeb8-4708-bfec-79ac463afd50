"""
Luxury Watch E-commerce Store
A professional e-commerce application for luxury watches with catalog, cart, and checkout.
"""
import os
from nicegui import ui, app
import uvicorn
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import random
from datetime import datetime
from typing import List, Dict, Optional, Any
import asyncio

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
Base = declarative_base()
engine = create_engine("sqlite:///watches.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define models
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    brand = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(255), nullable=False)
    stock = Column(Integer, default=10)
    features = Column(Text, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize session state
@app.middleware('before_request')
def init_session():
    if not hasattr(app.storage.user, 'cart'):
        app.storage.user.cart = []
    if not hasattr(app.storage.user, 'cart_total'):
        app.storage.user.cart_total = 0.0

# Sample data initialization
def initialize_sample_data():
    db = SessionLocal()
    # Check if we already have products
    if db.query(Product).count() == 0:
        # Watch categories
        categories = ["Luxury", "Chronograph", "Dive", "Dress", "Smart"]
        
        # Watch brands
        brands = ["Rolex", "Omega", "Tag Heuer", "Patek Philippe", "Audemars Piguet", 
                 "Seiko", "Citizen", "Breitling", "Cartier", "IWC"]
        
        # Watch features
        feature_options = [
            "Automatic movement", "Swiss made", "Sapphire crystal", 
            "Water resistant to 100m", "Chronograph function",
            "Date display", "Power reserve indicator", "GMT function",
            "Ceramic bezel", "Luminous hands", "Titanium case",
            "Perpetual calendar", "Tourbillon", "Moon phase display"
        ]
        
        # Sample watches
        watches = [
            {
                "name": "Submariner Date",
                "brand": "Rolex",
                "category": "Dive",
                "price": 9950.00,
                "description": "The Rolex Submariner Date is a reference among diving watches. Waterproof to a depth of 300 meters, this iconic timepiece combines technical performance and elegant design.",
                "image_url": f"https://source.unsplash.com/800x800/?luxury,dive,watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 5))
            },
            {
                "name": "Speedmaster Professional",
                "brand": "Omega",
                "category": "Chronograph",
                "price": 6250.00,
                "description": "The Omega Speedmaster Professional, also known as the 'Moonwatch', is a manual-winding chronograph that was worn during the first American spacewalk and the first lunar landing.",
                "image_url": f"https://source.unsplash.com/800x800/?chronograph,watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 5))
            },
            {
                "name": "Royal Oak",
                "brand": "Audemars Piguet",
                "category": "Luxury",
                "price": 25000.00,
                "description": "The Audemars Piguet Royal Oak is a true icon in the world of luxury watches. Its octagonal bezel with exposed screws and integrated bracelet revolutionized the industry when it was introduced in 1972.",
                "image_url": f"https://source.unsplash.com/800x800/?luxury,watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 5))
            },
            {
                "name": "Carrera Calibre 16",
                "brand": "Tag Heuer",
                "category": "Chronograph",
                "price": 4350.00,
                "description": "The TAG Heuer Carrera Calibre 16 is a sporty chronograph inspired by motor racing. It features a tachymeter scale on the bezel and three subdials for precise timing.",
                "image_url": f"https://source.unsplash.com/800x800/?chronograph,racing,watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 5))
            },
            {
                "name": "Nautilus",
                "brand": "Patek Philippe",
                "category": "Luxury",
                "price": 35000.00,
                "description": "The Patek Philippe Nautilus is one of the most sought-after luxury sports watches in the world. Its distinctive porthole-shaped case and horizontal embossed dial make it instantly recognizable.",
                "image_url": f"https://source.unsplash.com/800x800/?luxury,watch,nautilus&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 5))
            },
            {
                "name": "Presage Cocktail Time",
                "brand": "Seiko",
                "category": "Dress",
                "price": 425.00,
                "description": "The Seiko Presage Cocktail Time features a stunning sunburst dial inspired by the art of cocktail making. It offers exceptional value with its in-house automatic movement and elegant design.",
                "image_url": f"https://source.unsplash.com/800x800/?dress,watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 4))
            },
            {
                "name": "Navitimer B01 Chronograph",
                "brand": "Breitling",
                "category": "Chronograph",
                "price": 8500.00,
                "description": "The Breitling Navitimer is a pilot's chronograph with a circular slide rule bezel for performing various calculations related to airborne navigation. It's been a favorite among aviators since 1952.",
                "image_url": f"https://source.unsplash.com/800x800/?pilot,chronograph,watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 5))
            },
            {
                "name": "Tank Solo",
                "brand": "Cartier",
                "category": "Dress",
                "price": 2740.00,
                "description": "The Cartier Tank Solo continues the legacy of the iconic Tank watch, first created in 1917. Its rectangular case and clean dial epitomize elegant simplicity.",
                "image_url": f"https://source.unsplash.com/800x800/?cartier,watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 3))
            },
            {
                "name": "Portugieser Chronograph",
                "brand": "IWC",
                "category": "Chronograph",
                "price": 7600.00,
                "description": "The IWC Portugieser Chronograph is known for its clean dial design with applied Arabic numerals and a thin bezel that maximizes the dial opening. It's a sophisticated timepiece with a sporty character.",
                "image_url": f"https://source.unsplash.com/800x800/?iwc,chronograph,watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 4))
            },
            {
                "name": "Prospex Diver",
                "brand": "Seiko",
                "category": "Dive",
                "price": 1200.00,
                "description": "The Seiko Prospex Diver, affectionately known as the 'Turtle' due to its cushion-shaped case, is a professional diving watch with 200m water resistance and Seiko's reliable automatic movement.",
                "image_url": f"https://source.unsplash.com/800x800/?dive,watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 4))
            },
            {
                "name": "Seamaster Diver 300M",
                "brand": "Omega",
                "category": "Dive",
                "price": 5200.00,
                "description": "The Omega Seamaster Diver 300M gained worldwide fame as James Bond's watch. It features a wave-patterned dial, a helium escape valve, and exceptional water resistance.",
                "image_url": f"https://source.unsplash.com/800x800/?omega,dive,watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 5))
            },
            {
                "name": "Datejust 41",
                "brand": "Rolex",
                "category": "Dress",
                "price": 8500.00,
                "description": "The Rolex Datejust is the archetype of the classic watch. Introduced in 1945, it was the first self-winding waterproof chronometer wristwatch to display the date in a window at 3 o'clock on the dial.",
                "image_url": f"https://source.unsplash.com/800x800/?rolex,watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, 4))
            }
        ]
        
        # Generate additional watches to have a good catalog
        for i in range(8):
            brand = random.choice(brands)
            category = random.choice(categories)
            price_tier = random.choice([1, 2, 3, 4, 5])
            base_price = price_tier * 1000
            price = base_price + random.randint(0, 9) * 100 + random.randint(0, 9) * 10
            
            watch = {
                "name": f"{brand} {category} {random.choice(['Classic', 'Elite', 'Master', 'Pro', 'Limited'])}",
                "brand": brand,
                "category": category,
                "price": price,
                "description": f"A beautiful {category.lower()} watch from {brand}, featuring premium materials and expert craftsmanship. This timepiece combines elegant design with reliable performance.",
                "image_url": f"https://source.unsplash.com/800x800/?{category.lower()},watch&sig={random.randint(1, 1000)}",
                "features": ", ".join(random.sample(feature_options, random.randint(3, 5)))
            }
            watches.append(watch)
        
        # Add all watches to the database
        for watch_data in watches:
            watch = Product(**watch_data)
            db.add(watch)
        
        db.commit()
    db.close()

# Initialize sample data
initialize_sample_data()

# Helper functions
def get_all_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

def get_products_by_category(category: str):
    db = SessionLocal()
    products = db.query(Product).filter(Product.category == category).all()
    db.close()
    return products

def get_products_by_brand(brand: str):
    db = SessionLocal()
    products = db.query(Product).filter(Product.brand == brand).all()
    db.close()
    return products

def get_product_by_id(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    return product

def get_unique_categories():
    db = SessionLocal()
    categories = [category[0] for category in db.query(Product.category).distinct()]
    db.close()
    return categories

def get_unique_brands():
    db = SessionLocal()
    brands = [brand[0] for brand in db.query(Product.brand).distinct()]
    db.close()
    return brands

def format_price(price: float) -> str:
    return f"${price:,.2f}"

def add_to_cart(product_id: int, quantity: int = 1):
    product = get_product_by_id(product_id)
    if not product:
        return False
    
    # Check if product is already in cart
    for item in app.storage.user.cart:
        if item['id'] == product_id:
            item['quantity'] += quantity
            app.storage.user.cart_total += product.price * quantity
            return True
    
    # Add new product to cart
    cart_item = {
        'id': product.id,
        'name': product.name,
        'brand': product.brand,
        'price': product.price,
        'image_url': product.image_url,
        'quantity': quantity
    }
    app.storage.user.cart.append(cart_item)
    app.storage.user.cart_total += product.price * quantity
    return True

def remove_from_cart(product_id: int):
    for i, item in enumerate(app.storage.user.cart):
        if item['id'] == product_id:
            app.storage.user.cart_total -= item['price'] * item['quantity']
            app.storage.user.cart.pop(i)
            return True
    return False

def update_cart_quantity(product_id: int, quantity: int):
    if quantity <= 0:
        return remove_from_cart(product_id)
    
    for item in app.storage.user.cart:
        if item['id'] == product_id:
            app.storage.user.cart_total -= item['price'] * item['quantity']
            item['quantity'] = quantity
            app.storage.user.cart_total += item['price'] * quantity
            return True
    return False

def clear_cart():
    app.storage.user.cart = []
    app.storage.user.cart_total = 0.0

# UI Components
def create_header():
    with ui.header().classes('bg-black text-white'):
        with ui.row().classes('w-full items-center justify-between q-px-lg'):
            ui.label('LUXURY TIMEPIECES').classes('text-2xl font-bold cursor-pointer').on('click', lambda: ui.open('/'))
            
            with ui.row().classes('items-center'):
                ui.button('Home', on_click=lambda: ui.open('/')).classes('text-white bg-transparent')
                ui.button('Shop', on_click=lambda: ui.open('/shop')).classes('text-white bg-transparent')
                ui.button('About', on_click=lambda: ui.open('/about')).classes('text-white bg-transparent')
                ui.button('Contact', on_click=lambda: ui.open('/contact')).classes('text-white bg-transparent')
                
                with ui.button(on_click=lambda: ui.open('/cart')).classes('text-white bg-transparent q-ml-md'):
                    ui.icon('shopping_cart')
                    cart_count = ui.label(str(sum(item['quantity'] for item in app.storage.user.cart))).classes('text-xs bg-primary text-white rounded-full absolute px-1 -top-1 -right-1 min-w-4 h-4 flex items-center justify-center')
                    
                    def update_cart_count():
                        cart_count.text = str(sum(item['quantity'] for item in app.storage.user.cart))
                    
                    ui.timer(1, update_cart_count)

def create_footer():
    with ui.footer().classes('bg-black text-white p-8'):
        with ui.row().classes('w-full justify-between'):
            with ui.column().classes('w-1/4'):
                ui.label('LUXURY TIMEPIECES').classes('text-xl font-bold mb-4')
                ui.label('Curating the finest watches from around the world since 1985.')
                
            with ui.column().classes('w-1/4'):
                ui.label('SHOP').classes('text-lg font-bold mb-4')
                for category in get_unique_categories():
                    ui.link(category, f'/category/{category}').classes('block mb-2 text-white hover:text-primary')
                
            with ui.column().classes('w-1/4'):
                ui.label('INFORMATION').classes('text-lg font-bold mb-4')
                ui.link('About Us', '/about').classes('block mb-2 text-white hover:text-primary')
                ui.link('Contact', '/contact').classes('block mb-2 text-white hover:text-primary')
                ui.link('Shipping & Returns', '#').classes('block mb-2 text-white hover:text-primary')
                ui.link('Privacy Policy', '#').classes('block mb-2 text-white hover:text-primary')
                
            with ui.column().classes('w-1/4'):
                ui.label('CONTACT US').classes('text-lg font-bold mb-4')
                ui.label('123 Luxury Lane')
                ui.label('New York, NY 10001')
                ui.label('info@luxurytimepieces.com')
                ui.label('+1 (800) 555-1234')
                
        with ui.row().classes('w-full justify-center mt-8 pt-8 border-t border-gray-700'):
            ui.label(f'© {datetime.now().year} Luxury Timepieces. All rights reserved.').classes('text-sm')

def create_product_card(product):
    with ui.card().classes('w-full h-full product-card'):
        ui.image(product.image_url).classes('w-full h-48 object-cover')
        with ui.card_section():
            ui.label(product.brand).classes('text-sm text-gray-500')
            ui.label(product.name).classes('text-lg font-bold')
            ui.label(format_price(product.price)).classes('text-primary font-bold')
            
            with ui.row().classes('justify-between items-center mt-4'):
                ui.button('View Details', on_click=lambda p=product: ui.open(f'/product/{p.id}')).classes('bg-black text-white')
                ui.button(on_click=lambda p=product: add_to_cart_with_notification(p.id)).props('flat round color=primary').classes('ml-2').\
                    on('click', lambda: ui.notify('Added to cart', color='positive')).tooltip('Add to Cart').add(ui.icon('add_shopping_cart'))

def add_to_cart_with_notification(product_id: int):
    success = add_to_cart(product_id)
    if success:
        product = get_product_by_id(product_id)
        ui.notify(f'{product.name} added to cart', color='positive')
    else:
        ui.notify('Failed to add product to cart', color='negative')

# Page definitions
@ui.page('/')
def home_page():
    create_header()
    
    # Hero section
    with ui.column().classes('w-full relative'):
        ui.image('https://source.unsplash.com/1600x800/?luxury,watch,collection&sig=1').classes('w-full h-[500px] object-cover')
        with ui.column().classes('absolute inset-0 flex items-center justify-center text-center text-white bg-black bg-opacity-50 p-8'):
            ui.label('TIMELESS ELEGANCE').classes('text-5xl font-bold mb-4')
            ui.label('Discover our collection of luxury timepieces').classes('text-2xl mb-8')
            ui.button('SHOP NOW', on_click=lambda: ui.open('/shop')).classes('bg-primary text-white px-8 py-4 text-lg')
    
    # Featured categories
    with ui.column().classes('py-16 px-8 bg-white'):
        ui.label('FEATURED CATEGORIES').classes('text-3xl font-bold text-center mb-12')
        
        with ui.row().classes('w-full justify-center gap-8'):
            for category in get_unique_categories()[:3]:
                with ui.card().classes('w-1/4 category-card'):
                    ui.image(f'https://source.unsplash.com/800x600/?{category.lower()},watch&sig={random.randint(1, 1000)}').classes('w-full h-64 object-cover')
                    with ui.card_section().classes('text-center'):
                        ui.label(category.upper()).classes('text-xl font-bold')
                        ui.button('SHOP NOW', on_click=lambda c=category: ui.open(f'/category/{c}')).classes('bg-black text-white mt-4')
    
    # Featured products
    with ui.column().classes('py-16 px-8 bg-gray-100'):
        ui.label('FEATURED WATCHES').classes('text-3xl font-bold text-center mb-12')
        
        with ui.grid(columns=4).classes('gap-8'):
            for product in get_all_products()[:8]:
                create_product_card(product)
    
    # Brand showcase
    with ui.column().classes('py-16 px-8 bg-white'):
        ui.label('PRESTIGIOUS BRANDS').classes('text-3xl font-bold text-center mb-12')
        
        with ui.row().classes('w-full justify-center gap-12 flex-wrap'):
            for brand in get_unique_brands()[:6]:
                with ui.column().classes('items-center brand-card'):
                    ui.image(f'https://source.unsplash.com/300x200/?{brand.lower()},logo&sig={random.randint(1, 1000)}').classes('w-32 h-32 object-contain grayscale hover:grayscale-0 transition-all duration-300')
                    ui.label(brand.upper()).classes('text-lg font-bold mt-4')
    
    # Testimonials
    with ui.column().classes('py-16 px-8 bg-gray-900 text-white'):
        ui.label('WHAT OUR CUSTOMERS SAY').classes('text-3xl font-bold text-center mb-12')
        
        with ui.row().classes('w-full justify-center gap-8'):
            for i in range(3):
                with ui.card().classes('w-1/4 bg-gray-800 text-white'):
                    with ui.card_section().classes('text-center'):
                        ui.icon('format_quote').classes('text-4xl text-primary')
                        ui.label('The quality and craftsmanship of my new watch is exceptional. The online shopping experience was seamless.').classes('my-4 italic')
                        ui.label(['John Doe', 'Jane Smith', 'Robert Johnson'][i]).classes('font-bold')
                        ui.label(['New York, NY', 'Los Angeles, CA', 'Chicago, IL'][i]).classes('text-sm text-gray-400')
    
    # Newsletter
    with ui.column().classes('py-16 px-8 bg-primary text-white text-center'):
        ui.label('JOIN OUR NEWSLETTER').classes('text-3xl font-bold mb-4')
        ui.label('Subscribe to receive updates on new arrivals and special promotions').classes('mb-8')
        
        with ui.row().classes('w-full max-w-lg mx-auto'):
            email_input = ui.input(placeholder='Your email address').classes('w-3/4')
            ui.button('SUBSCRIBE', on_click=lambda: ui.notify('Thank you for subscribing!', color='positive')).classes('bg-black text-white w-1/4')
    
    create_footer()

@ui.page('/shop')
def shop_page():
    create_header()
    
    with ui.column().classes('p-8'):
        ui.label('ALL WATCHES').classes('text-3xl font-bold mb-8')
        
        with ui.row().classes('w-full gap-8'):
            # Filters sidebar
            with ui.column().classes('w-1/4'):
                ui.label('FILTER BY').classes('text-xl font-bold mb-4')
                
                ui.label('CATEGORIES').classes('font-bold mt-4 mb-2')
                for category in get_unique_categories():
                    ui.link(category, f'/category/{category}').classes('block mb-2 hover:text-primary')
                
                ui.label('BRANDS').classes('font-bold mt-6 mb-2')
                for brand in get_unique_brands():
                    ui.link(brand, f'/brand/{brand}').classes('block mb-2 hover:text-primary')
                
                ui.label('PRICE RANGE').classes('font-bold mt-6 mb-2')
                price_ranges = [
                    ('Under $1,000', '0-1000'),
                    ('$1,000 - $5,000', '1000-5000'),
                    ('$5,000 - $10,000', '5000-10000'),
                    ('$10,000 - $20,000', '10000-20000'),
                    ('$20,000+', '20000-999999')
                ]
                for label, range_val in price_ranges:
                    ui.link(label, f'/price-range/{range_val}').classes('block mb-2 hover:text-primary')
            
            # Products grid
            with ui.column().classes('w-3/4'):
                with ui.grid(columns=3).classes('gap-8'):
                    for product in get_all_products():
                        create_product_card(product)
    
    create_footer()

@ui.page('/product/{product_id}')
def product_page(product_id: int):
    create_header()
    
    product = get_product_by_id(product_id)
    if not product:
        with ui.column().classes('p-16 text-center'):
            ui.label('Product not found').classes('text-2xl font-bold')
            ui.button('Back to Shop', on_click=lambda: ui.open('/shop')).classes('bg-primary text-white mt-4')
        create_footer()
        return
    
    with ui.column().classes('p-8'):
        # Breadcrumb
        with ui.row().classes('mb-8 text-sm'):
            ui.link('Home', '/').classes('text-gray-500 hover:text-primary')
            ui.label('>').classes('mx-2 text-gray-500')
            ui.link('Shop', '/shop').classes('text-gray-500 hover:text-primary')
            ui.label('>').classes('mx-2 text-gray-500')
            ui.link(product.category, f'/category/{product.category}').classes('text-gray-500 hover:text-primary')
            ui.label('>').classes('mx-2 text-gray-500')
            ui.label(product.name).classes('text-gray-700')
        
        with ui.row().classes('gap-8'):
            # Product images
            with ui.column().classes('w-1/2'):
                ui.image(product.image_url).classes('w-full h-[500px] object-cover rounded-lg shadow-lg')
                
                # Additional images (simulated)
                with ui.row().classes('mt-4 gap-4'):
                    for i in range(3):
                        ui.image(f"https://source.unsplash.com/400x400/?{product.category.lower()},watch&sig={random.randint(1, 1000)}").classes('w-1/3 h-24 object-cover rounded cursor-pointer hover:opacity-80')
            
            # Product details
            with ui.column().classes('w-1/2'):
                ui.label(product.brand).classes('text-xl text-gray-500')
                ui.label(product.name).classes('text-3xl font-bold')
                ui.label(format_price(product.price)).classes('text-2xl text-primary font-bold mt-4')
                
                ui.separator().classes('my-6')
                
                ui.label('DESCRIPTION').classes('font-bold')
                ui.label(product.description).classes('mt-2 text-gray-700')
                
                if product.features:
                    ui.label('FEATURES').classes('font-bold mt-6')
                    with ui.column().classes('mt-2'):
                        for feature in product.features.split(', '):
                            with ui.row().classes('items-center mb-1'):
                                ui.icon('check').classes('text-primary mr-2')
                                ui.label(feature).classes('text-gray-700')
                
                ui.separator().classes('my-6')
                
                with ui.row().classes('items-center gap-4'):
                    quantity = ui.number(value=1, min=1, max=product.stock).classes('w-20')
                    ui.button('ADD TO CART', on_click=lambda: add_to_cart_with_notification(product.id)).classes('bg-primary text-white px-8')
                
                ui.label(f'In Stock: {product.stock}').classes('text-sm text-gray-500 mt-4')
                
                ui.separator().classes('my-6')
                
                with ui.row().classes('gap-4'):
                    with ui.row().classes('items-center'):
                        ui.icon('local_shipping').classes('mr-2')
                        ui.label('Free shipping on orders over $500')
                    
                    with ui.row().classes('items-center'):
                        ui.icon('verified').classes('mr-2')
                        ui.label('Authenticity guaranteed')
        
        # Related products
        with ui.column().classes('mt-16'):
            ui.label('YOU MAY ALSO LIKE').classes('text-2xl font-bold mb-8')
            
            with ui.grid(columns=4).classes('gap-8'):
                related_products = get_products_by_category(product.category)
                for related in related_products:
                    if related.id != product.id:
                        create_product_card(related)
                        if len(related_products) <= 4:
                            break
    
    create_footer()

@ui.page('/category/{category}')
def category_page(category: str):
    create_header()
    
    products = get_products_by_category(category)
    
    with ui.column().classes('p-8'):
        ui.label(f'{category.upper()} WATCHES').classes('text-3xl font-bold mb-8')
        
        if not products:
            ui.label('No products found in this category.').classes('text-xl text-center w-full py-16')
        else:
            with ui.grid(columns=4).classes('gap-8'):
                for product in products:
                    create_product_card(product)
    
    create_footer()

@ui.page('/brand/{brand}')
def brand_page(brand: str):
    create_header()
    
    products = get_products_by_brand(brand)
    
    with ui.column().classes('p-8'):
        ui.label(f'{brand.upper()}').classes('text-3xl font-bold mb-8')
        
        if not products:
            ui.label('No products found for this brand.').classes('text-xl text-center w-full py-16')
        else:
            with ui.grid(columns=4).classes('gap-8'):
                for product in products:
                    create_product_card(product)
    
    create_footer()

@ui.page('/price-range/{range_val}')
def price_range_page(range_val: str):
    create_header()
    
    min_price, max_price = map(int, range_val.split('-'))
    
    db = SessionLocal()
    products = db.query(Product).filter(Product.price >= min_price, Product.price <= max_price).all()
    db.close()
    
    range_label = f"Under ${min_price:,}" if min_price == 0 else f"${min_price:,} - ${max_price:,}" if max_price < 999999 else f"${min_price:,}+"
    
    with ui.column().classes('p-8'):
        ui.label(f'WATCHES: {range_label}').classes('text-3xl font-bold mb-8')
        
        if not products:
            ui.label('No products found in this price range.').classes('text-xl text-center w-full py-16')
        else:
            with ui.grid(columns=4).classes('gap-8'):
                for product in products:
                    create_product_card(product)
    
    create_footer()

@ui.page('/cart')
def cart_page():
    create_header()
    
    with ui.column().classes('p-8'):
        ui.label('YOUR SHOPPING CART').classes('text-3xl font-bold mb-8')
        
        if not app.storage.user.cart:
            with ui.column().classes('text-center py-16'):
                ui.label('Your cart is empty').classes('text-xl mb-4')
                ui.button('CONTINUE SHOPPING', on_click=lambda: ui.open('/shop')).classes('bg-primary text-white')
        else:
            with ui.column().classes('w-full'):
                # Cart items
                with ui.column().classes('w-full'):
                    with ui.row().classes('w-full font-bold p-4 bg-gray-100'):
                        ui.label('Product').classes('w-1/2')
                        ui.label('Price').classes('w-1/6 text-center')
                        ui.label('Quantity').classes('w-1/6 text-center')
                        ui.label('Total').classes('w-1/6 text-center')
                        ui.label('').classes('w-12')
                    
                    for item in app.storage.user.cart:
                        with ui.row().classes('w-full items-center p-4 border-b'):
                            with ui.row().classes('w-1/2 items-center'):
                                ui.image(item['image_url']).classes('w-16 h-16 object-cover mr-4')
                                with ui.column():
                                    ui.label(item['name']).classes('font-bold')
                                    ui.label(item['brand']).classes('text-sm text-gray-500')
                            
                            ui.label(format_price(item['price'])).classes('w-1/6 text-center')
                            
                            with ui.row().classes('w-1/6 justify-center'):
                                quantity_input = ui.number(value=item['quantity'], min=1).classes('w-16 text-center')
                                
                                async def update_quantity(e, item_id=item['id']):
                                    await asyncio.sleep(0.5)  # Debounce
                                    update_cart_quantity(item_id, int(quantity_input.value))
                                    cart_summary.refresh()
                                
                                quantity_input.on('change', update_quantity)
                            
                            ui.label(format_price(item['price'] * item['quantity'])).classes('w-1/6 text-center')
                            
                            ui.button(on_click=lambda item_id=item['id']: remove_item_and_refresh(item_id)).props('flat round color=negative icon=delete').classes('w-12')
                
                # Cart summary
                with ui.card().classes('w-full mt-8 p-6'):
                    @ui.refreshable
                    def cart_summary():
                        with ui.column().classes('w-full'):
                            with ui.row().classes('w-full justify-between mb-2'):
                                ui.label('Subtotal:').classes('font-bold')
                                ui.label(format_price(app.storage.user.cart_total)).classes('font-bold')
                            
                            with ui.row().classes('w-full justify-between mb-2'):
                                ui.label('Shipping:').classes('font-bold')
                                shipping = 0 if app.storage.user.cart_total >= 500 else 25
                                ui.label('Free' if shipping == 0 else format_price(shipping)).classes('font-bold')
                            
                            with ui.row().classes('w-full justify-between mb-2'):
                                ui.label('Tax:').classes('font-bold')
                                tax = app.storage.user.cart_total * 0.08  # 8% tax
                                ui.label(format_price(tax)).classes('font-bold')
                            
                            ui.separator().classes('my-4')
                            
                            with ui.row().classes('w-full justify-between mb-4'):
                                ui.label('Total:').classes('text-xl font-bold')
                                total = app.storage.user.cart_total + shipping + tax
                                ui.label(format_price(total)).classes('text-xl font-bold text-primary')
                            
                            with ui.row().classes('w-full justify-between'):
                                ui.button('CONTINUE SHOPPING', on_click=lambda: ui.open('/shop')).classes('bg-gray-800 text-white')
                                ui.button('PROCEED TO CHECKOUT', on_click=lambda: ui.open('/checkout')).classes('bg-primary text-white')
                    
                    cart_summary()
                
                def remove_item_and_refresh(item_id):
                    remove_from_cart(item_id)
                    cart_summary.refresh()
                    if not app.storage.user.cart:
                        ui.open('/cart')  # Refresh the page if cart is empty
    
    create_footer()

@ui.page('/checkout')
def checkout_page():
    create_header()
    
    if not app.storage.user.cart:
        ui.open('/cart')
        return
    
    with ui.column().classes('p-8'):
        ui.label('CHECKOUT').classes('text-3xl font-bold mb-8')
        
        with ui.row().classes('w-full gap-8'):
            # Customer information
            with ui.column().classes('w-2/3'):
                ui.label('SHIPPING INFORMATION').classes('text-xl font-bold mb-4')
                
                with ui.grid(columns=2).classes('gap-4 mb-6'):
                    ui.input('First Name').props('outlined required').classes('w-full')
                    ui.input('Last Name').props('outlined required').classes('w-full')
                    ui.input('Email Address').props('outlined required type=email').classes('w-full')
                    ui.input('Phone Number').props('outlined required').classes('w-full')
                    ui.input('Address Line 1').props('outlined required').classes('w-full').style('grid-column: span 2')
                    ui.input('Address Line 2').props('outlined').classes('w-full').style('grid-column: span 2')
                    ui.input('City').props('outlined required').classes('w-full')
                    ui.select(['Select State', 'California', 'New York', 'Texas', 'Florida'], value='Select State').props('outlined required').classes('w-full')
                    ui.input('ZIP Code').props('outlined required').classes('w-full')
                    ui.select(['United States', 'Canada', 'United Kingdom', 'Australia'], value='United States').props('outlined required').classes('w-full')
                
                ui.label('PAYMENT INFORMATION').classes('text-xl font-bold mt-8 mb-4')
                
                with ui.grid(columns=2).classes('gap-4'):
                    ui.input('Card Number').props('outlined required mask=#### #### #### ####').classes('w-full').style('grid-column: span 2')
                    ui.input('Cardholder Name').props('outlined required').classes('w-full').style('grid-column: span 2')
                    ui.input('Expiration Date').props('outlined required placeholder="MM/YY" mask=##/##').classes('w-full')
                    ui.input('CVV').props('outlined required mask=###').classes('w-full')
            
            # Order summary
            with ui.column().classes('w-1/3'):
                with ui.card().classes('w-full p-6'):
                    ui.label('ORDER SUMMARY').classes('text-xl font-bold mb-4')
                    
                    for item in app.storage.user.cart:
                        with ui.row().classes('w-full justify-between mb-2'):
                            ui.label(f"{item['name']} (x{item['quantity']})").classes('text-sm')
                            ui.label(format_price(item['price'] * item['quantity'])).classes('text-sm font-bold')
                    
                    ui.separator().classes('my-4')
                    
                    with ui.row().classes('w-full justify-between mb-2'):
                        ui.label('Subtotal:')
                        ui.label(format_price(app.storage.user.cart_total))
                    
                    with ui.row().classes('w-full justify-between mb-2'):
                        ui.label('Shipping:')
                        shipping = 0 if app.storage.user.cart_total >= 500 else 25
                        ui.label('Free' if shipping == 0 else format_price(shipping))
                    
                    with ui.row().classes('w-full justify-between mb-2'):
                        ui.label('Tax:')
                        tax = app.storage.user.cart_total * 0.08  # 8% tax
                        ui.label(format_price(tax))
                    
                    ui.separator().classes('my-4')
                    
                    with ui.row().classes('w-full justify-between mb-4'):
                        ui.label('Total:').classes('font-bold')
                        total = app.storage.user.cart_total + shipping + tax
                        ui.label(format_price(total)).classes('font-bold text-primary')
                    
                    ui.button('PLACE ORDER', on_click=place_order).classes('w-full bg-primary text-white')

def place_order():
    # In a real application, this would process the payment and create an order
    # For this demo, we'll just clear the cart and show a confirmation
    order_number = f"ORD-{random.randint(100000, 999999)}"
    clear_cart()
    ui.open(f'/order-confirmation/{order_number}')

@ui.page('/order-confirmation/{order_number}')
def order_confirmation_page(order_number: str):
    create_header()
    
    with ui.column().classes('p-16 text-center'):
        ui.icon('check_circle').classes('text-6xl text-green-500 mb-4')
        ui.label('ORDER CONFIRMED').classes('text-3xl font-bold mb-4')
        ui.label(f'Thank you for your purchase! Your order number is {order_number}.').classes('text-xl mb-8')
        ui.label('We have sent a confirmation email with your order details.').classes('mb-8')
        
        ui.button('CONTINUE SHOPPING', on_click=lambda: ui.open('/')).classes('bg-primary text-white px-8')
    
    create_footer()

@ui.page('/about')
def about_page():
    create_header()
    
    with ui.column().classes('p-8'):
        # Hero section
        with ui.column().classes('w-full relative mb-16'):
            ui.image('https://source.unsplash.com/1600x800/?watchmaker,workshop&sig=2').classes('w-full h-[400px] object-cover')
            with ui.column().classes('absolute inset-0 flex items-center justify-center text-center text-white bg-black bg-opacity-50 p-8'):
                ui.label('OUR STORY').classes('text-5xl font-bold mb-4')
                ui.label('Passionate about timepieces since 1985').classes('text-2xl')
        
        # About content
        with ui.row().classes('gap-16 mb-16'):
            with ui.column().classes('w-1/2'):
                ui.label('OUR HERITAGE').classes('text-3xl font-bold mb-6')
                ui.label('Founded in 1985 by master watchmaker Thomas Laurent, Luxury Timepieces began as a small repair shop in New York City. With a passion for precision and craftsmanship, Thomas quickly gained a reputation for his exceptional work and deep knowledge of horology.').classes('mb-4')
                ui.label('As the business grew, Thomas began curating a collection of the world\'s finest watches, establishing relationships with prestigious manufacturers and developing an eye for exceptional timepieces. Today, Luxury Timepieces is recognized globally as a premier destination for watch enthusiasts and collectors.').classes('mb-4')
                ui.label('While we have expanded to multiple locations and a robust online presence, our commitment to quality, authenticity, and customer service remains unchanged. Each watch in our collection is carefully selected and authenticated by our team of experts.').classes('mb-4')
            
            with ui.column().classes('w-1/2'):
                ui.image('https://source.unsplash.com/800x600/?watchmaker,craftsman&sig=3').classes('w-full h-[400px] object-cover rounded-lg shadow-lg')
        
        # Our values
        with ui.column().classes('mb-16 bg-gray-100 p-16'):
            ui.label('OUR VALUES').classes('text-3xl font-bold text-center mb-12')
            
            with ui.grid(columns=3).classes('gap-8'):
                with ui.card().classes('p-8 text-center'):
                    ui.icon('verified').classes('text-4xl text-primary mb-4')
                    ui.label('AUTHENTICITY').classes('text-xl font-bold mb-4')
                    ui.label('Every timepiece in our collection is meticulously authenticated by our expert team. We guarantee the provenance and authenticity of each watch we sell.')
                
                with ui.card().classes('p-8 text-center'):
                    ui.icon('diamond').classes('text-4xl text-primary mb-4')
                    ui.label('QUALITY').classes('text-xl font-bold mb-4')
                    ui.label('We curate only the finest timepieces from the world\'s most prestigious manufacturers. Our commitment to quality is unwavering.')
                
                with ui.card().classes('p-8 text-center'):
                    ui.icon('support_agent').classes('text-4xl text-primary mb-4')
                    ui.label('SERVICE').classes('text-xl font-bold mb-4')
                    ui.label('Our team of watch experts provides personalized service to help you find the perfect timepiece. We offer lifetime support for every purchase.')
        
        # Team section
        with ui.column().classes('mb-16'):
            ui.label('OUR TEAM').classes('text-3xl font-bold text-center mb-12')
            
            with ui.grid(columns=3).classes('gap-8'):
                for i in range(3):
                    with ui.card().classes('text-center'):
                        ui.image(f'https://source.unsplash.com/400x400/?portrait,professional&sig={i+10}').classes('w-full h-64 object-cover')
                        with ui.card_section().classes('p-6'):
                            ui.label(['Thomas Laurent', 'Sophie Chen', 'Michael Rodriguez'][i]).classes('text-xl font-bold')
                            ui.label(['Founder & Master Watchmaker', 'Head of Curation', 'Customer Experience Director'][i]).classes('text-primary mb-4')
                            ui.label(['With over 40 years of experience in horology, Thomas oversees our authentication process and special collections.', 
                                     'Sophie travels the world to discover exceptional timepieces and build relationships with manufacturers and collectors.', 
                                     'Michael ensures that every customer receives personalized service and expert guidance throughout their journey.'][i])
    
    create_footer()

@ui.page('/contact')
def contact_page():
    create_header()
    
    with ui.column().classes('p-8'):
        ui.label('CONTACT US').classes('text-3xl font-bold mb-8')
        
        with ui.row().classes('gap-16'):
            # Contact form
            with ui.column().classes('w-1/2'):
                ui.label('SEND US A MESSAGE').classes('text-xl font-bold mb-6')
                
                with ui.column().classes('gap-4'):
                    ui.input('Your Name').props('outlined required').classes('w-full')
                    ui.input('Email Address').props('outlined required type=email').classes('w-full')
                    ui.input('Phone Number').props('outlined').classes('w-full')
                    ui.select(['General Inquiry', 'Product Question', 'Order Status', 'Return Request', 'Other'], value='General Inquiry').props('outlined required').classes('w-full')
                    ui.textarea('Your Message').props('outlined required').classes('w-full')
                    
                    ui.button('SUBMIT', on_click=lambda: ui.notify('Your message has been sent. We\'ll get back to you shortly.', color='positive')).classes('bg-primary text-white mt-4')
            
            # Contact information
            with ui.column().classes('w-1/2'):
                ui.label('OUR LOCATIONS').classes('text-xl font-bold mb-6')
                
                with ui.row().classes('gap-8'):
                    with ui.column().classes('w-1/2'):
                        ui.label('NEW YORK').classes('font-bold')
                        ui.label('123 Luxury Lane')
                        ui.label('New York, NY 10001')
                        ui.label('+1 (212) 555-1234')
                        ui.label('newyork@luxurytimepieces.com')
                        
                        ui.label('HOURS').classes('font-bold mt-4')
                        ui.label('Monday - Friday: 10am - 7pm')
                        ui.label('Saturday: 10am - 6pm')
                        ui.label('Sunday: 12pm - 5pm')
                    
                    with ui.column().classes('w-1/2'):
                        ui.label('LOS ANGELES').classes('font-bold')
                        ui.label('456 Beverly Drive')
                        ui.label('Los Angeles, CA 90210')
                        ui.label('+1 (310) 555-5678')
                        ui.label('losangeles@luxurytimepieces.com')
                        
                        ui.label('HOURS').classes('font-bold mt-4')
                        ui.label('Monday - Friday: 10am - 7pm')
                        ui.label('Saturday: 10am - 6pm')
                        ui.label('Sunday: 12pm - 5pm')
                
                ui.label('CUSTOMER SERVICE').classes('text-xl font-bold mt-8 mb-6')
                
                with ui.column().classes('gap-2'):
                    with ui.row().classes('items-center'):
                        ui.icon('phone').classes('mr-2 text-primary')
                        ui.label('+1 (800) 555-1234')
                    
                    with ui.row().classes('items-center'):
                        ui.icon('email').classes('mr-2 text-primary')
                        ui.label('info@luxurytimepieces.com')
                    
                    with ui.row().classes('items-center'):
                        ui.icon('support_agent').classes('mr-2 text-primary')
                        ui.label('Live Chat: Available 24/7')
                
                ui.label('FOLLOW US').classes('text-xl font-bold mt-8 mb-6')
                
                with ui.row().classes('gap-4'):
                    for icon in ['facebook', 'instagram', 'twitter', 'youtube']:
                        ui.button().props(f'flat round color=primary icon={icon}')

# Add custom CSS
ui.add_head_html('''
<style>
:root {
    --primary: #d4af37;
    --primary-dark: #b8971f;
}

.bg-primary {
    background-color: var(--primary) !important;
}

.text-primary {
    color: var(--primary) !important;
}

.hover\:text-primary:hover {
    color: var(--primary) !important;
}

.border-primary {
    border-color: var(--primary) !important;
}

.product-card {
    transition: all 0.3s ease;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.category-card {
    transition: all 0.3s ease;
    overflow: hidden;
}

.category-card:hover img {
    transform: scale(1.05);
}

.category-card img {
    transition: all 0.3s ease;
}
</style>
''')

# Run the app
ui.run(title="Luxury Timepieces", favicon="🕰️")