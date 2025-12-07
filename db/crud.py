from sqlalchemy.orm import Session
from db import models, schemas
from typing import Type, TypeVar, Generic
from pydantic import BaseModel

from db.session import engine
from db import models
# --- 汎用的な Update (setattr) ロジック ---
def update_db_item(db_item: models.Base, item_update: BaseModel):
    """
    PydanticスキーマからDBモデルの属性を更新する汎用関数
    """
    if db_item:
        # Pydanticモデルから辞書を取得 (unset=Trueで未設定のキーを除外)
        update_data = item_update.model_dump(exclude_unset=True)
        # 辞書の各キー/バリューでDBモデルの属性を更新
        for key, value in update_data.items():
            setattr(db_item, key, value)
    return db_item

# --- 1. SpecialNotes ---

def get_special_note(db: Session, special_notes_id: int):
    return db.query(models.SpecialNotes).filter(models.SpecialNotes.special_notes_id == special_notes_id).first()

def get_special_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SpecialNotes).offset(skip).limit(limit).all()

def create_special_note(db: Session, special_note: schemas.SpecialNotesCreate):
    db_special_note = models.SpecialNotes(**special_note.model_dump())
    db.add(db_special_note)
    db.commit()
    db.refresh(db_special_note)
    return db_special_note

def update_special_note(db: Session, special_notes_id: int, special_note_update: schemas.SpecialNotesCreate):
    db_item = get_special_note(db, special_notes_id)
    db_item = update_db_item(db_item, special_note_update)
    if db_item:
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_special_note(db: Session, special_notes_id: int):
    db_item = get_special_note(db, special_notes_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# --- 2. Items ---

def get_item(db: Session, item_id: int):
    return db.query(models.Items).filter(models.Items.items_id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Items).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemsCreate):
    db_item = models.Items(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item_update: schemas.ItemsCreate):
    db_item = get_item(db, item_id)
    db_item = update_db_item(db_item, item_update)
    if db_item:
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# --- 3. ShelterInfo ---

def get_shelter_info(db: Session, shelter_info_id: int):
    return db.query(models.ShelterInfo).filter(models.ShelterInfo.shelter_info == shelter_info_id).first()

def get_shelter_infos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ShelterInfo).offset(skip).limit(limit).all()

def create_shelter_info(db: Session, shelter_info: schemas.ShelterInfoCreate):
    db_shelter_info = models.ShelterInfo(**shelter_info.model_dump())
    db.add(db_shelter_info)
    db.commit()
    db.refresh(db_shelter_info)
    return db_shelter_info

def update_shelter_info(db: Session, shelter_info_id: int, shelter_info_update: schemas.ShelterInfoCreate):
    db_item = get_shelter_info(db, shelter_info_id)
    db_item = update_db_item(db_item, shelter_info_update)
    if db_item:
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_shelter_info(db: Session, shelter_info_id: int):
    db_item = get_shelter_info(db, shelter_info_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# --- 4. Members ---

def get_member(db: Session, member_id: int):
    return db.query(models.Members).filter(models.Members.member_id == member_id).first()

def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Members).offset(skip).limit(limit).all()

def create_member(db: Session, member: schemas.MembersCreate):
    db_member = models.Members(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def update_member(db: Session, member_id: int, member_update: schemas.MembersCreate):
    db_item = get_member(db, member_id)
    db_item = update_db_item(db_item, member_update)
    if db_item:
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_member(db: Session, member_id: int):
    db_item = get_member(db, member_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# --- 5. RequestContent ---

def get_request_content(db: Session, request_content_id: int):
    return db.query(models.RequestContent).filter(models.RequestContent.request_content_id == request_content_id).first()

def get_request_contents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RequestContent).offset(skip).limit(limit).all()

def create_request_content(db: Session, request_content: schemas.RequestContentCreate):
    db_request_content = models.RequestContent(**request_content.model_dump())
    db.add(db_request_content)
    db.commit()
    db.refresh(db_request_content)
    return db_request_content

def update_request_content(db: Session, request_content_id: int, request_content_update: schemas.RequestContentCreate):
    db_item = get_request_content(db, request_content_id)
    db_item = update_db_item(db_item, request_content_update)
    if db_item:
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_request_content(db: Session, request_content_id: int):
    db_item = get_request_content(db, request_content_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# --- 6. Communities ---

def get_community(db: Session, community_id: int):
    return db.query(models.Communities).filter(models.Communities.community_id == community_id).first()

def get_communities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Communities).offset(skip).limit(limit).all()

def create_community(db: Session, community: schemas.CommunitiesCreate):
    db_community = models.Communities(**community.model_dump())
    db.add(db_community)
    db.commit()
    db.refresh(db_community)
    return db_community

def update_community(db: Session, community_id: int, community_update: schemas.CommunitiesCreate):
    db_item = get_community(db, community_id)
    db_item = update_db_item(db_item, community_update)
    if db_item:
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_community(db: Session, community_id: int):
    db_item = get_community(db, community_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# --- 7. Shelter ---

def get_shelter(db: Session, shelter_id: int):
    return db.query(models.Shelter).filter(models.Shelter.shelter_id == shelter_id).first()

def get_shelters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Shelter).offset(skip).limit(limit).all()

def create_shelter(db: Session, shelter: schemas.ShelterCreate):
    db_shelter = models.Shelter(**shelter.model_dump())
    db.add(db_shelter)
    db.commit()
    db.refresh(db_shelter)
    return db_shelter

def update_shelter(db: Session, shelter_id: int, shelter_update: schemas.ShelterCreate):
    db_item = get_shelter(db, shelter_id)
    db_item = update_db_item(db_item, shelter_update)
    if db_item:
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_shelter(db: Session, shelter_id: int):
    db_item = get_shelter(db, shelter_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# --- 8. SupportRequest ---

def get_support_request(db: Session, request_id: int):
    return db.query(models.SupportRequest).filter(models.SupportRequest.request_id == request_id).first()

def get_support_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SupportRequest).offset(skip).limit(limit).all()

def create_support_request(db: Session, support_request: schemas.SupportRequestCreate):
    db_support_request = models.SupportRequest(**support_request.model_dump())
    db.add(db_support_request)
    db.commit()
    db.refresh(db_support_request)
    return db_support_request

def update_support_request(db: Session, request_id: int, support_request_update: schemas.SupportRequestCreate):
    db_item = get_support_request(db, request_id)
    db_item = update_db_item(db_item, support_request_update)
    if db_item:
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_support_request(db: Session, request_id: int):
    db_item = get_support_request(db, request_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item