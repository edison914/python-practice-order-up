from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from ..models import Table, Employee, Order, MenuItem, OrderDetail, db
from app.forms import AssignTableForm, CloseTableForm, AddItemForm

bp = Blueprint('orders', __name__, url_prefix='')

@bp.route('/')
@login_required
def index():
    return render_template('orders.html')


@bp.route('/assign_table', methods=['GET', 'POST'])
@login_required
def assign_table():
    tables = Table.query.order_by(Table.id).all()
    employees = Employee.query.order_by(Employee.id).all()

    form = AssignTableForm()

    form.table_id.choices = [table.id for table in tables]
    form.employee_id.choices = [employee.id for employee in employees]

    if form.validate_on_submit():
        employee_id = form.employee_id.data
        table_id = form.table_id.data

        new_order = Order(employee_id=employee_id, table_id=table_id, finished=False)

        db.session.add(new_order)
        db.session.commit()
        return redirect (url_for('.index'))

    return render_template('assigntable.html', form=form)




@bp.route('/close_table', methods=['GET','POST'])
@login_required
def close_table():

    # how do i get filter tables that are open based on orders that attr finished = False
    open_orders = Order.query.filter(Order.finished == False)

    form = CloseTableForm()
    form.order_id.choices = [order.id for order in open_orders]

    if form.validate_on_submit():
        order_id = form.order_id.data
        order_selected = Order.query.get(order_id)
        order_selected.finished = True

        db.session.add(order_selected)
        db.session.commit()

        return redirect (url_for('.index'))

    return render_template('closetable.html', form=form)




@bp.route('/add_items', methods=['GET','POST'])
@login_required
def add_items():

    form = AddItemForm()

    # show a list of open orders
    open_orders = Order.query.filter(Order.finished == False)
    form.order_id.choices = [order.id for order in open_orders]

    #show a list of menu items that can be added
    menu_items = MenuItem.query.all()
    print(menu_items[0].id, menu_items[0].name)
    # create a list of choices to be selected in html, do not use choices for mutiple select?
    form.menu_item_ids.choices = [(item.id, item.name) for item in menu_items]

    if form.validate_on_submit():
        order_selected = form.order_id.data
        menu_items_selected = form.menu_item_ids.data
        print(menu_items_selected)

        #loop through the list of menus_items, create order_detail obj with selected item id
        for item in menu_items_selected:
            order_detail = OrderDetail(order_id=order_selected, menu_item_id=item)
            db.session.add(order_detail)
            db.session.commit()

        return redirect (url_for('.index'))

    return render_template('additems.html', form=form, menu_items=menu_items)
