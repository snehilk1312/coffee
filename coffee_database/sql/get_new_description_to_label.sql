-- for avoiding duplicates in NER - take only new rows for ner
with
coffee_first_scraped_at_1 as (select *, row_number() over (partition by name order by scraped_at) as rn
                                 from raw_scraped.savorworks
--                                  where scraped_at > '2024-09-06'
                                 ),
roaster1 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'savorworks'
  and name in (select name
               from coffee_first_scraped_at_1
               where rn = 1
                 and scraped_at >= current_date-20)),
coffee_first_scraped_at_2 as (select *, row_number() over (partition by "Name" order by scraped_at) as rn
                                 from raw_scraped.quick_brown_fox
                                 ),
roaster2 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'quick_brown_fox'
  and name in (select "Name"
               from coffee_first_scraped_at_2
               where rn = 1
               and scraped_at >=  current_date-20
               )
),
coffee_first_scraped_at_3 as (select *, row_number() over (partition by "name" order by scraped_at) as rn
                                 from raw_scraped.blue_tokai
                                 ),
roaster3 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'blue_tokai'
  and name in (select "name"
               from coffee_first_scraped_at_3
               where rn = 1
               and scraped_at >=  current_date-20
               )
),
coffee_first_scraped_at_4 as (select *, row_number() over (partition by "Name" order by scraped_at) as rn
                                 from raw_scraped.corridor_seven
                                 ),
roaster4 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'corridor_seven'
  and name in (select "Name"
               from coffee_first_scraped_at_4
               where rn = 1
               and scraped_at >=  current_date-20
               )
),
coffee_first_scraped_at_5 as (select *, row_number() over (partition by "Name" order by scraped_at) as rn
                                 from raw_scraped.curious_life
                                 ),
roaster5 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'curious_life'
  and name in (select "Name"
               from coffee_first_scraped_at_5
               where rn = 1
               and scraped_at >=  current_date-20
               )
),
coffee_first_scraped_at_6 as (select *, row_number() over (partition by "Product Name" order by scraped_at) as rn
                                 from raw_scraped.kapi_kottai
                                 ),
roaster6 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'kapi_kottai'
  and name in (select "Product Name"
               from coffee_first_scraped_at_6
               where rn = 1
               and scraped_at >=  current_date-5
               )
),
coffee_first_scraped_at_7 as (select *, row_number() over (partition by "Name" order by scraped_at) as rn
                                 from raw_scraped.kc_roasters
                                 ),
roaster7 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'kc_roasters'
  and name in (select "Name"
               from coffee_first_scraped_at_7
               where rn = 1
               and scraped_at >=  current_date
               )
),
coffee_first_scraped_at_8 as (select *, row_number() over (partition by "name" order by scraped_at) as rn
                                 from raw_scraped.koffie_genetics
                                 ),
roaster8 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'koffie_genetics'
  and name in (select "name"
               from coffee_first_scraped_at_8
               where rn = 1
               and scraped_at >=  current_date-20
               )
),
coffee_first_scraped_at_9 as (select *, row_number() over (partition by "Name of Coffee" order by scraped_at) as rn
                                 from raw_scraped.naivo
                                 ),
roaster9 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'naivo'
  and name in (select "Name of Coffee"
               from coffee_first_scraped_at_9
               where rn = 1
               and scraped_at >=  current_date-20
               )
),
coffee_first_scraped_at_10 as (select *, row_number() over (partition by "Name" order by scraped_at) as rn
                                 from raw_scraped.quick_brown_fox
                                 ),
roaster10 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'quick_brown_fox'
  and name in (select "Name"
               from coffee_first_scraped_at_10
               where rn = 1
               and scraped_at >=  current_date-20
               )
),
coffee_first_scraped_at_11 as (select *, row_number() over (partition by "Name" order by scraped_at) as rn
                                 from raw_scraped.greysoul
                                 ),
roaster11 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'greysoul'
  and name in (select "Name"
               from coffee_first_scraped_at_11
               where rn = 1
               and scraped_at >=  current_date-20
               )
),
coffee_first_scraped_at_12 as (select *, row_number() over (partition by "name" order by scraped_at) as rn
                                 from raw_scraped.rossette
                                 ),
roaster12 as (
select roaster,name,description
from public.transformed_stg
where roaster = 'rossette'
  and name in (select "name"
               from coffee_first_scraped_at_12
               where rn = 1
               and scraped_at >=  current_date-20
               )
),
final as (
select * from roaster1
union all
select * from roaster2
union all
select * from roaster3
union all
select * from roaster4
union all
select * from roaster5
union all
select * from roaster6
-- union all
-- select * from roaster7
union all
select * from roaster8
union all
select * from roaster9
union all
select * from roaster10
union all
select * from roaster11
union all
select * from roaster12
)
select description from final
