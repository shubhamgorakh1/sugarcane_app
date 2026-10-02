import json
import os
from datetime import date
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from io import BytesIO
from flask import (
    Flask,
    jsonify,
    redirect,
    flash,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_db_connection


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "SECRET_KEY=K8#vR2!mQ7@xP4$zN9^tL6&cW3*eH5")


# ============================================================
# TRANSLATIONS
# ============================================================

TRANSLATIONS = {
    "en": {
        "dashboard": "Dashboard",
        "farmers": "Farmers",
        "nondni": "Nondni",
        "nondni_records": "Nondni Records",
        "reports": "Reports",
        "seasons": "Seasons",
        "audit_logs": "Audit Logs",
        "change_password": "Change Password",
        "logout": "Logout",
        "language": "Language",
        "welcome": "Welcome to Sugarcane ERP",
        "dashboard_description": "Manage farmers, sugarcane Nondni, seasons and reports from one place.",
        "season": "Season",
        "all_years": "All Years",
        "total_farmers": "Total Farmers",
        "total_nondni": "Total Nondni",
        "total_area": "Total Planting Area",
        "active_seasons": "Active Seasons",
        "dashboard_info_title": "Dashboard Overview",
        "dashboard_info_text": "Use the season filter to view Nondni count and planting area for a selected season or all years.",
        "farmers_title": "Farmers",
        "farmer_code": "Farmer Code",
        "farmer_name": "Farmer Name",
        "mobile": "Mobile",
        "village": "Village",
        "taluka": "Taluka",
        "district": "District",
        "land_area": "Land Area",
        "aadhaar_no": "Aadhaar Number",
        "land_account_no": "Land Account Number",
        "latitude": "GPS Latitude",
        "longitude": "GPS Longitude",
        "search_farmer": "Search by name, mobile or village",
        "search": "Search",
        "clear": "Clear",
        "add_farmer": "Add Farmer",
        "action": "Action",
        "edit": "Edit",
        "no_farmers": "No farmers found.",
        "add_farmer_description": "Add permanent farmer information. Farmer Code is generated automatically.",
        "save_farmer": "Save Farmer",
        "cancel": "Cancel",
        "edit_farmer": "Edit Farmer",
        "edit_farmer_description": "Update permanent farmer information.",
        "update_farmer": "Update Farmer",
        "nondni_title": "Sugarcane Nondni",
        "nondni_description": "Search an existing farmer and enter the season-specific sugarcane registration details.",
        "search_farmer_title": "Search Farmer",
        "search_farmer_nondni": "Enter Farmer Code or Mobile Number",
        "farmer_details": "Farmer Details",
        "nondni_details": "Nondni Details",
        "survey_gat_no": "Survey / Gat No.",
        "planting_date": "Planting Date",
        "sugarcane_variety": "Sugarcane Variety",
        "crop_type": "Crop Type",
        "irrigation_method": "Irrigation Method",
        "planting_area": "Planting Area",
        "receipt_no": "Receipt No.",
        "save_nondni": "Save Nondni",
        "view_nondni_records": "View Nondni Records",
        "farmer_not_found": "Farmer not found.",
        "search_first": "Please search for a farmer first.",
        "nondni_saved": "Nondni saved successfully.",
        "save_error": "Unable to save Nondni.",
        "nondni_records_description": "View and search season-wise Nondni records.",
        "search_nondni": "Search by farmer code, name or village",
        "no_nondni_records": "No Nondni records found.",
        "edit_nondni": "Edit Nondni",
        "edit_nondni_description": "Update season-specific Nondni details.",
        "update_nondni": "Update Nondni",
        "back_to_records": "Back to Records",
        "reports_title": "Reports",
        "custom_date_report": "Custom Date Report",
        "reports_description": "Generate a report for a selected season and custom planting-date range.",
        "from_date": "From Date",
        "to_date": "To Date",
        "generate_report": "Generate Report",
        "report_summary": "Report Summary",
        "date_range": "Date Range",
        "download_pdf": "Download PDF",
        "no_report_data": "No report data found.",
        "select_dates_message": "Please select both dates.",
        "report_period": "Report Period",
        "season_management": "Season Management",
        "seasons_description": "Manage available sugarcane seasons.",
        "add_season": "Add Season",
        "season_name": "Season Name",
        "mark_as_active": "Set as Active Season",
        "save_season": "Save Season",
        "season_example": "e.g. 2026-27",
        "status": "Status",
        "created_at": "Created At",
        "active": "Active",
        "inactive": "Inactive",
        "no_seasons": "No seasons found.",
        "audit_logs_title": "Audit Logs",
        "audit_logs_description": "View important changes made in the system.",
        "username": "Username",
        "table": "Table",
        "record_id": "Record ID",
        "old_data": "Old Data",
        "new_data": "New Data",
        "date_time": "Date & Time",
        "no_audit_logs": "No audit logs found.",
        "change_password_description": "Change the current admin password securely.",
        "current_password": "Current Password",
        "new_password": "New Password",
        "confirm_password": "Confirm Password",
        "minimum_8_characters": "Minimum 8 characters",
        "change_password_button": "Change Password",
        "all_fields_required": "All fields are required.",
        "passwords_do_not_match": "New passwords do not match.",
        "password_minimum_length": "Password must be at least 8 characters.",
        "current_password_incorrect": "Current password is incorrect.",
        "password_changed_successfully": "Password changed successfully.",
        "total_nondni_label": "Total Nondni",
        "total_planting_area": "Total Planting Area",
    },
    "mr": {
        "dashboard": "डॅशबोर्ड",
        "farmers": "शेतकरी",
        "nondni": "नोंदणी",
        "nondni_records": "नोंदणी नोंदी",
        "reports": "अहवाल",
        "seasons": "हंगाम",
        "audit_logs": "ऑडिट नोंदी",
        "change_password": "पासवर्ड बदला",
        "logout": "लॉगआउट",
        "language": "भाषा",
        "welcome": "ऊस ERP मध्ये स्वागत आहे",
        "dashboard_description": "शेतकरी, ऊस नोंदणी, हंगाम आणि अहवाल एकाच ठिकाणी व्यवस्थापित करा.",
        "season": "हंगाम",
        "all_years": "सर्व वर्षे",
        "total_farmers": "एकूण शेतकरी",
        "total_nondni": "एकूण नोंदणी",
        "total_area": "एकूण लागवड क्षेत्र",
        "active_seasons": "सक्रिय हंगाम",
        "dashboard_info_title": "डॅशबोर्ड माहिती",
        "dashboard_info_text": "निवडलेल्या हंगामासाठी किंवा सर्व वर्षांसाठी नोंदणी संख्या आणि लागवड क्षेत्र पहा.",
        "farmers_title": "शेतकरी",
        "farmer_code": "शेतकरी कोड",
        "farmer_name": "शेतकरी नाव",
        "mobile": "मोबाईल",
        "village": "गाव",
        "taluka": "तालुका",
        "district": "जिल्हा",
        "land_area": "जमीन क्षेत्र",
        "aadhaar_no": "आधार क्रमांक",
        "land_account_no": "जमीन खाते क्रमांक",
        "latitude": "GPS अक्षांश",
        "longitude": "GPS रेखांश",
        "search_farmer": "नाव, मोबाईल किंवा गावाने शोधा",
        "search": "शोधा",
        "clear": "साफ करा",
        "add_farmer": "शेतकरी जोडा",
        "action": "कृती",
        "edit": "संपादित करा",
        "no_farmers": "शेतकरी सापडले नाहीत.",
        "add_farmer_description": "कायमस्वरूपी शेतकरी माहिती भरा. शेतकरी कोड आपोआप तयार होईल.",
        "save_farmer": "शेतकरी जतन करा",
        "cancel": "रद्द करा",
        "edit_farmer": "शेतकरी संपादित करा",
        "edit_farmer_description": "कायमस्वरूपी शेतकरी माहिती अद्ययावत करा.",
        "update_farmer": "शेतकरी अद्ययावत करा",
        "nondni_title": "ऊस नोंदणी",
        "nondni_description": "अस्तित्वातील शेतकरी शोधा आणि हंगामानुसार ऊस नोंदणी माहिती भरा.",
        "search_farmer_title": "शेतकरी शोधा",
        "search_farmer_nondni": "शेतकरी कोड किंवा मोबाईल क्रमांक टाका",
        "farmer_details": "शेतकरी माहिती",
        "nondni_details": "नोंदणी माहिती",
        "survey_gat_no": "सर्वे / गट क्र.",
        "planting_date": "लागवड दिनांक",
        "sugarcane_variety": "ऊस जात",
        "crop_type": "पीक प्रकार",
        "irrigation_method": "सिंचन पद्धत",
        "planting_area": "लागवड क्षेत्र",
        "receipt_no": "पावती क्र.",
        "save_nondni": "नोंदणी जतन करा",
        "view_nondni_records": "नोंदणी नोंदी पहा",
        "farmer_not_found": "शेतकरी सापडला नाही.",
        "search_first": "कृपया प्रथम शेतकरी शोधा.",
        "nondni_saved": "नोंदणी यशस्वीरीत्या जतन झाली.",
        "save_error": "नोंदणी जतन करता आली नाही.",
        "nondni_records_description": "हंगामानुसार नोंदणी नोंदी पहा आणि शोधा.",
        "search_nondni": "शेतकरी कोड, नाव किंवा गावाने शोधा",
        "no_nondni_records": "नोंदणी नोंदी सापडल्या नाहीत.",
        "edit_nondni": "नोंदणी संपादित करा",
        "edit_nondni_description": "हंगामानुसार नोंदणी माहिती अद्ययावत करा.",
        "update_nondni": "नोंदणी अद्ययावत करा",
        "back_to_records": "नोंदींकडे परत",
        "reports_title": "अहवाल",
        "custom_date_report": "सानुकूल दिनांक अहवाल",
        "reports_description": "निवडलेल्या हंगामासाठी आणि दिनांक श्रेणीसाठी अहवाल तयार करा.",
        "from_date": "पासून दिनांक",
        "to_date": "पर्यंत दिनांक",
        "generate_report": "अहवाल तयार करा",
        "report_summary": "अहवाल सारांश",
        "date_range": "दिनांक श्रेणी",
        "download_pdf": "PDF डाउनलोड करा",
        "no_report_data": "अहवालासाठी नोंदी नाहीत.",
        "select_dates_message": "कृपया दोन्ही दिनांक निवडा.",
        "report_period": "अहवाल कालावधी",
        "season_management": "हंगाम व्यवस्थापन",
        "seasons_description": "उपलब्ध ऊस हंगाम व्यवस्थापित करा.",
        "add_season": "हंगाम जोडा",
        "season_name": "हंगामाचे नाव",
        "mark_as_active": "सक्रिय हंगाम म्हणून सेट करा",
        "save_season": "हंगाम जतन करा",
        "season_example": "उदा. 2026-27",
        "status": "स्थिती",
        "created_at": "तयार दिनांक",
        "active": "सक्रिय",
        "inactive": "निष्क्रिय",
        "no_seasons": "हंगाम सापडले नाहीत.",
        "audit_logs_title": "ऑडिट नोंदी",
        "audit_logs_description": "सिस्टममध्ये झालेल्या महत्त्वाच्या बदलांच्या नोंदी पहा.",
        "username": "वापरकर्ता नाव",
        "table": "टेबल",
        "record_id": "रेकॉर्ड क्र.",
        "old_data": "जुनी माहिती",
        "new_data": "नवीन माहिती",
        "date_time": "दिनांक व वेळ",
        "no_audit_logs": "ऑडिट नोंदी सापडल्या नाहीत.",
        "change_password_description": "सध्याचा प्रशासक पासवर्ड सुरक्षितपणे बदला.",
        "current_password": "सध्याचा पासवर्ड",
        "new_password": "नवीन पासवर्ड",
        "confirm_password": "पासवर्ड पुन्हा टाका",
        "minimum_8_characters": "किमान 8 अक्षरे",
        "change_password_button": "पासवर्ड बदला",
        "all_fields_required": "सर्व माहिती भरणे आवश्यक आहे.",
        "passwords_do_not_match": "नवीन पासवर्ड जुळत नाहीत.",
        "password_minimum_length": "पासवर्ड किमान 8 अक्षरांचा असावा.",
        "current_password_incorrect": "सध्याचा पासवर्ड चुकीचा आहे.",
        "password_changed_successfully": "पासवर्ड यशस्वीरीत्या बदलला.",
        "total_nondni_label": "एकूण नोंदणी",
        "total_planting_area": "एकूण लागवड क्षेत्र",
    },
    "hi": {
        "dashboard": "डैशबोर्ड",
        "farmers": "किसान",
        "nondni": "पंजीकरण",
        "nondni_records": "पंजीकरण रिकॉर्ड",
        "reports": "रिपोर्ट",
        "seasons": "सीजन",
        "audit_logs": "ऑडिट लॉग",
        "change_password": "पासवर्ड बदलें",
        "logout": "लॉगआउट",
        "language": "भाषा",
        "welcome": "गन्ना ERP में आपका स्वागत है",
        "dashboard_description": "किसान, गन्ना पंजीकरण, सीजन और रिपोर्ट एक ही जगह प्रबंधित करें।",
        "season": "सीजन",
        "all_years": "सभी वर्ष",
        "total_farmers": "कुल किसान",
        "total_nondni": "कुल पंजीकरण",
        "total_area": "कुल रोपण क्षेत्र",
        "active_seasons": "सक्रिय सीजन",
        "dashboard_info_title": "डैशबोर्ड जानकारी",
        "dashboard_info_text": "चयनित सीजन या सभी वर्षों के लिए पंजीकरण संख्या और रोपण क्षेत्र देखें।",
        "farmers_title": "किसान",
        "farmer_code": "किसान कोड",
        "farmer_name": "किसान का नाम",
        "mobile": "मोबाइल",
        "village": "गांव",
        "taluka": "तालुका",
        "district": "जिला",
        "land_area": "भूमि क्षेत्र",
        "aadhaar_no": "आधार नंबर",
        "land_account_no": "भूमि खाता नंबर",
        "latitude": "GPS अक्षांश",
        "longitude": "GPS देशांतर",
        "search_farmer": "नाम, मोबाइल या गांव से खोजें",
        "search": "खोजें",
        "clear": "साफ करें",
        "add_farmer": "किसान जोड़ें",
        "action": "कार्य",
        "edit": "संपादित करें",
        "no_farmers": "कोई किसान नहीं मिला।",
        "add_farmer_description": "स्थायी किसान जानकारी दर्ज करें। किसान कोड अपने आप बनेगा।",
        "save_farmer": "किसान सेव करें",
        "cancel": "रद्द करें",
        "edit_farmer": "किसान संपादित करें",
        "edit_farmer_description": "स्थायी किसान जानकारी अपडेट करें।",
        "update_farmer": "किसान अपडेट करें",
        "nondni_title": "गन्ना पंजीकरण",
        "nondni_description": "मौजूदा किसान खोजें और सीजन के अनुसार गन्ना पंजीकरण जानकारी भरें।",
        "search_farmer_title": "किसान खोजें",
        "search_farmer_nondni": "किसान कोड या मोबाइल नंबर दर्ज करें",
        "farmer_details": "किसान जानकारी",
        "nondni_details": "पंजीकरण जानकारी",
        "survey_gat_no": "सर्वे / गट नंबर",
        "planting_date": "रोपण दिनांक",
        "sugarcane_variety": "गन्ने की किस्म",
        "crop_type": "फसल प्रकार",
        "irrigation_method": "सिंचाई पद्धति",
        "planting_area": "रोपण क्षेत्र",
        "receipt_no": "रसीद नंबर",
        "save_nondni": "पंजीकरण सेव करें",
        "view_nondni_records": "पंजीकरण रिकॉर्ड देखें",
        "farmer_not_found": "किसान नहीं मिला।",
        "search_first": "कृपया पहले किसान खोजें।",
        "nondni_saved": "पंजीकरण सफलतापूर्वक सेव हुआ।",
        "save_error": "पंजीकरण सेव नहीं हो सका।",
        "nondni_records_description": "सीजन के अनुसार पंजीकरण रिकॉर्ड देखें और खोजें।",
        "search_nondni": "किसान कोड, नाम या गांव से खोजें",
        "no_nondni_records": "कोई पंजीकरण रिकॉर्ड नहीं मिला।",
        "edit_nondni": "पंजीकरण संपादित करें",
        "edit_nondni_description": "सीजन के अनुसार पंजीकरण जानकारी अपडेट करें।",
        "update_nondni": "पंजीकरण अपडेट करें",
        "back_to_records": "रिकॉर्ड पर वापस जाएं",
        "reports_title": "रिपोर्ट",
        "custom_date_report": "कस्टम दिनांक रिपोर्ट",
        "reports_description": "चयनित सीजन और दिनांक सीमा के लिए रिपोर्ट बनाएं।",
        "from_date": "प्रारंभ दिनांक",
        "to_date": "अंतिम दिनांक",
        "generate_report": "रिपोर्ट बनाएं",
        "report_summary": "रिपोर्ट सारांश",
        "date_range": "दिनांक सीमा",
        "download_pdf": "PDF डाउनलोड करें",
        "no_report_data": "रिपोर्ट के लिए कोई रिकॉर्ड नहीं मिला।",
        "select_dates_message": "कृपया दोनों दिनांक चुनें।",
        "report_period": "रिपोर्ट अवधि",
        "season_management": "सीजन प्रबंधन",
        "seasons_description": "उपलब्ध गन्ना सीजन प्रबंधित करें।",
        "add_season": "सीज़न जोड़ें",
        "season_name": "सीज़न का नाम",
        "mark_as_active": "सक्रिय सीज़न के रूप में सेट करें",
        "save_season": "सीज़न सेव करें",
        "season_example": "जैसे 2026-27",
        "status": "स्थिति",
        "created_at": "बनाया गया",
        "active": "सक्रिय",
        "inactive": "निष्क्रिय",
        "no_seasons": "कोई सीजन नहीं मिला।",
        "audit_logs_title": "ऑडिट लॉग",
        "audit_logs_description": "सिस्टम में किए गए महत्वपूर्ण बदलाव देखें।",
        "username": "उपयोगकर्ता नाम",
        "table": "टेबल",
        "record_id": "रिकॉर्ड नंबर",
        "old_data": "पुरानी जानकारी",
        "new_data": "नई जानकारी",
        "date_time": "दिनांक व समय",
        "no_audit_logs": "कोई ऑडिट लॉग नहीं मिला।",
        "change_password_description": "वर्तमान एडमिन पासवर्ड सुरक्षित तरीके से बदलें।",
        "current_password": "वर्तमान पासवर्ड",
        "new_password": "नया पासवर्ड",
        "confirm_password": "पासवर्ड की पुष्टि करें",
        "minimum_8_characters": "कम से कम 8 अक्षर",
        "change_password_button": "पासवर्ड बदलें",
        "all_fields_required": "सभी जानकारी आवश्यक है।",
        "passwords_do_not_match": "नए पासवर्ड मेल नहीं खाते।",
        "password_minimum_length": "पासवर्ड कम से कम 8 अक्षरों का होना चाहिए।",
        "current_password_incorrect": "वर्तमान पासवर्ड गलत है।",
        "password_changed_successfully": "पासवर्ड सफलतापूर्वक बदल दिया गया।",
        "total_nondni_label": "कुल पंजीकरण",
        "total_planting_area": "कुल रोपण क्षेत्र",
    },
}


@app.context_processor
def inject_translations():
    language = session.get("language", "en")
    return {
        "t": lambda key: TRANSLATIONS.get(
            language,
            TRANSLATIONS["en"]
        ).get(key, key)
    }


@app.route("/set-language")
def set_language():
    language = request.args.get("lang", "en")
    if language not in ("en", "mr", "hi"):
        language = "en"

    session["language"] = language

    next_page = request.args.get("next", "")
    if next_page.startswith("/"):
        return redirect(next_page)

    return redirect(url_for("dashboard"))


# ============================================================
# HELPERS
# ============================================================

def require_login():
    if "admin_id" not in session:
        return redirect(url_for("login"))
    return None


def get_active_seasons():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, season_name, is_active, created_at
        FROM seasons
        WHERE is_active = TRUE
        ORDER BY season_name DESC
    """)
    seasons = cursor.fetchall()
    cursor.close()
    connection.close()
    return seasons


def get_all_seasons():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, season_name, is_active, created_at
        FROM seasons
        ORDER BY season_name DESC
    """)
    seasons = cursor.fetchall()
    cursor.close()
    connection.close()
    return seasons


def create_audit_log(table_name, record_id, action, old_data=None, new_data=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO audit_logs
            (
                user_id,
                username,
                table_name,
                record_id,
                action,
                old_data,
                new_data
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            session.get("admin_id"),
            session.get("username"),
            table_name,
            record_id,
            action,
            json.dumps(old_data, default=str, ensure_ascii=False) if old_data is not None else None,
            json.dumps(new_data, default=str, ensure_ascii=False) if new_data is not None else None,
        ))

        connection.commit()
        cursor.close()
        connection.close()
    except Exception as error:
        print("AUDIT LOG ERROR:", error)


def get_registration_or_404(registration_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            sr.*,
            f.farmer_code,
            f.farmer_name,
            f.village
        FROM sugarcane_registrations sr
        JOIN farmers f ON sr.farmer_id = f.id
        WHERE sr.id = %s
    """, (registration_id,))

    registration = cursor.fetchone()

    cursor.close()
    connection.close()

    return registration


# ============================================================
# HOME / LOGIN
# ============================================================

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM admin
            WHERE username = %s
              AND is_active = TRUE
            LIMIT 1
        """, (username,))

        admin = cursor.fetchone()

        cursor.close()
        connection.close()

        if admin and check_password_hash(admin["password"], password):
            session["admin_id"] = admin["id"]
            session["username"] = admin["username"]
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():
    if "admin_id" not in session:
        return redirect(url_for("login"))

    selected_season = request.args.get("season", "all").strip()

    seasons = get_active_seasons()

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM farmers")
    farmer_count = cursor.fetchone()[0]

    if selected_season and selected_season != "all":
        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(planting_area), 0)
            FROM sugarcane_registrations
            WHERE season = %s
        """, (selected_season,))
    else:
        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(planting_area), 0)
            FROM sugarcane_registrations
        """)

    result = cursor.fetchone()
    nondni_count = result[0]
    total_area = float(result[1] or 0)

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        farmer_count=farmer_count,
        nondni_count=nondni_count,
        total_area=total_area,
        seasons=seasons,
        selected_season=selected_season
    )


# ============================================================
# FARMERS
# ============================================================

@app.route("/farmers")
def farmers():
    if "admin_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if search:
        search_value = "%" + search + "%"
        cursor.execute("""
            SELECT *
            FROM farmers
            WHERE farmer_code LIKE %s
               OR farmer_name LIKE %s
               OR mobile LIKE %s
               OR village LIKE %s
            ORDER BY id DESC
        """, (
            search_value,
            search_value,
            search_value,
            search_value
        ))
    else:
        cursor.execute("""
            SELECT *
            FROM farmers
            ORDER BY id DESC
        """)

    farmers_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "farmers.html",
        farmers=farmers_data,
        search=search
    )


@app.route("/add-farmer", methods=["GET", "POST"])
def add_farmer():
    if "admin_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        farmer_name = request.form.get("farmer_name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        village = request.form.get("village", "").strip()
        taluka = request.form.get("taluka", "").strip()
        district = request.form.get("district", "").strip()
        land_area = request.form.get("land_area", "").strip() or None
        aadhaar_no = request.form.get("aadhaar_no", "").strip()
        land_account_no = request.form.get("land_account_no", "").strip()
        latitude = request.form.get("latitude", "").strip() or None
        longitude = request.form.get("longitude", "").strip() or None

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT farmer_code
                FROM farmers
                WHERE farmer_code IS NOT NULL
                ORDER BY id DESC
                LIMIT 1
            """)

            last_farmer = cursor.fetchone()

            if last_farmer:
                last_code = last_farmer[0]
                last_number = int(last_code.replace("SCF", ""))
                next_number = last_number + 1
            else:
                next_number = 1

            farmer_code = f"SCF{next_number:06d}"

            cursor.execute("""
                INSERT INTO farmers
                (
                    farmer_code,
                    farmer_name,
                    mobile,
                    village,
                    taluka,
                    district,
                    land_area,
                    aadhaar_no,
                    land_account_no,
                    latitude,
                    longitude
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                farmer_code,
                farmer_name,
                mobile,
                village,
                taluka,
                district,
                land_area,
                aadhaar_no,
                land_account_no,
                latitude,
                longitude
            ))

            farmer_id = cursor.lastrowid
            connection.commit()

            create_audit_log(
                "farmers",
                farmer_id,
                "INSERT",
                None,
                {
                    "farmer_code": farmer_code,
                    "farmer_name": farmer_name,
                    "mobile": mobile,
                    "village": village,
                    "taluka": taluka,
                    "district": district,
                    "land_area": land_area,
                    "aadhaar_no": aadhaar_no,
                    "land_account_no": land_account_no,
                    "latitude": latitude,
                    "longitude": longitude
                }
            )

            return redirect(url_for("farmers"))

        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    return render_template("add_farmer.html")


@app.route("/edit-farmer/<int:farmer_id>", methods=["GET", "POST"])
def edit_farmer(farmer_id):
    if "admin_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM farmers
        WHERE id = %s
    """, (farmer_id,))
    farmer = cursor.fetchone()

    if not farmer:
        cursor.close()
        connection.close()
        return "Farmer not found", 404

    if request.method == "POST":
        old_data = dict(farmer)

        farmer_name = request.form.get("farmer_name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        village = request.form.get("village", "").strip()
        taluka = request.form.get("taluka", "").strip()
        district = request.form.get("district", "").strip()
        land_area = request.form.get("land_area", "").strip() or None
        aadhaar_no = request.form.get("aadhaar_no", "").strip()
        land_account_no = request.form.get("land_account_no", "").strip()
        latitude = request.form.get("latitude", "").strip() or None
        longitude = request.form.get("longitude", "").strip() or None

        cursor.execute("""
            UPDATE farmers
            SET farmer_name = %s,
                mobile = %s,
                village = %s,
                taluka = %s,
                district = %s,
                land_area = %s,
                aadhaar_no = %s,
                land_account_no = %s,
                latitude = %s,
                longitude = %s
            WHERE id = %s
        """, (
            farmer_name,
            mobile,
            village,
            taluka,
            district,
            land_area,
            aadhaar_no,
            land_account_no,
            latitude,
            longitude,
            farmer_id
        ))

        connection.commit()

        new_data = {
            "farmer_name": farmer_name,
            "mobile": mobile,
            "village": village,
            "taluka": taluka,
            "district": district,
            "land_area": land_area,
            "aadhaar_no": aadhaar_no,
            "land_account_no": land_account_no,
            "latitude": latitude,
            "longitude": longitude
        }

        cursor.close()
        connection.close()

        create_audit_log(
            "farmers",
            farmer_id,
            "UPDATE",
            old_data,
            new_data
        )

        return redirect(url_for("farmers"))

    cursor.close()
    connection.close()

    return render_template(
        "edit_farmer.html",
        farmer=farmer
    )


# ============================================================
# NONDNI
# ============================================================

@app.route("/nondni")
def nondni():
    if "admin_id" not in session:
        return redirect(url_for("login"))

    seasons = get_active_seasons()

    return render_template(
        "nondni.html",
        seasons=seasons
    )


@app.route("/search-farmer")
def search_farmer():
    if "admin_id" not in session:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    search = request.args.get("search", "").strip()

    if not search:
        return jsonify({
            "success": False,
            "message": "Please enter Farmer Code or Mobile Number"
        })

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            farmer_code,
            farmer_name,
            aadhaar_no,
            mobile,
            village,
            taluka,
            district,
            land_account_no,
            latitude,
            longitude
        FROM farmers
        WHERE farmer_code = %s
           OR mobile = %s
        LIMIT 1
    """, (search, search))

    farmer = cursor.fetchone()

    cursor.close()
    connection.close()

    if not farmer:
        return jsonify({
            "success": False,
            "message": "Farmer not found"
        })

    return jsonify({
        "success": True,
        "farmer": farmer
    })


@app.route("/save-nondni", methods=["POST"])
def save_nondni():
    if "admin_id" not in session:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    connection = None
    cursor = None

    try:
        data = request.get_json(silent=True) or {}

        farmer_id = data.get("farmer_id")
        season = (data.get("season") or "").strip()
        survey_gat_no = (data.get("survey_gat_no") or "").strip() or None
        planting_date = (data.get("planting_date") or "").strip() or None
        sugarcane_variety = (data.get("sugarcane_variety") or "").strip() or None
        crop_type = (data.get("crop_type") or "").strip() or None
        irrigation_method = (data.get("irrigation_method") or "").strip() or None
        planting_area = data.get("planting_area") or None
        receipt_no = (data.get("receipt_no") or "").strip() or None

        if not farmer_id:
            return jsonify({
                "success": False,
                "message": "Please search for a farmer first"
            })

        if not season:
            return jsonify({
                "success": False,
                "message": "Please select a season"
            })

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id
            FROM farmers
            WHERE id = %s
        """, (farmer_id,))
        farmer = cursor.fetchone()

        if not farmer:
            return jsonify({
                "success": False,
                "message": "Farmer does not exist"
            })

        cursor.execute("""
            SELECT id
            FROM seasons
            WHERE season_name = %s
              AND is_active = TRUE
            LIMIT 1
        """, (season,))
        season_row = cursor.fetchone()

        if not season_row:
            return jsonify({
                "success": False,
                "message": "Selected season is not active"
            })

        cursor.execute("""
            INSERT INTO sugarcane_registrations
            (
                farmer_id,
                season,
                survey_gat_no,
                planting_date,
                sugarcane_variety,
                crop_type,
                irrigation_method,
                planting_area,
                receipt_no
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            farmer_id,
            season,
            survey_gat_no,
            planting_date,
            sugarcane_variety,
            crop_type,
            irrigation_method,
            planting_area,
            receipt_no
        ))

        registration_id = cursor.lastrowid
        connection.commit()

        cursor.execute("""
            SELECT *
            FROM sugarcane_registrations
            WHERE id = %s
        """, (registration_id,))
        new_data = cursor.fetchone()

        create_audit_log(
            "sugarcane_registrations",
            registration_id,
            "INSERT",
            None,
            new_data
        )

        return jsonify({
            "success": True,
            "message": "Nondni saved successfully"
        })

    except Exception as error:
        if connection:
            connection.rollback()

        print("NONDNI SAVE ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Unable to save Nondni."
        }), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route("/nondnis")
def nondnis():
    if "admin_id" not in session:
        return redirect(url_for("login"))

    season = request.args.get("season", "").strip()
    search = request.args.get("search", "").strip()

    seasons = get_active_seasons()

    if not season:
        season = seasons[0]["season_name"] if seasons else "2026-27"

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if search:
        search_value = "%" + search + "%"

        cursor.execute("""
            SELECT
                sr.id,
                sr.season,
                sr.survey_gat_no,
                sr.planting_date,
                sr.sugarcane_variety,
                sr.crop_type,
                sr.irrigation_method,
                sr.planting_area,
                sr.receipt_no,
                f.farmer_code,
                f.farmer_name,
                f.village
            FROM sugarcane_registrations sr
            JOIN farmers f ON sr.farmer_id = f.id
            WHERE sr.season = %s
              AND (
                    f.farmer_code LIKE %s
                    OR f.farmer_name LIKE %s
                    OR f.village LIKE %s
                  )
            ORDER BY sr.id DESC
        """, (
            season,
            search_value,
            search_value,
            search_value
        ))
    else:
        cursor.execute("""
            SELECT
                sr.id,
                sr.season,
                sr.survey_gat_no,
                sr.planting_date,
                sr.sugarcane_variety,
                sr.crop_type,
                sr.irrigation_method,
                sr.planting_area,
                sr.receipt_no,
                f.farmer_code,
                f.farmer_name,
                f.village
            FROM sugarcane_registrations sr
            JOIN farmers f ON sr.farmer_id = f.id
            WHERE sr.season = %s
            ORDER BY sr.id DESC
        """, (season,))

    nondnis_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "nondnis.html",
        nondnis=nondnis_data,
        season=season,
        search=search,
        seasons=seasons
    )


@app.route("/edit-nondni/<int:nondni_id>", methods=["GET", "POST"])
def edit_nondni(nondni_id):
    if "admin_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            sr.*,
            f.farmer_code,
            f.farmer_name,
            f.village
        FROM sugarcane_registrations sr
        JOIN farmers f ON sr.farmer_id = f.id
        WHERE sr.id = %s
    """, (nondni_id,))

    nondni_record = cursor.fetchone()

    if not nondni_record:
        cursor.close()
        connection.close()
        return "Nondni record not found", 404

    if request.method == "POST":
        old_data = dict(nondni_record)

        survey_gat_no = request.form.get("survey_gat_no", "").strip() or None
        planting_date = request.form.get("planting_date", "").strip() or None
        sugarcane_variety = request.form.get("sugarcane_variety", "").strip() or None
        crop_type = request.form.get("crop_type", "").strip() or None
        irrigation_method = request.form.get("irrigation_method", "").strip() or None
        planting_area = request.form.get("planting_area", "").strip() or None
        receipt_no = request.form.get("receipt_no", "").strip() or None

        cursor.execute("""
            UPDATE sugarcane_registrations
            SET survey_gat_no = %s,
                planting_date = %s,
                sugarcane_variety = %s,
                crop_type = %s,
                irrigation_method = %s,
                planting_area = %s,
                receipt_no = %s
            WHERE id = %s
        """, (
            survey_gat_no,
            planting_date,
            sugarcane_variety,
            crop_type,
            irrigation_method,
            planting_area,
            receipt_no,
            nondni_id
        ))

        connection.commit()

        cursor.execute("""
            SELECT *
            FROM sugarcane_registrations
            WHERE id = %s
        """, (nondni_id,))
        new_data = cursor.fetchone()

        cursor.close()
        connection.close()

        create_audit_log(
            "sugarcane_registrations",
            nondni_id,
            "UPDATE",
            old_data,
            new_data
        )

        return redirect(url_for(
            "nondnis",
            season=nondni_record["season"]
        ))

    seasons = get_active_seasons()

    cursor.close()
    connection.close()

    return render_template(
        "edit_nondni.html",
        nondni=nondni_record,
        seasons=seasons
    )


# ============================================================
# AUDIT LOGS
# ============================================================

@app.route("/audit-logs")
def audit_logs():
    if "admin_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            username,
            table_name,
            record_id,
            action,
            old_data,
            new_data,
            created_at
        FROM audit_logs
        ORDER BY id DESC
        LIMIT 500
    """)

    logs = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "audit_logs.html",
        logs=logs
    )


# ============================================================
# CHANGE PASSWORD
# ============================================================

@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if "admin_id" not in session:
        return redirect(url_for("login"))

    message = None
    error = None

    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not current_password or not new_password or not confirm_password:
            error = "All fields are required."

        elif new_password != confirm_password:
            error = "New passwords do not match."

        elif len(new_password) < 8:
            error = "Password must be at least 8 characters."

        else:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT password
                FROM admin
                WHERE id = %s
                LIMIT 1
            """, (session["admin_id"],))

            admin = cursor.fetchone()

            if not admin or not check_password_hash(
                admin["password"],
                current_password
            ):
                error = "Current password is incorrect."
            else:
                new_hash = generate_password_hash(new_password)

                cursor.execute("""
                    UPDATE admin
                    SET password = %s
                    WHERE id = %s
                """, (new_hash, session["admin_id"]))

                connection.commit()
                message = "Password changed successfully."

            cursor.close()
            connection.close()

    return render_template(
        "change_password.html",
        message=message,
        error=error
    )


# ============================================================
# SEASONS
# ============================================================

@app.route("/seasons", methods=["GET", "POST"])
def seasons():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        season_name = request.form.get("season_name", "").strip()
        is_active = request.form.get("is_active") == "1"

        if not season_name:
            flash("Season name is required.", "error")
            return redirect(url_for("seasons"))

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Prevent duplicate season names.
            cursor.execute("""
                SELECT id
                FROM seasons
                WHERE season_name = %s
                LIMIT 1
            """, (season_name,))

            existing = cursor.fetchone()

            if existing:
                flash("This season already exists.", "error")
                return redirect(url_for("seasons"))

            cursor.execute("""
                INSERT INTO seasons
                (
                    season_name,
                    is_active
                )
                VALUES (%s, %s)
            """, (
                season_name,
                is_active
            ))

            connection.commit()
            flash("Season added successfully.", "success")

        except Exception as error:
            if connection:
                connection.rollback()

            print("SEASON ERROR:", error)
            flash(f"Unable to add season: {error}", "error")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return redirect(url_for("seasons"))

    seasons_data = get_all_seasons()

    return render_template(
        "seasons.html",
        seasons=seasons_data
    )


# ============================================================
# REPORTS
# Custom Date Only
# ============================================================

def register_pdf_fonts():
    """
    Register Devanagari fonts for Marathi/Hindi PDF generation.
    """

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    font_dir = os.path.join(
        base_dir,
        "fonts"
    )

    regular_font = os.path.join(
        font_dir,
        "NotoSansDevanagari-Regular.ttf"
    )

    bold_font = os.path.join(
        font_dir,
        "NotoSansDevanagari-Bold.ttf"
    )

    if not os.path.exists(regular_font):
        raise FileNotFoundError(
            f"Missing font: {regular_font}"
        )

    if not os.path.exists(bold_font):
        raise FileNotFoundError(
            f"Missing font: {bold_font}"
        )

    if "NotoDevanagari" not in pdfmetrics.getRegisteredFontNames():

        pdfmetrics.registerFont(
            TTFont(
                "NotoDevanagari",
                regular_font
            )
        )

        pdfmetrics.registerFont(
            TTFont(
                "NotoDevanagari-Bold",
                bold_font
            )
        )

        pdfmetrics.registerFontFamily(
            "NotoDevanagari",
            normal="NotoDevanagari",
            bold="NotoDevanagari-Bold"
        )

@app.route("/reports", methods=["GET", "POST"])
def reports():
    if "admin_id" not in session:
        return redirect(url_for("login"))

    seasons = get_active_seasons()

    season = request.values.get("season", "").strip()
    from_date = request.values.get("from_date", "").strip()
    to_date = request.values.get("to_date", "").strip()

    if not season and seasons:
        season = seasons[0]["season_name"]

    report_data = []
    total_nondni = 0
    total_area = 0.0
    start_date = None
    end_date = None

    if from_date and to_date:
        try:
            start_date = date.fromisoformat(from_date)
            end_date = date.fromisoformat(to_date)
        except ValueError:
            start_date = None
            end_date = None

        if start_date and end_date and start_date <= end_date:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    sr.id,
                    sr.season,
                    sr.survey_gat_no,
                    sr.planting_date,
                    sr.sugarcane_variety,
                    sr.crop_type,
                    sr.irrigation_method,
                    sr.planting_area,
                    sr.receipt_no,
                    f.farmer_code,
                    f.farmer_name,
                    f.village
                FROM sugarcane_registrations sr
                JOIN farmers f ON sr.farmer_id = f.id
                WHERE sr.season = %s
                  AND sr.planting_date BETWEEN %s AND %s
                ORDER BY sr.planting_date ASC, sr.id ASC
            """, (
                season,
                start_date,
                end_date
            ))

            report_data = cursor.fetchall()

            cursor.close()
            connection.close()

            total_nondni = len(report_data)
            total_area = sum(
                float(row["planting_area"] or 0)
                for row in report_data
            )

    return render_template(
        "reports.html",
        seasons=seasons,
        report_data=report_data,
        season=season,
        from_date=from_date,
        to_date=to_date,
        start_date=start_date,
        end_date=end_date,
        total_nondni=total_nondni,
        total_area=total_area
    )


@app.route("/reports/pdf")
def reports_pdf():

    if "admin_id" not in session:
        return redirect(url_for("login"))

    # ======================================================
    # REGISTER DEVANAGARI FONTS
    # ======================================================

    try:
        register_pdf_fonts()
    except FileNotFoundError as error:
        return str(error), 500

    # ======================================================
    # GET FILTER VALUES
    # ======================================================

    season = request.args.get(
        "season",
        ""
    ).strip()

    from_date = request.args.get(
        "from_date",
        ""
    ).strip()

    to_date = request.args.get(
        "to_date",
        ""
    ).strip()

    # ======================================================
    # VALIDATE DATES
    # ======================================================

    try:

        start_date = date.fromisoformat(
            from_date
        )

        end_date = date.fromisoformat(
            to_date
        )

    except ValueError:

        return "Invalid date selection", 400

    if not season:
        return "Season is required", 400

    if start_date > end_date:
        return (
            "From date cannot be greater than To date",
            400
        )

    # ======================================================
    # GET LANGUAGE
    # ======================================================

    language = session.get(
        "language",
        "en"
    )

    translations = TRANSLATIONS.get(
        language,
        TRANSLATIONS["en"]
    )

    # ======================================================
    # GET REPORT DATA
    # ======================================================

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT
            sr.id,
            sr.season,
            sr.survey_gat_no,
            sr.planting_date,
            sr.sugarcane_variety,
            sr.crop_type,
            sr.irrigation_method,
            sr.planting_area,
            sr.receipt_no,

            f.farmer_code,
            f.farmer_name,
            f.village

        FROM sugarcane_registrations sr

        JOIN farmers f
            ON sr.farmer_id = f.id

        WHERE sr.season = %s

          AND sr.planting_date
              BETWEEN %s AND %s

        ORDER BY
            sr.planting_date ASC,
            sr.id ASC
        """,
        (
            season,
            start_date,
            end_date
        )
    )

    report_data = cursor.fetchall()

    cursor.close()
    connection.close()

    # ======================================================
    # TOTALS
    # ======================================================

    total_nondni = len(
        report_data
    )

    total_area = sum(
        float(
            row["planting_area"] or 0
        )
        for row in report_data
    )

    # ======================================================
    # PDF BUFFER
    # ======================================================

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,

        pagesize=landscape(A4),

        rightMargin=8 * mm,
        leftMargin=8 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm
    )

    # ======================================================
    # PDF STYLES
    # ======================================================

    title_style = ParagraphStyle(
        "PdfTitle",

        fontName="NotoDevanagari-Bold",

        fontSize=18,
        leading=22,

        alignment=1,

        textColor=colors.black,

        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "PdfNormal",

        fontName="NotoDevanagari",

        fontSize=9,
        leading=12,

        textColor=colors.black
    )

    bold_style = ParagraphStyle(
        "PdfBold",

        fontName="NotoDevanagari-Bold",

        fontSize=9,
        leading=12,

        textColor=colors.black
    )

    elements = []

    # ======================================================
    # PDF TITLE
    # ======================================================

    pdf_titles = {

        "en":
            "Sugarcane Nondni Report",

        "mr":
            "ऊस नोंदणी अहवाल",

        "hi":
            "गन्ना पंजीकरण रिपोर्ट"
    }

    pdf_title = pdf_titles.get(
        language,
        pdf_titles["en"]
    )

    elements.append(
        Paragraph(
            pdf_title,
            title_style
        )
    )

    # ======================================================
    # REPORT INFORMATION
    # ======================================================

    season_label = translations.get(
        "season",
        "Season"
    )

    report_period_label = translations.get(
        "report_period",
        "Report Period"
    )

    elements.append(
        Paragraph(
            f"<b>{season_label}:</b> {season}",
            normal_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>{report_period_label}:</b> "
            f"{start_date.strftime('%d-%m-%Y')} "
            f"to "
            f"{end_date.strftime('%d-%m-%Y')}",
            normal_style
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    # ======================================================
    # SUMMARY
    # ======================================================

    summary_data = [

        [
            translations.get(
                "total_nondni_label",
                "Total Nondni"
            ),

            str(total_nondni)
        ],

        [
            translations.get(
                "total_planting_area",
                "Total Planting Area"
            ),

            f"{total_area:.2f}"
        ]
    ]

    summary_table = Table(
        summary_data,

        colWidths=[
            50 * mm,
            35 * mm
        ]
    )

    summary_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "NotoDevanagari"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            )
        ])
    )

    elements.append(
        summary_table
    )

    elements.append(
        Spacer(1, 10)
    )

    # ======================================================
    # TABLE HEADERS
    # ======================================================

    table_data = [[

        "ID",

        translations.get(
            "farmer_code",
            "Farmer Code"
        ),

        translations.get(
            "farmer_name",
            "Farmer Name"
        ),

        translations.get(
            "village",
            "Village"
        ),

        translations.get(
            "survey_gat_no",
            "Gat No."
        ),

        translations.get(
            "planting_date",
            "Planting Date"
        ),

        translations.get(
            "sugarcane_variety",
            "Variety"
        ),

        translations.get(
            "crop_type",
            "Crop Type"
        ),

        translations.get(
            "irrigation_method",
            "Irrigation"
        ),

        translations.get(
            "planting_area",
            "Area"
        ),

        translations.get(
            "receipt_no",
            "Receipt"
        )

    ]]

    # ======================================================
    # TABLE DATA
    # ======================================================

    for row in report_data:

        planting_date = (

            row["planting_date"].strftime(
                "%d-%m-%Y"
            )

            if row["planting_date"]

            else ""
        )

        table_data.append([

            str(
                row["id"]
            ),

            str(
                row["farmer_code"] or ""
            ),

            str(
                row["farmer_name"] or ""
            ),

            str(
                row["village"] or ""
            ),

            str(
                row["survey_gat_no"] or ""
            ),

            planting_date,

            str(
                row["sugarcane_variety"] or ""
            ),

            str(
                row["crop_type"] or ""
            ),

            str(
                row["irrigation_method"] or ""
            ),

           f"{float(row['planting_area'] or 0):.2f}",

            str(
                row["receipt_no"] or ""
            )
        ])

    # ======================================================
    # REPORT TABLE
    # ======================================================

    report_table = Table(
        table_data,

        repeatRows=1,

        colWidths=[
            10 * mm,
            25 * mm,
            37 * mm,
            35 * mm,
            22 * mm,
            27 * mm,
            24 * mm,
            27 * mm,
            27 * mm,
            18 * mm,
            20 * mm
        ]
    )

    report_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.green
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.grey
            ),

            # IMPORTANT:
            # Use Devanagari font for ALL cells.

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "NotoDevanagari"
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "NotoDevanagari-Bold"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                6.5
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "ALIGN",
                (0, 0),
                (0, -1),
                "CENTER"
            ),

            (
                "ALIGN",
                (9, 1),
                (9, -1),
                "RIGHT"
            ),

            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),

                [
                    colors.white,
                    colors.whitesmoke
                ]
            )
        ])
    )

    elements.append(
        report_table
    )

    # ======================================================
    # BUILD PDF
    # ======================================================

    document.build(
        elements
    )

    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,

        as_attachment=True,

        download_name=(
            f"Nondni_Report_{season}.pdf"
        ),

        mimetype="application/pdf"
    )

# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))




@app.route('/delete_farmer/<int:farmer_id>', methods=['POST'])
def delete_farmer(farmer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM farmers WHERE id = %s",
            (farmer_id,)
        )

        if cursor.rowcount == 0:
            conn.rollback()
            flash("Farmer not found.", "error")
        else:
            conn.commit()
            flash("Farmer deleted successfully.", "success")

    except Exception:
        conn.rollback()
        flash(
            "Cannot delete this farmer because related records may exist.",
            "error"
        )

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('farmers'))
# ============================================================
# START APP
# IMPORTANT: keep this at the very bottom of app.py
# ============================================================

if __name__ == "__main__":
    app.run()