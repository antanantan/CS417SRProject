<template>
  <transition name="modal-animation">
    <div v-show="disclaimerActive" class="modal">
        <transition name="modal-animation-inner">
          <div v-show="disclaimerActive" class="modal-inner">
            <slot>
              <p>this is a test</p>
            </slot>
            <button @click="close" type="button">I Agree</button>
            <button>I Disagree</button>
          </div>
        </transition>
    </div>
  </transition>
</template>

<script>
export default {
props: ["disclaimerActive"],
setup(props, {emit}) {
  const close = () => {
    emit("close");
    return {close}
  }

}
};
</script>



<!--ref: https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/-->
<!--ref: https://www.youtube.com/watch?v=NFdvWBh-D6k-->