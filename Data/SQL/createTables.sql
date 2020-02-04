create table books (
    id                serial primary key,
    isbn              text not null,
    title             text not null,
    author            text not null,
    year              integer not null
);

create table users (
    id                serial primary key,
    username          text not null,
    password          text not null
);


create table reviews (
    id                serial primary key,
    user_id           serial references users,
    book_id           serial references books,
    score             smallserial not null,
    review_comment    text not null
);
