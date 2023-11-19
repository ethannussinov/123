
WITH source_data AS (
    SELECT
        material_id,
        poscar_data,
        band_gap
    FROM {{ source('deftpy', 'raw_perovskite_data') }}
)

SELECT
    material_id,
    poscar_data,
    band_gap
FROM source_data
