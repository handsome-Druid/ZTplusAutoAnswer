\
import sqlite3
import json
import os
import glob
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE_NAME = 'question_bank.db'
# 不再使用单一JSON文件，而是扫描所有JSON文件

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT UNIQUE,
        correct_answer TEXT
    )
    """)
    conn.commit()
    conn.close()

def load_json_to_db():
    """扫描当前目录下的所有JSON文件并加载到数据库中"""
    # 获取当前目录下所有的JSON文件
    json_files = glob.glob("*.json")
    
    if not json_files:
        print("Warning: No JSON files found in current directory.")
        return
    
    print(f"Found {len(json_files)} JSON files: {json_files}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    total_imported = 0
    total_skipped = 0
    
    for json_file in json_files:
        print(f"\nProcessing file: {json_file}")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{json_file}'. Skipping this file.")
            continue
        except Exception as e:
            print(f"Error reading file '{json_file}': {e}. Skipping this file.")
            continue
        
        # 验证数据格式
        if not isinstance(data, list):
            print(f"Error: '{json_file}' should contain a JSON array. Skipping this file.")
            continue
        
        file_imported = 0
        file_skipped = 0
        
        for item in data:
            if not isinstance(item, dict):
                print(f"Warning: Invalid item format in '{json_file}': {item}")
                file_skipped += 1
                continue
                
            question = item.get('question')
            answer = item.get('answer')
            
            if not question or not answer:
                print(f"Warning: Missing 'question' or 'answer' in '{json_file}': {item}")
                file_skipped += 1
                continue
            
            try:
                cursor.execute(
                    "INSERT INTO questions (question_text, correct_answer) VALUES (?, ?)", 
                    (question, answer)
                )
                file_imported += 1
            except sqlite3.IntegrityError:
                # 题目已存在（由于UNIQUE约束）
                file_skipped += 1
            except Exception as e:
                print(f"Error inserting item from '{json_file}': {e}")
                file_skipped += 1
        
        print(f"File '{json_file}': Imported {file_imported}, Skipped {file_skipped}")
        total_imported += file_imported
        total_skipped += file_skipped
    
    conn.commit()
    conn.close()
    
    print(f"\n=== Loading Summary ===")
    print(f"Total files processed: {len(json_files)}")
    print(f"Total questions imported: {total_imported}")
    print(f"Total questions skipped: {total_skipped}")
    print(f"Data loading complete.")

@app.route('/query', methods=['GET'])
def query_questions():
    search_term = request.args.get('term')
    if not search_term:
        return jsonify({"error": "Search term is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT question_text, correct_answer FROM questions WHERE question_text LIKE ?"
    # Add wildcards for LIKE query
    results = cursor.execute(query, (f"%{search_term}%",)).fetchall()
    
    conn.close()
    
    # Convert Row objects to dictionaries
    return jsonify([dict(row) for row in results])

@app.route('/status', methods=['GET'])
def status():
    conn = get_db_connection()
    cursor = conn.cursor()
    count = cursor.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    conn.close()
    return jsonify({"status": "running", "total_questions_in_db": count})

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Loading data from JSON to database...")
    load_json_to_db()
    print("Starting Flask server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
