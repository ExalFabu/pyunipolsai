class PositionData:
    def __init__(self, unix_timestamp, timezone, dst, lat, lon, address, zipcode):
        self.unix_timestamp = str(unix_timestamp)[:10]
        self.tz = timezone
        self.dst = dst
        self.lat = lat
        self.lon = lon
        self.address = address
        self.zipcode = zipcode
        self.time = PositionData.parse_unix(self.unix_timestamp, self.tz, self.dst)

    def __str__(self):
        return str({
            'unix_timestamp': self.unix_timestamp,
            'lat': self.lat,
            'lon': self.lon,
            'address': self.address,
            'zipcode': self.zipcode,
            'time': self.time})

    @staticmethod
    def parse_unix(unix_timestamp, tz, dst) -> dict:
        """
        Convert from UNIX timestamp to custom format timestamp
        :param unix_timestamp: unix timestamp
        :param tz: timezone
        :param dst: daylight saving time
        :returns: Date in custom format
        """
        import datetime
        timezone = datetime.timezone(datetime.timedelta(seconds=tz + dst))
        unix_timestamp = float(str(unix_timestamp)[:10])
        dt = datetime.datetime.fromtimestamp(unix_timestamp, timezone)
        return {'time': dt.strftime("%H:%m:%S"),
                'date': {
                    'day': dt.day,
                    'month': dt.month,
                    'year': dt.year
                },
                'date-iso': dt.strftime("%Y-%m-%d")
                }

    @staticmethod
    def parse_raw_position(raw_position):
        # Rememeber: raw_position is lastPosition
        return PositionData(
            unix_timestamp=raw_position.get("date"),
            timezone=raw_position.get("timeZone"),
            dst=raw_position.get("daylightSavingTime"),
            lat=raw_position.get("lat"),
            lon=raw_position.get("lon"),
            address=raw_position.get("address"),
            zipcode=raw_position.get("zipCode")
        )
