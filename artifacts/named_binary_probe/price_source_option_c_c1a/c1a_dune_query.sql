-- C1A bounded canary query - GENERATED TEXT, paste into Dune manually.
-- Source table/version must match each condition's source_table_version below.
-- One UNION ALL block per fixed condition; every predicate is fixed at manifest time.
-- LIMIT is per_condition_row_cap + 1 (over-fetch by one), NOT the cap itself - this
-- lets the canary script prove the cap was not exceeded instead of silently hiding it.
-- Each condition's LIMIT is scoped by wrapping it in its own subquery ('select * from
-- (... limit N)') so it cannot bind to the union's overall result instead of just
-- this condition's branch.

select * from (
  select
    '0x00e0e2e768260268c59fd8c43d77f771b19cf1d70ddfcf51c0198e4f58e0fc8e' as condition_id,
    cast(evt_tx_hash as varchar) as tx_hash,
    evt_block_time as block_time,
    cast(makerassetid as varchar) as makerAssetId,
    cast(takerassetid as varchar) as takerAssetId,
    cast(makeramountfilled as varchar) as makerAmountFilled,
    cast(takeramountfilled as varchar) as takerAmountFilled,
    'polymarket_polygon.ctfexchange_evt_orderfilled' as source_provenance
  from polymarket_polygon.ctfexchange_evt_orderfilled
  where evt_block_time between timestamp '2025-11-01 09:06:02' and timestamp '2025-11-01 12:01:17'
    and (
      cast(makerassetid as varchar) in ('29049922429446649461146694354483936502864436710335876981986601605122528969627', '21742204404384600964734963657535225070638256333681125923801932947414927580237')
      or cast(takerassetid as varchar) in ('29049922429446649461146694354483936502864436710335876981986601605122528969627', '21742204404384600964734963657535225070638256333681125923801932947414927580237')
    )
  limit 2001
)
union all

select * from (
  select
    '0x05e6b63f6a9a207c7d09a6165a7b42dc9b561129528a488509818c9d850d235d' as condition_id,
    cast(evt_tx_hash as varchar) as tx_hash,
    evt_block_time as block_time,
    cast(makerassetid as varchar) as makerAssetId,
    cast(takerassetid as varchar) as takerAssetId,
    cast(makeramountfilled as varchar) as makerAmountFilled,
    cast(takeramountfilled as varchar) as takerAmountFilled,
    'polymarket_polygon.ctfexchange_evt_orderfilled' as source_provenance
  from polymarket_polygon.ctfexchange_evt_orderfilled
  where evt_block_time between timestamp '2026-05-26 18:02:25' and timestamp '2026-05-27 01:40:31'
    and (
      cast(makerassetid as varchar) in ('12084325762110288271661309302443382103831099684872599064741932841529827151533', '102296316989770510250288891289803157485133402420572421146188522347367965087087')
      or cast(takerassetid as varchar) in ('12084325762110288271661309302443382103831099684872599064741932841529827151533', '102296316989770510250288891289803157485133402420572421146188522347367965087087')
    )
  limit 2001
)
union all

select * from (
  select
    '0x06a49f84dc36633874f4d11e26205ec7816bf06fcf5ca100c010a8e72ee0d34f' as condition_id,
    cast(evt_tx_hash as varchar) as tx_hash,
    evt_block_time as block_time,
    cast(makerassetid as varchar) as makerAssetId,
    cast(takerassetid as varchar) as takerAssetId,
    cast(makeramountfilled as varchar) as makerAmountFilled,
    cast(takeramountfilled as varchar) as takerAmountFilled,
    'polymarket_polygon.ctfexchange_evt_orderfilled' as source_provenance
  from polymarket_polygon.ctfexchange_evt_orderfilled
  where evt_block_time between timestamp '2025-03-17 21:08:07' and timestamp '2025-03-20 05:57:47'
    and (
      cast(makerassetid as varchar) in ('111165886097613873410436520982189866148083061940857280887903337730330435343906', '18435106059153240732678486855297603265483471579519971146989994242483053164136')
      or cast(takerassetid as varchar) in ('111165886097613873410436520982189866148083061940857280887903337730330435343906', '18435106059153240732678486855297603265483471579519971146989994242483053164136')
    )
  limit 2001
)
union all

select * from (
  select
    '0x0cb2ceea234b5983a21b51186d52aede1f85e242a519123508ea18ac53a561c2' as condition_id,
    cast(evt_tx_hash as varchar) as tx_hash,
    evt_block_time as block_time,
    cast(makerassetid as varchar) as makerAssetId,
    cast(takerassetid as varchar) as takerAssetId,
    cast(makeramountfilled as varchar) as makerAmountFilled,
    cast(takeramountfilled as varchar) as takerAmountFilled,
    'polymarket_polygon.ctfexchange_evt_orderfilled' as source_provenance
  from polymarket_polygon.ctfexchange_evt_orderfilled
  where evt_block_time between timestamp '2025-05-21 18:24:30' and timestamp '2025-05-22 05:44:45'
    and (
      cast(makerassetid as varchar) in ('14435256600956461523169994922369526133793986263085343330506586915623100183027', '75733971725278593390564231138542512168823400487237894119484650583660636319558')
      or cast(takerassetid as varchar) in ('14435256600956461523169994922369526133793986263085343330506586915623100183027', '75733971725278593390564231138542512168823400487237894119484650583660636319558')
    )
  limit 2001
)
union all

select * from (
  select
    '0x0d37350307c1f60f7f2f83387d9273ab0eac02ed7919e3875e5f28a71fbe675e' as condition_id,
    cast(evt_tx_hash as varchar) as tx_hash,
    evt_block_time as block_time,
    cast(makerassetid as varchar) as makerAssetId,
    cast(takerassetid as varchar) as takerAssetId,
    cast(makeramountfilled as varchar) as makerAmountFilled,
    cast(takeramountfilled as varchar) as takerAmountFilled,
    'polymarket_polygon.ctfexchange_evt_orderfilled' as source_provenance
  from polymarket_polygon.ctfexchange_evt_orderfilled
  where evt_block_time between timestamp '2025-03-24 16:02:30' and timestamp '2025-03-28 04:10:40'
    and (
      cast(makerassetid as varchar) in ('3807123503543018024946125050010222888775141148862146913433613908775102789007', '3256943658486415416032678885568955548110279202524902512258673365596219067175')
      or cast(takerassetid as varchar) in ('3807123503543018024946125050010222888775141148862146913433613908775102789007', '3256943658486415416032678885568955548110279202524902512258673365596219067175')
    )
  limit 2001
)

-- Global row cap ceiling for this manifest: 6000 (enforced client-side
-- by the C1A canary script after CSV export, via a running global count against
-- global_row_cap - Dune's per-block LIMIT above is the per-condition over-fetch
-- bound only, not a substitute for the global check.)