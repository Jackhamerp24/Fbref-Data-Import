# FBref Offline Scraper

Vietnamese Below

### Overview
FBref Offline Scraper is a cross-platform desktop tool that extracts football player statistics from offline FBref HTML pages and converts them into CSV files for analysis.

It works entirely offline. Once you have downloaded the HTML pages from FBref, you can analyze, convert, and save the data without any internet connection.

### Features
- Works completely offline  
- Extracts all FBref player tables, including:
  - Standard Stats
  - Shooting
  - Passing and Pass Types
  - Goal and Shot Creation
  - Possession and Defensive Actions  
- Converts all tables into structured CSV files  
- Supports multiple player HTML files at once  
- Simple, no-code interface  
- Works on Windows (.exe) and macOS (.dmg)

### Installation

#### Windows
1. Go to the Releases page:  
   https://github.com/Jackhamerp24/Fbref-Data-Import/releases
2. Download the latest file named `FBref_Offline_Scraper_Windows.zip`.
3. Extract it to a folder.
4. Double-click `FBref Offline Scraper.exe` to launch the app.

#### macOS
1. Download the latest `FBref_Offline_Scraper_macOS.dmg` file from the Releases page.  
2. Open the `.dmg` file and drag `FBref Offline Scraper.app` into your Applications folder.  
3. If macOS blocks the app, right-click it, choose "Open", then select "Allow".

### Usage

#### 1. Prepare HTML files
FBref does not provide an API. You must download each player's HTML page manually.

1. Visit a player’s FBref page, for example:  
   https://fbref.com/en/players/e7fcf289/Florian-Wirtz
2. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac).  
3. Choose “Webpage, Complete” and save the file to your computer.  
4. Move the downloaded `.html` file into the `HTML` folder next to the app.
5. 
#### 2. Run the application
When you start the program:
- It automatically scans the `HTML` folder for FBref files.
- Lists all available player HTML files.
- You select which one(s) to extract.
- The data is parsed and saved automatically as CSV files.

#### 3. Output
Extracted data is saved under an `output` folder, organized by player name.

### Notes
- Each player’s page may have different available tables depending on competitions.
- The app supports domestic leagues, cups, and international statistics.
- All processing happens locally; no data is uploaded.
- Multiple `.html` files can be processed at once.

### Developer Setup (Optional)
If you prefer to run directly from source:
git clone https://github.com/Jackhamerp24/Fbref-Data-Import.git
cd Fbref-Data-Import
pip install -r requirements.txt
python fbref_scraper.py

## Vietnamese Version

### Giới thiệu
FBref Offline Scraper là công cụ hỗ trợ trích xuất dữ liệu thống kê cầu thủ bóng đá từ các trang FBref đã tải về (HTML) và chuyển đổi chúng thành các tệp CSV để phân tích.

Ứng dụng hoạt động hoàn toàn ngoại tuyến. Sau khi tải HTML từ FBref, bạn có thể phân tích, chuyển đổi và lưu dữ liệu mà không cần internet.

### Tính năng
- Hoạt động hoàn toàn offline  
- Trích xuất tất cả các bảng thống kê cầu thủ:
  - Thống kê cơ bản (Standard)
  - Dứt điểm (Shooting)
  - Chuyền bóng (Passing, Pass Types)
  - Tạo cơ hội và bàn thắng (Goal and Shot Creation)
  - Kiểm soát bóng và phòng ngự (Possession, Defense)  
- Tự động xuất các bảng dữ liệu ra tệp CSV có cấu trúc rõ ràng  
- Hỗ trợ nhiều tệp HTML cùng lúc  
- Giao diện đơn giản, dễ sử dụng  
- Hỗ trợ cả Windows (.exe) và macOS (.dmg)

### Cài đặt

#### Windows
1. Truy cập trang Releases:  
   https://github.com/Jackhamerp24/Fbref-Data-Import/releases
2. Tải tệp `FBref_Offline_Scraper_Windows.zip` mới nhất.  
3. Giải nén vào một thư mục.  
4. Mở tệp `FBref Offline Scraper.exe` để chạy.

#### macOS
1. Tải tệp `FBref_Offline_Scraper_macOS.dmg` mới nhất từ trang Releases.  
2. Mở tệp `.dmg` và kéo ứng dụng vào thư mục Applications.  
3. Nếu macOS cảnh báo ứng dụng từ nhà phát triển không xác định, nhấn chuột phải → “Open” → “Allow”.

### Cách sử dụng

#### 1. Chuẩn bị tệp HTML
Do FBref không cung cấp API, bạn cần tải thủ công trang cầu thủ về.

1. Mở trang cầu thủ, ví dụ:  
   https://fbref.com/en/players/e7fcf289/Florian-Wirtz
2. Nhấn `Ctrl + S` (Windows) hoặc `Cmd + S` (Mac).  
3. Chọn “Webpage, Complete” và lưu về máy tính.  
4. Chuyển tệp `.html` đã tải vào thư mục `HTML` nằm cạnh ứng dụng.
#### 2. Chạy chương trình
Khi khởi động:
- Ứng dụng sẽ tự động quét thư mục `HTML` để tìm các tệp FBref.
- Hiển thị danh sách cầu thủ có sẵn.
- Bạn chọn cầu thủ cần trích xuất.
- Ứng dụng tự động tạo các tệp CSV trong thư mục `output`.

#### 3. Kết quả
Dữ liệu xuất ra sẽ được lưu theo từng cầu thủ trong thư mục `output`.
### Ghi chú
- Mỗi cầu thủ có thể có các bảng khác nhau tùy theo giải đấu.
- Hỗ trợ thống kê giải quốc nội, cúp và quốc tế.
- Dữ liệu được xử lý hoàn toàn nội bộ, không gửi ra ngoài.
- Có thể xử lý nhiều cầu thủ cùng lúc.

### Thiết lập cho lập trình viên (Tùy chọn)
Nếu muốn chạy mã nguồn trực tiếp:
git clone https://github.com/Jackhamerp24/Fbref-Data-Import.git
cd Fbref-Data-Import
pip install -r requirements.txt
python fbref_scraper.py
