class PositionData:
    def __init__(self, unix_timestamp, timezone, dst, lat, lon, address, zipcode, accuracy):
        self.unix_timestamp = str(unix_timestamp)[:10]
        self.tz = timezone
        self.dst = dst
        self.lat = lat
        self.lon = lon
        self.address = address
        self.zipcode = zipcode
        self.datetime = PositionData.parse_unix(self.unix_timestamp, self.tz, self.dst)
        self.accuracy = accuracy

    def as_dict(self) -> dict:
        return {'unix_timestamp': self.unix_timestamp,
                'lat': self.lat,
                'lon': self.lon,
                'address': self.address,
                'zipcode': self.zipcode,
                'time': self.datetime,
                'accuracy': self.accuracy}

    def __str__(self):
        return str(self.as_dict())

    @staticmethod
    def parse_unix(unix_timestamp, tz, dst) -> dict:
        """Convert from UNIX timestamp to custom format timestamp
        :param unix_timestamp: unix timestamp
        :param tz: timezone in seconds
        :param dst: daylight saving time in seconds
        :returns: Date in custom format
        """
        import datetime
        timezone = datetime.timezone(datetime.timedelta(seconds=tz + dst))
        unix_timestamp = float(str(unix_timestamp)[:10])
        dt = datetime.datetime.fromtimestamp(unix_timestamp, timezone)
        return {'time': dt.strftime("%H:%M:%S"),
                'date': dt.strftime("%Y-%m-%d")}

    @staticmethod
    def parse_raw_position(raw_position):
        # Rememeber: raw_position is lastPosition
        return PositionData(
            unix_timestamp=raw_position.get("date"),
            timezone=raw_position.get("timeZone"),
            dst=raw_position.get("daylightSavingTime"),
            lat=raw_position.get("lat"),
            lon=raw_position.get("lon"),
            address=raw_position.get("address") + ", " + raw_position.get("streetNumber"),
            zipcode=raw_position.get("zipCode"),
            accuracy=raw_position.get("accuracy")
        )
