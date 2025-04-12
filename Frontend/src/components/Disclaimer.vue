<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const emit = defineEmits(['close']); 

const close = (closeandNavigate) => {
  emit('close', closeandNavigate); // Sends true if "I disagree was clicked and false if "I agree" was clicked
};

</script>

<template>
  <div class="z-[9999] fixed inset-0 bg-neutral-700 bg-opacity-75 flex items-center justify-center">
    <div class="bg-white shadow-md w-3/4 md:w-1/2 max-h-[60vh] min-h-[100px] p-6 flex flex-col overflow-hidden relative rounded-xl">
      
      <!-- Header -->
      <header class="border-b border-neutral-2000 text-green-700 text-lg font-bold text-center pb-2">
        <slot name="header">
          DISCLAIMER
        </slot>
      </header>

      <!-- Body -->
      <section class="text-left text-base overflow-y-auto flex-1 px-2 py-2 indent-4">
        <slot name="body">
          <p>As people who have, or know people who have food allergies,
          we know that in every restaurant and dining establishment,
          there is always the risk of cross-contamination. While the 
          goal of this application is to reduce the risk of direct contact
          with allergens and the hassle for the sake of the customer and the 
          establishment, the risk is never completely eradicated.</p>
          <p>By inputting your food allergen/intolerance information and using
          this application, you are agreeing that we as the application
          developers are not directly responsible for injuries that occur
          as a result of the meal preparation at the eatery.</p>
        </slot>
      </section>

      <!-- Footer -->
      <footer class="border-t border-neutral-200 flex flex-col items-center text-center pt-4">
        <slot name="footer">

          <div class="flex justify-center space-x-4">
            <button
              type="button"
              class="px-4 w-32 h-11 border-1 border-rose-400 text-rose-400 rounded-full hover:text-white hover:bg-rose-400 transition "
              @click="close(true)"
            >
              I Agree
            </button>
            <button
              class="px-4 w-32 h-11 bg-neutral-300 text-neutral-800 rounded-full hover:bg-neutral-400"
              @click="close(false)"
            >
              I Disagree
            </button>
          </div>
        </slot>
      </footer>
    </div>
  </div>
</template>