
SELECT
    s.material_id,
    s.poscar_data,
    s.band_gap,

    
    -- use crystal_analysis.py her
    -- Assuming you have a function or method to calculate these properties
    calculate_bond_dissociation_enthalpies(s.poscar_data) AS bond_dissociation_enthalpies,
    calculate_reduction_potentials(s.poscar_data) AS reduction_potentials


FROM {{ ref('stg_perovskite_data') }} AS s
