<template>
  <div class="box">
    <form @submit.prevent="submitForm">
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
          :disabled="!isRemote"
          v-model="url"
          type="url"
        />
      </b-field>
      <b-field label="API Key">
        <b-input
          :disabled="!isRemote"
          v-model="key"
          type="text"
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
export default {
  name: 'SettingsForm',
  props: {
    prefill: Object,
  },
  data() {
    const { isRemote = false, url = '', key = '' } = this.prefill;
    return { isRemote, url, key };
  },
  methods: {
    submitForm() {
      const settings = {
        isRemote: this.isRemote,
        url: this.url,
        key: this.key,
      };

      this.$emit('save-settings', settings);
      this.$parent.close();
    },
  },
};
</script>
