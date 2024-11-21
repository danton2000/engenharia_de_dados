create schema if not exists minio.prod_bronze with (location = 's3a://bronze/');
create schema if not exists minio.prod_silver with (location = 's3a://silver/');
create schema if not exists minio.prod_gold with (location = 's3a://gold/');

create table if not exists minio.prod_bronze.climate_data (
	name VARCHAR,
	datetime VARCHAR,
	tempmax VARCHAR,
	tempmin VARCHAR,
	temp VARCHAR,
	feelslikemax VARCHAR,
	feelslikemin VARCHAR,
	feelslike VARCHAR,
	dew VARCHAR,
	humidity VARCHAR,
	precip VARCHAR,
	precipprob VARCHAR,
	precipcover VARCHAR,
	preciptype VARCHAR,
	snow VARCHAR,
	snowdepth VARCHAR,
	windgust VARCHAR,
	windspeed VARCHAR,
	winddir VARCHAR,
	sealevelpressure VARCHAR,
	cloudcover VARCHAR,
	visibility VARCHAR,
	solarradiation VARCHAR,
	solarenergy VARCHAR,
	uvindex VARCHAR,
	severerisk VARCHAR,
	sunrise VARCHAR,
	sunset VARCHAR,
	moonphase VARCHAR,
	conditions VARCHAR,
	description VARCHAR,
	icon VARCHAR,
	stations VARCHAR
) WITH (
            external_location = 's3a://bronze/',
            format = 'CSV',
            skip_header_line_count=1
        );


create table if not exists minio.prod_silver.climate_data_cleansed (
	name VARCHAR,
	datetime VARCHAR,
	tempmin VARCHAR,
	temp VARCHAR,
	tempmax VARCHAR
) WITH (
            external_location = 's3a://silver/',
            format = 'CSV',
            skip_header_line_count=1
        );


