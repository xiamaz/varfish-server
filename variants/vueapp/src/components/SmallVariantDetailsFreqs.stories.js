import trioVariantsData from '@variantsTest/data/variants-trio.json'

import SmallVariantDetailsFreqs from './SmallVariantDetailsFreqs.vue'

export default {
  title: 'Variants / Small Variant Details Frequencies',
  component: SmallVariantDetailsFreqs,
}

const Template = (args) => ({
  components: { SmallVariantDetailsFreqs },
  setup() {
    return { args }
  },
  template:
    '<SmallVariantDetailsFreqs\n' +
    '    :small-variant="args.smallVariant"\n' +
    '    :mitochondrial-freqs="args.mitochondrialFreqs"\n' +
    '    :populations="args.populations"\n' +
    '    :inhouse-freq="args.inhouseFreq"\n' +
    '    :pop-freqs="args.popFreqs"\n' +
    '/>',
})

export const Autosomal = Template.bind({})
Autosomal.args = {
  smallVariant: trioVariantsData[0],
  mitochondrialFreqs: {},
  populations: [
    'AFR',
    'AMR',
    'ASJ',
    'EAS',
    'FIN',
    'NFE',
    'OTH',
    'SAS',
    'Total',
  ],
  inhouseFreq: {
    hom: 1,
    het: 1,
    hemi: 1,
    carriers: 3,
  },
  popFreqs: {
    'gnomAD Exomes': {
      AFR: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      AMR: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      ASJ: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      EAS: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      FIN: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      NFE: {
        hom: 0,
        het: 2,
        hemi: null,
        af: 0.0000175923,
        controls_het: 1,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0.0000233852,
      },
      OTH: {
        hom: 0,
        het: 1,
        hemi: null,
        af: 0.000163079,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      SAS: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      Total: {
        hom: 0,
        het: 3,
        hemi: null,
        af: 0.0000119359,
        controls_het: 1,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0.00000914328,
      },
    },
    'gnomAD Genomes': {
      AFR: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      AMR: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      ASJ: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      EAS: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      FIN: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      NFE: {
        hom: 0,
        het: 1,
        hemi: null,
        af: 0.0000648088,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      OTH: {
        hom: 0,
        het: 0,
        hemi: null,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
      SAS: {
        hom: 0,
        het: 0,
        hemi: 0,
        af: 0,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: 0,
        controls_af: 0,
      },
      Total: {
        hom: 0,
        het: 1,
        hemi: null,
        af: 0.000031839,
        controls_het: 0,
        controls_hom: 0,
        controls_hemi: null,
        controls_af: 0,
      },
    },
    ExAC: {
      AFR: { hom: 0, het: 0, hemi: null, af: 0 },
      AMR: { hom: 0, het: 0, hemi: null, af: 0 },
      ASJ: { hom: 0, het: 0, hemi: 0, af: 0 },
      EAS: { hom: 0, het: 0, hemi: null, af: 0 },
      FIN: { hom: 0, het: 0, hemi: null, af: 0 },
      NFE: { hom: 0, het: 3, hemi: null, af: 0.0000454009 },
      OTH: { hom: 0, het: 0, hemi: null, af: 0 },
      SAS: { hom: 0, het: 0, hemi: null, af: 0 },
      Total: { hom: 0, het: 3, hemi: null, af: 0.00002502 },
    },
    '1000GP': {
      AFR: { hom: 0, het: 0, hemi: 0, af: 0 },
      AMR: { hom: 0, het: 0, hemi: 0, af: 0 },
      ASJ: { hom: 0, het: 0, hemi: 0, af: 0 },
      EAS: { hom: 0, het: 0, hemi: 0, af: 0 },
      FIN: { hom: 0, het: 0, hemi: 0, af: 0 },
      NFE: { hom: 0, het: 0, hemi: 0, af: 0 },
      OTH: { hom: 0, het: 0, hemi: 0, af: 0 },
      SAS: { hom: 0, het: 0, hemi: 0, af: 0 },
      Total: { hom: 0, het: 0, hemi: 0, af: 0 },
    },
  },
}

export const Mitochondrial = Template.bind({})
Mitochondrial.args = {
  smallVariant: {
    release: 'GRCh37',
    chromosome: 'MT',
    chromosome_no: 25,
    start: 4769,
    end: 4769,
    bin: 585,
    reference: 'A',
    alternative: 'G',
    var_type: 'snv',
    info: {},
    genotype: {
      'NA12878-N1-DNA1-WES1': { ad: 269, dp: 269, gq: 99, gt: '1/1' },
      'NA12891-N1-DNA1-WES1': { ad: 171, dp: 171, gq: 99, gt: '1/1' },
      'NA12892-N1-DNA1-WES1': { ad: 57, dp: 57, gq: 99, gt: '1/1' },
    },
    num_hom_alt: 0,
    num_hom_ref: 0,
    num_het: 0,
    num_hemi_alt: 0,
    num_hemi_ref: 0,
    in_clinvar: true,
    exac_frequency: 0,
    exac_homozygous: 0,
    exac_heterozygous: 0,
    exac_hemizygous: null,
    thousand_genomes_frequency: 0.992029,
    thousand_genomes_homozygous: 0,
    thousand_genomes_heterozygous: 0,
    thousand_genomes_hemizygous: null,
    gnomad_exomes_frequency: 0,
    gnomad_exomes_homozygous: 0,
    gnomad_exomes_heterozygous: 0,
    gnomad_exomes_hemizygous: null,
    gnomad_genomes_frequency: 0,
    gnomad_genomes_homozygous: 0,
    gnomad_genomes_heterozygous: 0,
    gnomad_genomes_hemizygous: null,
    refseq_gene_id: null,
    refseq_transcript_id: 'MTND2',
    ensembl_gene_id: 'ENSG00000198763',
    ensembl_transcript_id: 'ENST00000361453.3',
    gene_id: '4536',
    transcript_id: 'MTND2',
    transcript_coding: true,
    hgvs_c: 'c.300A>G',
    hgvs_p: 'p.I100M',
    effect: ['missense_variant'],
    effect_ambiguity: false,
    exon_dist: 0,
    case_uuid: '3b22fce8-9be8-4387-8e6e-3be73f4228fb',
    family_name: 'NA12878',
    mtdb_count: 2674,
    mtdb_frequency: 0.988905325443787,
    mtdb_dloop: false,
    helixmtdb_het_count: 5,
    helixmtdb_hom_count: 192006,
    helixmtdb_frequency: 0.976887,
    helixmtdb_is_triallelic: false,
    mitomap_count: 49006,
    mitomap_frequency: 0.976702,
    rsid: null,
    symbol: 'MT-ND2',
    gene_name:
      'mitochondrially encoded NADH:ubiquinone oxidoreductase core subunit 2',
    gene_family: 'NADH:ubiquinone oxidoreductase core subunits',
    pubmed_id: '',
    hgnc_id: 'HGNC:7456',
    uniprot_ids: 'P03891',
    gene_symbol: '',
    acmg_symbol: null,
    mgi_id: null,
    flag_count: null,
    flag_bookmarked: null,
    flag_candidate: null,
    flag_segregates: null,
    flag_doesnt_segregate: null,
    flag_final_causative: null,
    flag_for_validation: null,
    flag_no_disease_association: null,
    flag_molecular: null,
    flag_visual: null,
    flag_validation: null,
    flag_phenotype_match: null,
    flag_summary: null,
    comment_count: null,
    extra_annos: null,
    acmg_class_auto: null,
    acmg_class_override: null,
    modes_of_inheritance: null,
    disease_gene: 'True',
    gnomad_pLI: null,
    gnomad_mis_z: null,
    gnomad_syn_z: null,
    gnomad_oe_lof: null,
    gnomad_oe_lof_upper: null,
    gnomad_oe_lof_lower: null,
    gnomad_loeuf: null,
    exac_pLI: null,
    exac_mis_z: null,
    exac_syn_z: null,
    inhouse_hom_ref: 0,
    inhouse_het: 0,
    inhouse_hom_alt: 0,
    inhouse_hemi_ref: 0,
    inhouse_hemi_alt: 0,
    inhouse_carriers: 0,
    variation_type: 'snv',
    vcv: 'VCV000441150',
    summary_review_status_label:
      'single submitter, no assertion criteria provided',
    summary_pathogenicity_label: 'uncertain significance',
    summary_pathogenicity: ['uncertain significance'],
    summary_gold_stars: 0,
    details: [
      {
        id_no: 69333805,
        title: '[NO TITLE]',
        cv_assertions: [
          {
            id_no: 1174515,
            clin_sigs: [
              {
                comments: [
                  'GenomeConnect assertions are reported exactly as they appear on the patient-provided report from the testing laboratory. GenomeConnect staff make no attempt to reinterpret the clinical significance of the variant.',
                ],
                description: 'not provided',
                review_status: 'no assertion provided',
                date_evaluated: null,
              },
            ],
            trait_sets: [
              {
                id_no: null,
                traits: [
                  { preferred_name: 'Not Provided', alternate_names: [] },
                ],
                set_type: 'Disease',
              },
            ],
            version_no: 1,
            observed_in: {
              origin: 'unknown',
              species: 'human',
              comments: [],
              affected_status: 'unknown',
              observed_data_description: null,
            },
            genotype_sets: [
              {
                set_type: 'Variant',
                accession: 'None',
                measure_sets: [
                  {
                    measures: [
                      {
                        symbols: ['MT-ND2'],
                        comments: [],
                        hgnc_ids: [],
                        measure_type: 'Variation',
                        sequence_locations: {},
                      },
                    ],
                    set_type: 'Variant',
                    accession: 'None',
                  },
                ],
              },
            ],
            pathogenicity: 'not provided',
            record_status: 'current',
            review_status: 'no assertion provided',
            submitter_date: '2017-08-22',
            clinvar_accession: 'SCV000607324',
          },
        ],
        record_status: 'current',
        ref_cv_assertion: {
          id_no: 1175322,
          clin_sigs: [
            {
              comments: [],
              description: 'not provided',
              review_status: 'no assertion provided',
              date_evaluated: null,
            },
          ],
          gold_stars: 0,
          trait_sets: [
            {
              id_no: 9460,
              traits: [{ preferred_name: 'not provided', alternate_names: [] }],
              set_type: 'Disease',
            },
          ],
          version_no: 1,
          observed_in: {
            origin: 'unknown',
            species: 'human',
            comments: [],
            affected_status: 'unknown',
            observed_data_description: null,
          },
          date_created: '2017-10-14',
          date_updated: '2021-05-26',
          genotype_sets: [
            {
              set_type: 'Variant',
              accession: 'VCV000441150',
              measure_sets: [
                {
                  measures: [
                    {
                      symbols: ['MT-ND2'],
                      comments: [],
                      hgnc_ids: ['HGNC:7456'],
                      measure_type: 'single nucleotide variant',
                      sequence_locations: {
                        GRCh37: {
                          alt: 'G',
                          ref: 'A',
                          stop: 4769,
                          chrom: 'MT',
                          start: 4769,
                          assembly: 'GRCh37',
                          chrom_acc: 'NC_012920.1',
                          inner_stop: null,
                          outer_stop: null,
                          inner_start: null,
                          outer_start: null,
                        },
                        GRCh38: {
                          alt: 'G',
                          ref: 'A',
                          stop: 4769,
                          chrom: 'MT',
                          start: 4769,
                          assembly: 'GRCh38',
                          chrom_acc: 'NC_012920.1',
                          inner_stop: null,
                          outer_stop: null,
                          inner_start: null,
                          outer_start: null,
                        },
                      },
                    },
                  ],
                  set_type: 'Variant',
                  accession: 'VCV000441150',
                },
              ],
            },
          ],
          pathogenicity: 'not provided',
          record_status: 'current',
          review_status: 'no assertion provided',
          clinvar_accession: 'RCV000509491',
        },
      },
    ],
  },
  mitochondrialFreqs: {
    vars: {
      MITOMAP: [
        ['A', { ac: 1167, af: 0.023258594917787742, ac_het: 0, ac_hom: 0 }],
        ['C', { ac: 1, af: 0.0000199302, ac_het: 0, ac_hom: 0 }],
        ['G', { ac: 49006, af: 0.976702, ac_het: 0, ac_hom: 0 }],
        ['T', { ac: 1, af: 0.0000199302, ac_het: 0, ac_hom: 0 }],
      ],
      mtDB: [
        ['A', { ac: 30, af: 0.011094674556213017, ac_het: 0, ac_hom: 0 }],
        ['C', { ac: 0, af: 0, ac_het: 0, ac_hom: 0 }],
        ['G', { ac: 2674, af: 0.988905325443787, ac_het: 0, ac_hom: 0 }],
        ['T', { ac: 0, af: 0, ac_het: 0, ac_hom: 0 }],
      ],
      HelixMTdb: [
        ['A', { ac: 0, af: 0.0231081534845386, ac_het: 0, ac_hom: 4542 }],
        ['C', { ac: 0, af: 0.00000508766, ac_het: 0, ac_hom: 1 }],
        ['G', { ac: 0, af: 0.976887, ac_het: 5, ac_hom: 192006 }],
        ['T', { ac: 0, af: 0, ac_het: 0, ac_hom: 0 }],
      ],
    },
    an: { MITOMAP: 50175, mtDB: 2704, HelixMTdb: 196554 },
    is_triallelic: false,
    dloop: false,
  },
  populations: null,
  inhouseFreq: null,
  popFreqs: null,
}
