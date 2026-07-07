# -*- coding: utf-8 -*-
"""双选会报名系统 - Flask Web 应用"""
import os, sqlite3, json, csv, io
from flask import Flask, render_template, request, jsonify, g, send_file

app = Flask(__name__)
app.secret_key = os.urandom(24)
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")

SESSIONS = [
  {
    "id": 1,
    "name": "全国重点高校巡回招聘会",
    "city": "成都",
    "university": "四川大学（985/211/双一流）",
    "date": "9月7日（周一）14:30-17:30",
    "campus": "望江校区"
  },
  {
    "id": 2,
    "name": "全国重点高校巡回招聘会",
    "city": "成都",
    "university": "电子科技大学（985/211/双一流）",
    "date": "9月8日（周二）9:30-12:00",
    "campus": "清水河校区"
  },
  {
    "id": 3,
    "name": "全国重点高校巡回招聘会",
    "city": "成都",
    "university": "西南交通大学（211/双一流）",
    "date": "9月8日（周二）14:30-17:30",
    "campus": "犀浦校区"
  },
  {
    "id": 4,
    "name": "全国重点高校巡回招聘会",
    "city": "成都",
    "university": "成都理工大学（双一流）",
    "date": "9月9日（周三）14:30-17:30",
    "campus": "校本部"
  },
  {
    "id": 5,
    "name": "全国重点高校巡回招聘会",
    "city": "西安",
    "university": "西北大学（985/211/双一流）",
    "date": "9月10日（周四）14:30-17:30",
    "campus": "长安校区"
  },
  {
    "id": 6,
    "name": "全国重点高校巡回招聘会",
    "city": "西安",
    "university": "西南科技大学（211/双一流）",
    "date": "9月11日（周五）14:30-17:30",
    "campus": "未央校区"
  },
  {
    "id": 7,
    "name": "全国重点高校巡回招聘会",
    "city": "西安",
    "university": "西北大学（211/双一流）",
    "date": "9月14日（周一）14:30-17:30",
    "campus": "太白校区"
  },
  {
    "id": 8,
    "name": "全国重点高校巡回招聘会",
    "city": "西安",
    "university": "西安科技大学（211/双一流）",
    "date": "9月15日（周二）14:30-17:30",
    "campus": "雁塔校区"
  },
  {
    "id": 9,
    "name": "全国重点高校巡回招聘会",
    "city": "西安",
    "university": "西安交通大学（985/211/双一流）",
    "date": "9月16日（周三）14:30-17:30",
    "campus": "兴庆校区"
  },
  {
    "id": 10,
    "name": "全国重点高校巡回招聘会",
    "city": "西安",
    "university": "西安电子科技大学（211/双一流）",
    "date": "9月17日（周四）14:30-17:30",
    "campus": "北校区"
  },
  {
    "id": 11,
    "name": "全国重点高校巡回招聘会",
    "city": "西安",
    "university": "西北工业大学（985/211/双一流）",
    "date": "9月18日（周五）14:30-17:30",
    "campus": "友谊校区"
  },
  {
    "id": 12,
    "name": "全国重点高校巡回招聘会",
    "city": "哈尔滨",
    "university": "哈尔滨工程大学（985/211/双一流）",
    "date": "9月20日（周日）9:30-12:00",
    "campus": "本部"
  },
  {
    "id": 13,
    "name": "全国重点高校巡回招聘会",
    "city": "哈尔滨",
    "university": "哈尔滨工业大学（985/211/双一流）",
    "date": "9月20日（周日）14:30-17:30",
    "campus": "一校区"
  },
  {
    "id": 14,
    "name": "全国重点高校巡回招聘会",
    "city": "长春",
    "university": "吉林大学（985/211/双一流）",
    "date": "9月21日（周一）14:30-17:30",
    "campus": "前卫南区"
  },
  {
    "id": 15,
    "name": "全国重点高校巡回招聘会",
    "city": "长沙",
    "university": "湖南大学（985/211/双一流）",
    "date": "9月22日（周二）14:30-17:30",
    "campus": "南湖校区"
  },
  {
    "id": 16,
    "name": "全国重点高校巡回招聘会",
    "city": "长沙",
    "university": "中南大学（985/211/双一流）",
    "date": "9月23日（周三）14:30-17:30",
    "campus": "本部校区"
  },
  {
    "id": 17,
    "name": "全国重点高校巡回招聘会",
    "city": "南京",
    "university": "南京大学（985/211/双一流）",
    "date": "9月28日（周一）14:30-17:30",
    "campus": "鼓楼校区"
  },
  {
    "id": 18,
    "name": "全国重点高校巡回招聘会",
    "city": "南京",
    "university": "南京航空航天大学（211/双一流）",
    "date": "9月29日（周二）9:30-12:00",
    "campus": "将军路校区"
  },
  {
    "id": 19,
    "name": "全国重点高校巡回招聘会",
    "city": "南京",
    "university": "南京理工大学（211/双一流）",
    "date": "9月29日（周二）14:30-17:30",
    "campus": "南京校区"
  },
  {
    "id": 20,
    "name": "全国重点高校巡回招聘会",
    "city": "南京",
    "university": "东南大学（985/211/双一流）",
    "date": "9月30日（周三）9:30-12:00",
    "campus": "九龙湖校区"
  },
  {
    "id": 21,
    "name": "四川省重点高校巡回招聘会",
    "city": "成都",
    "university": "四川大学（985/211/双一流）",
    "date": "10月12日（周一）14:30-17:30",
    "campus": "望江校区"
  },
  {
    "id": 22,
    "name": "四川省重点高校巡回招聘会",
    "city": "成都",
    "university": "成都理工大学（双一流）",
    "date": "10月13日（周二）14:30-17:30",
    "campus": "成都校区"
  },
  {
    "id": 23,
    "name": "四川省重点高校巡回招聘会",
    "city": "成都",
    "university": "电子科技大学（985/211/双一流）",
    "date": "10月14日（周三）14:30-17:30",
    "campus": "清水河校区"
  },
  {
    "id": 24,
    "name": "四川省重点高校巡回招聘会",
    "city": "成都",
    "university": "西南交通大学（211/双一流）",
    "date": "10月15日（周四）14:30-17:30",
    "campus": "犀浦校区"
  },
  {
    "id": 25,
    "name": "四川省重点高校巡回招聘会",
    "city": "成都",
    "university": "西南财经大学（211/双一流）",
    "date": "10月16日（周五）14:30-17:30",
    "campus": "柳林校区"
  },
  {
    "id": 26,
    "name": "华中地区重点高校巡回招聘会",
    "city": "武汉",
    "university": "中国地质大学（211/双一流）",
    "date": "9月10日（周四）09:30-12:00",
    "campus": "南望山校区"
  },
  {
    "id": 27,
    "name": "华中地区重点高校巡回招聘会",
    "city": "武汉",
    "university": "中国地质大学（211/双一流）",
    "date": "9月10日（周四）14:00-17:30",
    "campus": "未来城校区"
  },
  {
    "id": 28,
    "name": "华中地区重点高校巡回招聘会",
    "city": "武汉",
    "university": "华中科技大学（985/211/双一流）",
    "date": "9月11日（周五）14:00-17:30",
    "campus": "主校区"
  },
  {
    "id": 29,
    "name": "华中地区重点高校巡回招聘会",
    "city": "武汉",
    "university": "武汉理工大学（211/双一流）",
    "date": "9月12日（周六）14:00-17:30",
    "campus": "马房山校区"
  },
  {
    "id": 30,
    "name": "华中地区重点高校巡回招聘会",
    "city": "武汉",
    "university": "武汉大学（985/211/双一流）",
    "date": "9月13日（周日）14:00-17:30",
    "campus": "主校区"
  },
  {
    "id": 31,
    "name": "成都地区重点高校巡回招聘会",
    "city": "成都",
    "university": "四川师范大学",
    "date": "9-12月（具体时间待定）",
    "campus": "狮子山校区"
  },
  {
    "id": 32,
    "name": "成都地区重点高校巡回招聘会",
    "city": "成都",
    "university": "成都信息工程大学",
    "date": "9-12月（具体时间待定）",
    "campus": "航空港校区"
  },
  {
    "id": 33,
    "name": "成都地区重点高校巡回招聘会",
    "city": "成都",
    "university": "西南石油大学（双一流）",
    "date": "9-12月（具体时间待定）",
    "campus": "校本部"
  },
  {
    "id": 34,
    "name": "成都地区重点高校巡回招聘会",
    "city": "成都",
    "university": "成都大学",
    "date": "9-12月（具体时间待定）",
    "campus": "龙泉校区"
  },
  {
    "id": 35,
    "name": "成都地区重点高校巡回招聘会",
    "city": "成都",
    "university": "成都工业学院",
    "date": "9-12月（具体时间待定）",
    "campus": "郫都校区"
  },
  {
    "id": 36,
    "name": "成都地区重点高校巡回招聘会",
    "city": "成都",
    "university": "四川大学锦城学院",
    "date": "9-12月（具体时间待定）",
    "campus": "高新校区"
  },
  {
    "id": 37,
    "name": "成都地区重点高校巡回招聘会",
    "city": "成都",
    "university": "四川传媒学院",
    "date": "9-12月（具体时间待定）",
    "campus": "航空港校区"
  },
  {
    "id": 38,
    "name": "成都地区重点高校巡回招聘会",
    "city": "成都",
    "university": "中国民用航空飞行学院",
    "date": "9-12月（具体时间待定）",
    "campus": "天府校区"
  }
]
TEACHERS = ["马老师", "孙老师", "连老师", "张老师", "其他"]

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("CREATE TABLE IF NOT EXISTS registrations (id INTEGER PRIMARY KEY AUTOINCREMENT,teacher TEXT,company_name TEXT,contact_person TEXT,contact_phone TEXT,company_type TEXT,industry TEXT,price TEXT,payment_status TEXT DEFAULT '未付款',invoice_info TEXT,company_intro TEXT,selected_sessions TEXT,job_positions TEXT,recruiters TEXT,created_at TEXT,updated_at TEXT)")
        g.db.commit()
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None: db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("CREATE TABLE IF NOT EXISTS registrations ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "teacher TEXT NOT NULL,"
        "company_name TEXT NOT NULL,"
        "contact_person TEXT,"
        "price TEXT,"
        "contact_phone TEXT,"
        "company_type TEXT,"
        "industry TEXT,"
        "invoice_info TEXT,"
        "payment_status TEXT DEFAULT '未付款',"
        "company_intro TEXT,"
        "job_positions TEXT DEFAULT '[]',"
        "recruiters TEXT DEFAULT '[]',"
        "selected_sessions TEXT DEFAULT '[]',"
        "created_at TEXT DEFAULT (datetime('now','localtime')),"
        "updated_at TEXT DEFAULT (datetime('now','localtime'))"
    ")")
    db.commit(); db.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html", teachers=TEACHERS, sessions=SESSIONS)

@app.route("/summary")
def summary():
    return render_template("summary.html", teachers=TEACHERS, sessions=SESSIONS)

@app.route("/api/registrations", methods=["GET"])
def get_registrations():
    db = get_db()
    rows = db.execute("SELECT * FROM registrations ORDER BY created_at DESC").fetchall()
    result = []
    for row in rows:
        r = dict(row)
        r["job_positions"] = json.loads(r["job_positions"])
        r["recruiters"] = json.loads(r["recruiters"])
        r["selected_sessions"] = json.loads(r["selected_sessions"])
        result.append(r)
    return jsonify(result)

@app.route("/api/registrations", methods=["POST"])
def add_registration():
    data = request.json
    required = ["teacher", "company_name"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": "缺少必填字段: " + f}), 400
    db = get_db()
    cursor = db.execute(
        "INSERT INTO registrations (teacher, company_name, contact_person, price,"
        " contact_phone, company_type, industry, invoice_info, payment_status, company_intro,"
        " job_positions, recruiters, selected_sessions) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (data.get("teacher"), data.get("company_name"), data.get("contact_person",""),
         data.get("price",""), data.get("contact_phone",""), data.get("company_type",""),
         data.get("industry",""), data.get("invoice_info",""), data.get("payment_status",""), data.get("company_intro",""),
         json.dumps(data.get("job_positions",[]), ensure_ascii=False),
         json.dumps(data.get("recruiters",[]), ensure_ascii=False),
         json.dumps(data.get("selected_sessions",[]), ensure_ascii=False)))
    db.commit()
    return jsonify({"id": cursor.lastrowid, "message": "提交成功"}), 201

@app.route("/api/registrations/<int:rid>", methods=["PUT"])
def update_registration(rid):
    data = request.json
    db = get_db()
    existing = db.execute("SELECT id FROM registrations WHERE id=?", (rid,)).fetchone()
    if not existing:
        return jsonify({"error": "记录不存在"}), 404
    db.execute("UPDATE registrations SET teacher=?, company_name=?, contact_person=?, price=?,"
        " contact_phone=?, company_type=?, industry=?, invoice_info=?, payment_status=?, company_intro=?,"
        " job_positions=?, recruiters=?, selected_sessions=?,"
        " updated_at=datetime('now','localtime') WHERE id=?",
        (data.get("teacher"), data.get("company_name"), data.get("contact_person",""),
         data.get("price",""), data.get("contact_phone",""), data.get("company_type",""),
         data.get("industry",""), data.get("invoice_info",""), data.get("payment_status",""), data.get("company_intro",""),
         json.dumps(data.get("job_positions",[]), ensure_ascii=False),
         json.dumps(data.get("recruiters",[]), ensure_ascii=False),
         json.dumps(data.get("selected_sessions",[]), ensure_ascii=False), rid))
    db.commit()
    return jsonify({"message": "更新成功"})

@app.route("/api/registrations/<int:rid>", methods=["DELETE"])
def delete_registration(rid):
    db = get_db()
    db.execute("DELETE FROM registrations WHERE id=?", (rid,))
    db.commit()
    return jsonify({"message": "删除成功"})

@app.route("/api/download")
def download_csv():
    db = get_db()
    rows = db.execute("SELECT * FROM registrations ORDER BY created_at DESC").fetchall()
    sess_map = {s["id"]: s for s in SESSIONS}
    output = io.StringIO()
    output.write("\ufeff")  # BOM for Excel
    writer = csv.writer(output)
    writer.writerow(["ID","维护老师","企业名称","联系人","报名金额","联系电话","单位性质","所属行业","是否付款",
                     "发票信息","企业简介","报名场次","招聘岗位","招聘联系人","提交时间","更新时间"])
    for row in rows:
        r = dict(row)
        sids = json.loads(r["selected_sessions"])
        session_str = "; ".join([f'{sid}.{sess_map[sid]["city"]}-{sess_map[sid]["university"]}' for sid in sids if sid in sess_map])
        positions = json.loads(r["job_positions"])
        pos_str = "; ".join([p.get("name","") + "(" + p.get("count","") + "人)" for p in positions]) if positions else ""
        recs = json.loads(r["recruiters"])
        rec_str = "; ".join([r2.get("name","") + "/" + r2.get("phone","") for r2 in recs]) if recs else ""
        writer.writerow([r["id"],r["teacher"],r["company_name"],r["contact_person"],
                         r["price"],r["contact_phone"],r["company_type"],r["industry"],
                         r["payment_status"],r["invoice_info"],r["company_intro"],session_str,pos_str,rec_str,
                         r["created_at"],r["updated_at"]])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode("utf-8-sig")),
                     mimetype="text/csv", as_attachment=True,
                     download_name="双选会报名数据.csv")

@app.route("/api/summary")
def get_summary():
    db = get_db()
    rows = db.execute("SELECT * FROM registrations ORDER BY created_at DESC").fetchall()
    session_summary = {}
    for sess in SESSIONS:
        session_summary[sess["id"]] = {"session_id":sess["id"],"session_name":sess["name"],
            "city":sess["city"],"university":sess["university"],"date":sess["date"],
            "campus":sess["campus"],"companies":[]}
    for row in rows:
        r = dict(row)
        selected = json.loads(r["selected_sessions"])
        for sid in selected:
            if sid in session_summary:
                session_summary[sid]["companies"].append({
                    "company_name":r["company_name"],"teacher":r["teacher"],
                    "contact_person":r["contact_person"],"contact_phone":r["contact_phone"],
                    "company_type":r["company_type"],"price":r["price"],
                    "created_at":r["created_at"]})
    return jsonify(list(session_summary.values()))

@app.route("/api/stats")
def get_stats():
    db = get_db()
    rows = db.execute("SELECT teacher, COUNT(*) as cnt, SUM(CAST(price AS REAL)) as total_price FROM registrations GROUP BY teacher").fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 9000))
    app.run(host="0.0.0.0", port=port, debug=False)
