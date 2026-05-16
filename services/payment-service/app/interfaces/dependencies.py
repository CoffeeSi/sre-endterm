from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request
from app.application.use_cases import (
    CreatePaymentUseCase,
    ProcessPaymentUseCase,
    GetPaymentUseCase,
    GetAllPaymentsUseCase,
    RefundPaymentUseCase,
)
from app.infrastructure.repositories import PaymentRepository

SECRET_KEY = "your-secret-key"  # Should be in environment variable


async def get_current_user_id(request: Request) -> int:
    """Extract user ID from JWT token"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid authorization header"
        )

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_payment_repository(request: Request) -> PaymentRepository:
    """Dependency for payment repository"""
    pool = request.app.state.db_pool
    return PaymentRepository(pool)


async def get_create_payment_use_case(
    repository: Annotated[PaymentRepository, Depends(get_payment_repository)],
) -> CreatePaymentUseCase:
    return CreatePaymentUseCase(repository)


async def get_process_payment_use_case(
    repository: Annotated[PaymentRepository, Depends(get_payment_repository)],
) -> ProcessPaymentUseCase:
    return ProcessPaymentUseCase(repository)


async def get_get_payment_use_case(
    repository: Annotated[PaymentRepository, Depends(get_payment_repository)],
) -> GetPaymentUseCase:
    return GetPaymentUseCase(repository)


async def get_get_all_payments_use_case(
    repository: Annotated[PaymentRepository, Depends(get_payment_repository)],
) -> GetAllPaymentsUseCase:
    return GetAllPaymentsUseCase(repository)


async def get_refund_payment_use_case(
    repository: Annotated[PaymentRepository, Depends(get_payment_repository)],
) -> RefundPaymentUseCase:
    return RefundPaymentUseCase(repository)
