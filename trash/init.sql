create table countries (
    id bigint not null auto_increment,
    iso2 varchar(2) not null,
    iso3 varchar(3) not null,
    denomination varchar(191) not null,
    primary key (id),
    constraint uk_country_iso2 unique (iso2),
    constraint uk_country_iso3 unique (iso3)
);

create table users (
    id bigint not null auto_increment,
    username varchar(191) not null,
    password varchar(191) not null,
    primary key (id),
    constraint uk_user_username unique (username)
);