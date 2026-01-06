from pydantic import BaseModel, ConfigDict
from typing import Optional

# SQLAlchemyモデル(ORM)からデータを読み取るための設定
orm_config = ConfigDict(from_attributes=True)

# --- 1. SpecialNotes ---
class SpecialNotesBase(BaseModel):
    notes_content_json: Optional[str] = None
    created_at: Optional[str] = None

class SpecialNotesCreate(SpecialNotesBase):
    pass # 作成時も特に必須項目なし

class SpecialNotes(SpecialNotesBase):
    special_notes_id: int
    model_config = orm_config

# --- 2. Items ---
class ItemsBase(BaseModel):
    item_name: Optional[str] = None
    unit: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

class ItemsCreate(ItemsBase):
    item_name: str # 作成時は品目名を必須とする

class Items(ItemsBase):
    items_id: int
    model_config = orm_config

# --- 3. ShelterInfo ---
class ShelterInfoBase(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None

class ShelterInfoCreate(ShelterInfoBase):
    pass # 特殊な要件なし

class ShelterInfo(ShelterInfoBase):
    shelter_info: int # PK
    model_config = orm_config

# --- 4. Members ---
class MembersBase(BaseModel):
    special_notes_id: Optional[int] = None
    created_at: Optional[str] = None

class MembersCreate(MembersBase):
    pass # 特殊な要件なし

class Members(MembersBase):
    member_id: int
    model_config = orm_config

# --- 5. RequestContent ---
class RequestContentBase(BaseModel):
    items_id: Optional[int] = None
    other_note: Optional[str] = None
    number: Optional[int] = None
    created_at: Optional[str] = None

class RequestContentCreate(RequestContentBase):
    items_id: int # 作成時は必須
    number: int # 作成時は必須

class RequestContent(RequestContentBase):
    request_content_id: int
    model_config = orm_config

# --- 6. Communities ---
class CommunitiesBase(BaseModel):
    member_id: Optional[int] = None
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    member_count: Optional[int] = None
    created_at: Optional[str] = None

class CommunitiesCreate(CommunitiesBase):
    name: str # 作成時は名前を必須とする
    password: str # 作成時はパスワードを必須とする

class Communities(CommunitiesBase):
    community_id: int
    credential_id: int
    model_config = orm_config
    
# --- 7. Shelter ---
class ShelterBase(BaseModel):
    shelter_info: Optional[int] = None
    community_id: Optional[int] = None
    created_at: Optional[str] = None

class ShelterCreate(ShelterBase):
    shelter_info: int # 作成時は必須
    community_id: int # 作成時は必須

class Shelter(ShelterBase):
    shelter_id: int
    model_config = orm_config

# --- 8. SupportRequest ---
class SupportRequestBase(BaseModel):
    community_id: Optional[int] = None
    request_content_id: Optional[int] = None
    status: Optional[str] = "pending"
    created_at: Optional[str] = None

class SupportRequestCreate(SupportRequestBase):
    community_id: int # 作成時は必須
    request_content_id: int # 作成時は必須

class SupportRequest(SupportRequestBase):
    request_id: int
    model_config = orm_config


# --- 9. Credential ---
class CredentialBase(BaseModel):
    created_at: Optional[str] = None

class CredentialCreate(CredentialBase):
    password: str  # 平文パスワード (ハッシュ化前)

class Credential(CredentialBase):
    credential_id: int
    model_config = orm_config


# --- 9. GovUser ---
class GovUserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[str] = None

class GovUserCreate(GovUserBase):
    password: str  # 平文パスワード (ハッシュ化前)

class GovUser(GovUserBase):
    gov_user_id: int
    credential_id: int
    model_config = orm_config


# --- 新規: ItemAdditionRequests (物品追加申請) ---
class ItemAdditionRequestsBase(BaseModel):
    community_id: Optional[int] = None
    item_name: Optional[str] = None
    item_unit: Optional[str] = None
    reason: Optional[str] = None
    timestamp: Optional[str] = None

class ItemAdditionRequestsCreate(ItemAdditionRequestsBase):
    community_id: int
    item_name: str
    timestamp: str

class ItemAdditionRequests(ItemAdditionRequestsBase):
    add_req_id: int
    model_config = orm_config

# --- 10. Auth / Token ---
class TokenRequest(BaseModel):
    user_type: str  # "community" または "gov"
    username: Optional[str] = None  # gov用
    community_id: Optional[int] = None  # community用
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    role: str  # "community" または "gov"

class ValidationRequest(BaseModel):
    user_type: str  # "community" または "gov"
    username: Optional[str] = None  # gov用
    community_id: Optional[int] = None  # community用
    password: str

class ValidationResponse(BaseModel):
    valid: bool