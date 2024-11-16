<!--for testing new components-->

<template>
<p>test</p>
<Disclaimer @close="toggleDisclaimer":disclaimerActive="disclaimerActive">
    <div class="modal-content">
      <h1>this is a test</h1>
      <p>this will be the disclaimer</p>
    </div>
  </Disclaimer>
  <button @click="toggleDisclaimer" type="button">Test</button>

</template>

<script>
import Disclaimer from '@/components/Disclaimer.vue'
export default {
    name: "Disclaimer",
    components: {
        Disclaimer,
    },
    setup() {
        const disclaimerActive = ref(true);

        const toggleDisclaimer = () => {
        disclaimerActive.value = !modalActive.value;
    }

    return {disclaimerActive, toggleDisclaimer}
    }
}
</script>