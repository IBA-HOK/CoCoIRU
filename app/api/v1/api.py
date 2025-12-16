from fastapi import APIRouter
from app.api.v1.endpoints import (
    items,
    special_notes,
    shelter_info,
    members,
    request_content,
    communities,
    shelter,
    support_request,
    gnss,
    login,
    token,
    government,
    public_items,
    validate
)
from app.api.v1.endpoints import item_addition_requests

api_router = APIRouter()

# 1. SpecialNotes
api_router.include_router(special_notes.router, prefix="/special_notes", tags=["Special Notes"])
# 2. Items
api_router.include_router(items.router, prefix="/items", tags=["Items"])
# 3. ShelterInfo
api_router.include_router(shelter_info.router, prefix="/shelter_info", tags=["Shelter Info"])
# 4. Members
api_router.include_router(members.router, prefix="/members", tags=["Members"])
# 5. RequestContent
api_router.include_router(request_content.router, prefix="/request_content", tags=["Request Content"])
# 6. Communities
api_router.include_router(communities.router, prefix="/communities", tags=["Communities"])
# 7. Shelter
api_router.include_router(shelter.router, prefix="/shelter", tags=["Shelter"])
# 8. SupportRequest
api_router.include_router(support_request.router, prefix="/support_requests", tags=["Support Requests"])
# 9. Additional Endpoints
api_router.include_router(gnss.router, prefix="/gnss", tags=["GNSS"])
# 10. Login and User Management
api_router.include_router(login.router, prefix="/login", tags=["login"])
# 11. Token issuance
api_router.include_router(token.router, prefix="/token", tags=["Auth"])
# 12. Government Dashboard
api_router.include_router(government.router, prefix="/government", tags=["Government Dashboard"])

# 13. Public endpoints (認証不要)
api_router.include_router(public_items.router, prefix="/public", tags=["Public"])

# 14. Validation
api_router.include_router(validate.router, prefix="/validate", tags=["Validation"])

# 15. Item Addition Requests
api_router.include_router(item_addition_requests.router, prefix="/item_addition_requests", tags=["Item Addition Requests"])
