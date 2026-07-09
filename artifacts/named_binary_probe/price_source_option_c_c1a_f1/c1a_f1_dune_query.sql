-- Option C C1A-F1 bounded canary query - PREP ONLY.
-- Generated from accepted C1A-F1 selector artifacts.
-- DO NOT RUN OR PASTE INTO DUNE until the Orchestrator separately authorizes the bounded Dune run.
-- Decoded OrderFilled tables only; no local tx_hash filter; cap+1 over-fetch preserved.
-- per_condition_row_cap = 2000; per-condition LIMIT = 2001; global_row_cap = 6000.

select * from (
select
  '0xf7361f4c577945b89d4a537eda2acd3cceb1e22cb722c8a48a3114eff058b8d7' as condition_id,
  'OVER_UNDER' as nb_subclass,
  cast(evt_tx_hash as varchar) as tx_hash,
  evt_block_time as block_time,
  cast(makerassetid as varchar) as makerAssetId,
  cast(takerassetid as varchar) as takerAssetId,
  cast(makeramountfilled as varchar) as makerAmountFilled,
  cast(takeramountfilled as varchar) as takerAmountFilled,
  'polymarket_polygon.ctfexchange_evt_orderfilled' as source_provenance
from polymarket_polygon.ctfexchange_evt_orderfilled
where evt_block_time between timestamp '2026-05-17 20:12:58' and timestamp '2026-05-17 22:57:23'
  and (
    cast(makerassetid as varchar) in ('99739207105257790128075344211534912968459868715904103406100301477967219589411', '106729855668864395518421132772923669991080130848538476329326157512462635983691')
    or cast(takerassetid as varchar) in ('99739207105257790128075344211534912968459868715904103406100301477967219589411', '106729855668864395518421132772923669991080130848538476329326157512462635983691')
  )
union all
select
  '0xf7361f4c577945b89d4a537eda2acd3cceb1e22cb722c8a48a3114eff058b8d7' as condition_id,
  'OVER_UNDER' as nb_subclass,
  cast(evt_tx_hash as varchar) as tx_hash,
  evt_block_time as block_time,
  cast(makerassetid as varchar) as makerAssetId,
  cast(takerassetid as varchar) as takerAssetId,
  cast(makeramountfilled as varchar) as makerAmountFilled,
  cast(takeramountfilled as varchar) as takerAmountFilled,
  'polymarket_polygon.negriskctfexchange_evt_orderfilled' as source_provenance
from polymarket_polygon.negriskctfexchange_evt_orderfilled
where evt_block_time between timestamp '2026-05-17 20:12:58' and timestamp '2026-05-17 22:57:23'
  and (
    cast(makerassetid as varchar) in ('99739207105257790128075344211534912968459868715904103406100301477967219589411', '106729855668864395518421132772923669991080130848538476329326157512462635983691')
    or cast(takerassetid as varchar) in ('99739207105257790128075344211534912968459868715904103406100301477967219589411', '106729855668864395518421132772923669991080130848538476329326157512462635983691')
  )
  limit 2001
)
union all

select * from (
select
  '0x2bd2a48746fbdecf0555bfe8f5138340341ac3909c7fb5bdf281293039e97148' as condition_id,
  'NAMED_OTHER' as nb_subclass,
  cast(evt_tx_hash as varchar) as tx_hash,
  evt_block_time as block_time,
  cast(makerassetid as varchar) as makerAssetId,
  cast(takerassetid as varchar) as takerAssetId,
  cast(makeramountfilled as varchar) as makerAmountFilled,
  cast(takeramountfilled as varchar) as takerAmountFilled,
  'polymarket_polygon.ctfexchange_evt_orderfilled' as source_provenance
from polymarket_polygon.ctfexchange_evt_orderfilled
where evt_block_time between timestamp '2026-02-28 07:37:53' and timestamp '2026-02-28 09:37:43'
  and (
    cast(makerassetid as varchar) in ('58628042844461990190086982042785508732336823662751558364538755697118206148037', '75024428455096870875984688928039027558009491467451272577964844877843591010157')
    or cast(takerassetid as varchar) in ('58628042844461990190086982042785508732336823662751558364538755697118206148037', '75024428455096870875984688928039027558009491467451272577964844877843591010157')
  )
union all
select
  '0x2bd2a48746fbdecf0555bfe8f5138340341ac3909c7fb5bdf281293039e97148' as condition_id,
  'NAMED_OTHER' as nb_subclass,
  cast(evt_tx_hash as varchar) as tx_hash,
  evt_block_time as block_time,
  cast(makerassetid as varchar) as makerAssetId,
  cast(takerassetid as varchar) as takerAssetId,
  cast(makeramountfilled as varchar) as makerAmountFilled,
  cast(takeramountfilled as varchar) as takerAmountFilled,
  'polymarket_polygon.negriskctfexchange_evt_orderfilled' as source_provenance
from polymarket_polygon.negriskctfexchange_evt_orderfilled
where evt_block_time between timestamp '2026-02-28 07:37:53' and timestamp '2026-02-28 09:37:43'
  and (
    cast(makerassetid as varchar) in ('58628042844461990190086982042785508732336823662751558364538755697118206148037', '75024428455096870875984688928039027558009491467451272577964844877843591010157')
    or cast(takerassetid as varchar) in ('58628042844461990190086982042785508732336823662751558364538755697118206148037', '75024428455096870875984688928039027558009491467451272577964844877843591010157')
  )
  limit 2001
)
union all

select * from (
select
  '0x8f08f282ea61a9a8ec2b22413e2a8764487eea351337fd14f4409ca34151dec7' as condition_id,
  'UP_DOWN' as nb_subclass,
  cast(evt_tx_hash as varchar) as tx_hash,
  evt_block_time as block_time,
  cast(makerassetid as varchar) as makerAssetId,
  cast(takerassetid as varchar) as takerAssetId,
  cast(makeramountfilled as varchar) as makerAmountFilled,
  cast(takeramountfilled as varchar) as takerAmountFilled,
  'polymarket_polygon.ctfexchange_evt_orderfilled' as source_provenance
from polymarket_polygon.ctfexchange_evt_orderfilled
where evt_block_time between timestamp '2025-06-14 21:00:20' and timestamp '2025-06-14 21:05:26'
  and (
    cast(makerassetid as varchar) in ('48991736195478188402624113441181522209031772931978706832085598958658129270671', '71508481217075253633242510255608914759767530465405876068993106076736030574871')
    or cast(takerassetid as varchar) in ('48991736195478188402624113441181522209031772931978706832085598958658129270671', '71508481217075253633242510255608914759767530465405876068993106076736030574871')
  )
union all
select
  '0x8f08f282ea61a9a8ec2b22413e2a8764487eea351337fd14f4409ca34151dec7' as condition_id,
  'UP_DOWN' as nb_subclass,
  cast(evt_tx_hash as varchar) as tx_hash,
  evt_block_time as block_time,
  cast(makerassetid as varchar) as makerAssetId,
  cast(takerassetid as varchar) as takerAssetId,
  cast(makeramountfilled as varchar) as makerAmountFilled,
  cast(takeramountfilled as varchar) as takerAmountFilled,
  'polymarket_polygon.negriskctfexchange_evt_orderfilled' as source_provenance
from polymarket_polygon.negriskctfexchange_evt_orderfilled
where evt_block_time between timestamp '2025-06-14 21:00:20' and timestamp '2025-06-14 21:05:26'
  and (
    cast(makerassetid as varchar) in ('48991736195478188402624113441181522209031772931978706832085598958658129270671', '71508481217075253633242510255608914759767530465405876068993106076736030574871')
    or cast(takerassetid as varchar) in ('48991736195478188402624113441181522209031772931978706832085598958658129270671', '71508481217075253633242510255608914759767530465405876068993106076736030574871')
  )
  limit 2001
)

-- Global row cap ceiling for this prepared C1A-F1 manifest: 6000.
-- This SQL text is an inert preparation artifact until a separate bounded Dune run authorization exists.
