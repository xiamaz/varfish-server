<script setup>
import { useVariantDetailsStore } from '@variants/stores/variantDetails.js'
import { useFilterQueryStore } from '@variants/stores/filterQuery.js'
import { useVariantCommentsStore } from '@variants/stores/variantComments.js'
import { useVariantFlagsStore } from '@variants/stores/variantFlags.js'

import VariantDetailsComments from '@varfish/components/VariantDetailsComments.vue'
import VariantDetailsFlags from '@varfish/components/VariantDetailsFlags.vue'

import VariantDetailsCallDetails from './VariantDetailsCallDetails.vue'
import VariantDetailsClinvar from './VariantDetailsClinvar.vue'
import VariantDetailsConservation from './VariantDetailsConservation.vue'
import VariantDetailsExtraAnnos from './VariantDetailsExtraAnnos.vue'
import VariantDetailsFreqs from './VariantDetailsFreqs.vue'
import VariantDetailsGa4ghBeacons from './VariantDetailsGa4ghBeacons.vue'
import VariantDetailsGene from './VariantDetailsGene.vue'
import VariantDetailsTranscripts from './VariantDetailsTranscripts.vue'
import VariantDetailsVariantValidator from './VariantDetailsVariantValidator.vue'
import VariantDetailsAcmgRating from './VariantDetailsAcmgRating.vue'
import VariantDetailsLinkOuts from './VariantDetailsLinkOuts.vue'

const detailsStore = useVariantDetailsStore()
const queryStore = useFilterQueryStore()
const flagsStore = useVariantFlagsStore()
flagsStore.initialize({ csrf_token: queryStore.csrfToken }, queryStore.caseUuid)
const commentsStore = useVariantCommentsStore()
commentsStore.initialize(
  { csrf_token: queryStore.csrfToken },
  queryStore.caseUuid
)
</script>

<template>
  <div style="font-size: 0.9em">
    <div class="card">
      <div class="card-header" style="font-size: 1.2em">
        <ul class="nav nav-pills">
          <li class="nav-item" role="presentation">
            <a
              class="nav-link active"
              id="info-tab"
              data-toggle="tab"
              data-target="#info"
              type="button"
              role="tab"
              aria-controls="info"
              aria-selected="true"
            >
              Info
            </a>
          </li>
          <li class="nav-item" role="presentation">
            <a
              class="nav-link"
              id="comments-flags-tab"
              data-toggle="tab"
              data-target="#comments-flags"
              type="button"
              role="tab"
              aria-controls="comments-flags"
              aria-selected="false"
            >
              Comments & Flags
            </a>
          </li>
          <li class="nav-item" role="presentation">
            <a
              class="nav-link"
              id="acmg-rating-tab"
              data-toggle="tab"
              data-target="#acmg-rating"
              type="button"
              role="tab"
              aria-controls="acmg-rating"
              aria-selected="false"
            >
              ACMG Rating
            </a>
          </li>
          <li class="nav-item" role="presentation">
            <a
              class="nav-link"
              id="second-hit-tab"
              data-toggle="tab"
              data-target="#second-hit"
              type="button"
              role="tab"
              aria-controls="second-hit"
              aria-selected="false"
            >
              Second Hit
            </a>
          </li>
          <li class="nav-item" role="presentation">
            <a
              class="nav-link"
              id="other-carriers-tab"
              data-toggle="tab"
              data-target="#other-carriers"
              type="button"
              role="tab"
              aria-controls="other-carriers"
              aria-selected="false"
            >
              Other Carriers
            </a>
          </li>
          <li class="nav-item" role="presentation">
            <a
              class="nav-link"
              id="variant-validator-tab"
              data-toggle="tab"
              data-target="#variant-validator"
              type="button"
              role="tab"
              aria-controls="variant-validator"
              aria-selected="false"
            >
              Variant Validator
            </a>
          </li>
        </ul>
      </div>
      <div class="card-body">
        <div class="tab-content">
          <div
            class="tab-pane fade show active"
            id="info"
            role="tabpanel"
            aria-labelledby="info-tab"
          >
            <VariantDetailsLinkOuts
              :gene="detailsStore.gene"
              :small-variant="detailsStore.smallVariant"
              :hgmd-pro-enabled="queryStore.hgmdProEnabled"
              :hgmd-pro-prefix="queryStore.hgmdProPrefix"
              :umd-predictor-api-token="queryStore.umdPredictorApiToken"
            />
            <div class="row">
              <div class="col-12 col-xl-6 pl-0 pr-2">
                <div class="card">
                  <div class="card-header">
                    <h4 class="card-title">Gene</h4>
                  </div>
                  <VariantDetailsGene
                    :gene="detailsStore.gene"
                    :release="detailsStore.smallVariant?.release"
                    :refseq-gene-id="detailsStore.smallVariant?.refseq_gene_id"
                    :ensembl-gene-id="
                      detailsStore.smallVariant?.ensembl_gene_id
                    "
                  />
                </div>
              </div>
              <div class="col-12 col-xl-6 pl-2 pr-0">
                <VariantDetailsGa4ghBeacons
                  v-if="queryStore.ga4ghBeaconNetworkWidgetEnabled"
                  :small-variant="detailsStore.smallVariant"
                />
                <VariantDetailsClinvar />
                <VariantDetailsFreqs
                  v-if="
                    (detailsStore.populations && detailsStore.popFreqs) ||
                    detailsStore.mitochondrialFreqs
                  "
                  :small-variant="detailsStore.smallVariant"
                  :mitochondrial-freqs="detailsStore.mitochondrialFreqs"
                  :populations="detailsStore.populations"
                  :inhouse-freq="detailsStore.inhouseFreq"
                  :pop-freqs="detailsStore.popFreqs"
                />
                <VariantDetailsExtraAnnos
                  :extra-annos="detailsStore.extraAnnos"
                />
              </div>
            </div>
            <div class="row">
              <div class="col-12 col-xl-6 pl-0 pr-2">
                <VariantDetailsTranscripts
                  :effect-details="detailsStore.effectDetails"
                />
              </div>
              <div class="col-12 col-xl-6 pl-2 pr-0">
                <VariantDetailsCallDetails
                  :case-description="queryStore.case"
                  :small-variant="detailsStore.smallVariant"
                />
              </div>
            </div>
            <div class="row">
              <div class="col-12 pl-0 pr-0">
                <VariantDetailsConservation
                  v-if="detailsStore.knownGeneAa"
                  :known-gene-aa="detailsStore.knownGeneAa"
                />
              </div>
            </div>
          </div>
          <div
            class="tab-pane fade"
            id="comments-flags"
            role="tabpanel"
            aria-labelledby="comments-flags-tab"
          >
            <VariantDetailsFlags
              :details-store="detailsStore"
              :flags-store="flagsStore"
              :variant="detailsStore.smallVariant"
            />
            <VariantDetailsComments
              :details-store="detailsStore"
              :comments-store="commentsStore"
              :variant="detailsStore.smallVariant"
            />
          </div>
          <div
            class="tab-pane fade"
            id="acmg-rating"
            role="tabpanel"
            aria-labelledby="acmg-rating-tab"
          >
            <VariantDetailsAcmgRating />
          </div>
          <div
            class="tab-pane fade"
            id="second-hit"
            role="tabpanel"
            aria-labelledby="second-hit-tab"
          >
            <div class="alert alert-secondary">
              <i-mdi-clock />
              Work in progress ...
            </div>
          </div>
          <div
            class="tab-pane fade"
            id="other-carriers"
            role="tabpanel"
            aria-labelledby="other-carriers-tab"
          >
            <div class="alert alert-secondary">
              <i-mdi-clock />
              Work in progress ...
            </div>
          </div>
          <div
            class="tab-pane fade"
            id="variant-validator"
            role="tabpanel"
            aria-labelledby="variant-validator-tab"
          >
            <VariantDetailsVariantValidator
              :small-variant="detailsStore.smallVariant"
              v-model:variant-validator-state="
                detailsStore.variantValidatorState
              "
              v-model:variant-validator-results="
                detailsStore.variantValidatorResults
              "
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
