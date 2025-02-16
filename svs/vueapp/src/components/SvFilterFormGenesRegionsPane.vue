<script setup>
import { computed, onMounted, ref } from 'vue'
import Multiselect from '@vueform/multiselect'

import TokenizingTextarea from '@variants/components/TokenizingTextarea.vue'

const props = defineProps({
  showFiltrationInlineHelp: Boolean,
  filtrationComplexityMode: String,
  /** The query settings to operate on. */
  querySettings: Object,
  /** CSRF token for querying the API. */
  csrfToken: String,
  /** API endpoint for querying genes. */
  lookupGeneApiEndpoint: {
    type: String,
    default: '/geneinfo/api/lookup-gene/',
  },
  lookupGenePanelApiEndpoint: {
    type: String,
    default: '/geneinfo/api/lookup-genepanel/',
  },
})

const emit = defineEmits(['update:querySettings'])

// Store field choice.
const listTypeRef = ref('gene_allowlist')
// Return field choice, empty other field when set.
const listType = computed({
  get() {
    return listTypeRef.value
  },
  set(value) {
    if (value === 'gene_allowlist') {
      props.querySettings.genomic_region = ''
    } else if (value === 'genomic_region') {
      props.querySettings.gene_allowlist = ''
    }
    listTypeRef.value = value
  },
})

// tokens copied here once it validates
const genomicRegionArrRef = ref([])
// this is where the text area writes to
const genomicRegionStrRef = ref('')
// local gene panel categories
const genePanelCategories = ref([])
// genomics england panel
const genomicsEnglandPanels = ref([])
// genomics england confidence
const genomicsEnglandConfidence = ref(3)

/** Regular expression for validating a genomic region. */
const regexRegion = new RegExp(
  '^' + // start
    '(?<chrom>(chr)?' + // open chrom
    '(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|X|Y|M|MT)' + // chrom name
    ')' + // close chrom
    '(:(?<start>(\\d+(,\\d+)*))-(?<stop>(\\d+(,\\d+)*)))?' + // optional range
    '$' // end
)

/** Load Genome England PanelApp presets. */
const loadPanelPage = async (page) => {
  await fetch('/proxy/panelapp/v1/panels/?page=' + page).then(
    async (response) => {
      const responseJson = await response.json()
      genomicsEnglandPanels.value = genomicsEnglandPanels.value.concat(
        responseJson.results.map((panel) => {
          return {
            label: `${panel.name} (v${panel.version})`,
            value: panel,
          }
        })
      )
      if (responseJson.next) {
        await loadPanelPage(page + 1)
      }
    }
  )
}

/** Insert genomics england panel. */
const insertGenomicsEnglandPanel = async (panel) => {
  await fetch(
    `/proxy/panelapp/v1/panels/${panel.id}/?version=${panel.version}`
  ).then(async (response) => {
    const responseJson = await response.json()
    let symbols = []

    for (const gene of responseJson.genes) {
      const confidence = parseInt(gene.confidence_level)
      if (confidence >= genomicsEnglandConfidence.value) {
        symbols.push(gene.gene_data.hgnc_id)
      }
    }

    props.querySettings.gene_allowlist =
      props.querySettings.gene_allowlist.concat(symbols)
  })
}

/** Insert local panel. */
const insertLocalPanel = (panel) => {
  props.querySettings.gene_allowlist =
    props.querySettings.gene_allowlist.concat(panel)
}

/** Validation function for genomic region. */
const validateRegion = (token) => {
  const matches = token.match(regexRegion)
  if (
    matches &&
    matches.groups &&
    matches.groups.start &&
    matches.groups.stop
  ) {
    const start = parseInt(matches.groups.start.replace(',', ''))
    const stop = parseInt(matches.groups.stop.replace(',', ''))
    return new Promise((resolved) => {
      resolved({ valid: stop >= start, label: 'example label' })
    })
  } else {
    return new Promise((resolved) => {
      resolved(!!matches)
    })
  }
}

/** Validation function for genes. */
const validateGene = async (token) => {
  let url = `${props.lookupGeneApiEndpoint}?query=${token}`
  if (token.startsWith('GENEPANEL:')) {
    url = `${props.lookupGenePanelApiEndpoint}?query=${token}`
  }
  const response = await fetch(url, {
    Accept: 'application/json',
    'Content-Type': 'application/json',
    'X-CSRFToken': props.csrfToken,
  })
  if (response.status === 404) {
    return false // not found
  } else {
    // Conversion to JSON will fail with an exception on error.
    const geneInfo = await response.json()
    if (token.startsWith('GENEPANEL:')) {
      return !!geneInfo.identifier
    }
    return !!geneInfo.hgnc_id
  }
}

/** Returns "*" if there is a failure with the given field. */
const indicateFailure = (key) => {
  const theRef = {
    genomic_region: genomicRegionTextareaRef,
    gene_allowlist: geneAllowListRegionTextareaRef,
  }[key]
  if (theRef.value && !theRef.value.isValidating() && !theRef.value.isValid()) {
    return '*'
  } else {
    return ''
  }
}

/** Reference to gene allow list TokenizingTextarea */
const geneAllowListRegionTextareaRef = ref(null)
/** Reference to genomic regions TokenizingTextarea */
const genomicRegionTextareaRef = ref(null)

/** Return array of invalid text areas. */
const invalidTextareas = () => {
  const result = []
  if (
    geneAllowListRegionTextareaRef.value &&
    !geneAllowListRegionTextareaRef.value.isValid()
  ) {
    result.push('gene allow list')
  }
  if (
    genomicRegionTextareaRef.value &&
    !genomicRegionTextareaRef.value.isValid()
  ) {
    result.push('genomic regions')
  }
  return result
}

/** Whether the tab is valid. */
const isValid = () => {
  return invalidTextareas().length == 0
}

/** Whether any subcomponent on tab is still validating. */
const isValidating = () => {
  return (
    (genomicRegionTextareaRef.value &&
      genomicRegionTextareaRef.value.isValidating()) ||
    (geneAllowListRegionTextareaRef.value &&
      geneAllowListRegionTextareaRef.value.isValidating())
  )
}

const loadGenePanelCategories = async () => {
  await fetch('/geneinfo/api/genepanel-category/list/').then(
    async (response) => {
      genePanelCategories.value = await response.json()
    }
  )
}

/** Take values from outside on mounted. */
onMounted(async () => {
  genomicRegionArrRef.value = props.querySettings.genomic_region
  genomicRegionStrRef.value = genomicRegionArrRef.value.join(' ')
  await loadPanelPage(1)
  await loadGenePanelCategories()
})

/** Define the exposed functions. */
defineExpose({
  isValid,
  isValidating,
})
</script>

<template>
  <div class="row">
    <div class="col-12">
      <div
        v-if="props.showFiltrationInlineHelp"
        class="alert alert-secondary small p-2 mt-3"
      >
        <i-mdi-information />
        You can use this tab to either a gene allow list or to define a list of
        genomic regions.
      </div>

      <div class="form-inline pl-0 pr-0 pb-3 mt-3">
        <label class="mr-2" for="gene-regions-list-type">List Type</label>
        <select
          v-model="listType"
          :class="{ 'is-invalid': !isValid() }"
          class="custom-select"
          id="gene-regions-list-type"
        >
          <option value="gene_allowlist">
            Gene Allow List{{ indicateFailure('gene_allowlist') }}
          </option>
          <option value="genomic_region">
            Genomic Regions{{ indicateFailure('genomic_region') }}
          </option>
        </select>
        <div class="invalid-feedback">
          There is a problem with: {{ invalidTextareas().join(', ') }}.
        </div>
      </div>

      <div
        v-show="listType === 'genomic_region'"
        class="form-group"
        id="genomic-region-section"
      >
        <TokenizingTextarea
          ref="genomicRegionTextareaRef"
          v-model="props.querySettings.genomic_region"
          :validate="validateRegion"
        />
        <small class="form-text">
          Enter a list of genomic regions to restrict your query to. For
          example: <code>X</code>, <code>chrX</code>,
          <code>chrX:1,000,000-2,000,000.</code>.
        </small>
      </div>
      <div v-show="listType === 'gene_allowlist'" class="form-group">
        <div class="form-inline">
          <label class="form-group">
            <Multiselect
              :options="genomicsEnglandPanels"
              placeholder="Add from GE PanelApp"
              :searchable="true"
              @select="insertGenomicsEnglandPanel"
            />
            Confidence
            <select class="form-control" v-model="genomicsEnglandConfidence">
              <option value="3">green</option>
              <option value="2">amber</option>
              <option value="1">red</option>
            </select>
            and above
          </label>

          <button
            class="btn btn-sm btn-outline-secondary dropdown-toggle"
            type="button"
            id="presets-menu-button"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            <span class="d-none d-sm-inline"> Add Local Panel </span>
            <div
              v-for="category in genePanelCategories"
              class="dropdown-menu"
              aria-labelledby="presets-menu-button"
            >
              <h6 class="dropdown-header">{{ category.title }}</h6>
              <a
                v-for="genepanel in category.genepanel_set"
                class="dropdown-item"
                href="#"
                @click="insertLocalPanel(`GENEPANEL:${genepanel.identifier}`)"
              >
                {{ genepanel.title }} (v{{ genepanel.version_major }}.{{
                  genepanel.version_minor
                }})
              </a>
            </div>
          </button>
        </div>

        <TokenizingTextarea
          ref="geneAllowListRegionTextareaRef"
          v-model="props.querySettings.gene_allowlist"
          :validate="validateGene"
        />
        <small class="form-text">
          Enter a list of genes to restrict your query to, separated with
          spaces. You can use gene symbols, HGNC ids, ENSEMBL gene IDs, or
          Entrez Gene IDs. For example, all of the following code for TGDS
          (TDP-glucose 4,6-dehydratase): <code>TGDS</code>,
          <code>HGNC:20324</code>, <code>ENSG00000088451</code>,
          <code>23483</code>.
        </small>
      </div>
    </div>
  </div>
  <div v-if="filtrationComplexityMode === 'dev'" class="card-footer">
    <i-mdi-account-hard-hat />
    <strong class="pl-2">Developer Info:</strong>
    <code>
      genomic_region = {{ JSON.stringify(querySettings.genomic_region) }},
      gene_allowlist = {{ JSON.stringify(querySettings.gene_allowlist) }},
    </code>
  </div>
</template>

<style src="@vueform/multiselect/themes/default.css"></style>
