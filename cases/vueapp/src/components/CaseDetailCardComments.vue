<script setup>
import { formatTime } from '@varfish/helpers.js'
import { useCaseDetailsStore } from '../stores/case-details.js'
import { useCasesStore } from '../stores/cases.js'

/** Define emits. */
const emit = defineEmits([
  'addCaseCommentClick',
  'updateCaseCommentClick',
  'deleteCaseCommentClick',
])

const casesStore = useCasesStore()
const caseDetailStore = useCaseDetailsStore()

/** Helper that returns whether the user has the permission to perform the action on the casecomment. */
const userHasPerm = (casecomment, action) => {
  const user = casesStore.appContext?.user
  if (!user) {
    return false
  }
  switch (action) {
    case 'delete':
    case 'update':
      return user.is_superuser || user.username === casecomment.author
    default:
      console.warn(`invalid action ${action}`)
  }
}
</script>

<template>
  <div
    class="card mb-3 varfish-case-list-card flex-grow-1"
    style="overflow-y: auto !important; max-height: 300px"
  >
    <div class="row card-header p-2 pl-2">
      <h5 class="col-auto ml-0 mr-0 mb-0">
        <i-mdi-comment-multiple />
        Case Comments ({{
          caseDetailStore.caseComments
            ? caseDetailStore.caseComments.length
            : 0
        }})
      </h5>
      <div class="btn-group ml-auto">
        <a
          class="btn btn-sm btn-primary"
          href="#"
          @click.prevent="emit('addCaseCommentClick')"
        >
          <i-mdi-comment-plus />
          Add Comment
        </a>
      </div>
    </div>
    <ul
      class="list-group list-group-flush list"
      style="overflow-y: auto !important; max-height: 300px"
      id="case-comment-list"
    >
      <template
        v-if="
          caseDetailStore.caseComments &&
          caseDetailStore.caseComments.length > 0
        "
      >
        <li
          v-for="caseComment in caseDetailStore.caseComments"
          class="list-group-item list-item"
        >
          <div>
            <span class="small text-muted">
              <strong>{{ caseComment.user }}</strong>
              {{ formatTime(caseComment.date_created) }}
              <template v-if="userHasPerm(caseComment, 'update')">
                &middot;
                <a
                  href="#"
                  @click.prevent="
                    emit('updateCaseCommentClick', caseComment.sodar_uuid)
                  "
                >
                  update
                </a>
              </template>
              <template v-if="userHasPerm(caseComment, 'delete')">
                &middot;
                <a
                  href="#"
                  @click.prevent="
                    emit('deleteCaseCommentClick', caseComment.sodar_uuid)
                  "
                >
                  delete
                </a>
              </template>
            </span>
            <div class="ml-3 font-italic">{{ caseComment.comment }}</div>
          </div>
        </li>
      </template>
      <li
        v-else
        class="list-group-item list-item text-center text-muted font-italic"
      >
        No case comments (yet).
      </li>
    </ul>
  </div>
</template>
