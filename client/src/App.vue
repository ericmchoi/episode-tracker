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
          <div class="level-item">
            <b-button @click="() => openSettingsModal()">
              <b-icon icon="settings"></b-icon>
            </b-button>
          </div>
        </div>
      </nav>
      <show-table
        :show-data="displayedShows"
        :confirm-delete="confirmDelete"
        :increment-episode="incrementEpisode"
      ></show-table>
      <b-modal
        :active.sync="isAddShowModalActive"
        scroll="keep"
        :can-cancel="['escape', 'x']"
      >
        <div class="box">
          <add-show-form @add-show="addShow" />
        </div>
      </b-modal>
      <b-modal
        :active.sync="isDeleteShowModalActive"
        scroll="keep"
        :can-cancel="['escape', 'x']"
      >
        <div class="box">
          <div
            class="content"
          >Are you sure you want to delete "{{ focusedShow.title }}"?</div>
          <div class="buttons">
            <b-button
              type="is-danger"
              @click="deleteShow(focusedShow.id)"
            >Delete</b-button>
            <b-button @click="isDeleteShowModalActive = false">Cancel</b-button>
          </div>
        </div>
      </b-modal>
    </div>
  </section>
</template>

<script>
import AddShowForm from './components/AddShowForm.vue';
import SettingsForm from './components/SettingsForm.vue';
import ShowTable from './components/ShowTable.vue';
import localStorageAPI from './api/localStorage';
import remoteAPI from './api/remote';

const DEFAULT_SETTINGS = {
  isRemote: false,
  url: '',
  key: '',
};

export default {
  name: 'app',
  components: { AddShowForm, ShowTable },
  data() {
    return {
      isAddShowModalActive: false,
      isDeleteShowModalActive: false,
      focusedShow: {},
      shows: [],
      filterQuery: '',
    };
  },
  methods: {
    addShow(show) {
      this.api
        .addShow(show)
        .then(() => { this.loadShows(); })
        .catch(err => console.error(err));
    },
    deleteShow(id) {
      console.log(`deleting: ${id}`);
      this.isDeleteShowModalActive = false;
      this.api
        .deleteShow(id)
        .then(() => { this.loadShows(); })
        .catch(err => console.error(err));
    },
    incrementEpisode(show) {
      this.api
        .editShow(show.id, { ...show, lastEpisode: show.lastEpisode + 1 })
        .then(() => this.loadShows())
        .catch(err => console.error(err));
    },
    loadShows() {
      this.api
        .getShows()
        .then((shows) => { console.log(shows); this.shows = shows; })
        .catch(err => console.error(err));
    },
    loadSettings() {
      if (this.settings.isRemote) {
        this.api = remoteAPI(this.settings.url, this.settings.key);
      } else {
        this.api = localStorageAPI();
      }
    },
    saveSettings(settings) {
      this.settings = settings || DEFAULT_SETTINGS;
      window.localStorage.setItem('settings', JSON.stringify(this.settings));

      this.loadSettings();
      this.loadShows();
    },
    confirmDelete(show) {
      this.focusedShow = show;
      this.isDeleteShowModalActive = true;
    },
    openSettingsModal() {
      this.$buefy.modal.open({
        parent: this,
        component: SettingsForm,
        props: {
          prefill: this.settings,
        },
        events: {
          'save-settings': this.saveSettings,
        },
      });
    },
  },
  created() {
    try {
      this.settings = JSON.parse(window.localStorage.getItem('settings')) || DEFAULT_SETTINGS;
    } catch {
      this.settings = DEFAULT_SETTINGS;
    }

    this.loadSettings();
    this.loadShows();
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
