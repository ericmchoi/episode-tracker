<template>
  <div class="box">
    <form @submit.prevent="handleSubmit">
      <div class="content">Are you sure you want to delete "{{ show.title }}"?</div>
      <b-field grouped>
        <p class="control">
          <b-button
            type="is-danger"
            tag="input"
            native-type="submit"
            value="Delete"
          />
        </p>
        <p class="control">
          <b-button @click="$parent.close()">Cancel</b-button>
        </p>
      </b-field>
    </form>
  </div>
</template>

<script>
export default {
  name: 'ConfirmDeleteForm',
  props: {
    show: {
      type: Object,
      required: true,
    },
  },
  methods: {
    handleSubmit() {
      this.$emit('delete-show', this.show.id);
      this.$parent.close();
    },
  },
};
</script>
