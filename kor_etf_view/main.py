import sys
import json
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QHeaderView, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

# JSON 파일의 상대 경로 설정
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(SCRIPT_DIR, 'stock.json')

class ETFDataViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("한국 주식(ETF) 데이터 현황")
        self.setGeometry(100, 100, 650, 450)

        main_layout = QVBoxLayout()

        # 전체 타이틀 추가
        title_label = QLabel("한국 주식(ETF) 정보 현황")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 23))
        main_layout.addWidget(title_label)

        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("URL을 입력하세요")
        self.url_input.returnPressed.connect(self.fetch_data)
        input_layout.addWidget(self.url_input)

        button_layout = QHBoxLayout()
        self.fetch_button = QPushButton("데이터 가져오기")
        self.fetch_button.clicked.connect(self.fetch_data)
        button_layout.addWidget(self.fetch_button)

        self.update_button = QPushButton("업데이트")
        self.update_button.clicked.connect(self.update_data)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("삭제")
        self.delete_button.clicked.connect(self.delete_data)
        button_layout.addWidget(self.delete_button)

        self.clear_button = QPushButton("초기화")
        self.clear_button.clicked.connect(self.clear_input)
        button_layout.addWidget(self.clear_button)

        input_layout.addLayout(button_layout)
        main_layout.addLayout(input_layout)

        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        # 인용구 섹션 수정
        footer_layout = QHBoxLayout()
        url_label = QLabel("URL : https://finance.naver.com/item/main.naver?code=360750")
        url_label.setFont(QFont("Arial", 12))
        footer_layout.addWidget(url_label)
        
        made_by_label = QLabel("made by 나종춘(2024)")
        made_by_label.setFont(QFont("Arial", 12))
        made_by_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        footer_layout.addWidget(made_by_label)
        
        main_layout.addLayout(footer_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.load_data_from_json()

        # 아이콘 설정
        self.setWindowIcon(QIcon('MyIcon.icns'))

    def fetch_data(self):
        url = self.url_input.text()
        if not url:
            url = "https://finance.naver.com/item/main.naver?code=459580"
        
        etf_data = self.get_etf_data(url)
        self.add_data_to_table(etf_data)
        self.save_data_to_json()
        self.url_input.clear()  # URL 입력 필드만 초기화
        QMessageBox.information(self, "성공", "데이터 가져오기에 성공했습니다.")

    def get_etf_data(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        etf_name = soup.select_one('div.wrap_company h2 a').text.strip()
        code = soup.select_one('div.description span.code').text.strip()
        
        market_cap = soup.select_one('div.first table em#_market_sum').text.strip()
        market_cap = market_cap.replace('\t', '').replace('\n', '')
        
        fee = soup.select_one('table.tbl_type1 td em').text.strip()
        
        asset_manager = soup.select('table.tbl_type1')[1].select('td')[1].text.strip()
        
        returns = soup.select('div#tab_con1 > div:last-child table tr')
        six_month_return = returns[2].select_one('td em').text.strip()
        one_year_return = returns[3].select_one('td em').text.strip()

        data = {
            '자산운용사': asset_manager,
            'ETF이름': etf_name,
            '종목코드': code,
            '시가총액': market_cap,
            '펀드보수': fee,
            '6개월 수익률': six_month_return,
            '1년 수익률': one_year_return
        }

        return data

    def add_data_to_table(self, data):
        if self.table.rowCount() == 0:
            self.table.setColumnCount(len(data))
            self.table.setHorizontalHeaderLabels(data.keys())

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        for col, (key, value) in enumerate(data.items()):
            item = QTableWidgetItem(str(value))
            if key == '종목코드':
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            elif key in ['시가총액', '펀드보수', '6개월 수익률', '1년 수익률']:
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_position, col, item)

        self.adjust_table_size()

    def adjust_table_size(self):
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            if self.table.horizontalHeaderItem(i).text() == "종목코드":
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
                self.table.setColumnWidth(i, 70)  # 6자리 정수 + 여유 공간
            elif self.table.horizontalHeaderItem(i).text() in ["시가총액", "펀드보수", "6개월 수익률", "1년 수익률"]:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
                self.table.setColumnWidth(i, 100)  # 10자리 정수 + 여유 공간
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

    def save_data_to_json(self):
        data = []
        for row in range(self.table.rowCount()):
            row_data = {}
            for col in range(self.table.columnCount()):
                header_item = self.table.horizontalHeaderItem(col)
                if header_item is not None:
                    key = header_item.text()
                    value = self.table.item(row, col).text() if self.table.item(row, col) is not None else ""
                    row_data[key] = value
            data.append(row_data)

        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data_from_json(self):
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data:
                self.table.setColumnCount(len(data[0]))
                self.table.setHorizontalHeaderLabels(data[0].keys())

                for row_data in data:
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    for col, (key, value) in enumerate(row_data.items()):
                        item = QTableWidgetItem(str(value))
                        if key == '종목코드':
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        elif key in ['시가총액', '펀드보수', '6개월 수익률', '1년 수익률']:
                            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                        self.table.setItem(row_position, col, item)

                self.adjust_table_size()

    def update_data(self):
        for row in range(self.table.rowCount()):
            code = self.table.item(row, 2).text()  # 종목코드는 3번째 열에 있습니다
            url = f"https://finance.naver.com/item/main.naver?code={code}"
            updated_data = self.get_etf_data(url)
            for col, (key, value) in enumerate(updated_data.items()):
                item = QTableWidgetItem(str(value))
                if key == '종목코드':
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                elif key in ['시가총액', '펀드보수', '6개월 수익률', '1년 수익률']:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, col, item)
        self.save_data_to_json()
        QMessageBox.information(self, "성공", "현재날짜 정보로 업데이트 완료했습니다.")

    def delete_data(self):
        selected_rows = set(index.row() for index in self.table.selectedIndexes())
        for row in sorted(selected_rows, reverse=True):
            self.table.removeRow(row)
        self.save_data_to_json()
        QMessageBox.information(self, "성공", "삭제 완료했습니다.")

    def clear_input(self):
        self.url_input.clear()
        QMessageBox.information(self, "성공", "초기화 완료했습니다.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ETFDataViewer()
    viewer.show()
    sys.exit(app.exec())
