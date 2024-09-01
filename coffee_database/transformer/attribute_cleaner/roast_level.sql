with cte1 as (select distinct roast
              from raw_scraped.bloom_coffee_roasters
              union
              select distinct roast
              from raw_scraped.blue_tokai
              union
              select distinct "Roasting Profile"
              from raw_scraped.corridor_seven
              union
              select distinct "Roast"
              from raw_scraped.curious_life
              union
              select distinct "Roast Profile"
              from raw_scraped.greysoul
              union
              select distinct "Roast Level"
              from raw_scraped.kapi_kottai
              union
              select distinct "Name"
              from raw_scraped.kc_roasters
              union
              select distinct roast
              from raw_scraped.koffie_genetics
              union
              select distinct "Roast Profile"
              from raw_scraped.naivo
              union
              select distinct "Roast"
              from raw_scraped.quick_brown_fox
              union
              select distinct "Roast Level"
              from raw_scraped.savorworks),
     unique_raw as (select distinct lower(roast) as roast_level_raw
                    from cte1
                    where roast is not null)
select roast_level_raw,
       case
           when roast_level_raw='slightly above medium roast with 20% dtr & total roast time of 10 mins.' then 'MEDIUM_DARK'
           when roast_level_raw ilike '%med%' and roast_level_raw ilike '%light%' then 'MEDIUM_LIGHT'
           when roast_level_raw ilike '%med%' and roast_level_raw ilike '%dark%' then 'MEDIUM_DARK'
           when roast_level_raw ilike '%med%' then 'MEDIUM'
           when roast_level_raw ilike '%dark%' then 'DARK'
           when roast_level_raw ilike '%light%' then 'LIGHT'
           when roast_level_raw ilike '%espresso%' then 'MEDIUM_DARK'
           when roast_level_raw ilike '%filter%' then 'MEDIUM_LIGHT'
           when roast_level_raw = 'omni roast' then 'OMNI_ROAST_TBD'
           else null
           end as roast_level
from unique_raw
