create table location
(
	id serial
		constraint location_pkey
			primary key
		constraint location_id_fkey
			references location,
	latitude double precision not null,
	longitude double precision not null
);

alter table location owner to postgres;

create table hourly_weather
(
	temperature_2m double precision,
	relativehumidity_2m double precision,
	dewpoint_2m double precision,
	pressure_msl double precision,
	cloudcover integer,
	precipitation double precision,
	weathercode integer,
	time timestamp not null,
	location_id integer
		constraint hourly_weather_location_id_fkey
			references location
);

alter table hourly_weather owner to postgres;
