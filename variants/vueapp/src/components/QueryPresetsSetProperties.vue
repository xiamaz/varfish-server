<script setup>
/** Editor component for the query preset set properties.
 */

import { computed } from 'vue'
import { randomString } from '@varfish/common.js'

/** Define props. */
const props = defineProps({
  label: String,
  idSuffix: {
    type: String,
    default: randomString(),
  },
})

/** Define emits. */
const emit = defineEmits(['update:label'])

/** Helper wrapper for the v-model:label. */
const labelModel = computed({
  get() {
    return props.label
  },
  set(newValue) {
    emit('update:label', newValue)
  },
})
</script>

<template>
  <div class="mr-2 mt-2">
    <div class="form-group">
      <label :for="'label' + idSuffix"> Label </label>
      <input
        type="text"
        class="form-control"
        :id="'label' + props.idSuffix"
        placeholder="PresetSet label"
        v-model="labelModel"
      />
      <small id="emailHelp" class="form-text text-muted">
        The label to use for display
      </small>
    </div>
  </div>
</template>
