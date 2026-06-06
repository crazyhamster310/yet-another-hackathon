from typing import Any

from fastapi import APIRouter, Depends, Query

from app.api.deps import (
    get_ujin_news_use_case,
    get_ujin_parking_use_case,
    get_ujin_storage_use_case,
)
from app.application.use_cases.data.get_ujin_news import GetUjinNewsUseCase
from app.application.use_cases.data.get_ujin_parking_stats import (
    GetUjinParkingStatsUseCase,
)
from app.application.use_cases.data.get_ujin_storage_stats import (
    GetUjinStorageStatsUseCase,
)

router = APIRouter()


@router.get("/news", response_model=list[dict[str, Any]])
async def get_news(
    complex_ids: list[int] | None = Query(None, alias="complex_ids[]"),
    building_ids: list[int] | None = Query(None, alias="building_ids[]"),
    news_type: str | None = Query(None, alias="news_type"),
    use_case: GetUjinNewsUseCase = Depends(get_ujin_news_use_case),
):
    return await use_case.execute(
        complex_ids=complex_ids, building_ids=building_ids, news_type=news_type
    )


@router.get("/parking", response_model=dict[str, Any])
async def get_parking_stats(
    complex_ids: list[int] | None = Query(None, alias="complex_ids[]"),
    building_ids: list[int] | None = Query(None, alias="building_ids[]"),
    use_case: GetUjinParkingStatsUseCase = Depends(get_ujin_parking_use_case),
):
    return await use_case.execute(
        complex_ids=complex_ids, building_ids=building_ids
    )


@router.get("/storage", response_model=dict[str, Any])
async def get_storage_stats(
    complex_ids: list[int] | None = Query(None, alias="complex_ids[]"),
    building_ids: list[int] | None = Query(None, alias="building_ids[]"),
    use_case: GetUjinStorageStatsUseCase = Depends(get_ujin_storage_use_case),
):
    return await use_case.execute(
        complex_ids=complex_ids, building_ids=building_ids
    )
