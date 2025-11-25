from sqlalchemy.orm import Session
from db import models

def get_dashboard_requests(db: Session):
    """
    行政ダッシュボード用に、支援要請に必要な全情報を結合して取得する。
    JOIN: SupportRequest -> Communities, RequestContent -> Items
    """
    # 必要なカラムを明示的に選択して取得
    results = db.query(
        models.SupportRequest.request_id,
        models.SupportRequest.community_id,
        models.SupportRequest.status,
        models.SupportRequest.created_at,
        
        # Communitiesテーブルから
        models.Communities.name.label("community_name"),
        models.Communities.latitude,
        models.Communities.longitude,
        
        # RequestContentテーブルから
        models.RequestContent.number,
        
        # Itemsテーブルから
        models.Items.item_name,
        models.Items.unit
        
    ).join(
        models.Communities, 
        models.SupportRequest.community_id == models.Communities.community_id
    ).join(
        models.RequestContent, 
        models.SupportRequest.request_content_id == models.RequestContent.request_content_id
    ).join(
        models.Items, 
        models.RequestContent.items_id == models.Items.items_id
    ).order_by(
        models.SupportRequest.created_at.desc()
    ).all()

    return results