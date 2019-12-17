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
            />
          </div>
          <div class="level-item">
            <b-button @click="openAddShowModal()">Add Show</b-button>
          </div>
          <div class="level-item">
            <b-button @click="() => openSettingsModal()">
              <b-icon icon="settings" />
            </b-button>
          </div>
        </div>
      </nav>
      <show-table
        :show-data="displayedShows"
        @confirm-delete="openConfirmDeleteModal"
        @edit-show="editShow"
        @increment-episode="incrementEpisode"
      />
    </div>
  </section>
</template>

<script>
import AddShowForm from './components/AddShowForm.vue';
import SettingsForm from './components/SettingsForm.vue';
import ConfirmDeleteForm from './components/ConfirmDeleteForm.vue';
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
  components: { ShowTable },
  data() {
    return {
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
        .catch(() => {
          this.openErrorSnackbar('Unable to perform action. Please check your API settings.');
        });
    },
    deleteShow(id) {
      this.isDeleteShowModalActive = false;
      this.api
        .deleteShow(id)
        .then(() => { this.loadShows(); })
        .catch(() => {
          this.openErrorSnackbar('Unable to perform action. Please check your API settings.');
        });
    },
    editShow(id, show) {
      this.api
        .editShow(id, show)
        .then(() => this.loadShows())
        .catch(() => {
          this.openErrorSnackbar('Unable to perform action. Please check your API settings.');
        });
    },
    incrementEpisode(show) {
      const lastEpisode = show.lastEpisode + 1;
      const totalEpisodes = lastEpisode > show.totalEpisodes ? lastEpisode : show.totalEpisodes;

      this.api
        .editShow(show.id, { ...show, lastEpisode, totalEpisodes })
        .then(() => this.loadShows())
        .catch(() => {
          this.openErrorSnackbar('Unable to perform action. Please check your API settings.');
        });
    },
    loadShows() {
      this.api
        .getShows()
        .then((shows) => {
          this.shows = shows;
        })
        .catch(() => {
          this.openErrorSnackbar('Unable to retrieve shows. Please check your API settings.');
        });
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
      this.$buefy.toast.open({
        message: 'Settings saved.',
        position: 'is-top',
      });
    },
    openSettingsModal() {
      this.closeSnackbar();
      this.$buefy.modal.open({
        parent: this,
        component: SettingsForm,
        onCancel: this.loadShows,
        props: {
          prefill: this.settings,
        },
        events: {
          'save-settings': this.saveSettings,
          'load-shows': this.loadShows,
        },
      });
    },
    openAddShowModal() {
      this.$buefy.modal.open({
        parent: this,
        component: AddShowForm,
        events: {
          'add-show': this.addShow,
        },
      });
    },
    openConfirmDeleteModal(show) {
      this.closeSnackbar();
      this.$buefy.modal.open({
        parent: this,
        component: ConfirmDeleteForm,
        props: { show },
        events: {
          'delete-show': this.deleteShow,
        },
      });
    },
    openErrorSnackbar(message) {
      this.closeSnackbar();
      this.currentSnackbar = this.$buefy.snackbar.open({
        message,
        type: 'is-danger',
        position: 'is-top',
        actionText: 'Settings',
        indefinite: true,
        onAction: this.openSettingsModal,
      });
    },
    closeSnackbar() {
      if (this.currentSnackbar) {
        this.currentSnackbar.close();
      }
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
