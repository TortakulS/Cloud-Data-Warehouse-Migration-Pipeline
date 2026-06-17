# End-to-End Sales Data Pipeline (Airflow to BigQuery)

ระบบท่อส่งข้อมูลอัตโนมัติ (Data Pipeline) แบบ End-to-End ที่ทำการกวาดข้อมูลยอดขายจากฐานข้อมูลหลังบ้าน ประมวลผลแยกมิติเชิงลึก และนำส่งขึ้นไปจัดเก็บบนคลังข้อมูลระดับคลาวด์โดยอัตโนมัติ ควบคุมและบริหารจัดการผ่าน Apache Airflow บนระบบ Docker

## Data Architecture & Workflow
กระบวนการทำงานของท่อข้อมูลแบ่งออกเป็นสเต็ป **ETL (Extract-Transform-Load)** ดังนี้:

1. **Extract**: ดึงข้อมูลยอดขายดิบ (Raw Sales Data) จากระบบฐานข้อมูล **PostgreSQL** หลังบ้าน ผ่านเครือข่าย Docker Network และบันทึกเป็นไฟล์ชั่วคราว
2. **Transform**: นำข้อมูลดิบมาทำความสะอาดและประมวลผลด้วย **Pandas** เพื่อสร้างตารางสรุปผลเชิงลึก (Analytical Metrics) แยกออกเป็น 6 มิติตามธุรกิจต้องการ:
   * ยอดขายรายวัน / รายเดือน
   * สินค้าขายดีที่สุด (ตามจำนวนชิ้น / ตามรายได้)
   * ค่าเฉลี่ยยอดสั่งซื้อต่อครั้ง (AOV)
3. **Load**: นำส่งข้อมูลสรุปทั้ง 6 มิติขึ้นไปจัดเก็บและอัปเดตบน **Google BigQuery** แยกเป็นตารางย่อยสวยงาม พร้อมใช้งานสำหรับทีม Data Analyst และการทำ Dashboard

---

## Tech Stack ที่เลือกใช้
* **Orchestration:** Apache Airflow (Celery Executor)
* **Containerization:** Docker & Docker Compose
* **Data Processing:** Python (Pandas)
* **Data Source:** PostgreSQL
* **Data Warehouse:** Google BigQuery

---

## Project Structure
```text
├── dags/
│   └── sales_etl_dag.py        # ไฟล์ควบคุมตารางเวลาและลำดับงานของ Airflow
├── scripts/
│   ├── extract.py              # สคริปต์เชื่อมต่อและดึงข้อมูลจาก Postgres
│   ├── transform.py            # สคริปต์คำนวณและแตกไฟล์สรุปผล 6 มิติ
│   └── load.py                 # สคริปต์กวาดไฟล์และโหลดขึ้น Google BigQuery
├── logs/
├── .env                        # ไฟล์เก็บความลับระบบ (Database Port, Project ID)
├── .gitignore                  # คุมระเบียบไฟล์ ซ่อนประวัติล็อกและกุญแจความลับ
└── docker-compose.yaml         # คอนฟิกหลักในการควบคุมตารางเรียนของทุก Service

