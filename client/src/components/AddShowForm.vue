<template>
  <form @submit.prevent="submitForm">
    <b-field label="Show Title *">
      <b-input v-model="title" type="text" maxlength="50" required />
    </b-field>
    <b-field label="Last Watched Episode *">
      <b-numberinput v-model="lastEpisode" min="0" required></b-numberinput>
    </b-field>
    <b-field label="Total # of Episodes *">
      <b-numberinput v-model="totalEpisodes" min="0" required></b-numberinput>
    </b-field>
    <b-field label="Link">
      <b-input v-model="link" type="url" />
    </b-field>
    <b-field grouped>
      <p class="control">
        <b-button type="is-primary" tag="input" native-type="submit" value="Submit" />
      </p>
      <p class="control">
        <b-button @click="$parent.close()">Close</b-button>
      </p>
    </b-field>
  </form>
</template>

<script>
export default {
  name: 'AddShowForm',
  data() {
    return {
      title: '',
      totalEpisodes: 0,
      lastEpisode: 0,
      link: '',
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

      this.$emit('add-show', info);
      this.$parent.close();
    },
  },
};
</script>
