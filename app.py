from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///selems.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Operator')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    equipments = db.relationship('Equipment', backref='category', lazy=True)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(50), nullable=False, default='Good')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    borrower_name = db.Column(db.String(100), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='Issued')

    equipment = db.relationship('Equipment', backref=db.backref('transactions', lazy=True))

with app.app_context():
    db.create_all()

# ==================== AUTH ROUTES ====================

@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('welcome.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            flash(f'Reset instructions sent to {email}. (Demo: Password has been reset to "admin123")', 'success')
            user.set_password('admin123')
            db.session.commit()
        else:
            flash('Email address not found in system records.', 'danger')
        return redirect(url_for('welcome'))
    
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('welcome'))

# ==================== APP MODULE ROUTES ====================

@app.route('/dashboard')
def index():
    if 'user_id' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('welcome'))
        
    total_equipment = Equipment.query.count()
    total_available = db.session.query(db.func.sum(Equipment.available_quantity)).scalar() or 0
    active_transactions = Transaction.query.filter_by(status='Issued').count()
    return render_template('index.html', total_equipment=total_equipment, total_available=total_available, active_transactions=active_transactions)

@app.route('/equipment', endpoint='equipment_list')
def equipment_list():
    if 'user_id' not in session:
        return redirect(url_for('welcome'))
    search_query = request.args.get('search', '')
    if search_query:
        equipment = Equipment.query.filter(Equipment.name.ilike(f'%{search_query}%')).all()
    else:
        equipment = Equipment.query.all()
    return render_template('equipment.html', equipment=equipment, search_query=search_query)

@app.route('/add', methods=['GET', 'POST'])
def add_equipment():
    if 'user_id' not in session:
        return redirect(url_for('welcome'))
    categories = Category.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        category_id = request.form.get('category_id')
        total_quantity = int(request.form.get('total_quantity'))
        location = request.form.get('location')
        condition = request.form.get('condition')

        new_item = Equipment(
            name=name,
            category_id=category_id,
            total_quantity=total_quantity,
            available_quantity=total_quantity,
            location=location,
            condition=condition
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Equipment added successfully!', 'success')
        return redirect(url_for('equipment_list'))
    
    return render_template('add_equipment.html', categories=categories)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):
    if 'user_id' not in session:
        return redirect(url_for('welcome'))
    item = Equipment.query.get_or_404(id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.category_id = request.form.get('category_id')
        item.total_quantity = int(request.form.get('total_quantity'))
        item.available_quantity = int(request.form.get('available_quantity'))
        item.location = request.form.get('location')
        item.condition = request.form.get('condition')
        
        db.session.commit()
        flash('Equipment updated successfully!', 'success')
        return redirect(url_for('equipment_list'))
        
    return render_template('edit_equipment.html', equipment=item, categories=categories)

@app.route('/delete/<int:id>')
def delete_equipment(id):
    if 'user_id' not in session:
        return redirect(url_for('welcome'))
    item = Equipment.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Equipment deleted successfully!', 'success')
    return redirect(url_for('equipment_list'))

@app.route('/issue/<int:id>', methods=['GET', 'POST'])
def issue_equipment(id):
    if 'user_id' not in session:
        return redirect(url_for('welcome'))
    item = Equipment.query.get_or_404(id)
    if request.method == 'POST':
        borrower = request.form.get('borrower_name')
        if item.available_quantity > 0:
            item.available_quantity -= 1
            transaction = Transaction(equipment_id=item.id, borrower_name=borrower, status='Issued')
            db.session.add(transaction)
            db.session.commit()
            flash('Equipment issued successfully!', 'success')
        else:
            flash('No available units left to issue!', 'danger')
        return redirect(url_for('equipment_list'))
    
    return render_template('issue_equipment.html', equipment=item)

@app.route('/return/<int:transaction_id>')
def return_equipment(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('welcome'))
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.status == 'Issued':
        transaction.status = 'Returned'
        transaction.return_date = datetime.utcnow()
        transaction.equipment.available_quantity += 1
        db.session.commit()
        flash('Equipment returned successfully!', 'success')
    return redirect(url_for('transaction_history'))

@app.route('/transactions')
def transaction_history():
    if 'user_id' not in session:
        return redirect(url_for('welcome'))
    transactions = Transaction.query.order_by(Transaction.issue_date.desc()).all()
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)