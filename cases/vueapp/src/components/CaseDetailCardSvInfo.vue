<script setup>
import { useCaseDetailsStore } from '@cases/stores/case-details.js'

const caseDetailsStore = useCaseDetailsStore()
</script>

<template>
  <div class="card mb-3 varfish-case-list-card flex-grow-1">
    <h5 class="card-header p-2 pl-2">
      <i-mdi-information />
      Structural Variant Annotation
    </h5>
    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th style="width: 33.3%">Genomebuild</th>
          <th style="width: 33.3%">Table</th>
          <th style="width: 33.3%">Release</th>
        </tr>
      </thead>
      <tbody>
        <template v-if="caseDetailsStore.caseSvAnnotationReleaseInfos">
          <tr v-for="info in caseDetailsStore.caseSvAnnotationReleaseInfos">
            <td>{{ info.genomebuild }}</td>
            <td>{{ info.table }}</td>
            <td>{{ info.release }}</td>
          </tr>
        </template>
        <template v-else>
          <tr>
            <td colspan="3" class="text-muted font-italic text-center">
              No SV annotation info.
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
