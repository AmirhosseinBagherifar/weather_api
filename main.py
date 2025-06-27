import sys
import os
import csv
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit
)
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("وضعیت آب و هوا ")
        self.setGeometry(300, 300, 400, 300)

        self.layout = QVBoxLayout()

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("نام شهر را وارد کنید ")
        self.layout.addWidget(self.city_input)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.layout.addWidget(self.result_box)

        self.get_button = QPushButton(" گرفتن اطلاعات آب‌وهوا")
        self.get_button.clicked.connect(self.get_weather)
        self.layout.addWidget(self.get_button)

        self.save_csv_button = QPushButton("📁 ذخیره در فایل CSV")
        self.save_csv_button.clicked.connect(self.save_to_csv)
        self.layout.addWidget(self.save_csv_button)

        self.setLayout(self.layout)
        self.latest_info = {}

    def get_weather(self):
        city_name = self.city_input.text().strip()
        if not city_name:
            self.result_box.setText("لطفاً نام شهر را وارد کنید.")
            return

        if not API_KEY:
            self.result_box.setText(" کلید API پیدا نشد. فایل .env را بررسی کنید.")
            return

        params = {
            "q": city_name,
            "appid": API_KEY,
            "units": "metric",
            "lang": "fa"
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            main = data["main"]
            weather = data["weather"][0]

            temp = main["temp"]
            humidity = main["humidity"]
            description = weather["description"]

            result = (
                f"🌆 شهر: {city_name}\n"
                f"🌤 وضعیت: {description}\n"
                f"🌡 دما: {temp}°C\n"
                f"💧 رطوبت: {humidity}%\n"
            )
            self.result_box.setText(result)

            self.latest_info = {
                "city": city_name,
                "description": description,
                "temp": temp,
                "humidity": humidity
            }
        else:
            self.result_box.setText(" خطا در دریافت اطلاعات.\n " + str(response.status_code))

    def save_to_csv(self):
        if self.latest_info:
            file_exists = os.path.isfile("weather.csv")
            with open("weather.csv", "a", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["شهر", "وضعیت", "دما (°C)", "رطوبت (%)"])
                writer.writerow([
                    self.latest_info['city'],
                    self.latest_info['description'],
                    self.latest_info['temp'],
                    self.latest_info['humidity']
                ])
            self.result_box.append("\n ذخیره شد در weather.csv")
        else:
            self.result_box.setText(" ابتدا اطلاعات را بگیرید.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
