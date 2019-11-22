<template>
  <section>
    <div class="container">
      <nav class="level header">
        <div class="level-left"></div>
        <div class="level-right">
          <div class="level-item">
            <b-input
              placeholder="Filter..."
              type="search"
              icon="magnify"
              v-model.lazy="filterQuery"
            ></b-input>
          </div>
          <div class="level-item">
            <b-button @click="isAddShowModalActive = true">Add Show</b-button>
          </div>
        </div>
      </nav>
      <b-table
        :data="displayedShows"
        :columns="displayedShows.length ? [] : $options.columns"
        detailed
        detail-key="id"
        :opened-detailed="openedShow"
        :show-detail-icon="false"
      >
        <template slot-scope="props">
          <b-table-column field="title" label="Title">
            <span v-if="props.row.link.length">
              <a
                target="_blank"
                rel="noopener noreferrer"
                :href="props.row.link"
              >{{ props.row.title }}</a>
            </span>
            <span v-else>{{ props.row.title }}</span>
          </b-table-column>
          <b-table-column field="lastEpisode" label="Episodes" width="500">
            <b-progress
              class="progress-bar"
              type="is-primary"
              size="is-medium"
              show-value
              :value="props.row.lastEpisode"
              :max="props.row.totalEpisodes"
            >{{ props.row.lastEpisode }} / {{ props.row.totalEpisodes }}</b-progress>
          </b-table-column>
          <b-table-column label="Actions" width="140" numeric>
            <div class="buttons is-right">
              <b-button
                type="is-text"
                size="is-small"
                @click="incrementEpisodeCount(props.row.id, props.row.lastEpisode)"
              >
                <b-icon icon="plus"></b-icon>
              </b-button>
              <b-button type="is-text" size="is-small" @click="openedShow = [props.row.id]">
                <b-icon icon="pencil-box-multiple"></b-icon>
              </b-button>
              <b-button
                type="is-text"
                size="is-small"
                @click="focusedShow = props.row; isDeleteShowModalActive = true"
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
                <b-icon icon="emoticon-sad" size="is-large"></b-icon>
              </p>
              <p>Nothing here.</p>
            </div>
          </section>
        </template>
      </b-table>
      <b-modal :active.sync="isAddShowModalActive" scroll="keep" :can-cancel="['escape', 'x']">
        <div class="box">
          <add-show-form @add-show="addShow" />
        </div>
      </b-modal>
      <b-modal :active.sync="isDeleteShowModalActive" scroll="keep" :can-cancel="['escape', 'x']">
        <div class="box">
          <div class="content">Are you sure you want to delete "{{ focusedShow.title }}"?</div>
          <div class="buttons">
            <b-button type="is-danger" @click="deleteShow(focusedShow.id)">Delete</b-button>
            <b-button @click="isDeleteShowModalActive = false">Cancel</b-button>
          </div>
        </div>
      </b-modal>
    </div>
  </section>
</template>

<script>
import AddShowForm from './components/AddShowForm.vue';
import localStorageAPI from './api/localStorage';

const DEFAULT_SETTINGS = {
  type: 'local',
  url: '',
  key: '',
};

export default {
  columns: [
    { label: 'Title' },
    { label: 'Episodes' },
    { label: 'Actions' },
  ],
  name: 'app',
  components: { AddShowForm },
  data() {
    return {
      isAddShowModalActive: false,
      isDeleteShowModalActive: false,
      openedShow: [],
      focusedShow: {},
      shows: [],
      filterQuery: '',
    };
  },
  methods: {
    addShow(info) {
      this.api.addShow(info);

      this.shows = this.api.getShows();
    },
    deleteShow(id) {
      console.log(`deleting: ${id}`);
      this.api.deleteShow(id);

      this.isDeleteShowModalActive = false;
      this.shows = this.api.getShows();
    },
    incrementEpisodeCount(id, lastEp) {
      this.api.editShow(id, { lastEpisode: lastEp + 1 });

      this.shows = this.api.getShows();
    },
    loadSettings() {
      try {
        this.settings = JSON.parse(window.localStorage.getItem('settings')) || DEFAULT_SETTINGS;
      } catch {
        this.settings = DEFAULT_SETTINGS;
      }

      if (this.settings.type === 'local') {
        this.api = localStorageAPI;
      }
    },
    saveSettings() {
      window.localStorage.setItem('settings', JSON.stringify(this.settings));
    },
  },
  created() {
    this.settings = DEFAULT_SETTINGS;
    this.loadSettings();
    this.shows = this.api.getShows();
  },
  computed: {
    displayedShows() {
      if (this.filterQuery) {
        return this.shows.filter((show) => {
          const title = show.title.toLowerCase();
          const query = this.filterQuery.toLowerCase();
          return title.indexOf(query) !== -1;
        });
      }

      return this.shows;
    },
  },
};
</script>

<style scoped>
.header {
  padding: 10px;
}

.progress-bar {
  margin-top: 4px;
}
</style>
