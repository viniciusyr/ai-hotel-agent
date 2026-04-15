from config.settings import Settings


def get_hotel_info(settings: Settings) -> str:
    return (
        f"{settings.hotel_name} is located in {settings.hotel_city}. "
        f"Check-in starts at {settings.hotel_checkin_time}, and check-out is at "
        f"{settings.hotel_checkout_time}. The front desk phone number is "
        f"{settings.hotel_phone}. The agent does not have live access to room "
        "inventory, room rates, restaurant hours, parking pricing, Wi-Fi "
        "passwords, or cancellation policy details. For those topics, gather "
        "the relevant guest details, avoid inventing facts, and offer to "
        "transfer the guest to a team member."
    )
