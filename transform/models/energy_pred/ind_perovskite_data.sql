
SELECT
    r.material_id,
    get_descriptors(r.structure)[0] AS structure,
    r.band_gap,

    get_descriptors(r.structure)[1] AS bond_dissociation_energies,
    get_descriptors(r.structure)[2] AS reduction_potentials


FROM {{ ref('stg_perovskite_data') }} AS r
