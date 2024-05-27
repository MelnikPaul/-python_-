from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
DATABASE_CONFIG = {
'user': 'root',
'password': 'root',
'host': '127.0.0.1',
'database': 'reports'
}

@app.route('/reports', methods=['POST'])
def add_report():
    data = request.get_json()
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reports (employee_name, report) VALUES (%s, %s)',
    (data.get('employee_name'), data.get('report')))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Report added successfully'})

@app.route('/reports/<employee_name>', methods=['GET'])
def get_reports(employee_name):
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports WHERE employee_name = %s', (employee_name,))
    reports = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({'reports': reports})

@app.route('/all_reports', methods=['GET'])
def get_all_reports():
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reports')
    reports = cursor.fetchall()
    conn.close()

    return jsonify({'reports': reports})

@app.route('/delete_employee/<employee_name>', methods=['DELETE'])
def delete_employee(employee_name):
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reports WHERE employee_name = %s', (employee_name,))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    if affected_rows > 0:
        return jsonify({'message': 'Report(s) deleted successfully'})
    else:
        return jsonify({'message': 'No reports found for the given employee name'}), 404

@app.route('/delete_line/<int:report_id>', methods=['DELETE'])
def delete_line(report_id):
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reports WHERE id = %s', (report_id,))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()
    if affected_rows > 0:
        return jsonify({'message': 'Report deleted successfully'})
    else:
        return jsonify({'message': 'No report found with the given ID'}), 404

@app.route('/delete_reports', methods=['DELETE'])
def delete_multiple_reports():
    data = request.get_json()
    report_ids = data.get('report_ids', [])

    if not report_ids:
        return jsonify({'message': 'No report IDs provided'}), 400

    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    format_strings = ','.join(['%s'] * len(report_ids))
    cursor.execute(f'DELETE FROM reports WHERE id IN ({format_strings})', tuple(report_ids))
    conn.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    conn.close()

    return jsonify({'message': f'{affected_rows} report(s) deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)