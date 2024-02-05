drop database crm;
create database crm;
use crm;

create table login
(
	login_id int(11) auto_increment,
    login_username varchar(50) not null,
    login_passwort varchar(70) not null,
    login_vorname varchar(50) not null,
    login_nachname varchar(50) not null,
    login_email varchar(50),
    primary key (login_id)
);

create table ort
(
	ort_id int(11) auto_increment,
    ort_name varchar(100) not null,
    primary key (ort_id)
);

insert into ort values
(default,"Wiesbaden"),
(default,"Mainz"),
(default,"Frankfurt");


create table plz
(
	plz_id int(11) auto_increment,
    plz varchar(10) not null,
    ort_id int(11) not null,
    primary key (plz_id),
    foreign key (ort_id) references ort(ort_id)
);

insert into plz values
(default,"65195",1),
(default,"65201",1),
(default,"65205",1),
(default,"55122",2),
(default,"55116",2),
(default,"55129",2),
(default,"60311",3),
(default,"60320",3);



create table kunde
(
	kunde_id int(11) auto_increment,
    kunde_anrede varchar(10) null,
    kunde_vorname varchar(50) not null,
    kunde_nachname varchar(50) not null,
    kunde_geburtsdatum date not null,
    kunde_straße varchar(50) not null,
    kunde_hausnr varchar(10) null,
    kunde_telefon varchar(20) null,
    kunde_email varchar(50) null,
    plz_id int(11) not null,
    primary key (kunde_id),
    foreign key (plz_id) references plz(plz_id)
);

insert into kunde values
(default,"Herr","Peter","Mayer","1969-05-22","Otto-Wels-Str.","22","0611/20406080","Peter@Mayer.de",1),
(default,null,"Allon","Harper","1980-02-21","Albertsberg","13",null,"Allon@Harper.com",2),
(default,"Herr","Klaus","Klausen","1991-01-01","Alemannenstraße","2","0611/3456782",null,3),
(default,"Frau","Frieda","Mayer","1970-08-08","Abraham-Lincoln-Straße","42","06131/568392923","Frida@Mayer.de",4),
(default,"Herr","Hans","Glück","1988-06-05","Adenauer-Ufer","33",null,"glück@aol.de",5),
(default,"Frau","Gutruhn","Schmidt","1901-09-24","Adam-Opel-Straße","14",null,null,6),
(default,null,"Kai","Yayana","2004-05-02","Allerheiligentor","33",null,null,7),
(default,"Frau","Alexa","Amazon","2015-06-23","Adolf-Reichwein-Straße","1","060/3322441","Alexa@Amazon.com",8);

create table dokumente
(
	kunde_id int(11) not null,
    dokument varchar(255) not null,
    foreign key (kunde_id) references kunde(kunde_id)
);

create view  alle_kundendaten as
select
		kunde_id ,
		kunde_anrede,
		kunde_vorname,
		kunde_nachname,
		kunde_geburtsdatum,
		concat(kunde_straße, " " , kunde_hausnr) as adresse,
        concat(plz," ", ort_name) as ort,
		kunde_telefon,
		kunde_email
from 	kunde
		inner join	plz
			on kunde.plz_id = plz.plz_id
        inner join ort
			on plz.ort_id = ort.ort_id
order by kunde.kunde_id
;