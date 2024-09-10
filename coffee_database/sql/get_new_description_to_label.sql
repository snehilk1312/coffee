-- for avoiding duplicates in NER - take only new rows for ner
with
coffee_first_scraped_at_1 as (select *, row_number() over (partition by name order by scraped_at) as rn
                                 from raw_scraped.savorworks
--                                  where scraped_at > '2024-09-06'
                                 ),
roaster1 as (
select description
from public.transformed_stg
where roaster = 'savorworks'
  and name in (select name
               from coffee_first_scraped_at_1
               where rn = 1
                 and scraped_at >= current_date)),
coffee_first_scraped_at_2 as (select *, row_number() over (partition by "Name" order by scraped_at) as rn
                                 from raw_scraped.quick_brown_fox
--                                  where scraped_at >= '2024-09-06'
                                 ),
roaster2 as (
select description
from public.transformed_stg
where roaster = 'quick_brown_fox'
  and name in (select "Name"
               from coffee_first_scraped_at_2
               where rn = 1
               and scraped_at >=  '2024-09-06' --current_date
               )
)
select * from roaster2
union all
select * from roaster1
union all
select description from transformed_stg where  description is not null and roaster='blue_tokai'
union all
select description from transformed_stg where  description is not null and roaster='kc_roasters'