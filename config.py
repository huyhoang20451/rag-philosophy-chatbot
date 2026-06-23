# config.py
import os

# Dữ liệu text mẫu (Rút gọn cho tối ưu, bạn có thể bổ sung thêm)
HUVO_TEXT = "Hư vô – khoảng trống để con người tìm thấy chính mình..."
BIQUAN_TEXT = "Chủ nghĩa bi quan (Pessimism) nhấn mạnh tính chất ưu thế của đau khổ..."
KHACKY_TEXT = "Chủ nghĩa Khắc Kỷ nhấn mạnh việc làm chủ cảm xúc và chấp nhận điều không thể kiểm soát..."
HIEN_SINH_TEXT = "Triết học hiện sinh nhấn mạnh vào tự do cá nhân, trách nhiệm, và ý nghĩa tự tạo..."
MACLENIN_TEXT = "Triết học Mác-Lênin là hệ thống quan điểm về thế giới quan duy vật biện chứng..."

CHATBOT_CONFIGS = {
    'huvo': {
        'school_name': 'Hư Vô',
        'text_data': HUVO_TEXT,
        'additional_instructions': "- TÍNH CÁCH: An nhiên, trấn tĩnh. - THÔNG ĐIỆP CHÍNH: 'Buông bỏ để tự do'."
    },
    'biquan': {
        'school_name': 'Bi Quan',
        'text_data': BIQUAN_TEXT,
        'additional_instructions': "- TÍNH CÁCH: Cảm xúc, sâu sắc. - THÔNG ĐIỆP CHÍNH: 'Chấp nhận nỗi buồn để lớn lên'."
    },
    'khacky': {
        'school_name': 'Khắc Kỷ',
        'text_data': KHACKY_TEXT,
        'additional_instructions': "- TÍNH CÁCH: Lý trí, vững vàng. - THÔNG ĐIỆP CHÍNH: 'Làm chủ cảm xúc và phản ứng'."
    },
    'hien_sinh': {
        'school_name': 'Hiện Sinh',
        'text_data': HIEN_SINH_TEXT,
        'additional_instructions': "- TÍNH CÁCH: Tự do, khám phá bản thân. - THÔNG ĐIỆP CHÍNH: 'Sống có ý nghĩa và trách nhiệm'."
    },
    'maclenin': {
        'school_name': 'Mác-Lênin',
        'text_data': MACLENIN_TEXT,
        'additional_instructions': "- TÍNH CÁCH: Nhân văn, kết nối. - THÔNG ĐIỆP CHÍNH: 'Cùng nhau tạo giá trị cho con người'."
    }
}