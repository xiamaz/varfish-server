import CaseDetailCardAnnotations from '@cases/components/CaseDetailCardAnnotations.vue'
import { beforeAll, describe, test, vi } from 'vitest'

import caseDetailsStoreData from '../../data/caseDetailsStoreData.json'
import { makeWrapper } from './CaseDetail.common.js'

describe('CaseDetailCardAnnotations.vue', () => {
  beforeAll(() => {
    // Disable warnings
    vi.spyOn(console, 'warn').mockImplementation(vi.fn())
  })

  test('smoke test with empty data', async () => {
    const _wrapper = makeWrapper(CaseDetailCardAnnotations)

    // No assertions on output yet.
  })

  test('smoke test with case detail store data', async () => {
    const _wrapper = makeWrapper(CaseDetailCardAnnotations, {
      caseDetails: caseDetailsStoreData,
    })

    // No assertions on output yet.
  })
})
