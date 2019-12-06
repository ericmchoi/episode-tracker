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
    <template slot-scope="props">
      <b-table-column
        field="title"
        label="Title"
      >
        <span v-if="props.row.link.length">
          <a
            target="_blank"
            rel="noopener noreferrer"
            :href="props.row.link"
          >{{ props.row.title }}</a>
        </span>
        <span v-else>{{ props.row.title }}</span>
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
          :value="props.row.lastEpisode"
          :max="props.row.totalEpisodes"
        >{{ props.row.lastEpisode }} / {{ props.row.totalEpisodes }}</b-progress>
      </b-table-column>
      <b-table-column
        label="Actions"
        width="140"
        numeric
      >
        <div class="buttons is-right">
          <b-button
            type="is-text"
            size="is-small"
            @click="$emit('increment-episode', props.row)"
          >
            <b-icon icon="plus"></b-icon>
          </b-button>
          <b-button
            type="is-text"
            size="is-small"
            @click="openedShow = [props.row.id]"
          >
            <b-icon icon="pencil-box-multiple"></b-icon>
          </b-button>
          <b-button
            type="is-text"
            size="is-small"
            @click="$emit('confirm-delete', props.row)"
          >
            <b-icon icon="delete"></b-icon>
          </b-button>
        </div>
      </b-table-column>
    </template>

    <template slot="detail">Coming Soon.</template>

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
export default {
  name: 'ShowTable',
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
};
</script>
