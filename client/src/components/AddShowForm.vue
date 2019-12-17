<template>
  <div class="box">
    <h1 class="title">Add Show</h1>
    <form
      @submit.prevent="handleSubmit"
      novalidate
    >
      <b-field
        label="Show Title *"
        :type="{ 'is-danger': errors.title }"
        :message="errors.title"
      >
        <b-input
          v-model="title"
          ref="title"
          :use-html5-validation="false"
          type="text"
          maxlength="50"
          required
        />
      </b-field>
      <b-field grouped>
        <b-field
          label="Last Watched Episode *"
          :type="{ 'is-danger': errors.episode }"
          :message="errors.episode"
          expanded
        >
          <b-numberinput
            v-model="lastEpisode"
            type
            min="0"
            required
          />
        </b-field>
        <b-field
          label="Total # of Episodes *"
          :type="{ 'is-danger': errors.episode }"
          expanded
        >
          <b-numberinput
            v-model="totalEpisodes"
            type
            min="0"
            required
          />
        </b-field>
      </b-field>
      <b-field
        label="Link"
        :type="{ 'is-danger': errors.link }"
        :message="errors.link"
      >
        <b-input
          v-model="link"
          ref="link"
          :use-html5-validation="false"
          type="url"
        />
      </b-field>
      <b-field grouped>
        <p class="control">
          <b-button
            type="is-primary"
            tag="input"
            native-type="submit"
            value="Submit"
          />
        </p>
        <p class="control">
          <b-button @click="$parent.close()">Close</b-button>
        </p>
      </b-field>
    </form>
  </div>
</template>

<script>
const DEFAULT_ERRORS = {
  title: '',
  episode: '',
  link: '',
};

export default {
  name: 'AddShowForm',
  data() {
    return {
      title: '',
      totalEpisodes: 0,
      lastEpisode: 0,
      link: '',
      errors: { ...DEFAULT_ERRORS },
    };
  },
  methods: {
    getInputByName(name) {
      return this.$refs[name].$el.getElementsByTagName('input')[0];
    },
    handleSubmit() {
      let hasError = false;
      const errors = { ...DEFAULT_ERRORS };

      if (this.lastEpisode > this.totalEpisodes) {
        hasError = true;
        errors.episode = 'Last watched episode must be less than or equal to the total.';
      }

      const titleInput = this.getInputByName('title');
      hasError = hasError || !titleInput.checkValidity();
      errors.title = titleInput.validationMessage;

      const linkInput = this.getInputByName('link');
      hasError = hasError || !linkInput.checkValidity();
      errors.link = linkInput.validationMessage;

      this.errors = errors;

      if (!hasError) {
        const info = {
          title: this.title,
          totalEpisodes: this.totalEpisodes,
          lastEpisode: this.lastEpisode,
          link: this.link,
        };

        this.$emit('add-show', info);
        this.$parent.close();
      }
    },
  },
};
</script>
