class PositionData:
    def __init__(self, unix_timestamp,timezone, dst, lat, lon, address, zipcode):
        self.unix_timestamp = unix_timestamp
        self.tz = timezone
        self.dst = dst
        self.lat = lat
        self.lon = lon
        self.address = address
        self.zipcode = zipcode
        self.formatted_date = PositionData.parse_unix(self.unix_timestamp, self.tz, self.dst)


    def __repr__(self) -> dict:
        return {
            'unix_timestamp': self.unix_timestamp,
            'lat': self.lat,
            'lon': self.lon,
            'address': self.address,
            'zipcode': self.zipcode,
            'datetime': self.formatted_date}

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def parse_unix(unix_timestamp, tz, dst, fmt="%H:%M %a - %d/%m/%y") -> str:
        """
        Convert from UNIX timestamp to custom format timestamp
        :param unix_timestamp: unix timestamp
        :param tz: timezone
        :param dst: daylight saving time
        :param fmt: custom date format
        :returns: Date in custom format
        """
        import datetime
        timezone = datetime.timezone(datetime.timedelta(seconds=tz + dst))
        unix_timestamp = float(str(unix_timestamp)[:10])
        unformatted_date = datetime.datetime.fromtimestamp(unix_timestamp, timezone)
        formatted_date = unformatted_date.strftime(fmt)
        return str(formatted_date)

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