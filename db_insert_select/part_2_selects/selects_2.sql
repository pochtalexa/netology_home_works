-- 1
select g.title, count(1) as singer_qnty from singer_genre as sg
join genre g on sg.id_genre = g.id
group by g.title
order by singer_qnty desc;


-- 2
select count(t.id) as track_qnty from track as t
join album a on t.id_album = a.id
where a.release_year between 2019 and 2020;


-- 3
select a.title, round(avg(t.duration),2) as avg_duration from track as t
join album a on t.id_album = a.id
group by a.title;


-- 4
select s.first_name,
       s.middle_name,
       s.last_name,
       s.nickname,
       a.release_year
from album as a
join singer_album sa on a.id = sa.id_album
join singer s on sa.id_singer = s.id
where a.release_year = 2020;


-- 5
select distinct c.title, s.nickname from collection as c
join collection_track ct on c.id = ct.id_collection
join track t on ct.id_track = t.id
join singer_album sa on t.id_album = sa.id_album
join singer s on sa.id_singer = s.id
where s.nickname = 'Высоцкий';


-- 6
select a.title from album as a
join singer_album sa on a.id = sa.id_album
join singer s on sa.id_singer = s.id
where s.id in (
    select sg.id_singer from singer_genre as sg
    group by sg.id_singer
    having count(1) > 1);


-- 7
select distinct t.title from track as t
where t.id not in (
    select distinct t.id from track as t
    join collection_track ct on t.id = ct.id_track);


-- 8
select s.first_name,
       s.middle_name,
       s.last_name,
       s.nickname
from track t
join singer_album sa on t.id_album = sa.id_album
join singer s on sa.id_singer = s.id
where t.duration = (select min(t.duration) from track as t);


-- 9
select a.title from track as t
join album a on t.id_album = a.id
group by a.title
having count(1) = (
    select min(qnty)
    from (
             select count(1) as qnty
             from track as t
             join album a on t.id_album = a.id
             group by a.id) AAA
);