class Config:
    SERVO_CONFIG = {
        # Pin the servo is connected to
        "MOTOR_PIN": 0,

        # Minimum degree of rotation
        "MIN_DEG": 0,

        # Maximum degree of rotation
        "MAX_DEG":180,

        # Degree at which the servo is extended
        "SERVO_EXTENDED_DEG": 0,

        # Degree at which the servo is retracted
        "SERVO_RETRACTED_DEG": 90,
    }

    NETWORK_CONFIG = {
        # Name of WIFI network (Must match in the transmitter)
        "SSID": "Wifi Lightswitch",
        "PASSWORD": "676767",
    }
    

        