<!--use this to test new components-->
<template>
  <div id="app">
    <Modal
      v-show="isModalVisible"
      @close="closeModal"/>
  </div>
</template>

<script>
import Modal from "@/components/Disclaimer.vue"
export default {
components: {
      Modal,
    },
    data() {
      return {
        isModalVisible: true,
      };
    },
    methods: {
      showModal() {
        this.isModalVisible = true;
      },
      closeModal() {
        this.isModalVisible = false;
      }
    }
};
</script>