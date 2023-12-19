from flask import Flask, request, jsonify
import pymysql
import pymysql.cursors

app = Flask(__name__)

def get_db_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='example',
                                 database='assign',
                                 port=13313,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

@app.route('/businesses', methods=['GET'])
def get_businesses():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Query parameters
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 25))
            name = request.args.get('name', None)
            city = request.args.get('city', None)
            category = request.args.get('category', None)

            query = "SELECT * FROM business WHERE 1=1"
            params = []

            if name:
                query += " AND name LIKE %s"
                params.append(f'%{name}%')
            if city:
                query += " AND city LIKE %s"
                params.append(f'%{city}%')
            if category:
                query += " AND categories LIKE %s"
                params.append(f'%{category}%')

            offset = (page - 1) * limit
            query += " LIMIT %s, %s"
            params.extend([offset, limit])

            cursor.execute(query, params)
            results = cursor.fetchall()
            return jsonify(results)
    except Exception as e:
        return str(e), 500
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=3000)
