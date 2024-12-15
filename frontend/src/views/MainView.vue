<script setup lang="ts">
import BackgroundImage from "@/assets/mainview-background.png";
import GalleryCarousel from "@/components/GalleryCarousel.vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import SurfaceCard from "@/components/SurfaceCard.vue";
import { useAuthStore } from "@/stores/auth";
import type { Class, Room } from "@/types";
import { TransitionRoot } from "@headlessui/vue";
import axios from "axios";
import { storeToRefs } from "pinia";
import { computed, onBeforeMount, ref } from "vue";
import { RouterLink } from "vue-router";

const BRAND_HOTEL_NAME = import.meta.env.VITE_BRAND_HOTEL_NAME;
const CURRENCY_SYMBOL = import.meta.env.VITE_CURRENCY_SYMBOL;

const rooms = ref<Room[]>([]);
const classes = ref<Class[]>([]);

const displayRooms = computed(() =>
  rooms.value
    .filter((x) => x.status == "free")
    .map((x) => {
      let room = x as Room & { class_info: Class };
      room.class_info = classes.value.find((y) => y.id == x.room_class)!;
      return room;
    }),
);

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);

const contentShow = ref(false);
onBeforeMount(async () => {
  setTimeout(() => {
    contentShow.value = true;
  }, 1000);

  rooms.value = (await axios.get("/api/room/")).data;
  classes.value = (await axios.get("/api/class/")).data;
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
        <div class="flex flex-row flex-wrap gap-y-4">
          <div
            v-for="room in displayRooms"
            v-bind:key="room.id"
            class="flex basis-full flex-col items-center md:basis-1/2 lg:basis-1/3 xl:basis-1/4"
          >
            <div
              v-if="
                room.class_info.gallery !== null &&
                room.class_info.gallery.images.length !== 0
              "
              class="h-[200px] w-[300px]"
            >
              <GalleryCarousel
                :gallery="room.class_info.gallery"
                imgClass="rounded-xl w-[300px] h-[200px] object-cover"
              />
            </div>
            <div
              v-else
              class="h-[200px] w-[300px] rounded-xl bg-secondary-light dark:bg-secondary-dark"
            />

            <div class="pt-2 text-2xl">
              {{ room.class_info.class_description }} - {{ room.places }} places
            </div>

            <div>
              Starting at {{ room.class_info.place_price * room.places }}
              {{ CURRENCY_SYMBOL }}
            </div>

            <RouterLink :to="currentUser === undefined ? '/login' : '/book'">
              <span
                class="text-link-light dark:text-link-darkfont-bold underline"
                >Book now</span
              >
            </RouterLink>
          </div>
        </div>
      </SurfaceCard>
    </section>
  </TransitionRoot>
</template>
