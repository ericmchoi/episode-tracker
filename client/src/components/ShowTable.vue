<template>
  <b-table
    :data="showData"
    :columns="showData.length ? [] : $options.columns"
    detailed
    detail-key="id"
    custom-row-key="id"
    :opened-detailed="openedShow"
    :show-detail-icon="false"
  >
    <template slot-scope="{ row: show }">
      <b-table-column
        field="title"
        label="Title"
      >
        <span v-if="show.link.length">
          <a
            target="_blank"
            rel="noopener noreferrer"
            :href="show.link"
          >{{ show.title }}</a>
        </span>
        <span v-else>{{ show.title }}</span>
      </b-table-column>
      <b-table-column
        field="lastEpisode"
        label="Episodes"
        width="500"
      >
        <b-progress
          class="progress-bar"
          type="is-primary"
          size="is-medium"
          show-value
          :value="show.lastEpisode"
          :max="show.totalEpisodes"
        >{{ show.lastEpisode }} / {{ show.totalEpisodes }}</b-progress>
      </b-table-column>
      <b-table-column
        label="Actions"
        width="140"
        numeric
      >
        <div class="buttons is-right">
          <b-tooltip label="Increment">
            <b-button
              type="is-text"
              size="is-small"
              @click="$emit('increment-episode', show)"
            >
              <b-icon icon="plus"></b-icon>
            </b-button>
          </b-tooltip>
          <b-tooltip label="Edit">
            <b-button
              type="is-text"
              size="is-small"
              @click="toggleOpenedShow(show.id)"
            >
              <b-icon icon="pencil-box-multiple"></b-icon>
            </b-button>
          </b-tooltip>
          <b-tooltip label="Delete">
            <b-button
              type="is-text"
              size="is-small"
              @click="$emit('confirm-delete', show)"
            >
              <b-icon icon="delete"></b-icon>
            </b-button>
          </b-tooltip>
        </div>
      </b-table-column>
    </template>

    <template
      slot="detail"
      slot-scope="{ row: show }"
    >
      <edit-show-form
        :prefill="show"
        @close-form="() => openedShow = []"
        @edit-show="handleEdit"
      />
    </template>

    <template slot="empty">
      <section class="section">
        <div class="content has-text-grey has-text-centered">
          <p>
            <b-icon
              icon="emoticon-sad"
              size="is-large"
            ></b-icon>
          </p>
          <p>Nothing here.</p>
        </div>
      </section>
    </template>
  </b-table>
</template>

<script>
import EditShowForm from './EditShowForm.vue';

export default {
  name: 'ShowTable',
  components: { EditShowForm },
  columns: [{ label: 'Title' }, { label: 'Episodes' }, { label: 'Actions' }],
  props: {
    showData: Array,
    confirmDelete: Function,
    incrementEpisode: Function,
  },
  data() {
    return {
      openedShow: [],
    };
  },
  methods: {
    toggleOpenedShow(id) {
      if (this.openedShow.length && this.openedShow[0] === id) {
        this.openedShow = [];
      } else {
        this.openedShow = [id];
      }
    },
    handleEdit(id, show) {
      this.openedShow = [];

      this.$emit('edit-show', id, show);
    },
  },
};
</script>
