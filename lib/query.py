# 查詢 category = 1 的編號，限定 Incident.id 範圍
import pandas as pd
from lib.db.db import SessionLocal
from lib.db.models import Incident, Target, Category, Institution, Severity, Vulnerability


def query_category1_df(start_sn: int) -> pd.DataFrame:
    session = SessionLocal()
    query = (
        session.query(
            Incident.id.label('ZeroDay ID'),
            Target.hostname.label('主機名稱'),
            Incident.vendor.label('單位名稱'),
            Category.name.label('單位類型'),
            Institution.name.label('教育單位名稱'),
            Institution.domain_name.label('教育單位網域名稱'),
            Incident.when_start.label('提交時間'),
            Incident.when_ended.label('公開時間'),
            Incident.duration.label('處理日數'),
            Incident.when_crawled.label('擷取時間'),
            Severity.name.label('風險等級'),
            Vulnerability.name.label('弱點名稱'),
            Vulnerability.description.label('弱點說明')
        )
        .join(Target.incident)
        .join(Target.category)
        .outerjoin(Target.institution)
        .join(Incident.vulnerability)
        .join(Incident.severity)
        .filter(Category.domain_name == 'edu.tw')
        .filter(Incident.sn >= start_sn)
    )

    df = pd.DataFrame(query.all(), columns=[
        'ZeroDay ID', '主機名稱', '單位名稱', '單位類型', '教育單位名稱', '教育單位網域名稱',
        '提交時間', '公開時間', '處理日數', '擷取時間', '風險等級', '弱點名稱', '弱點說明'
    ])
    return df