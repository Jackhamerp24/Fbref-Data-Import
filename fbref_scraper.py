#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FBref Desktop Scraper (Offline GUI)
-----------------------------------
• OFFLINE ONLY: không gọi mạng, không delay.
• Quét thư mục HTML (mặc định) hoặc folder do người dùng đặt làm Default.
• Cho phép duyệt chọn file HTML ở bất kỳ đâu (Add HTML Files…).
• Hiển thị bảng (kể cả trong HTML comments), preview và export CSV.
• Dùng PySide6 (Qt for Python).

Dependencies:
  pip install PySide6 pandas beautifulsoup4 lxml
"""
from __future__ import annotations

import sys, re, pathlib
from io import StringIO
from dataclasses import dataclass
from typing import List

import pandas as pd
from bs4 import BeautifulSoup, Comment
from PySide6 import QtCore, QtGui, QtWidgets

APP_NAME = "FBref Offline Scraper"
APP_ORG  = "DuongLabs"               # QSettings org name (tuỳ chọn)

# Base paths (support PyInstaller via _MEIPASS)
SCRIPT_DIR = pathlib.Path(getattr(sys, "_MEIPASS", pathlib.Path(__file__).resolve().parent)).resolve()
BASE_DIR   = pathlib.Path(sys.argv[0]).resolve().parent if getattr(sys, "_MEIPASS", None) else pathlib.Path(__file__).resolve().parent

# Mặc định dùng thư mục HTML cạnh app nếu user chưa set default
DEFAULT_HTML_DIR = BASE_DIR / "HTML"
OUT_DIR          = BASE_DIR / "out"

# ---- Friendly names cho các FBref table id (dùng cho nhãn hiển thị) ----
TABLE_ID_FRIENDLY = {
    "stats_standard_dom_lg": "Standard",
    "stats_shooting_dom_lg": "Shooting",
    "stats_passing_dom_lg": "Passing",
    "stats_passing_types_dom_lg": "Pass Types",
    "stats_gca_dom_lg": "Goal & Shot Creation",
    "stats_possession_dom_lg": "Possession",
    "stats_misc_dom_lg": "Misc",
}

# ---------------- Display helpers ----------------

def short_file_display_name(path: pathlib.Path) -> str:
    """Rút gọn tên FBref HTML thành dạng 'Florian Wirtz.html'."""
    name = path.stem
    name = re.sub(r"\s*\|\s*FBref\.com\s*$", "", name, flags=re.I)
    name = re.sub(r"\s*(Domestic League)?\s*Stats.*$", "", name, flags=re.I)
    name = re.sub(r"\s*Stats,\s*Goals,\s*Records.*$", "", name, flags=re.I)
    name = re.sub(r"\s*Match Logs.*$", "", name, flags=re.I)
    name = re.sub(r"\s+", " ", name).strip() or path.stem
    return f"{name}.html"


def _detect_player_name(source_stem: str) -> str:
    base = re.sub(r"\s*\|\s*FBref\.com\s*$", "", source_stem, flags=re.I)
    base = re.sub(r"\s*(Domestic League)?\s*Stats.*$", "", base, flags=re.I)
    base = re.sub(r"\s*Stats,\s*Goals,\s*Records.*$", "", base, flags=re.I)
    base = re.sub(r"\s*Match Logs.*$", "", base, flags=re.I)
    base = re.sub(r"\s+", " ", base).strip()
    return base or source_stem


def pretty_table_label(rec: "TableRecord") -> str:
    """Sinh nhãn ngắn gọn: 'Florian Wirtz Last 5 matches (domestic league)' hoặc 'Florian Wirtz – Shooting'."""
    stem = rec.source_file.stem
    player = _detect_player_name(stem)

    title = (rec.page_title or "") + " " + stem
    is_domestic = bool(re.search(r"Domestic League", title, flags=re.I))

    m_last = re.search(r"last[_\s-]?(\d+)", title, flags=re.I)
    if m_last:
        n = m_last.group(1)
        suffix = " (domestic league)" if is_domestic else ""
        return f"{player} Last {n} matches{suffix}"

    friendly = TABLE_ID_FRIENDLY.get(rec.table_id, rec.table_id)
    return f"{player} – {friendly}"

# ---------------- Utilities ----------------

def sanitize_filename(text: str) -> str:
    text = re.sub(r"[^\w\-.]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "table"


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten single/multi-level columns thành tên an toàn, duy nhất."""
    if isinstance(df.columns, pd.MultiIndex):
        new_cols = []
        for tup in df.columns:
            parts = [str(x).strip() for x in tup if str(x).strip() and not str(x).startswith("Unnamed")]
            col = "_".join(parts) if parts else "col"
            new_cols.append(col)
        df.columns = new_cols
    else:
        df.columns = [("col" if (c is None or str(c).strip() == "") else str(c).strip()) for c in df.columns]
    # De-duplicate
    seen = {}
    uniq = []
    for c in df.columns:
        if c not in seen:
            seen[c] = 0
            uniq.append(c)
        else:
            seen[c] += 1
            uniq.append(f"{c}_{seen[c]}")
    df.columns = uniq
    return df

@dataclass
class TableRecord:
    source_file: pathlib.Path
    table_id: str
    df: pd.DataFrame
    page_title: str | None


def read_all_tables_from_html_file(path: pathlib.Path) -> List[TableRecord]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "lxml")

    title_tag = soup.select_one("title")
    page_title = title_tag.text.strip() if title_tag else None

    records: List[TableRecord] = []

    # 1) Tables trong DOM
    for tbl in soup.select("table[id]"):
        try:
            dfs = pd.read_html(StringIO(str(tbl)), flavor="lxml")
        except ValueError:
            continue
        if not dfs:
            continue
        df = flatten_columns(dfs[0])
        tid = tbl.get("id") or "table"
        records.append(TableRecord(source_file=path, table_id=tid, df=df, page_title=page_title))

    # 2) Tables nằm trong HTML comments
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        if "<table" not in c:
            continue
        frag = BeautifulSoup(c, "lxml")
        for tbl in frag.select("table[id]"):
            tid = tbl.get("id") or "table"
            try:
                dfs = pd.read_html(StringIO(str(tbl)), flavor="lxml")
            except ValueError:
                continue
            if not dfs:
                continue
            df = flatten_columns(dfs[0])
            records.append(TableRecord(source_file=path, table_id=tid, df=df, page_title=page_title))

    return records

# ------------- Qt Widgets -------------------

class DataFramePreview(QtWidgets.QTableWidget):
    """Preview nhẹ (tối đa 50 dòng, 25 cột)."""
    def show_dataframe(self, df: pd.DataFrame, max_rows: int = 50, max_cols: int = 25):
        self.clear()
        if df is None or df.empty:
            self.setRowCount(0)
            self.setColumnCount(0)
            return
        sub = df.iloc[:max_rows, :max_cols].copy()
        self.setColumnCount(len(sub.columns))
        self.setRowCount(len(sub))

        self.setHorizontalHeaderLabels([str(c) for c in sub.columns])
        self.setVerticalHeaderLabels([str(i) for i in sub.index])

        for r in range(len(sub)):
            for c in range(len(sub.columns)):
                val = sub.iat[r, c]
                item = QtWidgets.QTableWidgetItem("" if pd.isna(val) else str(val))
                item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.setItem(r, c, item)

        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1100, 700)

        # --- QSettings: nhớ default HTML folder
        self.settings = QtCore.QSettings(APP_ORG, APP_NAME)
        saved_dir = self.settings.value("default_html_dir", str(DEFAULT_HTML_DIR))
        self.html_dir = pathlib.Path(saved_dir)

        # --- widgets
        self.file_list = QtWidgets.QListWidget()
        self.file_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.btn_refresh = QtWidgets.QPushButton("Refresh HTML Folder")
        self.btn_load = QtWidgets.QPushButton("Load Tables from Selected Files")
        self.btn_select_all_files = QtWidgets.QPushButton("Select All Files")
        self.btn_add_files = QtWidgets.QPushButton("Add HTML Files…")
        self.btn_clear_list = QtWidgets.QPushButton("Clear List")
        self.btn_set_default_dir = QtWidgets.QPushButton("Set Default Folder…")

        self.table_list = QtWidgets.QListWidget()
        self.table_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.btn_select_all_tables = QtWidgets.QPushButton("Select All Tables")
        self.btn_export_selected = QtWidgets.QPushButton("Export Selected Tables to CSV")
        self.btn_export_all = QtWidgets.QPushButton("Export ALL Loaded Tables")
        self.lbl_status = QtWidgets.QLabel("Ready.")
        self.preview = DataFramePreview()

        # layout
        left = QtWidgets.QVBoxLayout()
        self.lbl_folder = QtWidgets.QLabel()  # cập nhật động theo default dir
        left.addWidget(self.lbl_folder)
        left.addWidget(self.file_list, 1)

        left_btns = QtWidgets.QHBoxLayout()
        left_btns.addWidget(self.btn_refresh)
        left_btns.addWidget(self.btn_select_all_files)
        left.addLayout(left_btns)

        left_btns2 = QtWidgets.QHBoxLayout()
        left_btns2.addWidget(self.btn_add_files)
        left_btns2.addWidget(self.btn_clear_list)
        left_btns2.addWidget(self.btn_set_default_dir)
        left.addLayout(left_btns2)

        left.addWidget(self.btn_load)

        mid = QtWidgets.QVBoxLayout()
        mid.addWidget(QtWidgets.QLabel("Discovered Tables:"))
        mid.addWidget(self.table_list, 2)
        mid_btns = QtWidgets.QHBoxLayout()
        mid_btns.addWidget(self.btn_select_all_tables)
        mid_btns.addWidget(self.btn_export_selected)
        mid_btns.addWidget(self.btn_export_all)
        mid.addLayout(mid_btns)
        mid.addWidget(self.lbl_status)

        splitter = QtWidgets.QSplitter()
        left_widget = QtWidgets.QWidget(); left_widget.setLayout(left)
        mid_widget  = QtWidgets.QWidget();  mid_widget.setLayout(mid)
        splitter.addWidget(left_widget)
        splitter.addWidget(mid_widget)
        splitter.addWidget(self.preview)
        splitter.setSizes([300, 400, 400])

        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central)
        layout.addWidget(splitter)
        self.setCentralWidget(central)

        # data
        self.records: List[TableRecord] = []

        # connect
        self.btn_refresh.clicked.connect(self.refresh_files)
        self.btn_select_all_files.clicked.connect(self.select_all_files)
        self.btn_load.clicked.connect(self.load_tables)
        self.table_list.itemSelectionChanged.connect(self.on_table_selection)
        self.btn_select_all_tables.clicked.connect(self.select_all_tables)
        self.btn_export_selected.clicked.connect(lambda: self.export_tables(only_selected=True))
        self.btn_export_all.clicked.connect(lambda: self.export_tables(only_selected=False))
        self.btn_add_files.clicked.connect(self.add_files_via_dialog)
        self.btn_clear_list.clicked.connect(self.clear_file_list)
        self.btn_set_default_dir.clicked.connect(self.set_default_dir)

        # initial
        self.refresh_files()

    # --------- actions ---------
    def refresh_files(self):
        self.file_list.clear()
        if not self.html_dir.exists():
            self.html_dir.mkdir(parents=True, exist_ok=True)
        files = sorted([p for p in self.html_dir.iterdir() if p.suffix.lower() in {".html", ".htm"}])
        for p in files:
            label = short_file_display_name(p)
            it = QtWidgets.QListWidgetItem(label)
            it.setData(QtCore.Qt.UserRole, str(p))
            self.file_list.addItem(it)
        self.lbl_folder.setText(f"HTML folder: {self.html_dir}")
        self.lbl_status.setText(
            f"Found {len(files)} HTML file(s) in current folder. You can also use 'Add HTML Files…'"
        )

    def select_all_files(self):
        self.file_list.selectAll()

    def add_files_via_dialog(self):
        start_dir = str(self.html_dir if self.html_dir.exists() else BASE_DIR)
        paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            "Select HTML files",
            start_dir,
            "HTML Files (*.html *.htm)"
        )
        if not paths:
            return
        added = 0
        for p in paths:
            path = pathlib.Path(p)
            exists = any(self.file_list.item(i).data(QtCore.Qt.UserRole) == str(path)
                         for i in range(self.file_list.count()))
            if exists:
                continue
            label = short_file_display_name(path)
            it = QtWidgets.QListWidgetItem(label)
            it.setData(QtCore.Qt.UserRole, str(path))
            self.file_list.addItem(it)
            added += 1
        if added:
            self.lbl_status.setText(f"Added {added} file(s). Total: {self.file_list.count()}")

    def clear_file_list(self):
        self.file_list.clear()
        self.lbl_status.setText("File list cleared. Use 'Add HTML Files…' or 'Refresh HTML Folder'.")

    def set_default_dir(self):
        start_dir = str(self.html_dir if self.html_dir.exists() else BASE_DIR)
        picked = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Choose default HTML folder",
            start_dir
        )
        if not picked:
            return
        self.html_dir = pathlib.Path(picked)
        self.settings.setValue("default_html_dir", str(self.html_dir))
        self.refresh_files()
        QtWidgets.QMessageBox.information(
            self, APP_NAME,
            f"Default folder set to:\n{self.html_dir}"
        )

    def load_tables(self):
        self.records.clear()
        self.table_list.clear()
        selected = self.file_list.selectedItems()
        if not selected:
            QtWidgets.QMessageBox.information(self, APP_NAME, "Please select at least one HTML file.")
            return

        count_files = 0
        for it in selected:
            path = pathlib.Path(it.data(QtCore.Qt.UserRole))
            try:
                recs = read_all_tables_from_html_file(path)
                for r in recs:
                    self.records.append(r)
                    list_label = f"{pretty_table_label(r)} :: {r.df.shape[0]}x{r.df.shape[1]}"
                    it_tab = QtWidgets.QListWidgetItem(list_label)
                    it_tab.setData(QtCore.Qt.UserRole, len(self.records)-1)
                    self.table_list.addItem(it_tab)
                count_files += 1
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, APP_NAME, f"Failed to parse {path.name}:\n{e}")

        self.lbl_status.setText(f"Loaded {len(self.records)} table(s) from {count_files} file(s).")

    def on_table_selection(self):
        items = self.table_list.selectedItems()
        if not items:
            self.preview.show_dataframe(pd.DataFrame())
            return
        idx = items[0].data(QtCore.Qt.UserRole)
        rec = self.records[idx]
        self.preview.show_dataframe(rec.df)

    def select_all_tables(self):
        self.table_list.selectAll()

    def export_tables(self, only_selected: bool):
        if not self.records:
            QtWidgets.QMessageBox.information(self, APP_NAME, "No tables loaded.")
            return

        if only_selected:
            items = self.table_list.selectedItems()
            if not items:
                QtWidgets.QMessageBox.information(self, APP_NAME, "Please select table(s) to export.")
                return
            indices = [it.data(QtCore.Qt.UserRole) for it in items]
        else:
            indices = list(range(len(self.records)))

        OUT_DIR.mkdir(parents=True, exist_ok=True)

        dirs_used = set()
        count = 0
        for i in indices:
            rec = self.records[i]
            per_source = OUT_DIR / sanitize_filename(rec.source_file.stem)
            per_source.mkdir(parents=True, exist_ok=True)
            dirs_used.add(str(per_source.resolve()))
            base = f"{sanitize_filename(rec.source_file.stem)}__{sanitize_filename(rec.table_id)}.csv"
            fp = per_source / base
            try:
                rec.df.to_csv(fp, index=False)
                count += 1
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, APP_NAME, f"Failed to save {fp.name}:\n{e}")

        # Decide which folder to open: if all exports went to one folder, open that; otherwise open OUT_DIR
        if dirs_used:
            if len(dirs_used) == 1:
                folder_to_open = pathlib.Path(next(iter(dirs_used)))
            else:
                folder_to_open = OUT_DIR
        else:
            folder_to_open = OUT_DIR

        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle(APP_NAME)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(f"Exported {count} CSV file(s) into:\n{folder_to_open}")
        btn_open = msg.addButton("Open Folder", QtWidgets.QMessageBox.AcceptRole)
        btn_close = msg.addButton("Close", QtWidgets.QMessageBox.RejectRole)
        msg.exec()
        if msg.clickedButton() == btn_open:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(str(folder_to_open)))

# ------------- main -------------

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_ORG)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()