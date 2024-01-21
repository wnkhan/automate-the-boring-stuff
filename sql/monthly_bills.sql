select  month, year, category, sum(amount)
from transactions
where lower(category) like 'bills%'
group by month
order by year, month;