from sqlalchemy.orm import Session
from db import models, schemas
from typing import Type, TypeVar, Generic
from pydantic import BaseModel
import bcrypt
from datetime import datetime, timezone, timedelta

from db.session import engine
from db import models


def hash_password(plain_password: str) -> str:
    """平文パスワードをハッシュ化"""
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """平文パスワードとハッシュを検証"""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


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


# --- Timestamp helpers ---
def _now_iso():
    # Japan Standard Time (UTC+9)
    jst = timezone(timedelta(hours=9))
    return datetime.now(jst).isoformat()


def _apply_create_timestamps(db_obj: object):
    """モデルに `created_at` 属性があれば、未設定時に現在時刻を入れる。"""
    if hasattr(db_obj, "created_at"):
        cur = getattr(db_obj, "created_at", None)
        if not cur:
            try:
                setattr(db_obj, "created_at", _now_iso())
            except Exception:
                pass


def _apply_update_timestamps(db_obj: object):
    """モデルに `updated_at` 属性があれば更新時に現在時刻を入れる。"""
    if hasattr(db_obj, "updated_at"):
        try:
            setattr(db_obj, "updated_at", _now_iso())
        except Exception:
            pass

# --- 1. SpecialNotes ---

def get_special_note(db: Session, special_notes_id: int):
    return db.query(models.SpecialNotes).filter(models.SpecialNotes.special_notes_id == special_notes_id).first()

def get_special_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SpecialNotes).offset(skip).limit(limit).all()

def create_special_note(db: Session, special_note: schemas.SpecialNotesCreate):
    db_special_note = models.SpecialNotes(**special_note.model_dump())
    _apply_create_timestamps(db_special_note)
    db.add(db_special_note)
    db.commit()
    db.refresh(db_special_note)
    return db_special_note

def update_special_note(db: Session, special_notes_id: int, special_note_update: schemas.SpecialNotesCreate):
    db_item = get_special_note(db, special_notes_id)
    db_item = update_db_item(db_item, special_note_update)
    if db_item:
        _apply_update_timestamps(db_item)
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
    _apply_create_timestamps(db_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item_update: schemas.ItemsCreate):
    db_item = get_item(db, item_id)
    db_item = update_db_item(db_item, item_update)
    if db_item:
        _apply_update_timestamps(db_item)
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
    _apply_create_timestamps(db_shelter_info)
    db.add(db_shelter_info)
    db.commit()
    db.refresh(db_shelter_info)
    return db_shelter_info

def update_shelter_info(db: Session, shelter_info_id: int, shelter_info_update: schemas.ShelterInfoCreate):
    db_item = get_shelter_info(db, shelter_info_id)
    db_item = update_db_item(db_item, shelter_info_update)
    if db_item:
        _apply_update_timestamps(db_item)
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
    _apply_create_timestamps(db_member)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def update_member(db: Session, member_id: int, member_update: schemas.MembersCreate):
    db_item = get_member(db, member_id)
    db_item = update_db_item(db_item, member_update)
    if db_item:
        _apply_update_timestamps(db_item)
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


def get_supported_items(db: Session):
    """Request_content に登録されている品目に対応する Items レコードを返す
    重複を除き Items モデルのリストを返す（items_id, item_name, unit を含む）
    """
    return (
        db.query(models.Items)
        .join(models.RequestContent, models.Items.items_id == models.RequestContent.items_id)
        .distinct()
        .all()
    )

def create_request_content(db: Session, request_content: schemas.RequestContentCreate):
    db_request_content = models.RequestContent(**request_content.model_dump())
    _apply_create_timestamps(db_request_content)
    db.add(db_request_content)
    db.commit()
    db.refresh(db_request_content)
    return db_request_content

def update_request_content(db: Session, request_content_id: int, request_content_update: schemas.RequestContentCreate):
    db_item = get_request_content(db, request_content_id)
    db_item = update_db_item(db_item, request_content_update)
    if db_item:
        _apply_update_timestamps(db_item)
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
    # 1. Credential を先に作成
    credential_data = schemas.CredentialCreate(
        password=community.password,
        created_at=community.created_at
    )
    db_credential = create_credential(db, credential_data)
    
    # 2. コミュニティデータから password を除外して Communities を作成
    community_dict = community.model_dump(exclude={"password"})
    community_dict["credential_id"] = db_credential.credential_id
    
    db_community = models.Communities(**community_dict)
    _apply_create_timestamps(db_community)
    db.add(db_community)
    db.commit()
    db.refresh(db_community)
    return db_community

def update_community(db: Session, community_id: int, community_update: schemas.CommunitiesCreate):
    db_item = get_community(db, community_id)
    db_item = update_db_item(db_item, community_update)
    if db_item:
        _apply_update_timestamps(db_item)
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
    _apply_create_timestamps(db_shelter)
    db.add(db_shelter)
    db.commit()
    db.refresh(db_shelter)
    return db_shelter

def update_shelter(db: Session, shelter_id: int, shelter_update: schemas.ShelterCreate):
    db_item = get_shelter(db, shelter_id)
    db_item = update_db_item(db_item, shelter_update)
    if db_item:
        _apply_update_timestamps(db_item)
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
    _apply_create_timestamps(db_support_request)
    db.add(db_support_request)
    db.commit()
    db.refresh(db_support_request)
    return db_support_request

def update_support_request(db: Session, request_id: int, support_request_update: schemas.SupportRequestCreate):
    db_item = get_support_request(db, request_id)
    db_item = update_db_item(db_item, support_request_update)
    if db_item:
        _apply_update_timestamps(db_item)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_support_request(db: Session, request_id: int):
    db_item = get_support_request(db, request_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item


# --- 新規: ItemAdditionRequests (物品追加申請) ---
def get_item_addition_request(db: Session, add_req_id: int):
    return db.query(models.ItemAdditionRequests).filter(models.ItemAdditionRequests.add_req_id == add_req_id).first()


def get_item_addition_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ItemAdditionRequests).offset(skip).limit(limit).all()


def create_item_addition_request(db: Session, item_req: schemas.ItemAdditionRequestsCreate):
    db_item_req = models.ItemAdditionRequests(**item_req.model_dump())
    # timestamp はスキーマから受け取る想定。created_atヘルパーは該当しないためここではそのまま使用。
    db.add(db_item_req)
    db.commit()
    db.refresh(db_item_req)
    return db_item_req


def update_item_addition_request(db: Session, add_req_id: int, item_req_update: schemas.ItemAdditionRequestsCreate):
    db_item = get_item_addition_request(db, add_req_id)
    db_item = update_db_item(db_item, item_req_update)
    if db_item:
        _apply_update_timestamps(db_item)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item_addition_request(db: Session, add_req_id: int):
    db_item = get_item_addition_request(db, add_req_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item


# --- 9. Credential ---

def create_credential(db: Session, credential: schemas.CredentialCreate):
    """パスワードをハッシュ化して Credential レコードを作成"""
    hashed_pwd = hash_password(credential.password)
    db_credential = models.Credential(
        hashed_password=hashed_pwd,
        created_at=credential.created_at
    )
    _apply_create_timestamps(db_credential)
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential


def get_credential(db: Session, credential_id: int):
    return db.query(models.Credential).filter(
        models.Credential.credential_id == credential_id
    ).first()


def authenticate_community(db: Session, community_id: int, password: str):
    """コミュニティIDとパスワードで認証"""
    community = get_community(db, community_id)
    if not community:
        return None
    credential = get_credential(db, community.credential_id)
    if not credential:
        return None
    if not verify_password(password, credential.hashed_password):
        return None
    return community


# --- 10. GovUser ---

def get_gov_user(db: Session, gov_user_id: int):
    return db.query(models.GovUser).filter(models.GovUser.gov_user_id == gov_user_id).first()


def get_gov_user_by_username(db: Session, username: str):
    return db.query(models.GovUser).filter(models.GovUser.username == username).first()


def get_gov_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GovUser).offset(skip).limit(limit).all()


def create_gov_user(db: Session, gov_user: schemas.GovUserCreate):
    """パスワードをハッシュ化してGovUserレコードを作成"""
    # 1. Credential を先に作成
    credential_data = schemas.CredentialCreate(
        password=gov_user.password,
        created_at=gov_user.created_at
    )
    db_credential = create_credential(db, credential_data)
    
    # 2. GovUserデータから password を除外して GovUser を作成
    gov_user_dict = gov_user.model_dump(exclude={"password"})
    gov_user_dict["credential_id"] = db_credential.credential_id
    
    db_gov_user = models.GovUser(**gov_user_dict)
    _apply_create_timestamps(db_gov_user)
    db.add(db_gov_user)
    db.commit()
    db.refresh(db_gov_user)
    return db_gov_user


def authenticate_gov_user(db: Session, username: str, password: str):
    """govユーザー名とパスワードで認証"""
    gov_user = get_gov_user_by_username(db, username)
    if not gov_user:
        return None
    credential = get_credential(db, gov_user.credential_id)
    if not credential:
        return None
    if not verify_password(password, credential.hashed_password):
        return None
    if not gov_user.is_active:
        return None
    return gov_user


# --- 11. TokenBlacklist ---

def add_token_to_blacklist(db: Session, token: str, expires_at: str):
    """トークンをブラックリストに追加"""
    from datetime import datetime
    db_blacklist = models.TokenBlacklist(
        token=token,
        blacklisted_at=datetime.now().isoformat(),
        expires_at=expires_at
    )
    db.add(db_blacklist)
    db.commit()
    db.refresh(db_blacklist)
    return db_blacklist


def is_token_blacklisted(db: Session, token: str) -> bool:
    """トークンがブラックリストに登録されているかチェック"""
    result = db.query(models.TokenBlacklist).filter(
        models.TokenBlacklist.token == token
    ).first()
    return result is not None


def cleanup_expired_tokens(db: Session):
    """期限切れのブラックリストトークンを削除"""
    from datetime import datetime
    now = datetime.now().isoformat()
    db.query(models.TokenBlacklist).filter(
        models.TokenBlacklist.expires_at < now
    ).delete()
    db.commit()
