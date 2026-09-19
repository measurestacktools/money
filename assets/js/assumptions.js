/* Central material assumptions — SEPARATE from pure math.
   Every yield/coverage is an editable default. UI must state:
   "Actual yield varies by product. Check the manufacturer's specs." */
window.ASSUMPTIONS = {
  concreteBagYieldCuFt: { "40": 0.30, "60": 0.45, "80": 0.60 },
  mortarBagYieldCuFt: { "60": 0.45, "80": 0.60 },
  groutLbPerSqFt: 0.5,            // editable; varies by tile/joint
  paintCoverageSqFtPerGal: 350,   // editable
  paintWastePct: 10,
  generalWastePct: 10,
  tileWastePct: 10,
  gravelTonsPerCubicYard: 1.4,    // editable
  mulchBagsCuFt: 2,               // standard bag
  shingleBundlesPerSquare: 3,     // editable; varies by product
  feltRollSqFt: 400,
  nailsPerSquare: 320,
  metalPanelWidthIn: 36,
  blockNominalSqFt: 0.89,         // 16x8 in wall
  bricksPerSqFt: 6.5,
  insulationBatts: "see product coverage; editable",
  NOTE: "All yields/coverages are editable assumptions. Verify with manufacturer."
};
