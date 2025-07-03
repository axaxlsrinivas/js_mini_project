import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QLineEdit, QPushButton, QListWidgetItem, QStackedWidget, QFrame, QComboBox, QDialog, QTextEdit, QScrollArea, QMessageBox, QCalendarWidget
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
import db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os

DEPT_COLORS = ["#6ec6ad", "#4a90e2", "#f5a623", "#e94e77", "#7b8d8e", "#b8e986"]
DEFAULT_IMAGE = os.path.join(os.path.dirname(__file__), "images", "default.png")

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(10, 30, 10, 10)
        icons = [
            ("equipment", "🩺"),
            ("calendar", "📅"),
            ("chat", "💬"),
            ("profile", "👤")
        ]
        for name, emoji in icons:
            btn = QPushButton(emoji)
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("font-size: 22px; border: none; background: #222; color: #fff; border-radius: 10px;")
            layout.addWidget(btn)
        layout.addStretch()
        self.setLayout(layout)
        self.setStyleSheet("background: #181c1f;")

class EquipmentList(QWidget):
    def __init__(self, on_select, get_dept):
        super().__init__()
        self.on_select = on_select
        self.get_dept = get_dept
        self.layout = QVBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText('🔍 Search equipment...')
        self.search.setStyleSheet('''
            QLineEdit {
                background: #f5faff;
                border: 2px solid #4a90e2;
                border-radius: 16px;
                padding: 8px 16px;
                font-size: 15px;
                margin-bottom: 8px;
            }
            QLineEdit:focus {
                border: 2.5px solid #6ec6ad;
                background: #fff;
            }
        ''')
        self.search.textChanged.connect(self.update_list)
        self.layout.addWidget(self.search)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout()
        self.list_layout.setSpacing(12)
        self.list_widget.setLayout(self.list_layout)
        self.scroll.setWidget(self.list_widget)
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)
        self.update_list()

    def update_list(self):
        keyword = self.search.text()
        dept = self.get_dept()
        items = db.get_all_equipment() if keyword or dept == 'All' else db.get_nonexpired_equipment()
        if keyword:
            items = [i for i in items if keyword.lower() in i[1].lower()]
        if dept != 'All':
            items = [i for i in items if i[3] == dept]
        # Clear old
        for i in reversed(range(self.list_layout.count())):
            w = self.list_layout.itemAt(i).widget()
            if w: w.setParent(None)
        for item in items:
            card = EquipmentCard(item, self.on_select)
            self.list_layout.addWidget(card)
        self.list_layout.addStretch()

    def get_selected_dept(self):
        return self.selected_dept

class EquipmentCard(QFrame):
    def __init__(self, equip, on_select):
        super().__init__()
        self.equip = equip
        self.on_select = on_select
        self.setFrameShape(QFrame.StyledPanel)
        from datetime import datetime
        expired = False
        if len(equip) > 8 and equip[8]:
            try:
                exp_date = datetime.strptime(equip[8], '%Y-%m-%d').date()
                if exp_date <= datetime.today().date():
                    expired = True
            except Exception:
                pass
        style = "QFrame { background: #fff; border: 1.5px solid #4a90e2; border-radius: 12px; margin-bottom: 8px; } QFrame:hover { background: #f5faff; border: 2.5px solid #6ec6ad; }"
        if expired:
            style = "QFrame { background: #ffeaea; border: 2px solid #e94e77; border-radius: 12px; margin-bottom: 8px; } QFrame:hover { background: #fff0f0; border: 2.5px solid #e94e77; }"
        self.setStyleSheet(style)
        layout = QHBoxLayout()
        # Use relevant image for each equipment
        img_path = equip[7] if equip[7] and os.path.exists(os.path.join(os.path.dirname(__file__), equip[7])) else self.get_image_for_equipment(equip[1])
        if not os.path.isabs(img_path):
            img_path = os.path.join(os.path.dirname(__file__), img_path)
        pix = QPixmap(img_path)
        if not pix or pix.isNull():
            pix = QPixmap(DEFAULT_IMAGE)
        img = QLabel()
        img.setPixmap(pix)
        img.setFixedSize(70, 70)
        img.setScaledContents(True)
        img.setStyleSheet("border: none; background: #f5faff; border-radius: 8px;")
        layout.addWidget(img)
        info = QVBoxLayout()
        name = QLabel(f"<b>{equip[1]}</b>")
        name.setStyleSheet("font-size: 15px; border: none;")
        info.addWidget(name)
        t = QLabel(f"Type: {equip[2]} | Qty: {equip[4]}")
        t.setStyleSheet("border: none;")
        info.addWidget(t)
        d = QLabel(f"Dept: {equip[3]}")
        d.setStyleSheet("border: none;")
        info.addWidget(d)
        layout.addLayout(info)
        layout.addStretch()
        # Add clickable alert icon if expired
        if expired:
            alert = QPushButton("⚠️")
            alert.setStyleSheet("border: none; background: transparent; font-size: 22px; color: #e94e77;")
            alert.setToolTip('This item is expired! Click to remove.')
            alert.clicked.connect(self.handle_expired_click)
            layout.addWidget(alert)
        self.setLayout(layout)
        self.mousePressEvent = self.clicked

    def get_image_for_equipment(self, name):
        # Map equipment names to image files in images/ folder
        name_map = {
            'Syringe': 'syringe.png',
            'Surgical tweezers': 'tweezers.png',
            'Scarifier': 'scarifier.png',
            'Microscope': 'microscope.png',
            'Thermometer': 'thermometer.png',
            'Stethophonendoscope': 'stethoscope.png',
            'Disposable gloves': 'gloves.png',
            'Shoe covers': 'shoecovers.png',
        }
        fname = name_map.get(name, 'default.png')
        path = os.path.join(os.path.dirname(__file__), 'images', fname)
        return path if os.path.exists(path) else DEFAULT_IMAGE

    def clicked(self, event):
        self.on_select(self.equip[0])

    def handle_expired_click(self):
        # Do nothing when alert is clicked (no removal)
        pass

class LearnMoreDialog(QDialog):
    def __init__(self, equip):
        super().__init__()
        self.setWindowTitle(f"Learn More - {equip[1]}")
        layout = QVBoxLayout()
        details = QTextEdit()
        details.setReadOnly(True)
        details.setText(f"Name: {equip[1]}\nType: {equip[2]}\nDepartment: {equip[3]}\nQuantity: {equip[4]}\nCondition: {equip[6]}%\nDetails: {equip[5]}")
        layout.addWidget(details)
        self.setLayout(layout)
        self.resize(400, 300)

class EquipmentDetail(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.title = QLabel()
        self.title.setFont(QFont('Arial', 18, QFont.Bold))
        self.layout.addWidget(self.title)
        self.image = QLabel()
        self.image.setFixedSize(220, 150)
        self.image.setStyleSheet("background: #f0f0f0; border: 1px solid #ccc; border-radius: 8px;")
        self.layout.addWidget(self.image)
        self.info = QLabel('')
        self.info.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.info)
        self.learn_more = QPushButton('Learn More')
        self.learn_more.clicked.connect(self.open_learn_more)
        self.learn_more.setVisible(False)
        self.layout.addWidget(self.learn_more)
        self.chart = FigureCanvas(plt.Figure(figsize=(4,2)))
        self.layout.addWidget(self.chart)
        self.details = QLabel('')
        self.layout.addWidget(self.details)
        # Add bar graph icon button at the bottom right
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.graph_btn = QPushButton()
        graph_icon_path = os.path.join(os.path.dirname(__file__), 'images', 'bar-graph.png')
        if os.path.exists(graph_icon_path):
            self.graph_btn.setIcon(QIcon(graph_icon_path))
        self.graph_btn.setIconSize(QSize(32, 32))
        self.graph_btn.setFixedSize(40, 40)
        self.graph_btn.setStyleSheet("border: none; background: transparent;")
        self.graph_btn.clicked.connect(self.show_dept_graph_dialog)
        btn_layout.addWidget(self.graph_btn)
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)
        self.current_equip = None
        self.show_prompt()

    def show_prompt(self):
        self.title.setText('Select equipment to view details')
        self.title.setStyleSheet("color: #888; font-style: italic;")
        self.image.clear()
        self.info.setText('')
        self.learn_more.setVisible(False)
        self.details.setText('')
        self.chart.figure.clear()
        self.chart.draw()

    def show_equipment(self, equip):
        self.current_equip = equip
        if not equip:
            self.show_prompt()
            return
        self.title.setStyleSheet("")
        self.title.setText(f"{equip[1]} ({equip[2]})")
        # Use robust image path logic for details as in list
        img_path = equip[7] if equip[7] and os.path.exists(os.path.join(os.path.dirname(__file__), equip[7])) else self.get_image_for_equipment(equip[1])
        if not os.path.isabs(img_path):
            img_path = os.path.join(os.path.dirname(__file__), img_path)
        pix = QPixmap(img_path)
        if not pix or pix.isNull():
            pix = QPixmap(DEFAULT_IMAGE)
        self.image.setPixmap(pix)
        self.image.setScaledContents(True)
        # Highlighted, clickable added/expiry dates
        added_date = equip[9] if len(equip) > 9 and equip[9] else 'N/A'
        expiry_date = equip[8] if len(equip) > 8 and equip[8] else 'N/A'
        self.info.setText(f"<b>Department:</b> {equip[3]}<br><b>Quantity:</b> {equip[4]}<br>"
            f"<b>Added Date:</b> <a href='added' style='color:#4a90e2; text-decoration:underline;'><b>{added_date}</b></a><br>"
            f"<b>Expiry Date:</b> <a href='expiry' style='color:#e94e77; text-decoration:underline;'><b>{expiry_date}</b></a><br>"
            f"<b>Condition:</b> {equip[6]}%<br><b>Details:</b> {equip[5]}")
        self.info.setTextFormat(Qt.RichText)
        self.info.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.info.setOpenExternalLinks(False)
        self.info.linkActivated.connect(self.show_date_notification)
        self.learn_more.setVisible(True)
        self.plot_condition(equip[6])
        # Update bottom info text based on selected item
        good = equip[6]
        not_good = 100 - good
        note = f"{good}% of these items are in good condition. {not_good}% need replacement or repair."
        self.details.setText(note)

    def get_image_for_equipment(self, name):
        name_map = {
            'Syringe': 'syringe.png',
            'Surgical tweezers': 'tweezers.png',
            'Scarifier': 'scarifier.png',
            'Microscope': 'microscope.png',
            'Thermometer': 'thermometer.png',
            'Stethophonendoscope': 'stethoscope.png',
            'Disposable gloves': 'gloves.png',
            'Shoe covers': 'shoecovers.png',
        }
        fname = name_map.get(name, 'default.png')
        path = os.path.join(os.path.dirname(__file__), 'images', fname)
        return path if os.path.exists(path) else DEFAULT_IMAGE

    def plot_condition(self, percent):
        self.chart.figure.clear()
        ax = self.chart.figure.subplots()
        ax.bar(['Condition'], [percent], color='#6ec6ad')
        ax.set_ylim(0, 100)
        ax.set_ylabel('%')
        self.chart.draw()

    def open_learn_more(self):
        if self.current_equip:
            dlg = LearnMoreDialog(self.current_equip)
            dlg.exec_()

    def show_dept_graph_dialog(self):
        # Get parent MainWindow to access selected department
        parent = self.parent()
        while parent and not hasattr(parent, 'get_selected_dept'):
            parent = parent.parent()
        dept = parent.get_selected_dept() if parent else 'All'
        dlg = DepartmentGraphDialog(dept)
        dlg.exec_()

    def show_date_notification(self, link):
        equip = self.current_equip
        if not equip:
            return
        added_date = equip[9] if len(equip) > 9 and equip[9] else 'N/A'
        expiry_date = equip[8] if len(equip) > 8 and equip[8] else 'N/A'
        msg = QMessageBox(self)
        if link == 'added':
            msg.setWindowTitle('Item Added Date')
            msg.setText(f"This item was added on <b>{added_date}</b>.")
        elif link == 'expiry':
            msg.setWindowTitle('Item Expiry Date')
            msg.setText(f"This item will expire on <b>{expiry_date}</b>.")
        msg.exec_()

def plot_overall_condition():
    items = db.get_all_equipment()
    bins = [0]*10
    for i in items:
        idx = min(9, i[6]//10)
        bins[idx] += 1
    fig = plt.Figure(figsize=(5,2))
    ax = fig.subplots()
    ax.bar([f'{i*10+1}-{(i+1)*10}%' for i in range(10)], bins, color='#4a90e2')
    ax.set_title('Condition of All Equipment')
    ax.set_ylabel('Count')
    fig.tight_layout()
    return fig

class EquipmentGraphDialog(QDialog):
    def __init__(self, equip):
        super().__init__()
        self.setWindowTitle(f"Equipment Condition - {equip[1]}")
        layout = QVBoxLayout()
        # Bar graph for condition
        fig = plt.Figure(figsize=(4,2))
        ax = fig.subplots()
        ax.bar(['Condition'], [equip[6]], color='#4a90e2')
        ax.set_ylim(0, 100)
        ax.set_ylabel('%')
        ax.set_title('Condition')
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        # Details
        details = QLabel(f"<b>Name:</b> {equip[1]}<br><b>Type:</b> {equip[2]}<br><b>Department:</b> {equip[3]}<br><b>Quantity:</b> {equip[4]}<br><b>Condition:</b> {equip[6]}%<br><b>Details:</b> {equip[5]}")
        details.setStyleSheet("font-size: 14px;")
        details.setWordWrap(True)
        layout.addWidget(details)
        self.setLayout(layout)
        self.resize(420, 320)

class DepartmentGraphDialog(QDialog):
    def __init__(self, dept):
        super().__init__()
        self.setWindowTitle(f"Condition Statistics - {dept} Department" if dept != 'All' else "Condition Statistics - All Departments")
        layout = QVBoxLayout()
        # Get data for the selected department
        if dept == 'All':
            items = db.get_all_equipment()
        else:
            items = [i for i in db.get_all_equipment() if i[3] == dept]
        # Prepare data for bar graph
        names = [i[1] for i in items]
        conditions = [i[6] for i in items]
        fig = plt.Figure(figsize=(max(4, len(names)*0.7), 2.5))
        ax = fig.subplots()
        ax.bar(names, conditions, color='#4a90e2')
        ax.set_ylim(0, 100)
        ax.set_ylabel('% Condition')
        ax.set_title('Equipment Condition')
        ax.set_xticklabels(names, rotation=30, ha='right', fontsize=9)
        fig.tight_layout()
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        # Add summary
        summary = QLabel(f"<b>Total items:</b> {len(items)}")
        summary.setStyleSheet("font-size: 14px;")
        layout.addWidget(summary)
        self.setLayout(layout)
        self.resize(520, 340)

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Equipment Expiry Calendar')
        layout = QVBoxLayout()
        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)
        # List of items with expiry dates
        from datetime import datetime
        items = [i for i in db.get_all_equipment() if i[8]]
        items.sort(key=lambda x: x[8])
        label = QLabel('<b>Items with Expiry Dates:</b>')
        layout.addWidget(label)
        today = datetime.today().date()
        for item in items:
            exp = item[8]
            name = item[1]
            days = (datetime.strptime(exp, '%Y-%m-%d').date() - today).days
            if days < 0:
                # Expired: red bg, alert icon
                l = QLabel(f"<span style='background:#ffeaea; color:#d32f2f; padding:2px 6px; border-radius:6px;'>⚠️ <b>{name}</b> - {exp} (expired)</span>")
            else:
                color = 'orange' if days <= 30 else 'green'
                l = QLabel(f"<span style='color:{color}'>{name} - {exp} ({'in ' + str(days) + ' days'})</span>")
            layout.addWidget(l)
        self.setLayout(layout)
        self.resize(400, 400)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Medical Equipment Inventory')
        self.resize(1200, 750)
        db.init_db()
        # self.check_expired_items()  # Removed from here
        all_depts = sorted(set([row[3] for row in db.get_all_equipment()]))
        main_layout = QHBoxLayout()  # Use QHBoxLayout for sidebar
        self.sidebar = Sidebar()
        # Connect calendar icon to calendar dialog
        self.sidebar.findChildren(QPushButton)[1].clicked.connect(self.open_calendar_dialog)
        main_layout.addWidget(self.sidebar, 0)
        content_layout = QVBoxLayout()
        # Add page title
        title = QLabel('Medical Equipment Inventory')
        title.setFont(QFont('Arial', 22, QFont.Bold))
        title.setStyleSheet('color: #222; margin-bottom: 8px;')
        content_layout.addWidget(title, alignment=Qt.AlignHCenter)
        # Add department dropdown below title
        self.dept_dropdown = QComboBox()
        self.dept_dropdown.addItem('All')
        self.dept_dropdown.addItems(all_depts)
        self.dept_dropdown.currentIndexChanged.connect(self.on_dept_select_dropdown)
        self.dept_dropdown.setFixedWidth(450)
        self.dept_dropdown.setStyleSheet('''
            QComboBox {
                background: #f5faff;
                border: 2px solid #4a90e2;
                border-radius: 18px;
                padding: 12px 20px 12px 20px;
                font-size: 17px;
                min-height: 40px;
                margin-bottom: 16px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 36px;
                border-left: none;
                padding-left: 12px;
            }
            QComboBox::down-arrow {
                image: url("images/arrow-down.png");
                width: 18px;
                height: 18px;
                margin-right: 8px;
            }
            QComboBox:focus {
                border: 2.5px solid #6ec6ad;
                background: #fff;
            }
            QComboBox QAbstractItemView {
                border-radius: 14px;
                background: #fff;
                selection-background-color: #e6f7f1;
                font-size: 16px;
                padding: 8px;
            }
        ''')
        content_layout.addWidget(self.dept_dropdown, alignment=Qt.AlignLeft)
        self.selected_dept = 'All'
        content = QHBoxLayout()
        # Beautified and slightly wider items list view
        list_container = QFrame()
        list_container.setFixedWidth(450)
        list_container.setStyleSheet('''
            QFrame {
                background: #fff;
                border: 1.5px solid #e0eafc;
                border-radius: 18px;
                padding: 12px 6px 12px 6px;
            }
        ''')
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)
        self.list_panel = EquipmentList(self.show_details, self.get_selected_dept)
        self.list_panel.setStyleSheet('background: transparent; margin: 0; padding: 0;')
        list_layout.addWidget(self.list_panel)
        list_container.setLayout(list_layout)
        content.addWidget(list_container, 2)
        self.detail_panel = EquipmentDetail()
        content.addWidget(self.detail_panel, 3)
        content_layout.addLayout(content)
        main_layout.addLayout(content_layout, 1)
        self.setLayout(main_layout)
    
    def check_expired_items(self):
        import datetime
        today = datetime.date.today().isoformat()
        expired = [i for i in db.get_all_equipment() if i[8] and i[8] <= today]
        return expired

    def open_calendar_dialog(self):
        # Do not remove expired items; just show the calendar dialog
        dlg = CalendarDialog(self)
        dlg.exec_()

    def on_dept_select_dropdown(self, idx):
        self.selected_dept = self.dept_dropdown.currentText()
        if hasattr(self, 'list_panel') and self.list_panel:
            self.list_panel.update_list()
        if hasattr(self, 'detail_panel') and self.detail_panel:
            self.detail_panel.show_prompt()

    def show_details(self, equip_id):
        equip = db.get_equipment_by_id(equip_id)
        self.detail_panel.show_equipment(equip)

    def get_selected_dept(self):
        return self.selected_dept

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
