
create table if not exists singer (
	id serial primary key,
	first_name varchar(30),
	middle_name varchar(30),
	last_name varchar(30),
	nickname varchar(30) not null unique
);


create table if not exists collection (
	id serial primary key,
	title varchar(100) not null,
	release_year  int not null
);


create table if not exists genre (
    id serial primary key,
    title varchar(50) not null unique
);


create table if not exists album (
    id serial primary key,
    title varchar(100) not null,
    release_year  int not null
);


create table if not exists track (
    id serial primary key,
    id_album int references album(id),
    title varchar(100) not null,
    duration  numeric not null
);


create table if not exists singer_genre (
    id_singer int references singer(id),
    id_genre int references genre(id),
    constraint pk_singer_genre primary key (id_singer, id_genre)
);


create table if not exists singer_album (
    id_singer int references singer(id),
    id_album int references album(id),
    constraint pk_singer_album primary key (id_singer, id_album)
);


create table if not exists collection_track (
    id_collection int references collection(id),
    id_track int references track(id),
    constraint pk_collection_track primary key (id_collection, id_track)
);



-- 1
select a.title, a.release_year from album as a
where a.release_year = 2018;

-- 2
select a.title, a.duration from track as a
order by a.duration desc
limit(1);

-- 3
select a.title, a.duration from track as a
where a.duration >= 3.5;

-- 4
select a.title from collection as a
where a.release_year between 2018 and 2020;

-- 5
select a.first_name, a.middle_name, a.last_name, a.nickname from singer as a
where a.first_name not like '% %';

-- 6
select a.title from track as a
where a.title like '%мой%' or a.title like '%Мой%'
   or a.title like '%my%' or a.title like '%My%';
