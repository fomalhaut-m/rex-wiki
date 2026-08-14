列转字段，并用逗号分隔

```sql
listagg(iq.LOAD_TRAINS_NO, ',') within group (order by iq.LOAD_TRAINS_NO )
```

