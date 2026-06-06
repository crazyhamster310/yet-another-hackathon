from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_create_template_use_case,
    get_delete_template_use_case,
    get_get_template_use_case,
    get_list_templates_use_case,
    get_update_template_use_case,
)
from app.application.dtos.screen import (
    TemplateCreateDTO,
    TemplateDTO,
    TemplateUpdateDTO,
)
from app.application.use_cases.templates.create_template import (
    CreateTemplateUseCase,
)
from app.application.use_cases.templates.delete_template import (
    DeleteTemplateUseCase,
)
from app.application.use_cases.templates.get_template import GetTemplateUseCase
from app.application.use_cases.templates.list_templates import (
    ListTemplatesUseCase,
)
from app.application.use_cases.templates.update_template import (
    UpdateTemplateUseCase,
)

router = APIRouter()


@router.post(
    "/", response_model=TemplateDTO, status_code=status.HTTP_201_CREATED
)
async def create_template(
    dto: TemplateCreateDTO,
    use_case: CreateTemplateUseCase = Depends(get_create_template_use_case),
):
    return await use_case.execute(dto)


@router.get("/", response_model=list[TemplateDTO])
async def list_templates(
    use_case: ListTemplatesUseCase = Depends(get_list_templates_use_case),
):
    return await use_case.execute()


@router.patch("/", response_model=TemplateDTO)
async def update_template(
    template_id: UUID,
    dto: TemplateUpdateDTO,
    use_case: UpdateTemplateUseCase = Depends(get_update_template_use_case),
):
    return await use_case.execute(template_id, dto)


@router.get("/{template_id}", response_model=TemplateDTO)
async def get_template(
    template_id: UUID,
    use_case: GetTemplateUseCase = Depends(get_get_template_use_case),
):
    return await use_case.execute(template_id)


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: UUID,
    use_case: DeleteTemplateUseCase = Depends(get_delete_template_use_case),
):
    await use_case.execute(template_id)
