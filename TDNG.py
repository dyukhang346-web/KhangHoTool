# -*- coding: utf-8 -*-
from googletrans import Translator, LANGUAGES
from colorama import Style, init
import pyfiglet
import sys
from getpass import getpass  
import os
import json
import socket
from pathlib import Path
from datetime import datetime


init()

def rgb_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def gradient_text(text, start, end):
    result = ""
    n = len(text)
    for i, c in enumerate(text):
        t = i / max(1, n - 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        result += f"{rgb_ansi(r, g, b)}{c}\033[0m"
    return result

def banner():
    text = "KhangHo"
    ascii_art = pyfiglet.figlet_format(text, font="standard")
    lines = ascii_art.splitlines()
    total_chars = sum(len(line.replace(" ", "")) for line in lines)

    start = (148, 0, 211)   # tím
    end = (0, 255, 255)     # cyan

    def lerp(a, b, t):
        return int(a + (b - a) * t)

    char_count = 0
    colored_ascii = ""

    for line in lines:
        for c in line:
            if c == " ":
                colored_ascii += " "
            else:
                t = char_count / max(1, total_chars - 1)
                r = lerp(start[0], end[0], t)
                g = lerp(start[1], end[1], t)
                b = lerp(start[2], end[2], t)
                colored_ascii += f"{rgb_ansi(r, g, b)}{c}\033[0m"
                char_count += 1
        colored_ascii += "\n"

    # Gradient tím → đỏ cho thông tin
    start_info = (148, 0, 211)
    end_info = (255, 0, 0)

    print(colored_ascii)
    print(gradient_text("═" * 60, start_info, end_info))
    print(gradient_text(" Admin      : Hồ Duy Khang", start_info, end_info))
    print(gradient_text(" Facebook   : https://www.facebook.com/d4fresytDK", start_info, end_info))
    print(gradient_text(" TikTok     : https://tiktok.com/anhbanhatbox", start_info, end_info))
    print(gradient_text(" Gmail      : dyukhang346@gmail.com", start_info, end_info))
    print(gradient_text("═" * 60, start_info, end_info))
    print()

def gioi_thieu():
    print(gradient_text("Tool Dịch Văn Bản Đa Ngôn Ngữ", (148, 0, 211), (255, 0, 0)))
    print(gradient_text("By: Hồ Duy Khang\n", (148, 0, 211), (255, 0, 0)))

def dich_van_ban(van_ban, src_lang, list_ngon_ngu):
    translator = Translator()
    ket_qua = {}
    for lang_code in list_ngon_ngu:
        try:
            result = translator.translate(van_ban, src=src_lang, dest=lang_code)
            ket_qua[lang_code] = result.text
        except Exception as e:
            ket_qua[lang_code] = f"Lỗi dịch: {e}"
    return ket_qua

def hien_thi_ngon_ngu():
    print(gradient_text("\nDanh sách các ngôn ngữ khả dụng:", (148, 0, 211), (255, 0, 0)))
    for code, name in sorted(LANGUAGES.items()):
        print(gradient_text(f"{code}: {name}", (148, 0, 211), (255, 0, 0)))

def nhap_ngon_ngu(dest_only=False):
    while True:
        nguoi_dung = input(
            gradient_text(
                ("\nNhập mã ngôn ngữ cần dịch" if not dest_only else "\nNhập mã ngôn ngữ gốc: ")
                + " ('all' = tất cả): ",
                (148, 0, 211), (255, 0, 0)
            )
        ).strip().lower()

        if nguoi_dung == 'all' and not dest_only:
            return list(LANGUAGES.keys())
        elif dest_only:  
            if nguoi_dung in LANGUAGES:
                return nguoi_dung
            else:
                print(gradient_text("❌ Mã ngôn ngữ không hợp lệ!", (255, 0, 0), (148, 0, 211)))
                hien_thi_ngon_ngu()
        else:
            list_codes = [code.strip() for code in nguoi_dung.split(',')]
            invalid = [c for c in list_codes if c not in LANGUAGES]
            if invalid:
                print(gradient_text("❌ Mã ngôn ngữ không hợp lệ: " + str(invalid), (255, 0, 0), (148, 0, 211)))
                hien_thi_ngon_ngu()
            else:
                return list_codes

def nhap_nhieu_dong():
    print(gradient_text("👉 Nhập văn bản (Enter trống = xong, gõ 'e' = hủy):", (148, 0, 211), (255, 0, 0)))
    dong_van_ban = []
    while True:
        try:
            dong = input()
            if dong.strip().lower() == "e":
                return None
            if dong.strip() == "":
                break
            dong_van_ban.append(dong)
        except KeyboardInterrupt:
            break
    return "\n".join(dong_van_ban)

def menu():
    print(gradient_text("\n========= MENU =========", (148, 0, 211), (255, 0, 0)))
    print(gradient_text("1. Dịch từ Tiếng Việt sang ngôn ngữ khác", (148, 0, 211), (255, 0, 0)))
    print(gradient_text("2. Dịch từ ngôn ngữ khác sang Tiếng Việt", (148, 0, 211), (255, 0, 0)))
    print(gradient_text("3. Xem danh sách ngôn ngữ", (148, 0, 211), (255, 0, 0)))
    print(gradient_text("4. Thoát", (148, 0, 211), (255, 0, 0)))
    print(gradient_text("========================", (148, 0, 211), (255, 0, 0)))

# ===================== KEY CHECK + MAIN =====================
def check_key():
    CORRECT_KEY = "TDNG24032014"  
    MAX_TRIES = 5


    for attempt in range(1, MAX_TRIES + 1):
        entered = input(gradient_text("Nhập key để sử dụng tool: ", (148, 0, 211), (255, 0, 0)))

        if entered == CORRECT_KEY:
            print(gradient_text("✅ Key hợp lệ\n", (0, 255, 0), (148, 0, 211)))
            return True
        else:
            remaining = MAX_TRIES - attempt
            if remaining > 0:
                print(gradient_text(f"❌ Key không đúng. Còn {remaining} lần thử.", (255, 0, 0), (148, 0, 211)))
            else:
                print(gradient_text("❌ Bạn đã nhập sai quá nhiều lần. Thoát chương trình.", (255, 0, 0), (148, 0, 211)))
    return False


if __name__ == "__main__":
    if not check_key():
        sys.exit(1)

    banner()
    gioi_thieu()

    while True:
        menu()
        lua_chon = input("\033[96mChọn chức năng (1-4): \033[0m").strip()  # Giữ nguyên màu cyan

        # 1. Dịch từ tiếng Việt sang nhiều ngôn ngữ
        if lua_chon == "1":
            van_ban_day_du = nhap_nhieu_dong()
            if van_ban_day_du:
                hien_thi_ngon_ngu()
                list_ngon_ngu = nhap_ngon_ngu()
                print(gradient_text("\nĐang dịch............\n", (148, 0, 211), (255, 0, 0)))
                ket_qua_dich = dich_van_ban(van_ban_day_du, "vi", list_ngon_ngu)

                for lang_code, text_dich in ket_qua_dich.items():
                    print(gradient_text(f"[{lang_code} - {LANGUAGES[lang_code]}]:", (148, 0, 211), (255, 0, 0)))
                    print(gradient_text(text_dich, (148, 0, 211), (255, 0, 0)))
                    print(gradient_text("-" * 50, (148, 0, 211), (255, 0, 0)))

        # 2. Dịch từ ngôn ngữ khác sang Tiếng Việt
        elif lua_chon == "2":
            hien_thi_ngon_ngu()
            src_lang = nhap_ngon_ngu(dest_only=True)
            van_ban_day_du = nhap_nhieu_dong()
            if van_ban_day_du:
                print(gradient_text("\nĐang dịch sang Tiếng Việt............\n", (148, 0, 211), (255, 0, 0)))
                ket_qua_dich = dich_van_ban(van_ban_day_du, src_lang, ["vi"])
                print(gradient_text(f"[{src_lang} → vi]:", (148, 0, 211), (255, 0, 0)))
                print(gradient_text(ket_qua_dich["vi"], (148, 0, 211), (255, 0, 0)))
                print(gradient_text("-" * 50, (148, 0, 211), (255, 0, 0)))

        # 3. Xem danh sách ngôn ngữ
        elif lua_chon == "3":
            hien_thi_ngon_ngu()

        # 4. Thoát
        elif lua_chon == "4":
            print(gradient_text("\nCảm ơn đã sử dụng! Thoát chương trình.", (255, 0, 0), (148, 0, 211)))
            sys.exit()

        else:
            print(gradient_text("❌ Lựa chọn không hợp lệ, vui lòng thử lại!", (255, 0, 0), (148, 0, 211)))
