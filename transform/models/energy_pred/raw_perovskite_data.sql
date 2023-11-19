
SELECT
    material_id,
    structure,
    band_gap
FROM {{ source('deftpy', 'raw_perovskite_data') }}
