import singletonCaseData from '@variantsTest/data/case-singleton.json'
import trioCaseData from '@variantsTest/data/case-trio.json'
import querySettingsSingleton from '@variantsTest/data/query-settings-singleton.json'
import querySettingsTrio from '@variantsTest/data/query-settings-trio.json'
import { reactive } from 'vue'

import FilterFormGenotypePane from './FilterFormGenotypePane.vue'

export default {
  title: 'Variants / Filter Form Genotype',
  component: FilterFormGenotypePane,
}

const Template = (args) => ({
  components: { FilterFormGenotypePane },
  setup() {
    return { args }
  },
  template:
    '<FilterFormGenotypePane\n' +
    '    :show-filtration-inline-help="args.showFiltrationInlineHelp"\n' +
    '    :case="args.case"\n' +
    '    :query-settings="args.querySettings"\n' +
    '/>',
})

export const Trio = Template.bind({})
Trio.args = {
  showFiltrationInlineHelp: false,
  case: trioCaseData,
  querySettings: reactive(querySettingsTrio),
}

export const Singleton = Template.bind({})
Singleton.args = {
  showFiltrationInlineHelp: false,
  case: singletonCaseData,
  querySettings: reactive(querySettingsSingleton),
}

export const TrioWithHelp = Template.bind({})
TrioWithHelp.args = {
  showFiltrationInlineHelp: true,
  case: trioCaseData,
  querySettings: reactive(querySettingsTrio),
}
