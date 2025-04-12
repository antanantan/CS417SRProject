<template>
  <div class="modal-backdrop">
    <div class="modal">
      <header class="modal-header">
        <slot name="header">
          DISCLAIMER
        </slot>
      </header>

      <section class="modal-body">
        <slot name="body">
          As people who have, or know people who have food allergies,
          we know that in every restaurant and dining establishment,
          there is always the risk of cross-contamination. While the 
          goal of this application is to reduce the risk of direct contact
          with allergens and the hassle for the sake of the customer and the 
          establishment, the risk is never completely eradicated.
        </slot>
       </section>

      <footer class="modal-footer">
        <slot name="footer">
          By inputting your food allergen/intolerance information and using
          this application, you are agreeing that we as the application
          developers are not directly responsible for injuries that occur
          as a result of the meal preparation at the eatery.
         <div class="d-flex justify-content-center gap-3">
           <button type="button" class="btn-green" @click="close(false)">I Agree</button>
           <button class="btn-green" @click="close(true)">I Disagree</button> <!-- Using Routerlink doesn't close the modal before rerouting which may lead to future issues-->
         </div>
        </slot>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const emit = defineEmits(['close']); 

const close = (closeandNavigate) => {
  emit('close', closeandNavigate); // Sends true if "I disagree was clicked and false if "I agree" was clicked
};


</script>

<style scoped>
  .modal-backdrop {
    position: fixed;
    top: 10;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal {
    background: #F8F8FF;
    box-shadow: 2px 2px 20px 1px;
    display: flex;
    flex-direction: column;
    width: 50%;
    max-height: 60vh;
    min-height: 100px;
    overflow: hidden; 
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 20px;
  }
  .modal-header {
    position: relative;
    border-bottom: 1px solid #eeeeee;
    color: #2bb141;
    font-size: x-large;
    font-weight: bolder;
    justify-content: center;
    padding: 15px;
  }
  .modal-footer {
    border-top: 1px solid #eeeeee;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding-top: 20px;
    padding-bottom: 10px;
    gap: 10px;
    width: 100%;
  }

  .modal-footer div {
    display: flex;
    justify-content: center;
    gap: 10px;
  }

  .modal-body {
    position: relative;
    max-height: 60vh;
    font-size: medium;
    text-align: center;
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