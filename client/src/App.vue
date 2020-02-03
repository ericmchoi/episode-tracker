<template>
  <div>
    <section>
      <div class="app-controls container">
        <b-field
          position="is-right"
          grouped
          group-multiline
        >
          <b-input
            placeholder="Filter..."
            type="search"
            icon="magnify"
            v-model.lazy="filterQuery"
          />
          <p class="control">
            <b-button @click="openAddShowModal()">Add Show</b-button>
          </p>
          <p class="control">
            <b-button @click="() => openSettingsModal()">
              <b-icon icon="settings" />
            </b-button>
          </p>
        </b-field>
      </div>
    </section>
    <section>
      <div class="container">
        <show-table
          :show-data="displayedShows"
          @confirm-delete="openConfirmDeleteModal"
          @edit-show="editShow"
          @increment-episode="incrementEpisode"
        />
      </div>
    </section>
  </div>
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
  created() {
    try {
      this.settings = JSON.parse(window.localStorage.getItem('settings')) || DEFAULT_SETTINGS;
    } catch {
      this.settings = DEFAULT_SETTINGS;
    }

    this.loadSettings();
    this.loadShows();
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
          this.shows = [];
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
};
</script>

<style scoped>
.app-controls {
  padding: 0.75rem;
}

@media screen and (min-width: 1024px) {
  .app-controls {
    padding: 0.75rem 0;
  }
}

.progress-bar {
  margin-top: 4px;
}
</style>
