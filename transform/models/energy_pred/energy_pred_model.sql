
SELECT
    i.material_id,
    i.poscar_data,
    i.band_gap,
    i.bond_dissociation_energies,
    i.reduction_potentials

    predict_defect_energy(i.poscar_data, i.band_gap, i.bond_dissociation_energies, i.reduction_potentials) AS predicted_energy,

FROM {{ ref('transformed_perovskite_data') }} AS i
