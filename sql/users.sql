-- name: create table
create table users(
    active boolean not null default true
    , id integer primary key autoincrement
    , revision integer not null default 0
    , passwordhash text not null
    , useradmin boolean not null default false
    , username text unique not null
)
;

-- name: deactivate user
-- parameters: id revision id

update users
set active = 0 and revision = revision + 1
where id = ? and revision = ?;
select * from users where id = ?;

-- name: drop table
drop table users;

-- name: fetch by id
-- parameters: id
select * from users where id = ?;

-- name: fetch by name
-- parameters: name
select * from users where username = ?;

-- name: list all
select * from users;

-- name: list by active
-- parameters: active
select * from users where active = ?;

-- name: list by admin
-- parameters: useradmin
select * from users where useradmin = ?;

-- name: list by active and admin
-- parameters: active useradmin
select * from users where active = ? and  useradmin = ?;

-- name: list by partial name
-- parameters: name
select * from users where username like ?;

-- name: list by partial name and active
-- parameters: name active
select * from users where username like ? and active = ?;

-- name: list by partial name and admin
-- parameters: name useradmin
select * from users where username like ? and useradmin = ?;

-- name: list by partial name, active and admin
-- parameters: name active useradmin
select * from users where username like ? and active = ? and  useradmin = ?;

-- name: login
-- parameters: username passwordhash
select * from users where username = ? and passwordhash = ?;

-- name: register
-- parameters: name passwordhash active admin name
-- script: true
insert into users(name, passwordhash, active, useradmin) values(?, ?, ?, ?); 
select * from users where name = ?;

-- name: reset password
-- parameters: passwordhash id revision id
-- script: true
update users 
    set revision = revision + 1, passwordhash = ? 
    where id = ? and revision = ?;
select * from users where id = ?; 

-- name: toggle admin
-- parameters: id revision id
-- script: true
update users 
    set revision = revision + 1, useradmin = not useradmin 
    where id = ? and revision = ?;
select * from users where id = ?; 
