create table plresults(
Season_End_Year	int,
Wk	int,
Date	date,
Home	varchar(100),
HomeGoals	int,
AwayGoals	int,
Away	varchar(100),
FTR varchar(5)
);

--select * from plresults ;

create table plpoints (
Season_End_Year int,
team varchar(100),
win int default 0,
loss int default 0,
draw int default 0,
points int default 0,
goalscored int default 0,
goalagainst int default 0,
goaldifference int default 0
);


create table finalplpoints (
Season_End_Year int,
team varchar(100),
gamesplayed int default 0,
win int default 0,
loss int default 0,
draw int default 0,
points int default 0,
goalscored int default 0,
goalagainst int default 0,
goaldifference int default 0
);

--delete from plpoints;


--select * from plpoints order by 1 desc, 2 asc;


insert into plpoints
select a.season_end_year, a.Home, 
case when a.HomeGoals>a.AwayGoals then 1 end win,
case when a.AwayGoals>a.HomeGoals then 1 end lose,
case when a.HomeGoals=a.AwayGoals then 1 end draw,
case when a.HomeGoals>a.AwayGoals then 3
	when a.HomeGoals=a.AwayGoals then 1
	else 0
end points,
a.homegoals goalscored,
a.AwayGoals goalagainst,
a.homegoals-a.AwayGoals goaldifference
 from plresults a

union all

select 
a.season_end_year, a.Away, 
case when a.AwayGoals>a.HomeGoals then 1 end win,
case when a.HomeGoals>a.AwayGoals then 1 end lose,
case when a.HomeGoals=a.AwayGoals then 1 end draw,
case when a.AwayGoals>a.HomeGoals then 3
	when a.HomeGoals=a.AwayGoals then 1
	else 0
end points,
a.AwayGoals goalscored,
a.homegoals goalagainst,
a.AwayGoals-a.homegoals goaldifference
 from plresults a;


insert into finalplpoints
select season_end_year, team, count(*) gamesplayed,sum(win), sum(loss), sum(draw), sum(points), sum(goalscored), sum(goalagainst), sum(goaldifference) from plpoints
group by season_end_year, team order by 1 desc,2;



