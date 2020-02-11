<template>
  <div class="box">
    <form @submit.prevent="handleSubmit">
      <div class="block">
        <b-radio
          v-model="isRemote"
          name="isRemote"
          :native-value="false"
        >Local</b-radio>
        <b-radio
          v-model="isRemote"
          name="isRemote"
          :native-value="true"
        >Remote</b-radio>
      </div>
      <b-field label="API URL">
        <b-input
          :disabled="isDisabled"
          v-model="url"
          type="url"
        />
      </b-field>
      <b-field label="API Key">
        <b-input
          :disabled="isDisabled"
          v-model="key"
          type="password"
          password-reveal
        />
      </b-field>
      <b-field grouped>
        <p class="control">
          <b-button
            type="is-primary"
            tag="input"
            native-type="submit"
            value="Save"
          />
        </p>
        <p class="control">
          <b-button @click="closeForm">Close</b-button>
        </p>
      </b-field>
    </form>
  </div>
</template>

<script>
export default {
  name: 'SettingsForm',
  props: {
    prefill: Object,
  },
  data() {
    const { isRemote = false, url = '' } = this.prefill;
    return { isRemote, url, key: '' };
  },
  computed: {
    isDisabled() {
      return !this.isRemote || process.env.VUE_APP_DISABLE_API_FORM;
    },
  },
  methods: {
    handleSubmit() {
      const settings = {
        isRemote: this.isRemote,
        url: this.url,
        key: this.key,
      };

      this.$emit('save-settings', settings);
    },
    closeForm() {
      this.$emit('load-shows');
      this.$emit('close');
    },
  },
};
</script>
