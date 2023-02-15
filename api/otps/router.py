from fastapi import APIRouter, HTTPException, status
from api.otps import schema
from api.enums import otp
from api.otps import crud
from api.utils import otpUtil
import uuid



router =APIRouter(
    prefix="/api/v1"
)

@router.post("/otp/send")
async def send_otp(
    type: otp.OTPType,
    request: schema.CreateOTP
):
    #  Check block OTP
    otp_block = await crud.find_otp_block(request.recipient_id)
    if otp_block:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=" Sorry, this phone number is blocked in 5 minuts")

    # generate and save otp
    otp_code = otpUtil.random(6)
    session_id = str(uuid.uuid1())
    await crud.save_otp(request, session_id, otp_code)

    return {
        "recipient_id": request.recipient_id,
        "session_id": session_id,
        "otp_code": otp_code

    }


@router.post("/otp/verify")
async def send_verify(
        request: schema.VerifyOTP
):
    # Check block OTP
    otp_block = await crud.find_otp_block(request.recipient_id)
    if otp_block:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=" Sorry, this phone number is blocked in 5 minuts")
    #  check OTP code 6 digits lifetime (expired in 60 seconds)
    lifetime_result = await crud.find_otp_lifetime(request)
    if not lifetime_result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=" OTP code has expired, please request a new one.")
    lifetime_result = schema.OTPList(**lifetime_result)
    # check if OTP code is already used
    if lifetime_result.status == "9":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="OTP code has used, please request again")

    #  Verify OTP code,
    # If not verified,
    if lifetime_result.otp_code != request.otp_code:
        # Increment OTP failed count
        await crud.update_otp_failed_count(lifetime_result)


    # If OTP failed count 3 times
    # block OTP (py_otp_blocks)
        if lifetime_result.otp_failed_count + 1 == 3:
            await crud.save_block_otp(lifetime_result)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Sorry, this phone is blocked in 3 minutes")
        # Throw exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect OTP code")

    # Disable OTP code when success verified
    await crud.disable_otp_code(lifetime_result)

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "OTP verified successfully"
    }

