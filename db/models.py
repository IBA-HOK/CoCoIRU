from sqlalchemy import Column, Integer, REAL, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

# 1. Special_notes (依存先なし)
class SpecialNotes(Base):
    __tablename__ = "Special_notes"
    special_notes_id = Column(Integer, primary_key=True, index=True)
    notes_content_json = Column(TEXT)
    created_at = Column(TEXT)
    
    # 関連: Membersテーブルから参照される
    member = relationship("Members", back_populates="special_notes")

# 2. Items (依存先なし)
class Items(Base):
    __tablename__ = "Items"
    items_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(TEXT)
    unit = Column(TEXT)
    category = Column(TEXT)
    description = Column(TEXT)
    
    # 関連: Request_contentテーブルから参照される
    request_contents = relationship("RequestContent", back_populates="item")

# 3. Shelter_info (依存先なし)
class ShelterInfo(Base):
    __tablename__ = "Shelter_info"
    shelter_info = Column(Integer, primary_key=True, index=True) # PK名
    latitude = Column(REAL)
    longitude = Column(REAL)
    notes = Column(TEXT)
    created_at = Column(TEXT)
    
    # 関連: Shelterテーブルから参照される
    shelter = relationship("Shelter", back_populates="info")

# 3.5. Credential (依存先なし、CommunitiesとGovUserから参照される)
class Credential(Base):
    __tablename__ = "Credential"
    credential_id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(TEXT, nullable=False)
    created_at = Column(TEXT)
    
    # 関連: Communitiesテーブルから参照される
    community = relationship("Communities", back_populates="credential")
    # 関連: GovUserテーブルから参照される
    gov_user = relationship("GovUser", back_populates="credential")

# 4. Members (Special_notes に依存)
class Members(Base):
    __tablename__ = "Members"
    member_id = Column(Integer, primary_key=True, index=True)
    special_notes_id = Column(Integer, ForeignKey("Special_notes.special_notes_id"))
    created_at = Column(TEXT)
    
    # 関連: Special_notes へ
    special_notes = relationship("SpecialNotes", back_populates="member")
    # 関連: Communities から参照される
    community = relationship("Communities", back_populates="member")

# 5. Request_content (Items に依存)
class RequestContent(Base):
    __tablename__ = "Request_content"
    request_content_id = Column(Integer, primary_key=True, index=True)
    items_id = Column(Integer, ForeignKey("Items.items_id"))
    other_note = Column(TEXT)
    number = Column(Integer)
    created_at = Column(TEXT)
    
    # 関連: Items へ
    item = relationship("Items", back_populates="request_contents")
    # 関連: Support_Request から参照される
    support_request = relationship("SupportRequest", back_populates="request_content")

# 6. Communities (Members に依存)
class Communities(Base):
    __tablename__ = "Communities"
    community_id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("Members.member_id"))
    credential_id = Column(Integer, ForeignKey("Credential.credential_id"), nullable=False, unique=True)
    name = Column(TEXT)
    latitude = Column(REAL)
    longitude = Column(REAL)
    member_count = Column(Integer)
    created_at = Column(TEXT)
    
    # 関連: Members へ
    member = relationship("Members", back_populates="community")
    # 関連: Credential へ
    credential = relationship("Credential", back_populates="community")
    # 関連: Shelter, Support_Request から参照される
    shelters = relationship("Shelter", back_populates="community")
    support_requests = relationship("SupportRequest", back_populates="community")

# 7. Shelter (Shelter_info と Communities に依存)
class Shelter(Base):
    __tablename__ = "Shelter"
    shelter_id = Column(Integer, primary_key=True, index=True)
    shelter_info = Column(Integer, ForeignKey("Shelter_info.shelter_info"))
    community_id = Column(Integer, ForeignKey("Communities.community_id"))
    created_at = Column(TEXT)
    
    # 関連: ShelterInfo と Communities へ
    info = relationship("ShelterInfo", back_populates="shelter")
    community = relationship("Communities", back_populates="shelters")

# 8. Support_Request (Communities と Request_content に依存)
class SupportRequest(Base):
    __tablename__ = "Support_Request"
    request_id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("Communities.community_id"))
    request_content_id = Column(Integer, ForeignKey("Request_content.request_content_id"))
    status = Column(TEXT)
    created_at = Column(TEXT)
    
    # 関連: Communities と Request_content へ
    community = relationship("Communities", back_populates="support_requests")
    request_content = relationship("RequestContent", back_populates="support_request")

# 9. GovUser (Credential に依存)
class GovUser(Base):
    __tablename__ = "GovUser"
    gov_user_id = Column(Integer, primary_key=True, index=True)
    username = Column(TEXT, unique=True, nullable=False, index=True)
    credential_id = Column(Integer, ForeignKey("Credential.credential_id"), nullable=False, unique=True)
    email = Column(TEXT)
    full_name = Column(TEXT)
    is_active = Column(Integer, default=1)  # SQLiteではBooleanの代わりにInteger
    created_at = Column(TEXT)
    
    # 関連: Credential へ
    credential = relationship("Credential", back_populates="gov_user")

# 10. TokenBlacklist (依存先なし)
class TokenBlacklist(Base):
    __tablename__ = "TokenBlacklist"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(TEXT, unique=True, nullable=False, index=True)
    blacklisted_at = Column(TEXT, nullable=False)
    expires_at = Column(TEXT, nullable=False)  # トークンの有効期限