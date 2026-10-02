from app import app, db, Category, Equipment, User

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables created fresh from scratch.")

    # 1. Create Default Admin User
    admin = User(username="admin", email="admin@selemslab.com", role="Administrator")
    admin.set_password("admin123")
    db.session.add(admin)

    # 2. Create Categories
    cat1 = Category(name="Measuring Instruments", description="Scopes, multimeters, and analyzers")
    cat2 = Category(name="Power Supplies", description="DC and AC bench power sources")
    cat3 = Category(name="Development Boards", description="Microcontrollers and FPGA kits")
    cat4 = Category(name="Semiconductors & ICs", description="Active components and evaluation modules")
    db.session.add_all([cat1, cat2, cat3, cat4])
    db.session.commit()

    # 3. Create Extended Equipment Inventory
    equipments = [
        Equipment(name="Digital Storage Oscilloscope (100MHz)", category_id=cat1.id, total_quantity=6, available_quantity=6, location="Bench A1", condition="Good"),
        Equipment(name="Digital Multimeter (True-RMS)", category_id=cat1.id, total_quantity=15, available_quantity=14, location="Bench A2", condition="Good"),
        Equipment(name="Function Generator (3MHz)", category_id=cat1.id, total_quantity=5, available_quantity=5, location="Bench A3", condition="Good"),
        Equipment(name="DC Bench Power Supply (30V, 5A)", category_id=cat2.id, total_quantity=10, available_quantity=9, location="Bench B1", condition="Good"),
        Equipment(name="Programmable Dual DC Supply", category_id=cat2.id, total_quantity=4, available_quantity=4, location="Bench B2", condition="Good"),
        Equipment(name="Arduino Mega 2560 Dev Kit", category_id=cat3.id, total_quantity=12, available_quantity=10, location="Cabinet C1", condition="Fair"),
        Equipment(name="Raspberry Pi 4 Model B (4GB)", category_id=cat3.id, total_quantity=8, available_quantity=8, location="Cabinet C2", condition="Good"),
        Equipment(name="Xilinx FPGA Spartan-6 Board", category_id=cat3.id, total_quantity=6, available_quantity=5, location="Cabinet C3", condition="Good"),
        Equipment(name="MOSFET & Transistor Assortment Kit", category_id=cat4.id, total_quantity=20, available_quantity=18, location="Rack D1", condition="Good")
    ]

    db.session.add_all(equipments)
    db.session.commit()
    print("Successfully seeded database with extended laboratory inventory and admin user!")