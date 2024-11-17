

<template>
  <div class="modal-backdrop">
    <div class="modal">
      <header class="modal-header">
        <slot name="header">
          DISCLAIMER
        </slot>
        <button
          type="button"
          class="btn-close"
          @click="close">
        </button>
      </header>

      <section class="modal-body">
        <slot name="body">
          As people who have, or know people who have food allergies,
          we know that in every restaurant and dining establishment,
          there is always the risk of cross-contamination. While the 
          goal of this application is to reduce the risk of direct contact
          with allergens adn the hassle for the sake of the cusomer and the 
          establishment, the risk is never completely eradicated.
        </slot>
       </section>

      <footer class="modal-footer">
        <slot name="footer">
          By inputting your food allergen/intolerance information and using
          this application, you are agreeing that we as the application
          developers are not directly responsible for injuries that occur
          as a result of the meal preparation at the eatery.

        <button type="button" class="btn-green" @click="close">I Agree</button>
        <RouterLink class="btn-green":to="'/'">I Disagree</RouterLink>
        </slot>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
    name: 'Modal',
    methods: {
      close() {
        this.$emit('close');
      },
    },
  };
</script>

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal {
    background: #FFFFFF;
    box-shadow: 2px 2px 20px 1px;
    overflow-x: auto;
    display: flex;
    flex-direction: column;
    width: 600px;
  }

  .modal-header,
  .modal-footer {
    padding: 15px;
    display: flex;
  }

  .modal-header {
    position: relative;
    border-bottom: 1px solid #eeeeee;
    color: #2bb141;
    font-size: x-large;
    font-weight: bolder;
    justify-content: center;
  }

  .modal-footer {
    border-top: 1px solid #eeeeee;
    flex-direction: column;
    justify-content: flex-end;
    font-size: large;
  }

  .modal-body {
    position: relative;
    padding: 20px 10px;
    font-size: medium;
  }

  .btn-green {
    color: white;
    background: #e590c5;
    border: 1px solid #df5399;
    border-radius: 2px;
    width: 100px;
  }
  .btn-green:hover {
    background: #72ce64;
    border: 1px solid #2fb43f;
  }
</style>



<!--ref: https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/-->
<!--ref: https://www.youtube.com/watch?v=NFdvWBh-D6k-->
<!--ref: https://www.digitalocean.com/community/tutorials/vuejs-vue-modal-component-->