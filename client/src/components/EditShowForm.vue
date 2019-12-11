<template>
  <form @submit.prevent="submitForm">
    <b-field label="Show Title *">
      <b-input
        v-model="title"
        type="text"
        maxlength="50"
        required
      />
    </b-field>
    <b-field grouped>
      <b-field
        label="Last Watched Episode *"
        expanded
      >
        <b-numberinput
          v-model="lastEpisode"
          min="0"
          required
        ></b-numberinput>
      </b-field>
      <b-field
        label="Total # of Episodes *"
        expanded
      >
        <b-numberinput
          v-model="totalEpisodes"
          min="0"
          required
        ></b-numberinput>
      </b-field>
    </b-field>
    <b-field label="Link">
      <b-input
        v-model="link"
        type="url"
      />
    </b-field>
    <b-field position="is-right" grouped>
      <p class="control">
        <b-button
          type="is-primary"
          tag="input"
          native-type="submit"
          value="Update"
        />
      </p>
      <p class="control">
        <b-button @click="$emit('close-form')">Close</b-button>
      </p>
    </b-field>
  </form>
</template>

<script>
export default {
  name: 'AddShowForm',
  props: {
    prefill: Object,
  },
  data() {
    const {
      title = '',
      totalEpisodes = 0,
      lastEpisode = 0,
      link = '',
    } = this.prefill;

    return {
      title,
      totalEpisodes,
      lastEpisode,
      link,
    };
  },
  methods: {
    submitForm() {
      const info = {
        title: this.title,
        totalEpisodes: this.totalEpisodes,
        lastEpisode: this.lastEpisode,
        link: this.link,
      };

      this.$emit('edit-show', this.prefill.id, info);
    },
  },
};
</script>
