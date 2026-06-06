from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.data.get_ujin_news import GetUjinNewsUseCase
from app.application.use_cases.data.get_ujin_parking_stats import (
    GetUjinParkingStatsUseCase,
)
from app.application.use_cases.data.get_ujin_storage_stats import (
    GetUjinStorageStatsUseCase,
)
from app.application.use_cases.screens.activate_emergency import (
    ActivateEmergencyUseCase,
)
from app.application.use_cases.screens.create_screen import CreateScreenUseCase
from app.application.use_cases.screens.list_screens import ListScreensUseCase
from app.application.use_cases.screens.get_screen_config import (
    GetScreenConfigUseCase,
)
from app.application.use_cases.templates.assign_template_to_slot import (
    AssignTemplateToSlotUseCase,
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
from app.core.config import settings
from app.domain.interfaces.providers.ujin import IUjinProvider
from app.domain.interfaces.repositories.screen import IScreenRepository
from app.domain.interfaces.repositories.template import ITemplateRepository
from app.infrastructure.database.session import get_db
from app.infrastructure.providers.ujin import UjinProvider
from app.infrastructure.repositories.screen import SqlAlchemyScreenRepository
from app.infrastructure.repositories.template import (
    SqlAlchemyTemplateRepository,
)

# --- INFRASTRUCTURE ---


def get_screen_repository(
    session: AsyncSession = Depends(get_db),
) -> IScreenRepository:
    return SqlAlchemyScreenRepository(session)


def get_template_repository(
    session: AsyncSession = Depends(get_db),
) -> ITemplateRepository:
    return SqlAlchemyTemplateRepository(session)


def get_ujin_provider() -> IUjinProvider:
    return UjinProvider(
        token=settings.UJIN_API_TOKEN, base_url=settings.UJIN_API_BASE_URL
    )


# --- USE CASES ---

# SCREEN


def get_get_screen_config_use_case(
    repo: IScreenRepository = Depends(get_screen_repository),
) -> GetScreenConfigUseCase:
    return GetScreenConfigUseCase(repo)


def get_activate_emergency_use_case(
    repo: IScreenRepository = Depends(get_screen_repository),
) -> ActivateEmergencyUseCase:
    return ActivateEmergencyUseCase(repo)


def get_create_screen_use_case(
    repo: IScreenRepository = Depends(get_screen_repository),
) -> CreateScreenUseCase:
    return CreateScreenUseCase(repo)

def get_list_screens_use_case(
    repo: IScreenRepository = Depends(get_screen_repository),
) -> ListScreensUseCase:
    return ListScreensUseCase(repo)


# TEMPLATE


def get_create_template_use_case(
    repo: ITemplateRepository = Depends(get_template_repository),
) -> CreateTemplateUseCase:
    return CreateTemplateUseCase(repo)


def get_assign_template_use_case(
    screen_repo: IScreenRepository = Depends(get_screen_repository),
    template_repo: ITemplateRepository = Depends(get_template_repository),
) -> AssignTemplateToSlotUseCase:
    return AssignTemplateToSlotUseCase(screen_repo, template_repo)


def get_list_templates_use_case(
    repo: ITemplateRepository = Depends(get_template_repository),
) -> ListTemplatesUseCase:
    return ListTemplatesUseCase(repo)


def get_get_template_use_case(
    repo: ITemplateRepository = Depends(get_template_repository),
) -> GetTemplateUseCase:
    return GetTemplateUseCase(repo)


def get_delete_template_use_case(
    repo: ITemplateRepository = Depends(get_template_repository),
) -> DeleteTemplateUseCase:
    return DeleteTemplateUseCase(repo)


# UJIN


def get_ujin_news_use_case(
    provider: IUjinProvider = Depends(get_ujin_provider),
) -> GetUjinNewsUseCase:
    return GetUjinNewsUseCase(provider)


def get_ujin_parking_use_case(
    provider: IUjinProvider = Depends(get_ujin_provider),
) -> GetUjinParkingStatsUseCase:
    return GetUjinParkingStatsUseCase(provider)


def get_ujin_storage_use_case(
    provider: IUjinProvider = Depends(get_ujin_provider),
) -> GetUjinStorageStatsUseCase:
    return GetUjinStorageStatsUseCase(provider)
