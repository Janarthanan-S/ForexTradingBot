
from datetime import datetime
from config import CONFIG

class SessionFilter:

    @staticmethod
    def allowed():

        hour = datetime.utcnow().hour
        print(f"Current UTC hour: {hour}")

        if hour >= CONFIG["SESSION_START"] and hour <= CONFIG["SESSION_END"]:
            return True

        return False
