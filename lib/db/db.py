#db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from lib.db.models import Base, Category, Severity, Institution
import pandas as pd
import os

# 尋找路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "zddd.db")
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        # 寫入 category（若空）
        if session.query(Category).count() == 0:
            session.add_all([
                Category(sn=1, name='教育單位', domain_name='edu.tw'),
                Category(sn=2, name='公司行號', domain_name='com'),
                Category(sn=3, name='公司行號（台灣）', domain_name='com.tw'),
                Category(sn=4, name='政府機關', domain_name='gov.tw'),
                Category(sn=5, name='公共組織', domain_name='org'),
                Category(sn=6, name='公共組織（台灣）', domain_name='org.tw'),
                Category(sn=7, name='其他', domain_name=None),
            ])
            print("category 資料已匯入")

        # 寫入 severity（若空）
        if session.query(Severity).count() == 0:
            session.add_all([
                Severity(sn=1, name='無'),
                Severity(sn=2, name='低'),
                Severity(sn=3, name='中'),
                Severity(sn=4, name='高'),
                Severity(sn=5, name='嚴重'),
            ])
            print("severity 資料已匯入")

        # 匯入 institution.csv（若檔案存在）
        csv_path = "lib/db/institution.csv"
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path, dtype=str)
                if "sn" in df.columns:
                    added = 0
                    exists = session.query(Institution).first()
                    if not exists:
                        for _, row in df.iterrows():                        
                            inst = Institution(
                                sn=int(row["sn"]),
                                id=row["id"],
                                name=row["name"],
                                domain_name=row["domain_name"]
                            )
                            session.add(inst)
                        added += 1
                    
                    if added > 0:
                        print("institution.csv 匯入完成")
                else:
                    print("institution.csv 缺少欄位 'sn'，已跳過匯入")
            except Exception as e:
                print("institution.csv 匯入失敗：", e)

        # 提交所有變更
        session.commit()