from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_activate_emergency_use_case,
    get_assign_template_use_case,
    get_create_screen_use_case,
    get_get_screen_config_use_case,
)
from app.application.dtos.screen import (
    EmergencyUpdateDTO,
    ScreenCreateDTO,
    ScreenReadDTO,
)
from app.application.use_cases.screens.activate_emergency import (
    ActivateEmergencyUseCase,
)
from app.application.use_cases.screens.create_screen import CreateScreenUseCase
from app.application.use_cases.screens.get_screen_config import (
    GetScreenConfigUseCase,
)
from app.application.use_cases.templates.assign_template_to_slot import (
    AssignTemplateToSlotUseCase,
)

router = APIRouter()


@router.post(
    "/", response_model=ScreenReadDTO, status_code=status.HTTP_201_CREATED
)
async def create_screen(
    dto: ScreenCreateDTO,
    use_case: CreateScreenUseCase = Depends(get_create_screen_use_case),
):
    return await use_case.execute(dto)


@router.get("/{slug}", response_model=ScreenReadDTO)
async def get_screen_configuration(
    slug: str,
    use_case: GetScreenConfigUseCase = Depends(get_get_screen_config_use_case),
):
    return await use_case.execute(slug)


@router.post("/emergency", status_code=status.HTTP_204_NO_CONTENT)
async def update_emergency_mode(
    dto: EmergencyUpdateDTO,
    use_case: ActivateEmergencyUseCase = Depends(
        get_activate_emergency_use_case
    ),
):
    await use_case.execute(dto)


@router.post(
    "/{screen_id}/slots/{slot_index}", status_code=status.HTTP_204_NO_CONTENT
)
async def assign_template_to_slot(
    screen_id: UUID,
    slot_index: int,
    template_id: UUID | None = None,
    use_case: AssignTemplateToSlotUseCase = Depends(
        get_assign_template_use_case
    ),
):
    await use_case.execute(
        screen_id=screen_id, template_id=template_id, slot_index=slot_index
    )
