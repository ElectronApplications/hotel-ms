<script setup lang="ts">
import BackgroundImage from "@/assets/mainview-background.png";
import PrimaryButton from "@/components/PrimaryButton.vue";
import SurfaceCard from "@/components/SurfaceCard.vue";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { RouterLink } from "vue-router";

const BRAND_HOTEL_NAME = import.meta.env.VITE_BRAND_HOTEL_NAME;

const roomsAmount = 10; // TODO: dynamically load

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);
</script>

<template>
  <main>
    <div
      class="container mx-auto flex flex-row flex-wrap gap-y-4 px-2 pt-[60px]"
    >
      <div class="flex basis-full flex-col lg:basis-1/3">
        <h1 class="text-center text-6xl font-extrabold lg:text-left">
          Welcome to the {{ BRAND_HOTEL_NAME }}!
        </h1>
        <h2
          class="text-secondary-active-light pt-6 text-center text-2xl font-semibold lg:text-left"
        >
          We have a total of
          <span
            class="text-primary-active-light dark:text-primary-active-dark"
            >{{ roomsAmount }}</span
          >
          rooms with varied levels of service and comfort
        </h2>
        <div class="pt-6">
          <RouterLink :to="currentUser === undefined ? '/login' : '/profile'">
            <PrimaryButton class="w-full py-4 lg:w-fit lg:px-8"
              >Book now</PrimaryButton
            >
          </RouterLink>
        </div>
      </div>
      <div class="basis-full lg:basis-2/3">
        <img :src="BackgroundImage" alt="Hotel background" />
      </div>
    </div>
  </main>

  <section>
    <SurfaceCard class="container mx-auto text-center">
      <span>Some content here!!!</span>
    </SurfaceCard>
  </section>
</template>
