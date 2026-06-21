from flask import Flask, render_template, request, redirect, url_for
from models import init_db, get_db_connection, OPTIONS
import psycopg2.extras

app = Flask(__name__)

# Boot up schema validation check on launch
init_db()

def get_form_val(req, key, is_num=False):
    val = req.form.get(key, '').strip()
    if is_num:
        return float(val) if val else 0.0
    return val

@app.route('/')
def index():
    success = request.args.get('success')
    success_msg = "✓ දත්ත සාර්ථකව සුරැකුණි!" if success else None
    return render_template('index.html', view_type='form', options=OPTIONS, success_msg=success_msg)

@app.route('/save_project', methods=['POST'])
def save_project():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO DevProjects (
            ProjectYear, ProgramName, MinistryName, MP_Name, GN_Division, ProjectType, ProjectNumber,
            ProjectName, ImplementingAgency, ProjectProgress, ApprovedAmount, EstimatedAmount,
            AllocationAmount, CivilWorkAmount, TaxAmount, ContingencyAmount,
            ContractorName, AgreedAmount, CostAmount, RetentionPayment, MaintenanceDuration, 
            ApprovedDate, EstimatedDate, AllocationReceivedDate, AgreementDate, StartDate, EndDate, 
            BillPaidDate, RetentionPaidDate, MaintenanceHandoverDate, MaintenanceAgency, TenderReferDate,
            ProcurementDate, OrderDate, GoodsReceivedDate, HandoverDate
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        get_form_val(request, 'ProjectYear'), get_form_val(request, 'ProgramName'), get_form_val(request, 'MinistryName'), get_form_val(request, 'MP_Name'), get_form_val(request, 'GN_Division'), get_form_val(request, 'ProjectType'), get_form_val(request, 'ProjectNumber'),
        get_form_val(request, 'ProjectName'), get_form_val(request, 'ImplementingAgency'), get_form_val(request, 'ProjectProgress'), get_form_val(request, 'ApprovedAmount', True), get_form_val(request, 'EstimatedAmount', True),
        get_form_val(request, 'AllocationAmount', True), get_form_val(request, 'CivilWorkAmount', True), get_form_val(request, 'TaxAmount', True), get_form_val(request, 'ContingencyAmount', True),
        get_form_val(request, 'ContractorName'), get_form_val(request, 'AgreedAmount', True), get_form_val(request, 'CostAmount', True), get_form_val(request, 'RetentionPayment', True), get_form_val(request, 'MaintenanceDuration'),
        get_form_val(request, 'ApprovedDate'), get_form_val(request, 'EstimatedDate'), get_form_val(request, 'AllocationReceivedDate'), get_form_val(request, 'AgreementDate'), get_form_val(request, 'StartDate'), get_form_val(request, 'EndDate'),
        get_form_val(request, 'BillPaidDate'), get_form_val(request, 'RetentionPaidDate'), get_form_val(request, 'MaintenanceHandoverDate'), get_form_val(request, 'MaintenanceAgency'), get_form_val(request, 'TenderReferDate'),
        get_form_val(request, 'ProcurementDate'), get_form_val(request, 'OrderDate'), get_form_val(request, 'GoodsReceivedDate'), get_form_val(request, 'HandoverDate')
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index', success=1))

@app.route('/search_page')
def search_page():
    s_vals = {
        's_year': request.args.get('s_year', ''),
        's_program': request.args.get('s_program', ''),
        's_mp': request.args.get('s_mp', ''),
        's_gn': request.args.get('s_gn', ''),
        's_type': request.args.get('s_type', ''),
        's_progress': request.args.get('s_progress', '')
    }

    success_update = request.args.get('success_update')
    success_delete = request.args.get('success_delete')
    success_msg = None
    if success_update:
        success_msg = "✓ රිපෝට් එකේ දත්ත සාර්ථකව සංස්කරණය (Update) කරන ලදී!"
    elif success_delete:
        success_msg = "✓ රිපෝට් එකේ දත්ත සාර්ථකව මකා දමන (Delete) ලදී!"

    conditions = []
    bind_args = []
    
    # Using ILIKE ensures localized strings match even with invisible character variations
    if s_vals['s_year']: conditions.append("projectyear ILIKE %s"); bind_args.append(s_vals['s_year'])
    if s_vals['s_program']: conditions.append("programname ILIKE %s"); bind_args.append(s_vals['s_program'])
    if s_vals['s_mp']: conditions.append("mp_name ILIKE %s"); bind_args.append(s_vals['s_mp'])
    if s_vals['s_gn']: conditions.append("gn_division ILIKE %s"); bind_args.append(s_vals['s_gn'])
    if s_vals['s_type']: conditions.append("projecttype ILIKE %s"); bind_args.append(s_vals['s_type'])
    if s_vals['s_progress']: conditions.append("projectprogress ILIKE %s"); bind_args.append(s_vals['s_progress'])

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    conn = get_db_connection()
    # RealDictCursor returns lowercased keys natively from PostgreSQL
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM DevProjects" + where_clause, bind_args)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', view_type='search', options=OPTIONS, rows=rows, search_vals=s_vals, success_msg=success_msg)

@app.route('/edit_page')
def edit_page():
    pid = request.args.get('id', '')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM DevProjects WHERE ProjectID = %s", (pid,))
    project = cursor.fetchone()
    cursor.close()
    conn.close()

    if not project:
        return "Project Not Found", 404

    return render_template('index.html', view_type='edit', options=OPTIONS, project=project)

@app.route('/update_project', methods=['POST'])
def update_project():
    pid = get_form_val(request, 'ProjectID')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE DevProjects SET 
            ProjectYear=%s, ProgramName=%s, MinistryName=%s, MP_Name=%s, GN_Division=%s, ProjectType=%s, ProjectNumber=%s,
            ProjectName=%s, ImplementingAgency=%s, ProjectProgress=%s, ApprovedAmount=%s, EstimatedAmount=%s,
            AllocationAmount=%s, CivilWorkAmount=%s, TaxAmount=%s, ContingencyAmount=%s,
            ContractorName=%s, AgreedAmount=%s, CostAmount=%s, RetentionPayment=%s, MaintenanceDuration=%s, 
            ApprovedDate=%s, EstimatedDate=%s, AllocationReceivedDate=%s, AgreementDate=%s, StartDate=%s, EndDate=%s, 
            BillPaidDate=%s, RetentionPaidDate=%s, MaintenanceHandoverDate=%s, MaintenanceAgency=%s, TenderReferDate=%s,
            ProcurementDate=%s, OrderDate=%s, GoodsReceivedDate=%s, HandoverDate=%s
        WHERE ProjectID=%s
    """, (
        get_form_val(request, 'ProjectYear'), get_form_val(request, 'ProgramName'), get_form_val(request, 'MinistryName'), get_form_val(request, 'MP_Name'), get_form_val(request, 'GN_Division'), get_form_val(request, 'ProjectType'), get_form_val(request, 'ProjectNumber'),
        get_form_val(request, 'ProjectName'), get_form_val(request, 'ImplementingAgency'), get_form_val(request, 'ProjectProgress'), get_form_val(request, 'ApprovedAmount', True), get_form_val(request, 'EstimatedAmount', True),
        get_form_val(request, 'AllocationAmount', True), get_form_val(request, 'CivilWorkAmount', True), get_form_val(request, 'TaxAmount', True), get_form_val(request, 'ContingencyAmount', True),
        get_form_val(request, 'ContractorName'), get_form_val(request, 'AgreedAmount', True), get_form_val(request, 'CostAmount', True), get_form_val(request, 'RetentionPayment', True), get_form_val(request, 'MaintenanceDuration'),
        get_form_val(request, 'ApprovedDate'), get_form_val(request, 'EstimatedDate'), get_form_val(request, 'AllocationReceivedDate'), get_form_val(request, 'AgreementDate'), get_form_val(request, 'StartDate'), get_form_val(request, 'EndDate'),
        get_form_val(request, 'BillPaidDate'), get_form_val(request, 'RetentionPaidDate'), get_form_val(request, 'MaintenanceHandoverDate'), get_form_val(request, 'MaintenanceAgency'), get_form_val(request, 'TenderReferDate'),
        get_form_val(request, 'ProcurementDate'), get_form_val(request, 'OrderDate'), get_form_val(request, 'GoodsReceivedDate'), get_form_val(request, 'HandoverDate'), pid
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('search_page', success_update=1))

@app.route('/delete_project')
def delete_project():
    pid = request.args.get('id', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM DevProjects WHERE ProjectID = %s", (pid,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('search_page', success_delete=1))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)