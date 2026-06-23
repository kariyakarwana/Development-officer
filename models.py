import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv


load_dotenv()
# Pull connection parameter straight from the host runtime environment variables
NEON_DATABASE_URL = os.environ.get(
    'DATABASE_URL'
)

def get_db_connection():
    # Psycopg2 parses standard dictionary queries naturally bypassing old Lisp runtime bottlenecks
    conn = psycopg2.connect(NEON_DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DevProjects (
        ProjectID SERIAL PRIMARY KEY,
        ProjectYear VARCHAR(50),
        ProgramName TEXT,
        MinistryName TEXT,
        MP_Name TEXT,
        GN_Division TEXT,
        ProjectType TEXT,
        ProjectNumber TEXT,
        ProjectProgress TEXT,
        ProjectName TEXT,
        ApprovedAmount NUMERIC(15, 2),
        EstimatedAmount NUMERIC(15, 2),
        ContractorName TEXT,
        AgreedAmount NUMERIC(15, 2),
        CostAmount NUMERIC(15, 2),
        CompletionDate VARCHAR(50),
        RetentionPayment NUMERIC(15, 2),
        MaintenanceDuration TEXT,
        ApprovedDate VARCHAR(50),
        EstimatedDate VARCHAR(50),
        AllocationReceivedDate VARCHAR(50),
        AgreementDate VARCHAR(50),
        StartDate VARCHAR(50),
        EndDate VARCHAR(50),
        RetentionPaidDate VARCHAR(50),
        MaintenanceHandoverDate VARCHAR(50),
        MaintenanceAgency TEXT,
        TenderReferDate VARCHAR(50),
        ProcurementDate VARCHAR(50),
        OrderDate VARCHAR(50),
        GoodsReceivedDate VARCHAR(50),
        HandoverDate VARCHAR(50),
        ImplementingAgency TEXT,
        AllocationAmount NUMERIC(15, 2),
        CivilWorkAmount NUMERIC(15, 2),
        TaxAmount NUMERIC(15, 2),
        ContingencyAmount NUMERIC(15, 2),
        BillPaidDate VARCHAR(50)
    );
    """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Users (
                       UserID SERIAL PRIMARY KEY,
                       Username VARCHAR(50) UNIQUE NOT NULL,
                       Password VARCHAR(255) NOT NULL,
                       Role VARCHAR(20) NOT NULL    
                    );""")
    
    cursor.execute("SELECT COUNT(*) FROM Users;")
    if cursor.fetchone()[0] == 0:
        admin_user = os.environ.get('DEFAULT_ADMIN_USER', 'admin')
        admin_pass = os.environ.get('DEFAULT_ADMIN_PASS', 'admin123')
        officer_user = os.environ.get('DEFAULT_OFFICER_USER', 'officer')
        officer_pass = os.environ.get('DEFAULT_OFFICER_PASS', 'user123')
        cursor.execute("INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s);", (admin_user, admin_pass, 'admin'))
        cursor.execute("INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s);", (officer_user, officer_pass, 'user'))
    conn.commit()
    cursor.close()
    conn.close()

# Structural static parameters to feed Jinja selectors
OPTIONS = {
    "years": ["2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"],
    "programs": [
        "විමධ්‍යගත අයවැය වැඩසටහන", "ග්‍රාමීය මාර්ග සංවර්ධන වැඩසටහන", "පළාත් නිශ්චිත වැඩසටහන", 
        "උපමාන පාදක වැඩසටහන", "රේඛීය අමාත්‍යාංශය", "ප්‍රජාශක්ති වැඩසටහන", "නිලසෙවණ අළුත්වැඩියා", 
        "ප්‍රා.ලේ. කාර්යාල අළුත්වැඩියාව", "දිස්ත්‍රික් සංවර්ධන වැඩසටහන", "ද.ප. ග්‍රාම සංවර්ධන වැඩසටහන",
        "ද.ප. ක්‍රීඩා සංවර්ධන වැඩසටහන", "ද.ප. නිවාස දෙපාර්තමේන්තු වැඩසටහන", "ජාතික නිවාස සංවර්ධන වැඩසටහන", "වෙනත්"
    ],
    "ministries": [
        "  ", "මුදල් හා ක්‍රමසම්පාදන අමාත්‍යාංශය", "ප්‍රවාහන හා මහාමාර්ග අමාත්‍යාංශය", 
        "ග්‍රාමීය සංවර්ධන සමාජ ආරක්ෂණ හා ප්‍රජා සවිබල ගැන්වීමේ අමාත්‍යාංශය", "බුද්ධ ශාසන හා සංස්කෘතික කටයුතු අමාත්‍යාංශය", 
        "රාජ්‍ය පරිපාලන හා ස්වදේශ කටයුතු අමාත්‍යාංශය", "පළාත් ආණ්ඩුකාර කාර්යාලය", 
        "දකුණු පළාත් ක්‍රීඩා සමාජ හා ග්‍රාම සංවර්ධන අමාත්‍යාංශය", "දකුණු පළාත් ධීවර අමාත්‍යාංශය", 
        "දකුණු පළාත් වෙනත් අමාත්‍යාංශ", "ද.ප. නිවාස දෙපාර්තමේන්තුව", "ජාතික නිවාස සංවර්ධන අධිකාරිය", "වෙනත් රේඛීය අමාත්‍යාංශ"
    ],
    "mps": [
        "  ", "නිශාන්ත පෙරේරා මැතිතුමා", "ගයන්ත කරුණාතිලක මැතිතුමා", "හසාරා ලියනගේ මැතිණිය", 
        "නලින් හේවාගේ මැතිතුමා", "චානක මාදුගොඩ මැතිතුමා", "සම්පත් අතුකෝරාළ මැතිතුමා", "ගීතා කුමාරසිංහ මැතිණීය", 
        "මොහාන් invariants මැතිතුමා", "වජිර අබේවර්ධන මැතිතුමා", "රමේෂ් පතිරණ මැතිතුමා", "ඉසුරු දොඩංගොඩ මැතිතුමා", 
        "ශාන් විජයලාල්සිල්වා මැතිතුමා", "දුල්ෂාන් පද්මසිරි කාරියවසම් මැතිතුමා"
    ],
    "gn_divisions": [
        "  ","පහුරුමුල්ල", "අංගාගොඩ", "වරාහේන", "යාත්‍රාමුල්ල", "බෝධිමළුව", "සිංහරූපාගම", "කෝම්මල", 
        "හුංගන්තොට වඩුමුල්ල", "දෝපේ", "කහගල්ල", "දෙද්දුව", "යාලේගම", "ගල්බඩ", "ඔලගන්දූව", "අතුරුවැල්ල", 
        "කයිකාවල", "ඇටවලවත්ත බටහිර", "ඇටවලවත්ත නැගෙනහිර", "හබක්කල", "කහවෙගම්මැද්ද", "ವರකාමුල්ල", 
        "අකාඩේගොඩ", "කන්දෙමුල්ල", "ගෝනගල", "මුල්ලෙගොඩ", "ගල්තුඩුව", "ගලගම", "දොඹගහවත්ත", "කොළණිය", 
        "හබුරුගල", "තොටකනත්ත", "තුන්දූව නැගෙනහිර", "තුන්දූව බටහිර", "සූරියගම", "ඇලකාක", "වියන්දූව", 
        "රන්තොටුවිල", "මොරගොඩ", "මාලවල", "මහගොඩ", "මිරිස්වත්ත", "මහවිල නැගෙනහිර", "මහවිල බටහිර", 
        "පිලේකුඹුරු", "ඇතුන්ගාගොඩ", "මහ ඌරගහ", "කොටුවබැන්දහේන", "හිපන්වත්ත", "කුඩා ඌරගහ", "ඉහලමාලවල", "දෙල්කබලගොඩ"
    ],
    "types": [
        "මාර්ග සංවර්ධනය", "බෝක්කු/පාලම්", "ඇල මාර්ග", "රජයේ ගොඩනැගිලි", "කෘෂිකාර්මික", 
        "ස්වේච්ඡා සංවිධාන සදහා උපකරණ", "පාසැල් සදහා උපකරණ", "ආගමික මධ්‍යස්ථාන සංවර්ධනය", 
        "වෙනත් ඉදිකිරීම්", "නිවාස", "වැසිකිළි", "වෙනත් මිලදී ගැනීම්"
    ],
    "progress_opts": [
        "අනුමත වී ඇත", "ප්‍රතිපාදන ලැබී ඇත", "ඇස්තමේන්තු සකස් කර ඇත", "ගිවිසුම්ගතවී ඇත", "වැඩ ආරම්භකර ඇත", 
        "(1-25)% අතර", "(26-50)% අතර", "(51-75)% අතර", "(76-99)% අතර", "වැඩ අවසන්", "බිල්පත් සකසමින් ඇත", 
        "ගෙවීම් සඳහා ගිණුම් අංශයට දී ඇත", "ගෙවා අවසන්", "රැදවුම් ගෙවීමට වාර්තා කැදවා ඇත", "රැඳවුම් ගෙවීමට ඇත", 
        "රැදවුම්ගෙවා ඇත", "මිල කැදවීමට භාරදී ඇත", "ප්‍රසම්පාදනය කර ඇත", "ඇගයීම් කරමින් පවතී", "ඇනවුම් කර ඇත", 
        "භාණ්ඩ ලැබී ඇත", "භාණ්ඩ බෙදාදී ඇත"
    ],
    "maintenance_opts": ["මාස 3", "මාස 6", "අවු 1", "වෙනත්"],
    "agencies": [
        "ප්‍රාදේශීය ලේකම් කාර්යාලය", "ප්‍රාදේශීය සභාව", "ප්‍රාදේශීය වාරිමාර්ග ඉංජිනේරු කාර්යාලය", 
        "පළාත් වාරිමාර්ග දෙපාර්තමේන්තුව", "ගොවිජන සංවර්ධන මධ්‍යස්ථානය", "ජාතික ජලසම්පාදන මණ්ඩලය", 
        "ලංකා විදුලිබල මණ්ඩලය", "වෙනත්"
    ]
}