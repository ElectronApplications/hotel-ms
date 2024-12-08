<script setup lang="ts">
import BackgroundImage from "@/assets/mainview-background.png";
import PrimaryButton from "@/components/PrimaryButton.vue";
import SurfaceCard from "@/components/SurfaceCard.vue";
import { useAuthStore } from "@/stores/auth";
import type { Room } from "@/types";
import { TransitionRoot } from "@headlessui/vue";
import axios from "axios";
import { storeToRefs } from "pinia";
import { onBeforeMount, ref } from "vue";
import { RouterLink } from "vue-router";

const BRAND_HOTEL_NAME = import.meta.env.VITE_BRAND_HOTEL_NAME;

const rooms = ref<Room[]>([]);

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);

const contentShow = ref(false);
onBeforeMount(async () => {
  setTimeout(() => {
    contentShow.value = true;
  }, 1000);

  rooms.value = (await axios.get("/api/room/")).data;
});
</script>

<template>
  <main class="container mx-auto">
    <div class="flex flex-row flex-wrap gap-y-4 px-2 pt-[60px]">
      <div class="flex basis-full flex-col lg:basis-1/3">
        <h1 class="text-center text-6xl font-extrabold lg:text-left">
          Welcome to the {{ BRAND_HOTEL_NAME }}!
        </h1>
        <h2
          class="pt-6 text-center text-2xl font-semibold text-secondary-active-light lg:text-left"
        >
          We have a total of
          <span
            class="text-primary-active-light dark:text-primary-active-dark"
            >{{ rooms.length }}</span
          >
          rooms with varied levels of service and comfort
        </h2>
        <div class="pt-6">
          <RouterLink :to="currentUser === undefined ? '/login' : '/book'">
            <PrimaryButton class="w-full py-4 lg:w-fit lg:px-8"
              >Book now</PrimaryButton
            >
          </RouterLink>
        </div>
      </div>
      <div class="basis-full self-end lg:basis-2/3">
        <img :src="BackgroundImage" alt="Hotel background" />
      </div>
    </div>
  </main>

  <TransitionRoot
    :show="contentShow"
    enter="transition-opacity duration-500"
    enter-from="opacity-0"
    enter-to="opacity-100"
  >
    <section class="container mx-auto px-2">
      <SurfaceCard
        class="rounded-t-none rounded-tr-none text-center lg:rounded-tl-3xl"
      >
        <span>Some content here!!!</span>
      </SurfaceCard>
    </section>
  </TransitionRoot>
</template>
