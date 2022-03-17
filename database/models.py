from sqlalchemy import MetaData, Table, Column, Float, Integer, \
    ForeignKey, ForeignKeyConstraint

meta = MetaData()

location = Table(
    "location", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("latitude", Float, nullable=False),
    Column("longitude", Float, nullable=False),
    ForeignKeyConstraint(["id"], ["location.id"])
)

hourly_weather = Table(
    "hourly_weather", meta,
    Column("temperature_2m", Float),
    Column("relativehumidity_2m", Float),
    Column("dewpoint_2m", Float),
    Column("pressure_msl", Float),
    Column("cloudcover", Integer),
    Column("precipitation", Float),
    Column("weathercode", Integer),
    Column("location_id", Integer, ForeignKey("location.id"))
)

